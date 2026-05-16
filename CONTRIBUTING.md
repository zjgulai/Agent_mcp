# Contributing to Agent_mcp

Thanks for considering a contribution! Agent_mcp is the **context layer** of a three-repo system — MCP servers that connect AI agents to GitHub, the filesystem, browsers, databases, etc.

## Three-repo system

- **[Agent_skills](https://github.com/zjgulai/Agent_skills)** — methodology · 16 skills
- **[Agent_hook](https://github.com/zjgulai/Agent_hook)** — enforcement · 9 hooks
- **[Agent_mcp](https://github.com/zjgulai/Agent_mcp)** (this repo) — context · 10 MCPs

`agent/lib/manifest.py` is **byte-identical** across all three repos (md5 `b46c2f55980b9aa2ea93b87941c833e2`).

## Quick start (development)

```bash
git clone https://github.com/zjgulai/Agent_mcp.git ~/project/Agent_mcp
cd ~/project/Agent_mcp
python3 -m pip install --user pyyaml tomli tomli_w pytest

python3 -m pytest tests/   # 39 tests must pass

./bin/agent-mcp list
./bin/agent-mcp doctor    # checks env + binaries availability
```

## MCP manifest contract

Every `registry/<name>/manifest.yaml` MUST declare:

```yaml
kind: mcp                                     # required
name: kebab-case-name                         # required: [a-z][a-z0-9-]{1,63}
version: 0.1.0                                # required: semver
description: |                                # required: 20+ chars (WHAT + WHEN)
  GitHub MCP server providing repo, issue, PR access.
  Use whenever working with github.com workflows.
domain: ops                                   # required: meta|code-quality|desktop|founder|frontend|research|data|ops|general
priority: P0                                  # required: P0|P1|P2

compatibility:                                # required: all 4 clients
  opencode: native
  codex: native
  cursor: native
  kimi: native

source:
  type: npm                                   # local | external | git | npm | pypi
  package: "@modelcontextprotocol/server-github"

mcp_command:                                  # required when kind=mcp
  - npx
  - "-y"
  - "@modelcontextprotocol/server-github"

requires:
  binaries: [npx, node]                       # what must be on PATH
  env: [GITHUB_TOKEN]                         # secret env var NAMES, never values

triggers: [github, pull request, issue]       # phrases that should activate this MCP

links:
  upstream: https://github.com/...
```

## Secret model — STRICTLY ENV-VAR

**Tokens never live in any file managed by agent-mcp.** Schema enforces this with a regex check that rejects literal `ghp_*`, `sk-[a-zA-Z0-9]{10,}`, `AIza[0-9A-Za-z_-]{20,}` patterns at load time.

The flow:

1. User exports the token in their shell: `export GITHUB_TOKEN=ghp_...`
2. Manifest declares the env name: `requires.env: [GITHUB_TOKEN]`
3. Adapter writes `${GITHUB_TOKEN}` (a literal interpolation directive, **not** the value) into client config
4. Client runtime inherits the actual value from the shell

If you submit a manifest with a literal token, **the schema validator will reject it** at PR test time. This is intentional and non-negotiable.

## Adapter contracts

Each `agent/lib/adapter_<client>.py` must implement:

- **opencode** — merge into `~/.config/opencode/opencode.json` `mcp.<name>` JSON path
- **codex** — merge into `~/.codex/config.toml` `[mcp_servers.<name>]` TOML section
- **cursor** — merge into `~/.cursor/mcp.json` `mcpServers.<name>` JSON path
- **kimi** — shell out to `kimi mcp add <name> -- <command...>` (kimi has a native CLI)

**Hard rules**:

1. Anchor every write — `_managed_by: agent-mcp` field (opencode/cursor) or `~/.codex/.agent-mcp-managed.json` registry (codex/kimi).
2. Backup before mutate; `prune_backups(keep=5)` after.
3. Refuse to delete entries we didn't add.
4. Test with `monkeypatch` paths.

## Pull request rules

1. **Tests pass** — 39+ tests, all green.
2. **Schema valid** — `python3 -m pytest tests/test_manifest_schema.py`.
3. **No literal tokens** in any diff (CI will reject if `ghp_`, `sk-`, `AIza` strings appear in YAML/JSON files).
4. **Conventional commit message**.
5. **CHANGELOG.md updated**.
6. If touching `agent/lib/manifest.py` → sync to all 3 repos via `agent/lib/sync_manifest_lib.sh`.

## Adding a new MCP

```bash
# 1. Scaffold
~/project/Agent/agent-kit/bin/agent-kit new mcp my-mcp

# 2. Fill in manifest.yaml:
#    - mcp_command (npx/uvx/python ...)
#    - requires.binaries + requires.env
#    - compatibility for 4 clients
#    - description with concrete trigger scenarios

# 3. Verify the upstream MCP package actually starts:
npx -y <package>  # or uvx <package>

# 4. Run tests + doctor
python3 -m pytest tests/
./bin/agent-mcp doctor

# 5. Smoke test (real opencode):
./bin/agent-mcp install my-mcp --client opencode
opencode mcp list   # should show my-mcp connected
./bin/agent-mcp uninstall my-mcp --client opencode

# 6. Open PR
```

## Issue reporting

<https://github.com/zjgulai/Agent_mcp/issues>. Include:

- MCP name + repo SHA
- `./bin/agent-mcp doctor` output
- For runtime issues: `opencode mcp list` output (or equivalent for other CLIs)
- Whether the upstream MCP works standalone (`npx -y <package>`)

## License

By contributing, you agree your work is licensed under [MIT](LICENSE).
