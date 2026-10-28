"""Show the board: every open workspace item, its next action and who it waits on.

Implements the Next action table in docs/process.md#next-action, using only
item.md frontmatter and the log vocabulary (docs/workspace.md#log-vocabulary).
Change both together.

Usage:
    python3 -I scripts/board.py                      markdown board
    python3 -I scripts/board.py --json               the same, as JSON
    python3 -I scripts/board.py --item <project>/<id or slug>  one item, as JSON
    python3 -I scripts/board.py --workspace <path>   use another workspace (tests)
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG_LINE = re.compile(r"^- (\d{4}-\d{2}-\d{2}): (.*)$")
PHASE_EVENT = re.compile(r"^(discover|define|develop|deliver) (drafted|revised|reopened|approved|waived)\b")
ORDER = {"blocked": 0, "you": 1, "active": 2, "proposed": 3}


def item_paths(workspace, archived=True):
    """Every item.md under projects/, then archive/ unless archived is False."""
    paths = list(workspace.glob("projects/*/items/*/item.md"))
    return paths + list(workspace.glob("archive/*/*/item.md")) if archived else paths


def phases_for(kind, size):
    """Phase path by size and kind (docs/process.md#sizing)."""
    if kind in ("investigation", "initiative"):
        return ["discover", "define", "deliver"]
    return {"S": ["deliver"], "M": ["define", "deliver"]}.get(size, ["discover", "define", "develop", "deliver"])


def parse_item(path):
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("no frontmatter")
    meta = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            value = value.strip()
            quoted = re.match(r'^"([^"]*)"', value)
            meta[key.strip()] = quoted.group(1) if quoted else re.split(r"\s#", value, 1)[0].strip()
    for key in ("id", "title", "kind", "status", "phase", "size"):
        if not meta.get(key):
            raise ValueError(f"missing {key}")
    log = []
    in_log = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_log = line.strip() == "## Log"
            continue
        m = LOG_LINE.match(line) if in_log else None
        if m:
            log.append((m.group(1), m.group(2)))
    return meta, log


def next_action(meta, log):
    """Return (next action, waiting on) per docs/process.md#next-action."""
    status, phase = meta["status"], meta["phase"]
    if status == "blocked":
        cause = next((e[len("blocked: "):] for _, e in reversed(log) if e.startswith("blocked:")), "see log")
        return f"Resolve the block ({cause}), then resume", "you"
    events = [m.group(2) for _, e in log if (m := PHASE_EVENT.match(e)) and m.group(1) == phase]
    # Approved per docs/criteria.md#phase-state: approved or waived, with no later reopened.
    # Deliver's authorization can never be waived, so a deliver waiver is ignored.
    approvals = ("approved",) if phase == "deliver" else ("approved", "waived")
    last_approval = max((i for i, e in enumerate(events) if e in approvals), default=-1)
    last_reopen = max((i for i, e in enumerate(events) if e == "reopened"), default=-1)
    if last_approval > last_reopen:
        latest = "approved"
    else:
        drafting = [e for e in events if e in ("drafted", "revised", "reopened")]
        latest = drafting[-1] if drafting else None
    if phase == "deliver":
        deliver_lines = [e for _, e in log if e.startswith(("deliver authorized", "review:", "merged", "task ",
                                                            "PR opened", "waiting on ", "unblocked"))]
        last = deliver_lines[-1] if deliver_lines else ""
        if last.startswith("waiting on you:"):
            return last[len("waiting on you: "):].strip() or "See the log", "you"
        if last.startswith("waiting on items:"):
            return f"Wait for items {last[len('waiting on items: '):].strip()}", "items"
        if not any(e.startswith("deliver authorized") for e in deliver_lines):
            return "Run /deliver: plan, then one approval", "claude"
        if last.startswith("review: incomplete"):  # never counts as passed
            return "Finish the review (/review)", "claude"
        if last.startswith("review: failed"):
            return "Fix the findings (/deliver), or accept them", "you"
        if last.startswith("review:"):
            return "Merge, or resume /deliver", "you"
        return "Resume /deliver", "claude"
    if latest is None:
        return f"Run /{phase}", "claude"
    if latest == "reopened":
        return f"Revise {phase}.md (/{phase})", "claude"
    if latest in ("drafted", "revised"):
        return f"Answer and approve the {phase} gate", "you"
    path = phases_for(meta["kind"], meta["size"])
    later = path[path.index(phase) + 1:] if phase in path else ["deliver"]
    return f"Run /{later[0]}", "claude"


def is_done_line(line):
    """A log line that closes the item: `done`, `done (<note>)`, or `<note>; done`."""
    return bool(re.match(r"(?:[^:]*;\s*)?done\b", line))


def find_workspace(start=ROOT):
    """The live workspace: the nearest folder at or above start that holds workspace/projects,
    so scripts run from a deliver worktree still read the real one."""
    for folder in [start, *start.parents]:
        if (folder / "workspace/projects").is_dir():
            return folder / "workspace"
    return start / "workspace"


def calibration_due(workspace, criteria_path):
    """docs/criteria.md#calibration. Reads its thresholds from criteria.md."""
    text = criteria_path.read_text() if criteria_path.exists() else ""
    dates = re.findall(r"^\| (\d{4}-\d{2}-\d{2}) \|", text, re.M)
    done_at = re.search(r"after (\d+) items have reached `done`", text)
    fired_at = re.search(r"trigger has fired (\d+) times", text)
    if not (done_at and fired_at):
        return ["can't read the calibration thresholds in docs/criteria.md#calibration"]
    done_at, fired_at = int(done_at.group(1)), int(fired_at.group(1))
    since = max(dates) if dates else "0000-00-00"
    done, triggers = 0, {}
    for path in item_paths(workspace):
        try:
            _, log = parse_item(path)
        except ValueError:
            continue
        done += any(is_done_line(e) for d, e in log if d >= since)
        for d, e in log:
            m = re.match(r"re-sized \S+: (.*)", e)
            if m and d >= since:
                triggers[m.group(1)] = triggers.get(m.group(1), 0) + 1
    reasons = []
    if done >= done_at:
        reasons.append(f"{done} items done since {since}")
    reasons += [f"re-size trigger '{t}' logged {n} times" for t, n in triggers.items() if n >= fired_at]
    return reasons


def ids(value):
    return [i.zfill(3) for i in re.findall(r"\d+", value or "")]


def all_statuses(workspace):
    """(project, id) -> (status, parent) for every readable item, open or archived."""
    found = {}
    for path in item_paths(workspace):
        project = path.parts[-4] if path.parts[-3] == "items" else path.parts[-3]
        try:
            meta, _ = parse_item(path)
        except ValueError:
            continue
        found[(project, meta["id"].zfill(3))] = (meta["status"], (ids(meta.get("parent")) or [None])[0])
    return found


def stale_days(criteria_path):
    """docs/criteria.md#context: the stale-item threshold."""
    m = re.search(r"no log line in the last (\d+) days", criteria_path.read_text()) if criteria_path.exists() else None
    return int(m.group(1)) if m else None


def collect(workspace, today=None, criteria_path=ROOT / "docs/criteria.md"):
    items, problems = [], []
    today = today or datetime.date.today()
    days = stale_days(criteria_path)
    statuses = all_statuses(workspace)
    closed = ("done", "dropped")
    for path in sorted(item_paths(workspace, archived=False)):
        project = path.parts[-4]
        try:
            meta, log = parse_item(path)
        except ValueError as err:
            problems.append(f"{path.relative_to(workspace)}: {err}")
            continue
        if meta["status"] in closed:
            continue
        action, waiting = next_action(meta, log)
        # depends_on (docs/criteria.md#splitting): unfinished dependencies come first.
        pending = [d for d in ids(meta.get("depends_on")) if statuses.get((project, d), ("",))[0] not in closed]
        if pending and meta["status"] != "blocked":
            action, waiting = f"Wait for items {', '.join(pending)}", "items"
        kids = [s for (proj, _), (s, parent) in statuses.items() if proj == project and parent == meta["id"].zfill(3)]
        if kids:
            action += f" · children: {sum(s in closed for s in kids)}/{len(kids)}"
        last = max([d for d, _ in log] or [meta.get("created", "")])
        try:
            stale = bool(days) and meta["status"] == "proposed" and (today - datetime.date.fromisoformat(last)).days > days
        except ValueError:
            stale = False
            problems.append(f"{path.relative_to(workspace)}: bad date {last!r}")
        group = "blocked" if meta["status"] == "blocked" else "you" if waiting == "you" else \
            "active" if meta["status"] == "active" else "proposed"
        items.append({"project": project, "id": meta["id"], "title": meta["title"], "kind": meta["kind"],
                      "size": meta["size"], "phase": meta["phase"], "status": meta["status"],
                      "next": action, "waiting_on": waiting, "group": group,
                      "parent": (ids(meta.get("parent")) or [None])[0], "depends_on": ids(meta.get("depends_on")),
                      "stale": stale,
                      "path": str(path.parent.relative_to(workspace.parent))})
    items.sort(key=lambda i: (i["project"], ORDER[i["group"]], i["id"]))
    return nest(items), problems


def nest(items):
    """Children follow their open parent, in board order."""
    open_ids = {(i["project"], i["id"]) for i in items}
    top = [i for i in items if (i["project"], i["parent"]) not in open_ids]
    out = []
    def place(item, depth):
        item["depth"] = depth
        out.append(item)
        for child in (c for c in items if c["parent"] == item["id"] and c["project"] == item["project"]):
            place(child, depth + 1)
    for item in top:
        place(item, 0)
    return out


def inbox_count(workspace):
    inbox = workspace / "inbox.md"
    return sum(1 for line in inbox.read_text().splitlines() if line.startswith("- ")) if inbox.exists() else 0


def render(items, problems, inbox, calibration):
    out = []
    for project in sorted({i["project"] for i in items}):
        out += [f"## {project}", "", "| ID | Title | Kind | Size | Phase | Status | Next action | Waiting on |",
                "|---|---|---|---|---|---|---|---|"]
        for i in (i for i in items if i["project"] == project):
            out.append(f"| {'↳ ' * i['depth']}{i['id']} | {i['title']} | {i['kind']} | {i['size']} | {i['phase']} | {i['status']} "
                       f"| {i['next']} | {i['waiting_on']} |")
        out.append("")
    if not items:
        out += ["No open items.", ""]
    out.append(f"Inbox: {inbox} {'entry' if inbox == 1 else 'entries'}")
    stale = [f"{i['project']}/{i['id']}" for i in items if i["stale"]]
    if stale:
        out.append("Stale: " + ", ".join(stale))
    if calibration:
        out.append("Calibration due (run /hq tidy): " + "; ".join(calibration))
    for p in problems:
        out.append(f"Problem: {p}")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workspace", type=pathlib.Path, default=find_workspace())
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--item", help="<project>/<id>")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    items, problems = collect(workspace)
    if args.item:
        project, _, item_id = args.item.partition("/")
        match = [i for i in items if i["project"] == project and
                 (i["id"] == item_id.zfill(3) or i["path"].endswith(f"-{item_id}"))]
        if not match:
            print(json.dumps({"error": f"no open item {args.item}"}))
            return 1
        print(json.dumps(match[0], indent=2))
        return 0
    calibration = calibration_due(workspace, ROOT / "docs/criteria.md")
    if stale_days(ROOT / "docs/criteria.md") is None:
        problems.append("can't read the stale-item threshold in docs/criteria.md#context")
    if args.json:
        print(json.dumps({"items": items, "inbox": inbox_count(workspace), "calibration_due": calibration,
                          "problems": problems}, indent=2))
    else:
        print(render(items, problems, inbox_count(workspace), calibration))
    return 0


if __name__ == "__main__":
    sys.exit(main())
