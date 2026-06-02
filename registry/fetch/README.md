# fetch MCP

Fetches any URL and converts HTML to clean Markdown for LLM consumption. No browser required.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install fetch --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `uvx` (uv tool runner) |
| Env vars | None |

## Typical usage

```
Fetch the content of https://docs.stripe.com/api/charges and summarise the rate limits.
Retrieve https://example.com/changelog and extract all breaking changes.
```

## Notes

- Converts HTML → Markdown before returning — lower token cost than raw HTML.
- Does **not** execute JavaScript. For JS-heavy SPAs, use `playwright` instead.
- Respects `robots.txt` by default.
