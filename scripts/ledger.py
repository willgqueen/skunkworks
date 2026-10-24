"""The change ledger: every change made through the toolkit, distilled.

One entry per committed task or merge (from item logs and deliver.md tasks),
grouped under its item. Items without such lines get one entry from their
Outcome. See docs/how-to.md#see-what-changed.

Usage:
    python3 -I scripts/ledger.py [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--project P]
    python3 -I scripts/ledger.py --changelog     write CHANGELOG.md for skunkworks
"""
import argparse
import datetime
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import board  # noqa: E402

ROOT = board.ROOT


def section(text, name):
    m = re.search(rf"^## {name}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def entries(workspace):
    items = []
    paths = list(workspace.glob("projects/*/items/*/item.md")) + list(workspace.glob("archive/*/*/item.md"))
    for path in paths:
        project = path.parts[-4] if path.parts[-3] == "items" else path.parts[-3]
        try:
            meta, log = board.parse_item(path)
        except ValueError:
            continue
        folder = path.parent
        deliver = (folder / "deliver.md").read_text() if (folder / "deliver.md").exists() else ""
        develop = (folder / "develop.md").read_text() if (folder / "develop.md").exists() else ""
        tasks = {n: re.sub(r"\s+\(`?[0-9a-f]{7,40}`?\)$", "", t)
                 for n, t in re.findall(r"^- \[x\] (\d+)\. (.+)$", section(deliver, "Tasks"), re.M)}
        changes, notes = [], []
        for date, line in log:
            if m := re.match(r"task (\d+) committed (\S+)", line):
                changes.append((date, tasks.get(m.group(1), f"Task {m.group(1)}"), m.group(2)))
            elif m := re.match(r"merged (\S+)", line):
                changes.append((date, "Merged", m.group(1)))
            elif line.startswith("ledger: "):
                notes.append(line[len("ledger: "):])
        done = [d for d, l in log if board.is_done_line(l)]
        if not changes and meta["status"] == "done":
            # Items closed without per-task commit lines (bootstrap): one unlinked entry from the Outcome.
            outcome = [l for l in section(deliver, "Outcome").splitlines() if l.strip() and not l.startswith("<!--")]
            changes.append((done[-1] if done else log[-1][0], outcome[0] if outcome else "Done", ""))
        if not changes:
            continue
        decisions = re.findall(r"^### D\d+: (.+)\n- \*\*Kind:\*\* significant", develop, re.M)
        items.append({"project": project, "id": meta["id"], "title": meta["title"], "kind": meta["kind"],
                      "size": meta["size"], "repos": meta.get("repos", ""), "changes": changes,
                      "notes": notes, "decisions": decisions, "date": max(c[0] for c in changes)})
    return sorted(items, key=lambda i: (i["date"], i["project"], i["id"]), reverse=True)


# docs/criteria.md#building-blocks: secrets, personal data, local machine details, internal URLs.
SENSITIVE = re.compile("|".join([
    r"/Users/|/home/|/var/folders/|(?<![\w.])~/",                                  # local paths
    r"\b(?:sk|pk|rk)[-_][\w-]{16,}|\bgh[pousr]_\w{20,}|\bgithub_pat_\w{20,}|\bglpat-[\w-]{20,}|\b(?:hf|npm)_\w{20,}",
    r"\bxox[abprs]-[\w-]{10,}|\bAKIA[0-9A-Z]{16}\b|\bAIza[\w-]{30,}",               # tokens and keys
    r"\beyJ[\w-]{10,}\.[\w-]{10,}\.|-----BEGIN [A-Z ]*PRIVATE KEY|\bBearer\s+\S{12,}",
    r"(?i:\b(?:password|passwd|secret|token|api[_-]?key)\s*[=:]\s*\S+)",
    r"[\w.+-]+@[A-Za-z][\w-]*\.[A-Za-z]{2,}",                                       # emails
    r"(?<![.\w])[\w-]+(?:\.[\w-]+)*\.(?:local|internal|corp|lan|intranet)\b(?!\.)",  # hosts, internal URLs
    r"\b\w+://[^/\s:@]+:[^/\s@]+@",                                                 # credentials in URLs
]))


def render(items, since=None, until=None, project=None):
    out = []
    for i in items:
        changes = [c for c in i["changes"] if (not since or c[0] >= since) and (not until or c[0] <= until)]
        if not changes or (project and i["project"] != project):
            continue
        repos = ", ".join(re.findall(r"[\w.-]+", i["repos"] or "")) or "no repo"
        out.append(f"## {max(c[0] for c in changes)} · {i['project']} · {repos} · {i['id']} {i['title']} ({i['kind']}, {i['size']})")
        out += [f"- {d} {summary}" + (f" ({ref})" if ref else "") for d, summary, ref in changes]
        out += [f"- Decision: {d}" for d in i["decisions"]]
        out += [f"- Note: {n}" for n in i["notes"]]
        out.append("")
    return "\n".join(out) or "No changes in range."


def write_changelog(items, path):
    """Write skunkworks' entries to path, refusing if any line looks sensitive (docs/criteria.md#building-blocks)."""
    if not any(i["project"] == "skunkworks" for i in items):
        return ["no skunkworks entries found: wrong workspace?"]
    body = render(items, project="skunkworks")
    problems = [line for line in body.splitlines() if SENSITIVE.search(line)]
    if not problems:
        path.write_text("# Changelog\n\nskunkworks' own changes, generated by `scripts/ledger.py --changelog`.\n\n" + body + "\n")
    return problems


def iso_date(value):
    try:
        return str(datetime.date.fromisoformat(value))
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a YYYY-MM-DD date: {value}")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--workspace", type=pathlib.Path, default=board.find_workspace())
    p.add_argument("--since", type=iso_date)
    p.add_argument("--until", type=iso_date)
    p.add_argument("--project")
    p.add_argument("--changelog", action="store_true")
    a = p.parse_args()
    items = entries(a.workspace.resolve())
    if a.changelog:
        problems = write_changelog(items, ROOT / "CHANGELOG.md")
        for p_ in problems:
            print(f"possible sensitive content, not written: {p_}")
        if problems:
            return 1
        print("CHANGELOG.md written")
    else:
        print(render(items, a.since, a.until, a.project))
    return 0


if __name__ == "__main__":
    sys.exit(main())
