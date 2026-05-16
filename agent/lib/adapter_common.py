from __future__ import annotations

import datetime as _dt
import shutil
from pathlib import Path
from typing import Iterable

ANCHOR = "managed-by: agent-mcp"


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    ts = _dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak.{ts}")
    shutil.copy2(path, backup)
    return backup


def list_old_backups(path: Path, keep: int = 5) -> list[Path]:
    parent = path.parent
    if not parent.exists():
        return []
    pattern = path.name + ".bak.*"
    backups = sorted(parent.glob(pattern), key=lambda p: p.name, reverse=True)
    return backups[keep:]


def prune_backups(path: Path, keep: int = 5) -> int:
    n = 0
    for b in list_old_backups(path, keep=keep):
        b.unlink()
        n += 1
    return n


def is_managed(entry: dict | None) -> bool:
    if not isinstance(entry, dict):
        return False
    if "_managed_by" in entry and "agent-mcp" in str(entry["_managed_by"]):
        return True
    return False


def stamp(entry: dict, manifest_name: str) -> dict:
    entry = dict(entry)
    entry["_managed_by"] = "agent-mcp"
    entry["_managed_name"] = manifest_name
    entry["_managed_at"] = _dt.datetime.now().isoformat(timespec="seconds")
    return entry


def env_dict_from_requires(env_names: Iterable[str]) -> dict[str, str]:
    return {name: "${" + name + "}" for name in env_names}
