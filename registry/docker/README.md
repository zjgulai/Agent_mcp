# docker MCP

List containers, manage images, start/stop services, read logs, and orchestrate Docker Compose stacks.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install docker --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `uvx` + Docker daemon running |
| Env vars | None (uses local Docker socket) |

Docker Desktop or Docker Engine must be running. Connects via `/var/run/docker.sock`.

## Typical usage

```
List all running containers and their port mappings.
Show the last 100 log lines from the "api" container.
Restart the "worker" container.
Bring up the services in ./docker-compose.dev.yml.
```

## Notes

- For remote Docker hosts, set `DOCKER_HOST` in your shell before starting the MCP server.
