---
description: 体检：manifest 合法性、客户端配置一致性、env 满足度、MCP 服务器可启动性（轻量探针）。
agent: mcp-manager
---

# /mcp-doctor

按顺序检查：

1. 所有 `registry/*/manifest.yaml` 通过 schema 验证
2. 每个 MCP 的 `requires.binaries`（npx/uvx/python）在 PATH 中可用
3. 每个 MCP 的 `requires.env` 都已设置
4. 客户端配置文件中的 anchor 与 registry 一致（无孤儿、无遗漏）
5. （可选）冒烟启动：跑 `mcp_command` 几秒看能否握手
