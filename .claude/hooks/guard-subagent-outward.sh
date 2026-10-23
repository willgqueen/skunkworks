#!/usr/bin/env bash
# PreToolUse hook (Bash and MCP tools): blocks pushes and merges when the call
# comes from a subagent. Main-session calls carry no agent_id and pass.
# A pattern guard, not a sandbox: it errs toward blocking. See docs/agents.md.
input=$(cat)

# Cheap exit for the main session, which never has an agent_id.
case "$input" in
  *'"agent_id"'*) ;;
  *) exit 0 ;;
esac

# From here on the caller may be a subagent, so fail closed.
command -v python3 >/dev/null 2>&1 || { echo "Blocked: guard hook needs python3." >&2; exit 2; }
printf '%s' "$input" | python3 -I -c '
import json, re, sys
try:
    data = json.load(sys.stdin)
except ValueError:
    sys.stderr.write("Blocked: guard hook could not read its input.\n")
    sys.exit(2)
if not data.get("agent_id"):
    sys.exit(0)
tool = data.get("tool_name", "")
agent = data.get("agent_type", "subagent")
blocked = False
if tool.startswith("mcp__"):
    # MCP tools that push, merge or update refs (e.g. a GitHub server).
    blocked = re.search(r"push|merge|update_ref|create_ref", tool, re.I) is not None
else:
    cmd = (data.get("tool_input") or {}).get("command", "")
    seg = r"[^\n;&|]*?"
    word = lambda w: r"(?<![\w.=-])" + w + r"(?![\w-])"
    patterns = [
        word("git") + seg + word("(?:push|merge)"),
        word("gh") + r"\s+pr\s+merge\b",
        word("gh") + r"\s+api\b" + seg + r"(?:/merges?\b|/git/refs|(?:-X|--method)[\s=]*(?:PUT|POST|PATCH|DELETE)\b)",
    ]
    blocked = any(re.search(p, cmd) for p in patterns)
if blocked:
    sys.stderr.write(f"Blocked: pushes and merges are reserved for the main session ({agent}).\n")
    sys.exit(2)
'
