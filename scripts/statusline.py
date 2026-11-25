"""Claude Code status line: context fill, with a hand-off nudge at the fill threshold.

The threshold is the fill trigger in docs/criteria.md (Context, Hand off bullet).
Never fails: unknown or malformed input still prints a line and exits 0.

Usage (reads the status line JSON on stdin):
    python3 -I scripts/statusline.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRITERIA = ROOT / "docs/criteria.md"
FILL = re.compile(r"context fill\b[^*]*?reaches \*\*(\d+)%\*\*")
NUDGE = "hand off at the next gate"


def fill_threshold(criteria=CRITERIA):
    """The fill percentage from criteria.md, or None if it can't be read."""
    try:
        match = FILL.search(criteria.read_text())
    except (OSError, UnicodeDecodeError):
        return None
    return int(match.group(1)) if match else None


def used_percentage(raw):
    """The context fill as a rounded int from the status line JSON, or None."""
    try:
        value = json.loads(raw)["context_window"]["used_percentage"]
    except (ValueError, TypeError, KeyError):
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value != value:
        return None
    return round(value)


def render(percent, threshold):
    if percent is None:
        return "context –"
    line = f"context {percent}%"
    if threshold is not None and percent >= threshold:
        line += f" · \033[33m{NUDGE}\033[0m"
    return line


def main():
    try:
        raw = sys.stdin.read()
    except (OSError, UnicodeDecodeError):
        raw = ""
    print(render(used_percentage(raw), fill_threshold()))


if __name__ == "__main__":
    main()
