# vercel MCP

Deployment management, build status, environment variable management, and log access via the Vercel API.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install vercel --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `VERCEL_TOKEN` |

```bash
export VERCEL_TOKEN=...
```

Create a token at <https://vercel.com/account/settings/tokens>.

## Typical usage

```
What was the last deployment status for the "my-app" project on production?
Show the build logs for the failed deployment dpl_xyz.
List all environment variables set on the "api" project for the production environment.
```
