---
description: 安装一个 MCP 到指定客户端（或全部）。
agent: mcp-manager
---

# /mcp-install <name> [--client opencode|codex|cursor|kimi|all]

工作流：

1. 读 `registry/<name>/manifest.yaml`，校验 schema
2. 检查 `compatibility.<client>`，`unsupported` 直接退出
3. 检查 `requires.env`，未设置时给 warning（不阻止）
4. **备份** 目标客户端配置 `cp <target> <target>.bak.{timestamp}`
5. 调用 `agent/lib/adapter_<client>.py` 写入（带锚点）
6. 输出：写入位置 + 备份位置 + 验证命令（如 `kimi mcp list`）
