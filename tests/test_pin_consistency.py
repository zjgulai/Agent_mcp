"""Offline pin-consistency lint: every npm/pypi MCP must pin an exact version
in mcp_command, and the pinned token must reference source.package correctly.

Born from the 2026-09 audit: @playwright/mcp@3.1.0 was pinned in June but
never existed on npm -- nothing caught it for three months.
"""
from pathlib import Path

import pytest

from agent.lib.manifest import iter_registry
from agent.lib.pincheck import pinned_spec

REPO_ROOT = Path(__file__).parent.parent


def _all_mcps():
    return list(iter_registry(REPO_ROOT, expected_kind="mcp"))


def test_registry_size():
    mcps = _all_mcps()
    assert len(mcps) == 39, f"expected 39 MCPs after 2026-09 update, got {len(mcps)}"


def test_every_npm_pypi_mcp_is_pinned():
    unpinned = [m.name for m in _all_mcps()
                if m.source.get("type") in ("npm", "pypi") and pinned_spec(m) is None]
    # git-sourced binaries (ripwire) are the only legitimate unpinned entries
    assert unpinned == [], f"MCPs without an exact registry pin: {unpinned}"


def test_pin_token_references_source_package():
    """pinned_spec must succeed => the command pin literally names source.package."""
    for m in _all_mcps():
        if m.source.get("type") in ("npm", "pypi"):
            spec = pinned_spec(m)
            assert spec is not None, f"{m.name}: pin token does not match source.package"


def test_bridge_entries_are_consistent():
    """mcp-remote bridges: package mcp-remote, url arg right after the pinned pkg."""
    for m in _all_mcps():
        if m.source.get("package") == "mcp-remote":
            spec = pinned_spec(m)
            assert spec == ("mcp-remote", "0.14.2"), f"{m.name}: bad bridge pin {spec}"
            assert any(str(a).startswith("https://") or a == "${MCP_REMOTE_URL}"
                       for a in m.mcp_command), f"{m.name}: bridge missing remote URL arg"


def test_known_bad_pins_are_gone():
    """Regression guards for the 2026-09 audit findings."""
    pins = {m.name: pinned_spec(m) for m in _all_mcps()}
    assert pins.get("playwright") == ("@playwright/mcp", "0.0.81")          # was 3.1.0 (never existed)
    assert pins.get("context7") == ("@upstash/context7-mcp", "4.1.1")       # was 0.9.0
    assert pins.get("aws") == ("awslabs.aws-api-mcp-server", "1.5.5")       # was core-mcp-server
    assert pins.get("brave-search") == ("@brave/brave-search-mcp-server", "2.1.3")  # was archived ref pkg
    assert pins.get("gitlab") == ("@zereight/mcp-gitlab", "2.1.62")         # pypi pkg removed


def test_kubernetes_uses_npm_channel():
    for m in _all_mcps():
        if m.name == "kubernetes":
            assert m.source["type"] == "npm"
            assert m.mcp_command[:3] == ["npx", "-y", "mcp-server-kubernetes@4.1.7"]
