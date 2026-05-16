# Security Policy

## Reporting a vulnerability

Please **do not** open a public GitHub issue. Instead:

1. Email **zjgulai@github.com** (or open a private GitHub Security Advisory at <https://github.com/zjgulai/Agent_mcp/security/advisories>)
2. Include:
   - Repo + commit SHA you reproduced on
   - MCP name, command line that's affected
   - Whether it involves a client config mutation, secret exposure, or upstream MCP server vulnerability
   - For client-config issues: the `before / after` state observed

We aim to triage within **3 business days**.

## What we consider a security issue

Agent_mcp connects AI agents to **real services** (GitHub, Postgres, Sentry, Linear, ...). Bugs here can leak production data:

| Severity | Example |
|---|---|
| Critical | A literal token is written to a checked-in manifest and the schema validator fails to reject it |
| Critical | An MCP launch command interpolates a user-provided string into `npx` args without escaping (command injection at MCP startup) |
| Critical | An adapter writes the **value** of an env var (instead of `${VAR}` interpolation directive) into a client config |
| High | A manifest's `mcp_command` includes `--dangerously-allow-something` flag that bypasses the upstream MCP's own protections |
| High | Adapter accidentally deletes a non-managed MCP entry from a user's client config |
| Medium | `requires.env` declares the wrong env name, so the MCP runs with a different secret than intended |
| Medium | `prune_backups()` deletes more than `keep=N` files |
| Low | Documentation describes an env var that the manifest doesn't actually require |

## What is NOT a security issue

- The user choosing not to set a `requires.env` value — `doctor` reports WARN, install proceeds, MCP fails at runtime. Expected.
- An upstream MCP package (e.g. `@modelcontextprotocol/server-github`) having a vulnerability — file an issue with that upstream project. We can pin a version range as a mitigation.
- A user's `~/.zshrc` containing tokens — that's their secret store.

## Token / secret model — STRICTLY ENV-VAR

**Tokens never live in any file managed by this repo.** The flow:

1. User exports tokens: `export GITHUB_TOKEN=ghp_...`
2. Manifest declares only the env-var **name**: `requires.env: [GITHUB_TOKEN]`
3. Adapter writes literal `${GITHUB_TOKEN}` (interpolation directive) — opencode/cursor — or shells out `kimi mcp add ... -e GITHUB_TOKEN=$GITHUB_TOKEN` — kimi.
4. Client runtime inherits the value from shell env at MCP child-process start.

Schema validator regex: `(ghp_|gho_|sk-[a-zA-Z0-9]{10,}|AIza[0-9A-Za-z\-_]{20,})`. Any manifest containing this pattern is rejected at load time. **If a literal token slips through into a committed manifest, that is a critical bug — report it.**

## MCP launch command security

`mcp_command` items must be **literal strings**, not user input. We do not interpolate user-supplied values into `mcp_command` at install time. The only interpolation is `${ENV_VAR}` directives, which clients expand at runtime.

Forbidden in `mcp_command`:
- Backticks, `$()` shell expansion
- Anything from a user-supplied flag at install time

Allowed:
- Literal arguments from the manifest YAML
- `${VAR_NAME}` env-var references (only if `VAR_NAME` is in `requires.env`)
- `--allowlist <path>` style arguments where `<path>` is a literal in the manifest

## Update policy

Critical / High issues:
- Patch within **7 business days** of confirmation
- CVE filed if exploitable
- Fix coordinated across all three companion repos if `manifest.py` schema is involved

## Companion repos

- [Agent_skills](https://github.com/zjgulai/Agent_skills) (methodology layer)
- [Agent_hook](https://github.com/zjgulai/Agent_hook) (enforcement layer)

Shared `agent/lib/manifest.py` (md5 `b46c2f55980b9aa2ea93b87941c833e2`) is the spine. Schema-affecting fixes require coordinated patches.
