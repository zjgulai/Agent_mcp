# slack MCP

Send messages, read channel history, post notifications, and manage Slack workspaces.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install slack --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID` |

```bash
export SLACK_BOT_TOKEN=xoxb-...
export SLACK_TEAM_ID=T0123456
```

Create a Slack app at <https://api.slack.com/apps>, add scopes (`channels:read`, `chat:write`, `channels:history`), install to workspace, copy Bot User OAuth Token.

`SLACK_TEAM_ID` is visible in the Slack URL: `app.slack.com/client/T0123456/...`

## Typical usage

```
Post a deploy summary to #deployments: "v2.3.1 shipped, 0 errors in first 5 min."
Search #incidents for messages mentioning "database timeout" in the last 24 hours.
List all public channels with more than 100 members.
```
