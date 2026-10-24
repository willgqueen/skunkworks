#!/usr/bin/env bash
# Installs a git pre-commit hook that runs scripts/test.py. Optional.
# Usage: scripts/install-hooks.sh [--force]
set -e
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
hooks=$(git -C "$root" rev-parse --path-format=absolute --git-path hooks)
target="$hooks/pre-commit"
if [ -e "$target" ] && [ "$1" != "--force" ]; then
  echo "A pre-commit hook already exists at $target; rerun with --force to replace it." >&2
  exit 1
fi
mkdir -p "$hooks"
printf '#!/usr/bin/env bash\nexec python3 -I "%s/scripts/test.py"\n' "$root" > "$target"
chmod +x "$target"
echo "pre-commit hook installed at $target"
