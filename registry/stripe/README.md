# stripe MCP

Customer lookup, payment intents, subscriptions, invoices, and dispute management via the Stripe API.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install stripe --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `STRIPE_API_KEY` |

```bash
export STRIPE_API_KEY=sk_test_...   # use sk_live_... for production
```

Use a **restricted key** scoped to only the permissions needed — never a full-access live key in shared environments.

## Typical usage

```
Look up customer john@example.com and show their active subscriptions and last 5 invoices.
Why did payment intent pi_3Xyz fail? Show the decline code.
List all disputed charges from the last 30 days over $100.
```
