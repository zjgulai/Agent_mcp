from __future__ import annotations

import datetime as _dt
import json
import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib as _toml_r
else:
    import tomli as _toml_r
import tomli_w

from .adapter_common import backup_file, prune_backups
from .manifest import Manifest

CLIENT_NAME = "codex"
CONFIG_PATH = Path.home() / ".codex" / "config.toml"
MANAGED_REGISTRY = Path.home() / ".codex" / ".agent-mcp-managed.json"


def _load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    with CONFIG_PATH.open("rb") as f:
        return _toml_r.load(f)


def _save_config(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("wb") as f:
        tomli_w.dump(data, f)


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


def install(m: Manifest) -> dict:
    if m.compatibility.get("codex") == "unsupported":
        raise ValueError(f"{m.name}: codex marked unsupported")

    backup = backup_file(CONFIG_PATH)
    data = _load_config()
    servers = data.setdefault("mcp_servers", {})
    cmd = list(m.mcp_command)
    entry = {"command": cmd[0], "args": cmd[1:]}
    env_names = m.requires.get("env", [])
    if env_names:
        entry["env"] = {name: "${" + name + "}" for name in env_names}
    servers[m.name] = entry
    _save_config(data)

    reg = _load_registry()
    reg[m.name] = {
        "installed_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "manifest_version": m.version,
    }
    _save_registry(reg)

    pruned = prune_backups(CONFIG_PATH, keep=5)
    return {
        "client": CLIENT_NAME,
        "config": str(CONFIG_PATH),
        "registry": str(MANAGED_REGISTRY),
        "name": m.name,
        "backup": str(backup) if backup else None,
        "pruned_backups": pruned,
    }


def uninstall(name: str) -> dict:
    if not CONFIG_PATH.exists():
        return {"client": CLIENT_NAME, "name": name, "removed": False, "reason": "config-missing"}
    reg = _load_registry()
    if name not in reg:
        return {"client": CLIENT_NAME, "name": name, "removed": False, "reason": "not-managed-by-agent-mcp"}
    backup = backup_file(CONFIG_PATH)
    data = _load_config()
    servers = data.get("mcp_servers", {})
    if name in servers:
        del servers[name]
        if not servers:
            data.pop("mcp_servers", None)
        _save_config(data)
    del reg[name]
    _save_registry(reg)
    prune_backups(CONFIG_PATH, keep=5)
    return {"client": CLIENT_NAME, "name": name, "removed": True, "backup": str(backup) if backup else None}


def list_installed() -> list[dict]:
    data = _load_config()
    reg = _load_registry()
    out = []
    for name, entry in (data.get("mcp_servers") or {}).items():
        out.append({
            "name": name,
            "managed": name in reg,
            "command": [entry.get("command")] + list(entry.get("args", [])),
        })
    return out


def status_for(name: str) -> str:
    for row in list_installed():
        if row["name"] == name:
            return "managed" if row["managed"] else "external"
    return "absent"
