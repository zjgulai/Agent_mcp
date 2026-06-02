# google-drive MCP

Search and access Google Drive files, Docs, and Sheets — read and organise cloud-stored documents.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install google-drive --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `GDRIVE_CLIENT_ID`, `GDRIVE_CLIENT_SECRET`, `GDRIVE_REDIRECT_URI` |

```bash
export GDRIVE_CLIENT_ID=...apps.googleusercontent.com
export GDRIVE_CLIENT_SECRET=GOCSPX-...
export GDRIVE_REDIRECT_URI=http://localhost:3000/oauth/callback
```

Create OAuth 2.0 credentials at <https://console.cloud.google.com/apis/credentials> with the Google Drive API enabled.

## Typical usage

```
Find all spreadsheets in my Drive modified in the last 7 days.
Read the content of "Q2 2026 OKRs" Google Doc and summarise the key results.
List files in the "Product Specs" folder shared with my team.
```
