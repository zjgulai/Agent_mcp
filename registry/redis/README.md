# redis MCP

Read, write, and manage Redis key-value store — inspect cache state, debug sessions, explore data structures.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install redis --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `uvx` (uv tool runner) |
| Env vars | `REDIS_URL` |

```bash
export REDIS_URL=redis://localhost:6379
# with auth:
export REDIS_URL=redis://:password@host:6379/0
```

## Typical usage

```
List all keys matching "session:*" and show their TTLs.
Get the value of key "feature_flags:payments_v2".
Check if rate-limit key "rl:user:42" exists and show its current value.
```

## Notes

- Point at a **read-replica or staging instance** for production safety.
