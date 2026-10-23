"""Check the repo's docs: every relative link and #anchor resolves, and every
skill, agent and template has an entry in its reference doc.

Usage: python3 -I scripts/check_docs.py
See docs/contributing.md#checking-the-docs.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def slug(heading):
    heading = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return heading.replace(" ", "-")


def anchors(path):
    return {slug(h) for h in re.findall(r"^#+\s+(.*)$", path.read_text(), re.M)}


def tracked_markdown():
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--cached", "--others",
                          "--exclude-standard", "*.md"], capture_output=True, text=True, check=True)
    return [ROOT / p for p in out.stdout.split()]


def check_links(files):
    problems = []
    for f in files:
        for target in re.findall(r"\]\(([^)\s]+)\)", f.read_text()):
            if re.match(r"[a-z]+:", target):
                continue
            path, _, anchor = target.partition("#")
            dest = (f.parent / path).resolve() if path else f
            rel = f.relative_to(ROOT)
            if not dest.exists():
                problems.append(f"missing link: {rel} -> {target}")
            elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
                problems.append(f"missing anchor: {rel} -> {target}")
    return problems


def check_coverage():
    problems = []
    skills_doc = (ROOT / "docs/skills.md").read_text()
    for skill in sorted((ROOT / ".claude/skills").glob("*/SKILL.md")):
        name = skill.parent.name
        if not re.search(rf"^## {re.escape(name)}$", skills_doc, re.M):
            problems.append(f"skill not in docs/skills.md: {name}")
    agents_doc = (ROOT / "docs/agents.md").read_text()
    for agent in sorted((ROOT / ".claude/agents").glob("*.md")):
        if f"[{agent.stem}]" not in agents_doc:
            problems.append(f"agent not in docs/agents.md: {agent.stem}")
    templates_doc = (ROOT / "docs/templates.md").read_text()
    for tpl in sorted((ROOT / "templates").rglob("*.md")):
        if f"[{tpl.name}]" not in templates_doc:
            problems.append(f"template not in docs/templates.md: {tpl.relative_to(ROOT)}")
    return problems


def main():
    files = tracked_markdown()
    problems = check_links(files) + check_coverage()
    for p in problems:
        print(p)
    print(f"{len(files)} markdown files checked, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
