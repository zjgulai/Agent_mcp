# Changelog

All notable changes to **Agent_mcp** are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning is [SemVer](https://semver.org/).

## [Unreleased]

Pre-1.0. Coordinated 1.0.0 will land alongside [Agent_skills](https://github.com/zjgulai/Agent_skills) and [Agent_hook](https://github.com/zjgulai/Agent_hook) once the `manifest.py` schema and CLI surface are pinned.

### Added

- Xquik remote MCP registry entry with `mcp-remote@0.1.38` and env-only `XQUIK_API_KEY` authentication.

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
