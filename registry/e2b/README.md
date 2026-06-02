# e2b MCP

Run arbitrary code in secure cloud sandboxes — safe execution of untrusted scripts in isolated containers.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install e2b --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `E2B_API_KEY` |

```bash
export E2B_API_KEY=e2b_...
```

Get a free key at <https://e2b.dev> (sandbox hours in free tier).

## Typical usage

```
Run this Python data-processing script against the CSV and return the output.
Execute these shell commands in a clean Ubuntu environment and show stdout/stderr.
Test this regex against 50 sample strings without running it locally.
```

## Notes

- Supports Python, Node.js, Bash, and custom Docker images.
- Each sandbox is isolated — no risk to the local machine.
