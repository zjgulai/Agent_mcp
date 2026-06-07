import copy
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).parent.parent
sys.path.insert(0, str(REPO))

from agent.lib import (
    adapter_codex,
    adapter_common,
    adapter_cursor,
    adapter_dispatch,
    adapter_opencode,
)
from agent.lib.manifest import Manifest, load_manifest


VALID_MCP_GITHUB = {
    "kind": "mcp",
    "name": "github",
    "version": "0.1.0",
    "description": "GitHub MCP server providing repo, issue, PR, code search, CI workflow access for ops scenarios.",
    "domain": "tooling",
    "priority": "P0",
    "compatibility": {"opencode": "native", "codex": "native", "cursor": "native", "kimi": "native"},
    "source": {"type": "npm", "package": "@modelcontextprotocol/server-github"},
    "mcp_command": ["npx", "-y", "@modelcontextprotocol/server-github"],
    "requires": {"binaries": ["npx"], "env": ["GITHUB_TOKEN"]},
}


@pytest.fixture
def github_manifest(tmp_path):
    import yaml
    p = tmp_path / "registry" / "github" / "manifest.yaml"
    p.parent.mkdir(parents=True)
    p.write_text(yaml.safe_dump(VALID_MCP_GITHUB), encoding="utf-8")
    return load_manifest(p)


@pytest.fixture
def isolated_paths(monkeypatch, tmp_path):
    opencode_cfg = tmp_path / "opencode" / "opencode.json"
    codex_cfg = tmp_path / "codex" / "config.toml"
    codex_reg = tmp_path / "codex" / ".agent-mcp-managed.json"
    cursor_cfg = tmp_path / "cursor" / "mcp.json"
    kimi_cfg = tmp_path / "kimi" / "mcp.json"
    kimi_reg = tmp_path / "kimi" / ".agent-mcp-managed.json"
    monkeypatch.setattr(adapter_opencode, "CONFIG_PATH", opencode_cfg)
    monkeypatch.setattr(adapter_codex, "CONFIG_PATH", codex_cfg)
    monkeypatch.setattr(adapter_codex, "MANAGED_REGISTRY", codex_reg)
    monkeypatch.setattr(adapter_cursor, "CONFIG_PATH", cursor_cfg)
    monkeypatch.setattr(adapter_kimi := __import__("agent.lib.adapter_kimi", fromlist=["x"]),
                        "MANAGED_REGISTRY", kimi_reg)
    monkeypatch.setattr(adapter_kimi, "KIMI_MCP_JSON", kimi_cfg)
    return {
        "opencode": opencode_cfg, "codex": codex_cfg, "codex_reg": codex_reg,
        "cursor": cursor_cfg, "kimi": kimi_cfg, "kimi_reg": kimi_reg,
    }


def test_opencode_install_then_uninstall(github_manifest, isolated_paths):
    res = adapter_opencode.install(github_manifest)
    assert res["client"] == "opencode"
    cfg = json.loads(isolated_paths["opencode"].read_text())
    assert "github" in cfg["mcp"]
    entry = cfg["mcp"]["github"]
    assert entry["command"] == ["npx", "-y", "@modelcontextprotocol/server-github"]
    assert entry["environment"] == {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
    assert entry["_managed_by"] == "agent-mcp"

    res2 = adapter_opencode.uninstall("github")
    assert res2["removed"] is True
    cfg2 = json.loads(isolated_paths["opencode"].read_text())
    assert "github" not in cfg2.get("mcp", {})


def test_opencode_preserves_existing_unmanaged_mcp(github_manifest, isolated_paths):
    isolated_paths["opencode"].parent.mkdir(parents=True, exist_ok=True)
    isolated_paths["opencode"].write_text(json.dumps({
        "$schema": "https://opencode.ai/config.json",
        "mcp": {"aim-memory": {"type": "local", "command": ["npx", "-y", "mcp-knowledge-graph@1.3.2"]}}
    }))
    adapter_opencode.install(github_manifest)
    cfg = json.loads(isolated_paths["opencode"].read_text())
    assert "aim-memory" in cfg["mcp"]
    assert "github" in cfg["mcp"]
    assert cfg["mcp"]["aim-memory"].get("_managed_by") is None


def test_opencode_refuses_to_remove_unmanaged(github_manifest, isolated_paths):
    isolated_paths["opencode"].parent.mkdir(parents=True, exist_ok=True)
    isolated_paths["opencode"].write_text(json.dumps({
        "mcp": {"aim-memory": {"type": "local", "command": ["npx"]}}
    }))
    res = adapter_opencode.uninstall("aim-memory")
    assert res["removed"] is False
    assert "not-managed" in res["reason"]


def test_codex_install_then_uninstall(github_manifest, isolated_paths):
    res = adapter_codex.install(github_manifest)
    assert res["client"] == "codex"
    text = isolated_paths["codex"].read_text()
    assert "[mcp_servers.github]" in text
    assert 'command = "npx"' in text
    reg = json.loads(isolated_paths["codex_reg"].read_text())
    assert "github" in reg

    res2 = adapter_codex.uninstall("github")
    assert res2["removed"] is True
    text2 = isolated_paths["codex"].read_text()
    assert "[mcp_servers.github]" not in text2


def test_codex_refuses_unmanaged(isolated_paths):
    isolated_paths["codex"].parent.mkdir(parents=True, exist_ok=True)
    isolated_paths["codex"].write_text(
        '[mcp_servers.external-one]\ncommand = "uvx"\nargs = ["x"]\n'
    )
    res = adapter_codex.uninstall("external-one")
    assert res["removed"] is False
    assert "not-managed" in res["reason"]


def test_cursor_install_then_uninstall(github_manifest, isolated_paths):
    res = adapter_cursor.install(github_manifest)
    assert res["client"] == "cursor"
    cfg = json.loads(isolated_paths["cursor"].read_text())
    assert "github" in cfg["mcpServers"]
    entry = cfg["mcpServers"]["github"]
    assert entry["command"] == "npx"
    assert entry["args"] == ["-y", "@modelcontextprotocol/server-github"]
    assert entry["_managed_by"] == "agent-mcp"

    res2 = adapter_cursor.uninstall("github")
    assert res2["removed"] is True


def test_dispatch_routes_correctly(github_manifest, isolated_paths):
    res = adapter_dispatch.install(github_manifest, "opencode")
    assert res["client"] == "opencode"
    res2 = adapter_dispatch.install(github_manifest, "cursor")
    assert res2["client"] == "cursor"


def test_dispatch_unknown_client_rejected(github_manifest):
    with pytest.raises(ValueError, match="unknown client"):
        adapter_dispatch.install(github_manifest, "vim")


def test_dispatch_install_all_skips_unsupported(github_manifest, isolated_paths):
    m = github_manifest
    m.compatibility["kimi"] = "unsupported"
    results = adapter_dispatch.install_all_clients(m, clients=["opencode", "kimi"])
    by_client = {r["client"]: r for r in results}
    assert "opencode" in by_client
    assert by_client["kimi"].get("skipped") is True


def test_backup_created_when_config_exists(github_manifest, isolated_paths):
    isolated_paths["opencode"].parent.mkdir(parents=True, exist_ok=True)
    isolated_paths["opencode"].write_text('{"mcp": {}}')
    res = adapter_opencode.install(github_manifest)
    assert res["backup"] is not None
    assert Path(res["backup"]).exists()


def test_backup_not_created_when_config_absent(github_manifest, isolated_paths):
    res = adapter_opencode.install(github_manifest)
    assert res["backup"] is None
    assert isolated_paths["opencode"].exists()
