# Adapters · cursor

写入 `~/.cursor/mcp.json`（全局），格式参考 cursor 官方 MCP 文档。

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" },
      "_managed_by": "agent-mcp"
    }
  }
}
```

实现：[`../../agent/lib/adapter_cursor.py`](../../agent/lib/adapter_cursor.py)（P1.2）
