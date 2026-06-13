# xquik MCP

Remote MCP access for Xquik X/Twitter data workflows, API exploration, public data collection, media metadata, and monitoring setup.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install xquik --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `XQUIK_API_KEY` |

```bash
export XQUIK_API_KEY=your_api_key
```

Get an API key from the Xquik dashboard. Keep it in your shell environment or secret manager, not in tracked files.

## Typical usage

```
Explore available Xquik MCP tools for read-only X/Twitter data collection.
Build a source-backed tweet search workflow for these public keywords.
Prepare a monitoring plan for this public account and include validation steps.
```

## Notes

- Uses `mcp-remote@0.1.38` to bridge the documented remote MCP endpoint into stdio-only clients.
- The API key is passed through the `XQUIK_API_KEY` environment variable only.
- Check intended use, consent, and data protection requirements before collecting or storing personal data.
