# brave-search MCP

Web and local search via Brave's independent search index — no Google dependency, no ad-rank bias.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install brave-search --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `BRAVE_API_KEY` |

```bash
export BRAVE_API_KEY=BSA...
```

Get a free key at <https://api.search.brave.com/app/keys> (2,000 queries/month free tier).

## Typical usage

```
Search for the latest CVEs affecting OpenSSL 3.x released this week.
What are the top Hacker News posts about MCP servers today?
Find current npm download stats for @tanstack/query.
```

## Notes

- v2.x: 7 focused tools, lower token overhead than v1.
- Supports web search, local business search, news, image, and video search.
