"""Static lint for skills and agents: required frontmatter, no model names in
skills, every log line a skill (or process.md's shared phase skill steps) writes is in the log vocabulary
(docs/workspace.md#log-vocabulary), and every skill has a manual test scenario
(tests/scenarios/<skill>.md, docs/testing.md), and the context size budgets read from
docs/criteria.md#context.

Usage: python3 -I scripts/lint_skills.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODELS = re.compile(r"\b(opus|sonnet|haiku|fable)\b", re.I)
LOGGED = re.compile(r"`- <date>: ([^`]+)`|\b[Ll]og `([^`]+)`")
PHASES = {
    "<phase>": "(?:discover|define|develop|deliver)",
    "<planning phase>": "(?:discover|define|develop)",
}


def frontmatter(path):
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.S)
    if not m:
        return {}
    pairs = (line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    return {k.strip(): v.strip() for k, v in pairs if v.strip()}


def pattern(entry):
    """A vocabulary entry as a full-match regex: <phase> is any phase name, <planning phase> a planning one, any other <placeholder> is any text."""
    out = ""
    for i, part in enumerate(re.split(r"(<[^>]+>)", entry)):
        out += PHASES.get(part, ".+") if i % 2 else re.escape(part)
    return re.compile(out)


def vocabulary(root=ROOT):
    table = (root / "docs/workspace.md").read_text().split("## Log vocabulary", 1)[1]
    return [pattern(e) for cell in re.findall(r"^\| (.+?) \|", table, re.M) for e in re.findall(r"`([^`]+)`", cell)]


def in_vocabulary(line, vocab):
    """Placeholders in a skill's line stand for any value: (planning) phases for a phase name, the rest for text."""
    line = re.sub(r"^- <date>: ", "", line).replace("<phase>", "define").replace("<planning phase>", "define")
    line = re.sub(r"<[^<>]*>", "x", line)
    return any(v.fullmatch(line) for v in vocab)


BUDGETS = {
    "claude_lines": r"`CLAUDE\.md` at most \*\*([\d,]+) lines",
    "skill_lines": r"`SKILL\.md` at most \*\*([\d,]+) lines",
    "description_chars": r"skill description at most \*\*([\d,]+) characters",
    "criteria_chars": r"`docs/criteria\.md` at most \*\*([\d,]+) characters",
}


def budgets(root=ROOT):
    """docs/criteria.md#context: the size budgets, as ({name: limit}, [unreadable names])."""
    path = root / "docs/criteria.md"
    text = path.read_text() if path.exists() else ""
    found = {k: re.search(p, text) for k, p in BUDGETS.items()}
    return {k: int(m.group(1).replace(",", "")) for k, m in found.items() if m}, [k for k, m in found.items() if not m]


def lint(root=ROOT):
    problems, vocab = [], vocabulary(root)
    limits, unreadable = budgets(root)
    problems += [f"docs/criteria.md#context: can't read the {k} budget" for k in unreadable]
    claude = root / "CLAUDE.md"
    if "claude_lines" in limits and claude.is_file() and len(claude.read_text().splitlines()) > limits["claude_lines"]:
        problems.append(f"CLAUDE.md: over {limits['claude_lines']} lines")
    criteria = root / "docs/criteria.md"
    if "criteria_chars" in limits and len(criteria.read_text()) > limits["criteria_chars"]:
        problems.append(f"docs/criteria.md: over {limits['criteria_chars']} characters")
    for path in sorted((root / ".claude/skills").glob("*/SKILL.md")):
        name = path.parent.name
        if not {"name", "description", "argument-hint"} <= set(frontmatter(path)):
            problems.append(f"{name}: frontmatter needs name, description, argument-hint")
        if not (root / "tests/scenarios" / f"{name}.md").is_file():
            problems.append(f"{name}: no scenario in tests/scenarios/{name}.md")
        text = path.read_text()
        if "skill_lines" in limits and len(text.splitlines()) > limits["skill_lines"]:
            problems.append(f"{name}: SKILL.md over {limits['skill_lines']} lines")
        if "description_chars" in limits and len(frontmatter(path).get("description", "")) > limits["description_chars"]:
            problems.append(f"{name}: description over {limits['description_chars']} characters")
        model = MODELS.search(text)
        if model:
            problems.append(f"{name}: names a model ({model.group(0)}); apply the model policy instead")
        for full, short in LOGGED.findall(text):
            line = full or short
            if not in_vocabulary(line, vocab):
                problems.append(f"{name}: log line not in the vocabulary: {line}")
    _, found, shared = (root / "docs/process.md").read_text().partition("\n## Phase skill steps\n")
    if not found:
        problems.append("process.md: no ## Phase skill steps section")
    shared = shared.split("\n## ", 1)[0]
    for full, short in LOGGED.findall(shared):
        if not in_vocabulary(full or short, vocab):
            problems.append(f"process.md#phase-skill-steps: log line not in the vocabulary: {full or short}")
    for path in sorted((root / ".claude/agents").glob("*.md")):
        if not {"name", "description", "model", "effort", "tools"} <= set(frontmatter(path)):
            problems.append(f"agent {path.stem}: frontmatter needs name, description, model, effort, tools")
    return problems


def main():
    problems = lint()
    for p in problems:
        print(p)
    print(f"lint: {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
