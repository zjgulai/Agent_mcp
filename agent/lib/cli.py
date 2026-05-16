from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from .adapter_dispatch import ADAPTERS, install, install_all_clients, list_installed, uninstall
from .manifest import iter_registry, load_manifest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _format_table(rows: list[dict], cols: list[str]) -> str:
    if not rows:
        return "(empty)"
    widths = {c: max(len(c), max(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    head = "  ".join(c.ljust(widths[c]) for c in cols)
    sep = "  ".join("-" * widths[c] for c in cols)
    body = "\n".join("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols) for r in rows)
    return f"{head}\n{sep}\n{body}"


def cmd_list(args):
    manifests = list(iter_registry(REPO_ROOT, expected_kind="mcp"))
    rows = []
    for m in manifests:
        row = {"name": m.name, "priority": m.priority, "domain": m.domain}
        for c in ADAPTERS:
            row[c] = ADAPTERS[c].status_for(m.name)
        rows.append(row)
    print(_format_table(rows, ["name", "priority", "domain"] + list(ADAPTERS.keys())))
    return 0


def cmd_install(args):
    manifest_path = REPO_ROOT / "registry" / args.name / "manifest.yaml"
    if not manifest_path.exists():
        print(f"ERROR: registry/{args.name}/manifest.yaml not found", file=sys.stderr)
        return 2
    m = load_manifest(manifest_path, expected_kind="mcp")
    targets = list(ADAPTERS.keys()) if args.client == "all" else [args.client]
    results = install_all_clients(m, clients=targets)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


def cmd_uninstall(args):
    targets = list(ADAPTERS.keys()) if args.client == "all" else [args.client]
    results = []
    for c in targets:
        try:
            results.append(uninstall(args.name, c))
        except Exception as e:
            results.append({"client": c, "error": str(e)})
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


def cmd_doctor(args):
    issues = 0
    print("== schema ==")
    for m in iter_registry(REPO_ROOT, expected_kind="mcp"):
        print(f"  ok {m.name} v{m.version}")
    print("\n== binaries ==")
    for m in iter_registry(REPO_ROOT, expected_kind="mcp"):
        for b in m.requires.get("binaries", []):
            found = shutil.which(b)
            mark = "ok" if found else "MISSING"
            if not found:
                issues += 1
            print(f"  {mark:7s} {m.name:22s} -> {b} ({found or 'not on PATH'})")
    print("\n== env ==")
    for m in iter_registry(REPO_ROOT, expected_kind="mcp"):
        for e in m.requires.get("env", []):
            present = bool(os.environ.get(e))
            mark = "ok" if present else "WARN"
            print(f"  {mark:7s} {m.name:22s} -> {e} ({'set' if present else 'not set'})")
    print("\n== client config consistency ==")
    for c, mod in ADAPTERS.items():
        rows = mod.list_installed()
        managed = [r["name"] for r in rows if r["managed"]]
        print(f"  {c:8s}: {len(managed)} managed by agent-mcp ({', '.join(managed) if managed else 'none'})")
    return 0 if issues == 0 else 1


def cmd_show(args):
    manifest_path = REPO_ROOT / "registry" / args.name / "manifest.yaml"
    if not manifest_path.exists():
        print(f"ERROR: registry/{args.name}/manifest.yaml not found", file=sys.stderr)
        return 2
    m = load_manifest(manifest_path, expected_kind="mcp")
    print(json.dumps(m.raw, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent-mcp", description="Manage local MCP servers across opencode/codex/cursor/kimi.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List all registered MCPs and their install status across clients.")
    p_list.set_defaults(func=cmd_list)

    p_install = sub.add_parser("install", help="Install an MCP to a client (or all).")
    p_install.add_argument("name")
    p_install.add_argument("--client", choices=list(ADAPTERS.keys()) + ["all"], default="all")
    p_install.set_defaults(func=cmd_install)

    p_uninstall = sub.add_parser("uninstall", help="Uninstall an MCP from a client (or all).")
    p_uninstall.add_argument("name")
    p_uninstall.add_argument("--client", choices=list(ADAPTERS.keys()) + ["all"], default="all")
    p_uninstall.set_defaults(func=cmd_uninstall)

    p_doctor = sub.add_parser("doctor", help="Health check: schema, binaries, env, client config consistency.")
    p_doctor.set_defaults(func=cmd_doctor)

    p_show = sub.add_parser("show", help="Print a manifest as JSON.")
    p_show.add_argument("name")
    p_show.set_defaults(func=cmd_show)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
