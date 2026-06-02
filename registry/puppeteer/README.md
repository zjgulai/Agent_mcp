# puppeteer MCP

Headless Chrome automation — screenshots, PDF generation, JavaScript-heavy page scraping.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install puppeteer --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | None |

Puppeteer downloads Chromium on first run (~170 MB). Subsequent runs use the cached binary.

## Typical usage

```
Take a screenshot of https://example.com/dashboard at 1440×900 and save it.
Generate a PDF of https://docs.example.com/api for offline reading.
Scrape the product prices from this React SPA (needs JS execution).
```

## Notes

- Prefer `playwright` for new work — it's faster, supports more browsers, and has better tooling.
- Use `puppeteer` when Chrome-specific behaviour is required or `playwright` is unavailable.
