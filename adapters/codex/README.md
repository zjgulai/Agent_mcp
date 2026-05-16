# Adapters · codex

写入 `~/.codex/config.toml` 的 `[mcp_servers.<name>]` 段。

```toml
# managed-by: agent-mcp · github
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_TOKEN = "${GITHUB_TOKEN}" }
```

注意 codex config.toml 的字段名以 codex CLI 的实际 schema 为准（P1.2 实现时通过 `codex --help mcp` 探针确认）。

实现：[`../../agent/lib/adapter_codex.py`](../../agent/lib/adapter_codex.py)（P1.2）
