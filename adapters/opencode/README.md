# Adapters · opencode

写入 `~/.config/opencode/opencode.json` 的 `mcp` 段。

```json
{
  "mcp": {
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" },
      "_managed_by": "agent-mcp",
      "_managed_at": "2026-05-16T..."
    }
  }
}
```

实现：[`../../agent/lib/adapter_opencode.py`](../../agent/lib/adapter_opencode.py)（P1.2）
