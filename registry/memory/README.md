# memory MCP

Knowledge-graph-based persistent memory across agent sessions.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install memory --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | None |

## Typical usage

```
Remember that the payments service owner is Alice and she prefers Slack DMs.
What do you know about the auth-service architecture decisions we discussed last week?
Store the fact that staging DB is read-only and requires VPN.
```

## Notes

- Stores entities, relationships, and observations in a local JSON knowledge graph.
- Persists across sessions — data survives agent restarts.
- Use `create_entities` / `add_observations` / `search_nodes` MCP tools.
