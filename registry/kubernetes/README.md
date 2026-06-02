# kubernetes MCP

Pod inspection, deployment management, log retrieval, and cluster resource status via kubectl.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install kubernetes --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `uvx` + `kubectl` on PATH |
| Env vars | `KUBECONFIG` |

```bash
export KUBECONFIG=~/.kube/config    # default location — set explicitly for non-default paths
```

`kubectl` must be installed and configured with access to the target cluster.

## Typical usage

```
List all pods in the "payments" namespace that are not in Running state.
Show the last 200 log lines from the "api-server" pod in production.
What deployments were rolled out in the "backend" namespace in the last 24 hours?
Scale the "worker" deployment in staging to 3 replicas.
```

## Notes

- Uses the kubeconfig context that is active in your shell — switch contexts with `kubectl config use-context` before starting the MCP.
- For read-only cluster inspection, bind a `ClusterRole` with `get`, `list`, `watch` verbs only.
