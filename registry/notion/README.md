# notion MCP

Read and write Notion pages, databases, and blocks — AI-driven interaction with team wikis and knowledge bases.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install notion --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `NOTION_API_KEY` |

```bash
export NOTION_API_KEY=secret_...
```

Create an integration at <https://www.notion.so/my-integrations>, then share the relevant pages/databases with the integration.

## Typical usage

```
Find all pages in the "Engineering" workspace tagged "RFC" and updated this week.
Create a new page in the "Meeting Notes" database with today's date as title.
Update the "Status" property on task "Migrate auth service" to "In Review".
```

## Notes

- The integration only sees pages/databases explicitly shared with it — share what you need first.
