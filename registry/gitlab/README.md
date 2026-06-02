# gitlab MCP

Merge requests, CI/CD pipeline inspection, issue tracking, and repository access via the GitLab API.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install gitlab --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `uvx` (uv tool runner) |
| Env vars | `GITLAB_PERSONAL_ACCESS_TOKEN`, `GITLAB_URL` |

```bash
export GITLAB_PERSONAL_ACCESS_TOKEN=glpat-...
export GITLAB_URL=https://gitlab.com         # or your self-hosted instance
```

Create a Personal Access Token at GitLab → User Settings → Access Tokens with `api` scope.

## Typical usage

```
List open MRs assigned to me that have failed pipeline checks.
Show the CI/CD pipeline logs for the last failed job in the "backend" project.
Create an issue in project "infra/k8s" titled "Upgrade cert-manager to v1.14".
```
