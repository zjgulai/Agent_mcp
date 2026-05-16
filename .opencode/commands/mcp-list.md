---
description: 列出所有已注册的 MCP 以及它们在 4 个客户端的安装状态、env 满足度。
agent: mcp-manager
---

# /mcp-list

读取 `registry/*/manifest.yaml`，对每个 MCP 检查：

- opencode: `~/.config/opencode/opencode.json` 的 `mcp` 段是否包含本 MCP
- codex: `~/.codex/config.toml` 的 `[mcp_servers.<name>]` 是否存在
- cursor: `~/.cursor/mcp.json` 是否包含本 MCP
- kimi: `kimi mcp list` 输出是否包含本 MCP
- env: `requires.env` 列出的环境变量是否都已设置

输出表格。
