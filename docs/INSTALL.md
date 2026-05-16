# Agent_mcp 安装指南

把 Agent_mcp 从零装到 4 个 AI CLI 都连上 MCP,约 5 分钟。覆盖 macOS(首选)+ Linux(最小适配)。Windows 不在 v0.1 支持范围。

> 假设你已经有 git、Python 3.9+、Node 22+(npx)、curl。没有的话先装这些。

---

## 一、先决条件

| 工具 | 最低版本 | 检查 | 用途 |
|---|---|---|---|
| git | 2.30+ | `git --version` | clone |
| Python | 3.9+ | `python3 --version` | CLI |
| Node | 22+(npx) | `npx --version` | 大多数 MCP 走 npm |
| uvx | 0.4+ | `uvx --version` | git MCP 走 pypi |

uvx 装法: `brew install uv` 或 `pip install uv`。

**至少安装一个 AI CLI**:

| CLI | 安装 | MCP 配置位置 |
|---|---|---|
| [opencode](https://opencode.ai/) | `npm install -g opencode-ai` | `~/.config/opencode/opencode.json` `mcp` 段 |
| [codex](https://github.com/openai/codex-cli) | brew/npm | `~/.codex/config.toml` `[mcp_servers.x]` |
| [cursor](https://cursor.com/) | 桌面 App | `~/.cursor/mcp.json` |
| [kimi](https://kimi.com/) | `pip install kimi-cli` 或下载 | `kimi mcp add` 命令 |

四家全部 native 支持 MCP(MCP 是标准协议,每个现代 CLI 都讲)。

---

## 二、Clone + 装 Python 依赖

```bash
mkdir -p ~/project
cd ~/project
git clone https://github.com/zjgulai/Agent_mcp.git
cd Agent_mcp

python3 -m pip install --user pyyaml tomli tomli_w pytest
```

---

## 三、设置 secret(只配你需要的)

```bash
# 添加到 ~/.zshrc(或 ~/.bashrc)
export GITHUB_TOKEN=ghp_yourtoken                          # github MCP
export POSTGRES_CONNECTION_STRING=postgres://user:pwd@host/db  # postgres MCP
export SENTRY_AUTH_TOKEN=...                               # sentry MCP
export FIGMA_API_TOKEN=...                                 # figma MCP
export LINEAR_API_KEY=lin_api_...                          # linear MCP

source ~/.zshrc
```

不用的 MCP 可以跳过对应 env。`doctor` 会用 WARN 提示但不阻止安装。

---

## 四、跑测试 + 体检

```bash
python3 -m pytest tests/   # 应输出 39 passed

./bin/agent-mcp list       # 看注册的 10 个 MCP
./bin/agent-mcp doctor     # 验证 schema + 二进制(npx/uvx) + env 满足度
```

`doctor` 输出示例:

```
== schema ==
  ok github v0.1.0       (P0, ops)
  ok playwright v0.1.0   (P0, frontend)
  ...

== binaries ==
  ok    github       -> npx (/opt/homebrew/bin/npx)
  ok    git          -> uvx (/Users/you/.local/bin/uvx)
  ...

== env ==
  ok    github       -> GITHUB_TOKEN (set)
  WARN  postgres     -> POSTGRES_CONNECTION_STRING (not set)
  ...
```

---

## 五、装一个 MCP 到一个客户端

```bash
./bin/agent-mcp install context7 --client opencode
# context7 不需要 token,所以最适合首次试装
```

输出示例:

```json
[
  {
    "client": "opencode",
    "config": "/Users/you/.config/opencode/opencode.json",
    "name": "context7",
    "backup": "/Users/you/.config/opencode/opencode.json.bak.20260516T120000",
    "pruned_backups": 0
  }
]
```

---

## 六、装 6 个 P0 MCP 到所有 4 个客户端

```bash
for m in github filesystem context7 playwright sequential-thinking git; do
  ./bin/agent-mcp install "$m" --client all
done

./bin/agent-mcp list   # 应显示每个 MCP 在 4 客户端的状态都是 "managed"
```

---

## 七、各客户端原生方式验证

```bash
# opencode
opencode mcp list
# 应输出: ✓ context7 connected / ✓ github connected / ...

# codex
grep -E "^\[mcp_servers" ~/.codex/config.toml
# 应输出 6 行 [mcp_servers.<name>]

# cursor
python3 -c 'import json; print(list(json.load(open("/Users/you/.cursor/mcp.json"))["mcpServers"].keys()))'

# kimi
kimi mcp list
```

---

## 八、卸载

```bash
./bin/agent-mcp uninstall github --client all
# 按锚点删除,不破坏其他 MCP
```

---

## 九、故障排查

| 现象 | 原因 / 解决 |
|---|---|
| `agent-mcp: command not found` | `chmod +x bin/agent-mcp` |
| `npx: command not found` | 装 Node + npm: `brew install node` |
| `uvx: command not found` | `brew install uv` 或 `pip install uv` |
| 装完后 opencode 不显示 MCP | opencode 进程要重启才加载新 MCP — 退出当前 session 重新开 |
| `WARN env not set` | 只 WARN 不阻止;真用到这个 MCP 时才会运行时失败 |
| `kimi mcp add` 报错 | 确认 `kimi --version` 可执行;kimi 必须已登录 |
| `context7` 启动慢 | npx 首次拉包,后续就快了;可手动 `npx -y @upstash/context7-mcp@latest` 预热 |
| schema 拒收"明文 token" | 这是正确行为 — manifest 里**不能**写 `ghp_*`/`sk-*`/`AIza*` 真值,改用 `requires.env: [VAR_NAME]` |

---

## 十、下一步

- [Handbook](https://zjgulai.github.io/Agent_mcp/handbook.html) — 10 个 MCP 详细参考 + secret 模型
- [Architecture](https://zjgulai.github.io/Agent_mcp/architecture.html) — 单注册表 + 4 适配器形态
- [Agent_skills](https://github.com/zjgulai/Agent_skills) — 配套方法论层(16 skills)
- [Agent_hook](https://github.com/zjgulai/Agent_hook) — 配套强制层(9 hooks)
