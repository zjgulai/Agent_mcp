# sqlite MCP

Query local SQLite databases — schema inspection, SQL execution, data analysis on embedded files.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install sqlite --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `uvx` (uv tool runner) |
| Env vars | `SQLITE_DB_PATH` |

```bash
export SQLITE_DB_PATH=/path/to/database.db
```

## Typical usage

```
Show the schema of the "orders" table.
How many rows in "events", grouped by event_type?
Find users who signed up in the last 30 days and haven't placed an order.
```

## Notes

- Supports read and write — use a copy of the file for destructive operations.
- Ideal for local dev DBs, embedded app DBs, or exported data files.
