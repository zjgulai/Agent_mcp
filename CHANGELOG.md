# Changelog

All notable changes to **Agent_mcp** are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning is [SemVer](https://semver.org/).

## [Unreleased]

Pre-1.0. Coordinated 1.0.0 will land alongside [Agent_skills](https://github.com/zjgulai/Agent_skills) and [Agent_hook](https://github.com/zjgulai/Agent_hook) once the `manifest.py` schema and CLI surface are pinned.

### [2026-09-17] Registry update — 30 → 39 MCPs

Audit window: 2026-07-17 → 2026-09-17 (npm/PyPI version truth + GitHub release
activity + live `initialize` handshake on every shipped entry).

**Fixed (7 broken entries — all verified broken before, working after):**

- `playwright`: pinned `@playwright/mcp@3.1.0` never existed on npm → `0.0.81`
- `aws`: was `awslabs.core-mcp-server` (base server, no cloud control) → `awslabs.aws-api-mcp-server@1.5.5`
- `vercel` / `linear` / `slack`: nonexistent or squatter npm packages → official
  remote MCP servers bridged to stdio via `mcp-remote@0.14.2`
- `figma`: nonexistent `@figma/mcp-server` → `figma-developer-mcp@0.13.2` (de-facto standard)
- `gitlab`: `mcp-server-gitlab` removed from PyPI → `@zereight/mcp-gitlab@2.1.62`

**Aligned (12 pins):** brave-search → official `@brave/brave-search-mcp-server@2.1.3` ·
context7 `4.1.1` · notion `2.5.1` · supabase `0.12.0` · sentry `0.39.0` ·
filesystem/memory/sequential-thinking `2026.8.31` · fetch/git/time `2026.8.18` ·
postgres `0.6.2` · docker `0.3.0` · sqlite `2025.4.25` · redis `0.1.1`.
Env renamed by upstreams: `SENTRY_AUTH_TOKEN` → `SENTRY_ACCESS_TOKEN`,
`SUPABASE_URL`+`SERVICE_ROLE_KEY` → `SUPABASE_ACCESS_TOKEN`.
`kubernetes`: stale PyPI 0.1.6 (2025-03) → npm `mcp-server-kubernetes@4.1.7`.

**Added (9, each passed a live MCP handshake on macOS/Node 26/uv 0.11):**

- P0: `chrome-devtools` (official, 52k★), `mcp-remote` (bridge enabler)
- P1: `firecrawl`, `antv-chart` (official AntV), `ripwire` (Red Hat), `exa`, `anysearch` (remote bridge)
- P2: `arxiv`, `jupyter` (Datalayer)

**Rejected after verification:** `docs-mcp-server` (hangs pre-argparse on Node v26),
`cve-mcp-server` (no package-manager distribution). Recorded for later reconsideration.

**Tooling:** `agent/lib/pincheck.py` + 6 offline tests (45 total) +
`agent-mcp doctor --pins` online registry check — the playwright@3.1.0 class of
bad pin can no longer land silently.

## [0.1.1] — 2026-05-16

### Documentation

- Full Chinese i18n coverage on all 4 content pages plus 3 redirect stubs (commit `497ac64`):
  - index: 42 dict keys / 395 zh chars rendered
  - getting-started: 33 keys / 217 chars
  - architecture: 46 keys / 373 chars
  - handbook: 62 keys / 481 chars
  - All 8 pages pass `linkedom` zh-switch simulation with `unfilled keys = 0`

## [0.1.0] — 2026-05-16

Initial release. Single source of truth for MCP servers shared by opencode, codex, cursor, kimi.

### Added

- 10 MCPs (6 P0 + 4 P1):
  - **P0**: `github`, `filesystem`, `context7`, `playwright`, `sequential-thinking`, `git`
  - **P1**: `postgres`, `sentry`, `figma`, `linear`
- 4-client adapter system:
  - opencode: merge into `~/.config/opencode/opencode.json` `mcp` section
  - codex: merge into `~/.codex/config.toml` `[mcp_servers.<name>]`
  - cursor: merge into `~/.cursor/mcp.json` `mcpServers`
  - kimi: shell out to `kimi mcp add` (native CLI subcommand)
- `agent/lib/manifest.py` — shared schema validator (byte-identical with Agent_skills, Agent_hook; md5 `b46c2f55980b9aa2ea93b87941c833e2`)
- `agent/lib/cli.py` + `bin/agent-mcp` — `list / install / uninstall / doctor / show`
- Secret model: tokens declared by env-var **name** in manifest (`requires.env: [GITHUB_TOKEN]`), interpolated as `${GITHUB_TOKEN}` at write time, never persisted on disk
- Schema-level literal-token rejection: `ghp_*`, `sk-*`, `AIza*` patterns refused at load time
- Test suite: 28 schema + 11 adapter = **39 tests, all green**
- GitHub Pages site: index / getting-started / architecture / handbook (indigo accent, dark zinc base) + 3 redirect stubs
- Companion-repo links to Agent_skills and Agent_hook in README

### Verified

- All 6 P0 MCPs × 4 clients = 24 install round-trips clean
- Real opencode 1.15.1 integration: `opencode mcp list` reports `✓ context7 connected` after `agent-mcp install context7 --client opencode`

## Compatibility

| Version | manifest.py md5 | Companion repos required |
|---|---|---|
| 0.1.x | `b46c2f55980b9aa2ea93b87941c833e2` | Agent_skills ≥ 0.2.0, Agent_hook ≥ 0.1.1 |
