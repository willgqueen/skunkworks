---
name: integrate
description: Add an MCP server or external API to the toolkit the standard way, through a normal item: scope, credentials, agent access, guard rules and a registry entry. Use when the user wants to connect a service, an MCP server or an API.
argument-hint: <service or MCP server> [purpose]
---

# integrate

Follow [docs/integrations.md](../../../docs/integrations.md). Integrations touch secrets and outward actions, a [risk area](../../../docs/criteria.md#building-blocks); size the item by [criteria.md](../../../docs/criteria.md#size).

1. **Research** (a `researcher` agent): the official server or API, its tools or endpoints, which of them act outward, its auth options and narrowest scopes, and whether it's maintained. Prefer official servers.
2. **Create the item** with **new-item** (`skunkworks` project), recording in its Intent: the purpose, scope (project `.mcp.json` or local), credentials (env var names), the agents that need it, and the outward tools.
3. Deliver adds:
   - the server config: stdio servers through `scripts/with-env.sh <VARS> -- <command>`, HTTP servers with a headersHelper; variable names (no values) in `.env.local.example`
   - each read-only tool the agents need, in `.claude/hooks/mcp-allow.txt` and the agent's `tools` list; outward tools stay main-session only
   - the registry row in docs/integrations.md
4. **Never** write a credential value into any file but `.env.local`.
