# perplexity MCP

Citation-backed deep web research with multi-source synthesis via the Perplexity AI API.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install perplexity --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `PERPLEXITY_API_KEY` |

```bash
export PERPLEXITY_API_KEY=pplx-...
```

Get a key at <https://www.perplexity.ai/settings/api>.

## Typical usage

```
Research the current state of MCP security vulnerabilities in 2026, with citations.
Compare Cloudflare Workers vs AWS Lambda pricing and performance for edge use cases.
What open-source LLM inference frameworks have gained the most traction in the last 6 months?
```

## Notes

- Best for research tasks that require verifiable sources (technical articles, competitive analysis).
- Use `brave-search` for quick lookups; use `perplexity` when you need multi-source synthesis.
