from __future__ import annotations

import datetime as _dt
import json
import os
import subprocess
from pathlib import Path

from .manifest import Manifest

CLIENT_NAME = "kimi"
MANAGED_REGISTRY = Path.home() / ".kimi" / ".agent-mcp-managed.json"
KIMI_MCP_JSON = Path.home() / ".kimi" / "mcp.json"


def _load_registry() -> dict:
    if not MANAGED_REGISTRY.exists():
        return {}
    with MANAGED_REGISTRY.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_registry(data: dict) -> None:
    MANAGED_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with MANAGED_REGISTRY.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def _run_kimi(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["kimi"] + args,
        capture_output=True,
        text=True,
        env={**os.environ, "PAGER": "cat"},
    )
    return proc.returncode, proc.stdout, proc.stderr


def install(m: Manifest) -> dict:
    if m.compatibility.get("kimi") == "unsupported":
        raise ValueError(f"{m.name}: kimi marked unsupported")

    cmd = list(m.mcp_command)
    if not cmd:
        raise ValueError(f"{m.name}: empty mcp_command")

    args = ["mcp", "add", m.name, "--transport", "stdio"]
    for env_name in m.requires.get("env", []):
        actual = os.environ.get(env_name, "")
        args += ["-e", f"{env_name}={actual}"]
    args += ["--", *cmd]

    rc, out, err = _run_kimi(args)
    success = rc == 0
    if not success:
        return {
            "client": CLIENT_NAME,
            "name": m.name,
            "installed": False,
            "rc": rc,
            "stderr": err.strip(),
            "command": " ".join(["kimi"] + args[:5]) + " ... --",
        }

    reg = _load_registry()
    reg[m.name] = {
        "installed_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "manifest_version": m.version,
        "env_used": list(m.requires.get("env", [])),
    }
    _save_registry(reg)
    return {
        "client": CLIENT_NAME,
        "name": m.name,
        "installed": True,
        "registry": str(MANAGED_REGISTRY),
        "config_hint": str(KIMI_MCP_JSON),
    }


def uninstall(name: str) -> dict:
    reg = _load_registry()
    if name not in reg:
        rc, out, err = _run_kimi(["mcp", "remove", name])
        if rc == 0:
            return {"client": CLIENT_NAME, "name": name, "removed": True,
                    "reason": "not-managed-but-existed"}
        return {"client": CLIENT_NAME, "name": name, "removed": False, "reason": "not-found"}
    rc, out, err = _run_kimi(["mcp", "remove", name])
    success = rc == 0
    if success:
        del reg[name]
        _save_registry(reg)
    return {
        "client": CLIENT_NAME,
        "name": name,
        "removed": success,
        "rc": rc,
        "stderr": err.strip() if err.strip() else None,
    }


def list_installed() -> list[dict]:
    if not KIMI_MCP_JSON.exists():
        return []
    try:
        with KIMI_MCP_JSON.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []
    reg = _load_registry()
    out = []
    servers = data.get("mcpServers") or data.get("servers") or data
    if not isinstance(servers, dict):
        return []
    for name, entry in servers.items():
        if not isinstance(entry, dict):
            continue
        out.append({
            "name": name,
            "managed": name in reg,
            "command": entry.get("command") or entry.get("args"),
        })
    return out


def status_for(name: str) -> str:
    for row in list_installed():
        if row["name"] == name:
            return "managed" if row["managed"] else "external"
    return "absent"
