#!/usr/bin/env bash
# PreToolUse hook: guards subagent tool calls (logic in guard.py).
# Main-session calls carry no agent_id and pass. Fails closed.
input=$(cat)
case "$input" in
  *'"agent_id"'*) ;;
  *) exit 0 ;;
esac
command -v python3 >/dev/null 2>&1 || { echo "Blocked: guard hook needs python3." >&2; exit 2; }
printf '%s' "$input" | python3 -I "$(dirname "$0")/guard.py"
