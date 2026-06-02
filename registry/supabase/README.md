# supabase MCP

Full Supabase backend access: Postgres queries, auth user management, storage operations, edge function deployment.

See [manifest.yaml](manifest.yaml) for the full schema. Managed by the [Agent_mcp](../../README.md) source repo.

## Install

```bash
agent-mcp install supabase --client opencode|codex|cursor|kimi|all
```

## Requirements

| Item | Value |
|------|-------|
| Runtime | `npx` / Node.js |
| Env vars | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` |

```bash
export SUPABASE_URL=https://xxxx.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

Both values: Supabase project → Settings → API.
**Service role key bypasses RLS** — use read-only Postgres role for production queries.

## Typical usage

```
How many users signed up in the last 7 days? Query auth.users.
List all storage buckets and their sizes.
Show RLS policies on the "posts" table.
Deploy the edge function in ./supabase/functions/send-email/index.ts.
```
