# Phase 0 · Agent_mcp Bootstrap

> 创建时间：2026-05-16
> 决策来源：与 user 讨论确认的 8 项决策（见 aim-memory `agent-kit` context）

## 目标

让 `Agent_mcp/` 拥有与 `Agent_skills/` / `Agent_hook/` 同形的"管理面板"骨架。

## 必须落地的目录

```
Agent_mcp/
├── AGENTS.md                ✅ 项目级 AI 协作规则
├── README.md                ✅
├── opencode.json            ✅
├── .opencode/
│   ├── agent/mcp-manager.md            ✅
│   └── commands/{list,install,uninstall,doctor,sync}.md  ✅
├── .sisyphus/plans/
│   ├── 01-bootstrap.md      ← 本文件
│   └── 02-execution-todo.md
├── agent/
│   ├── lib/                 manifest.py + 4 个 adapter_*.py（P0.4）
│   └── docs/
├── registry/                空（P1.1 开始填）
├── adapters/{opencode,codex,cursor,kimi}/
├── docs/                    空
└── tests/
```

## 验收标准

- [ ] `tree -L 3 Agent_mcp/` 与上面骨架一致
- [ ] AGENTS.md UTF-8 NO BOM
- [ ] P0.4 之后 `pytest tests/` passing

## 不做的事

- ❌ 不写 portal/
- ❌ 不创建任何具体 MCP —— P1 才开始
- ❌ 不动客户端配置文件
