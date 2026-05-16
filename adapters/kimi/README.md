# Adapters · kimi

通过 shell 调用 `kimi mcp add <name> --command <cmd> --arg <a1> --arg <a2> --env KEY=value`。

不直接写文件，因为 kimi CLI 提供原生命令。

锚点写在 manifest 维护的本地清单文件 `~/.kimi/.agent-mcp-managed.json`，记录我们装过哪些，方便卸载。

实现：[`../../agent/lib/adapter_kimi.py`](../../agent/lib/adapter_kimi.py)（P1.2）
