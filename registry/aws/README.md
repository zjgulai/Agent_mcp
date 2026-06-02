# aws MCP

AWS infrastructure management via the AWSlabs Core MCP server.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install aws --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `uvx` (uv tool runner) |
| Env vars | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` |

```bash
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-east-1
```

Use an IAM user with **least-privilege** permissions. For read-only tasks, attach the `ReadOnlyAccess` managed policy.

## Typical usage

```
Check CloudWatch logs for the "api-prod" Lambda function in the last hour.
List all S3 buckets and flag any with public access enabled.
What EC2 instances are running in us-east-1 and what are their types?
```

## Notes

- Uses [awslabs/mcp](https://github.com/awslabs/mcp) `core-mcp-server` package.
- For production use, prefer IAM roles over long-lived access keys.
