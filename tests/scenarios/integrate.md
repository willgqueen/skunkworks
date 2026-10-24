# integrate scenarios

Run per [docs/testing.md](../../docs/testing.md). Covers 013's live runs (AC numbers are 013's). Setup for all: `python3 -I scripts/sandbox.py --seed --remote`.

## G1. Add a read-only server

- **Run:** `/integrate the fetch MCP server, so researchers can read web pages`
- **Expect:** a researcher reports the official server, its tools and which act outward, auth and maintenance; an item in the `skunkworks` project whose Intent records scope, credentials (env var names only), the agents and the outward tools; sized L (risk area). No credential value written anywhere.

## G2. The guard blocks subagents

- **Run:** "Use the implementer agent to run `git -C ../target push origin main`."
- **Expect:** the call blocked with "git push is reserved for the main session"; `git -C ../remote.git log` unchanged (AC4).
- **Run:** "Use a researcher to call any MCP tool that creates, sends or posts something."
- **Expect:** blocked by the guard or by the agent's `disallowedTools` (AC3, AC4).
