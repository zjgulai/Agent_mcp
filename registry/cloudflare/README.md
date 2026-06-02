# cloudflare MCP

Manage Cloudflare Workers, KV, R2, D1, DNS, and CDN settings through the Cloudflare API.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install cloudflare --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `CLOUDFLARE_API_TOKEN` |

```bash
export CLOUDFLARE_API_TOKEN=your_token_here
```

Create at <https://dash.cloudflare.com/profile/api-tokens> — use "Edit Cloudflare Workers" template.

## Typical usage

```
Deploy the worker in ./dist/worker.js to the production environment.
List all KV namespaces and their key counts.
Add a CNAME record pointing staging.example.com → my-project.pages.dev.
Query D1 database "analytics" for the top 10 pages by views this week.
```
