# time MCP

Current time retrieval and timezone conversion — lightweight, zero-config.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install time --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `uvx` (uv tool runner) |
| Env vars | None |

## Typical usage

```
What time is it now in Tokyo, London, and New York simultaneously?
Convert 2026-06-15 09:00 UTC to Australia/Sydney local time.
How many hours until 2026-12-31 23:59 UTC from now?
```

## Notes

- No API key required — reads system time and converts via IANA timezone database.
- Useful for scheduling tasks, log correlation, and meeting time coordination.
