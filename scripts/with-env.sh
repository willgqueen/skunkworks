#!/usr/bin/env bash
# Starts a command with only the named variables loaded from .env.local, so
# credentials reach one MCP server's process and nothing else.
# Usage: scripts/with-env.sh VAR1,VAR2 -- command [args...]
set -euo pipefail
[ $# -ge 1 ] && [ -n "$1" ] || { echo "usage: with-env.sh VAR1,VAR2 -- command [args...]" >&2; exit 1; }
names=$1; shift
[ "${1:-}" = "--" ] && shift
[ $# -gt 0 ] || { echo "with-env: no command given" >&2; exit 1; }
env_file="$(cd "$(dirname "$0")/.." && pwd)/.env.local"
args=()
IFS=, read -ra wanted <<< "$names"
for name in "${wanted[@]}"; do
  [[ $name =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || { echo "with-env: bad variable name: $name" >&2; exit 1; }
  value=$(awk -v n="$name" '{sub(/\r$/, ""); sub(/^export[ \t]+/, "")} index($0, n "=") == 1 {v = substr($0, length(n) + 2)} END {if (v == "") exit 1; print v}' "$env_file") \
    || { echo "with-env: $name not in .env.local" >&2; exit 1; }
  value=${value#\"}; value=${value%\"}; value=${value#\'}; value=${value%\'}
  args+=("$name=$value")
done
exec env "${args[@]}" "$@"
