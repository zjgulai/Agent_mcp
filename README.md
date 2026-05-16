# Agent_mcp

> 🔌 MCP server registry for the [agent-kit](https://github.com/zjgulai) workflow factory · one install command, four AI CLIs
>
> **Docs site**: [zjgulai.github.io/Agent_mcp](https://zjgulai.github.io/Agent_mcp/)

## What

**Agent_mcp** is the single source of truth for MCP (Model Context Protocol) servers shared across opencode + codex + cursor + kimi. One manifest per server. Adapters write the right config into each AI CLI's native format. Tokens stay in environment variables — never in any file.

| | |
|---|---|
| MCPs registered | **10** (6 P0 + 4 P1) |
| Tests passing | **39** (28 schema + 11 adapter) |
| Clients supported | opencode, codex, cursor, kimi |
| Companion repos | [Agent_skills](https://github.com/zjgulai/Agent_skills) · [Agent_hook](https://github.com/zjgulai/Agent_hook) |

## Quick start

```bash
git clone https://github.com/zjgulai/Agent_mcp.git ~/project/Agent_mcp
cd ~/project/Agent_mcp
python3 -m pip install --user pyyaml tomli tomli_w

export GITHUB_TOKEN=ghp_yourtoken
export POSTGRES_CONNECTION_STRING=postgres://...

./bin/agent-mcp doctor
./bin/agent-mcp install github --client all
./bin/agent-mcp list
```

## The 10 MCPs

**P0 (must-install)**:

| Name | Use case | Env required |
|---|---|---|
| github | PRs, issues, code search, CI | `GITHUB_TOKEN` |
| filesystem | Allowlist-bounded file IO | — |
| context7 | Up-to-date docs for fast-moving SDKs | — |
| playwright | Real browser navigation, screenshots | — |
| sequential-thinking | Structured multi-step reasoning | — |
| git | Local history, blame, diff | — (uvx) |

**P1 (recommended)**:

| Name | Use case | Env required |
|---|---|---|
| postgres | Schema inspection, query | `POSTGRES_CONNECTION_STRING` |
| sentry | Production exception → fix loop | `SENTRY_AUTH_TOKEN` |
| figma | Design tokens, components | `FIGMA_API_TOKEN` |
| linear | Tickets, status updates | `LINEAR_API_KEY` |

## Architecture

See [Architecture](https://zjgulai.github.io/Agent_mcp/architecture.html) and [Handbook](https://zjgulai.github.io/Agent_mcp/handbook.html).

```
registry/<name>/manifest.yaml            ← single source of truth

agent/lib/manifest.py                    ← shared schema (byte-identical 3 repos)
agent/lib/adapter_opencode.py            ← merges into ~/.config/opencode/opencode.json
agent/lib/adapter_codex.py               ← merges into ~/.codex/config.toml
agent/lib/adapter_cursor.py              ← merges into ~/.cursor/mcp.json
agent/lib/adapter_kimi.py                ← shells out to: kimi mcp add
agent/lib/cli.py                         ← agent-mcp list/install/uninstall/doctor/show
```

Each write to a client config:

1. `cp <target> <target>.bak.{timestamp}` (timestamped backup)
2. Write with `_managed_by: agent-mcp` anchor
3. `prune_backups(keep=5)` to bound storage
4. On uninstall: refuse to delete entries we didn't manage

## Secret model

Tokens **never** live in any file managed by agent-mcp. The manifest declares the env-var **name**:

```yaml
requires:
  binaries: [npx, node]
  env: [GITHUB_TOKEN]
```

The adapter writes `${GITHUB_TOKEN}` into client configs. The CLI runtime inherits the actual value from the shell. Schema rejects literal `ghp_*`, `sk-*`, `AIza*` patterns at load time.

## Test

```bash
python3 -m pytest tests/   # 39 tests, all green
```

## License

MIT.

## Related

- [Agent_skills](https://github.com/zjgulai/Agent_skills) — the **methodology** layer (16 skills)
- [Agent_hook](https://github.com/zjgulai/Agent_hook) — the **enforcement** layer (9 hooks)
