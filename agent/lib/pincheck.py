"""Pin consistency helpers for Agent_mcp (repo-local, not vendored).

Extracts (package, pinned_version) from a manifest's mcp_command so both
pytest (offline) and `agent-mcp doctor --pins` (online) can verify that
pinned versions actually exist in their registry.

Rules:
  - source.type == npm  -> one mcp_command token must be `<package>@<version>`
                           (bare `npx -y <pkg>` without a pin is a lint error).
  - source.type == pypi -> mcp_command[0] == "uvx" and [1] == `<package>@<version>`.
  - source.type == git  -> binary/external install (e.g. ripwire); no pin to check,
                           but the package itself is exempt from registry lookup.
  - `uvx`-launched pypi pins also accept `<package>==<version>`? No: uvx uses `@`.
"""
from __future__ import annotations

import re

from .manifest import Manifest

_VERSION_CHARS = r"[0-9A-Za-z.+-]+"


def pinned_spec(m: Manifest) -> tuple[str, str] | None:
    """Return (package, version) pinned in mcp_command, or None when exempt/unknown."""
    if m.source.get("type") not in ("npm", "pypi"):
        return None
    pkg = m.source.get("package") or ""
    pkg_re = re.compile("^" + re.escape(pkg) + "@(" + _VERSION_CHARS + ")$")
    if m.source.get("type") == "pypi":
        # uvx <pkg>@<ver> [extra args...]
        for tok in m.mcp_command[1:3]:
            match = pkg_re.match(tok)
            if match:
                return pkg, match.group(1)
        return None
    # npm / npx -y <pkg>@<ver>
    for tok in m.mcp_command:
        match = pkg_re.match(tok)
        if match:
            return pkg, match.group(1)
    return None


REGISTRY_URL = {
    "npm": "https://registry.npmjs.org/{pkg}/{ver}",
    "pypi": "https://pypi.org/pypi/{pkg}/{ver}/json",
}


def check_pin_online(m: Manifest, *, timeout: float = 10.0) -> dict:
    """Verify the pinned version exists in its registry. Returns a result dict."""
    import urllib.error
    import urllib.request

    spec = pinned_spec(m)
    if spec is None:
        return {"name": m.name, "status": "exempt", "detail": "no registry pin (git/binary source)"}
    pkg, ver = spec
    url = REGISTRY_URL[m.source["type"]].format(pkg=pkg, ver=ver)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            resp.read(1)  # touch the body; HTTP 200 alone is the existence signal
        return {"name": m.name, "status": "ok", "detail": f"{pkg}@{ver} exists"}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"name": m.name, "status": "BAD-PIN", "detail": f"{pkg}@{ver} NOT in registry"}
        return {"name": m.name, "status": "error", "detail": f"HTTP {e.code} for {url}"}
    except Exception as e:  # network down, DNS, timeout
        return {"name": m.name, "status": "error", "detail": str(e)[:120]}
