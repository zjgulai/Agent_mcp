---
name: agent-mcp-rules
description: Agent_mcp 项目级 AI 协作规则。定义 MCP 源仓库的硬约束、目录边界、四客户端适配协议、Manifest schema 规范、Secret 管理。当你在 Agent_mcp 目录下做任何修改时使用。
---

# Agent_mcp · 项目规则

本项目级规则覆盖 `~/.config/opencode/AGENTS.md` 中冲突的部分（项目级优先），未覆盖的部分继承全局。

## 一、项目定位

**Agent_mcp** —— MCP（Model Context Protocol）服务器的本地用户级源仓库。三仓之一。

**单一真相源**：`registry/<mcp-name>/manifest.yaml` 是 MCP 的元数据 + 启动指令。

**四客户端分发**：`adapters/{opencode,codex,cursor,kimi}/` 把 manifest 翻译成各客户端的原生 MCP 配置：

- `opencode/` → merge 到 `~/.config/opencode/opencode.json` 的 `mcp` 段
- `codex/` → merge 到 `~/.codex/config.toml` 的 `[mcp_servers.*]`
- `cursor/` → merge 到 `~/.cursor/mcp.json`
- `kimi/` → 调用 `kimi mcp add <name> --command ...`

## 二、必读

接到任何任务前先读：

1. [本仓 README](README.md)
2. `.sisyphus/plans/01-bootstrap.md` —— Phase 0 决策与目标结构
3. [统一 manifest schema](agent/lib/manifest.py)
4. [上级目录 AGENTS.md](file:///Users/lute/project/Agent/AGENTS.md)（如存在）

## 三、硬约束（不可违反）

### 文件系统访问

| 对象 | 谁能改 | 怎么改 |
|---|---|---|
| `registry/<name>/manifest.yaml` | agent 直接改 | 必须通过 `agent/lib/manifest.py` 验证 |
| `adapters/<client>/` | agent 直接改 | 写客户端配置前**必须** `cp <target> <target>.bak.{timestamp}` |
| 客户端配置文件 | **必须**走 adapter | 锚点：`# managed-by: agent-mcp` 或 JSON 中 `_managed_by: agent-mcp` 属性 |

### MCP Manifest 必填字段

`kind: mcp`；`mcp_command: [...]`（启动命令数组，含 `npx`/`uvx`/`python` 等）；`compatibility` 四客户端必须显式声明；如需要 Secret，必须在 `requires.env: [...]` 列出（**绝不**写明文 token）。

### Secret 管理

按决策 8：所有 MCP 需要的 Secret 走**环境变量**。

- Manifest 的 `requires.env: [GITHUB_TOKEN, SENTRY_AUTH_TOKEN, ...]` 是真相
- Adapter 在写客户端配置时，把 env name 写进 `env:` 字段（如 opencode mcp 的 `env: { GITHUB_TOKEN: "${GITHUB_TOKEN}" }`），让客户端运行时从 shell 环境继承
- **绝不**把实际 token 写进任何文件

### 端口约定

- MCP 服务器多数用 stdio，无端口。
- 若未来引入 SSE / WebSocket MCP，端口由 manifest.mcp_command 显式声明，并在 doctor 命令里校验。

## 四、协作纪律

- **不动 Agent_skills 和 Agent_hook** —— 三仓互不交叉文件级修改。
- 写代码前 → 先看 `registry/` 已有哪些 MCP 注册。
- 改 adapter → 必须跑 `pytest tests/` 全绿，必须先备份目标客户端配置。
- 新增 MCP → 走 P4 的 `agent-mcp new <name>` 脚手架。

## 五、术语

- **Source / 源** = `registry/<name>/manifest.yaml`，单一真相
- **Adapter / 适配器** = `adapters/<client>/` 翻译脚本
- **Anchor / 锚点** = 客户端配置中的 managed-by 标识，用于按锚点删除
- **Native** = 该客户端有专门的 MCP 注册命令（kimi）或字段（opencode/codex/cursor 都有）—— 我们四个都视为 native
