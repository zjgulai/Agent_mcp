from __future__ import annotations

import json
from pathlib import Path

from .adapter_common import backup_file, env_dict_from_requires, is_managed, prune_backups, stamp
from .manifest import Manifest

CLIENT_NAME = "opencode"
CONFIG_PATH = Path.home() / ".config" / "opencode" / "opencode.json"


def _load() -> dict:
    if not CONFIG_PATH.exists():
        return {"$schema": "https://opencode.ai/config.json", "mcp": {}}
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if "mcp" not in data or not isinstance(data["mcp"], dict):
        data["mcp"] = {}
    return data


def _save(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def install(m: Manifest) -> dict:
    if m.compatibility.get("opencode") == "unsupported":
        raise ValueError(f"{m.name}: opencode marked unsupported")

    backup = backup_file(CONFIG_PATH)
    data = _load()
    env_names = m.requires.get("env", [])
    entry = {
        "type": "local",
        "enabled": True,
        "command": list(m.mcp_command),
    }
    if env_names:
        entry["environment"] = env_dict_from_requires(env_names)
    data["mcp"][m.name] = stamp(entry, m.name)
    _save(data)
    pruned = prune_backups(CONFIG_PATH, keep=5)
    return {
        "client": CLIENT_NAME,
        "config": str(CONFIG_PATH),
        "name": m.name,
        "backup": str(backup) if backup else None,
        "pruned_backups": pruned,
    }


def uninstall(name: str) -> dict:
    if not CONFIG_PATH.exists():
        return {"client": CLIENT_NAME, "name": name, "removed": False, "reason": "config-missing"}
    backup = backup_file(CONFIG_PATH)
    data = _load()
    entry = data.get("mcp", {}).get(name)
    if entry is None:
        return {"client": CLIENT_NAME, "name": name, "removed": False, "reason": "not-found"}
    if not is_managed(entry):
        return {"client": CLIENT_NAME, "name": name, "removed": False,
                "reason": "not-managed-by-agent-mcp", "backup": str(backup) if backup else None}
    del data["mcp"][name]
    _save(data)
    prune_backups(CONFIG_PATH, keep=5)
    return {"client": CLIENT_NAME, "name": name, "removed": True, "backup": str(backup) if backup else None}


def list_installed() -> list[dict]:
    data = _load()
    out = []
    for name, entry in (data.get("mcp") or {}).items():
        out.append({
            "name": name,
            "managed": is_managed(entry),
            "command": entry.get("command"),
        })
    return out


def status_for(name: str) -> str:
    for row in list_installed():
        if row["name"] == name:
            return "managed" if row["managed"] else "external"
    return "absent"
