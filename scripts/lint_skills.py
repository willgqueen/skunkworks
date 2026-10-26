"""Static lint for skills and agents: required frontmatter, no model names in
skills, every log line a skill writes is in the log vocabulary
(docs/workspace.md#log-vocabulary), and every skill has a manual test scenario
(tests/scenarios/<skill>.md, docs/testing.md).

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
    """Placeholders in a skill's line stand for any value: <phase> for a phase name, the rest for text."""
    line = re.sub(r"^- <date>: ", "", line).replace("<phase>", "define")
    line = re.sub(r"<[^<>]*>", "x", line)
    return any(v.fullmatch(line) for v in vocab)


def lint(root=ROOT):
    problems, vocab = [], vocabulary(root)
    for path in sorted((root / ".claude/skills").glob("*/SKILL.md")):
        name = path.parent.name
        if not {"name", "description", "argument-hint"} <= set(frontmatter(path)):
            problems.append(f"{name}: frontmatter needs name, description, argument-hint")
        if not (root / "tests/scenarios" / f"{name}.md").is_file():
            problems.append(f"{name}: no scenario in tests/scenarios/{name}.md")
        text = path.read_text()
        model = MODELS.search(text)
        if model:
            problems.append(f"{name}: names a model ({model.group(0)}); apply the model policy instead")
        for full, short in LOGGED.findall(text):
            line = full or short
            if not in_vocabulary(line, vocab):
                problems.append(f"{name}: log line not in the vocabulary: {line}")
    for path in sorted((root / ".claude/agents").glob("*.md")):
        if not {"name", "description", "model", "effort"} <= set(frontmatter(path)):
            problems.append(f"agent {path.stem}: frontmatter needs name, description, model, effort")
    return problems


def main():
    problems = lint()
    for p in problems:
        print(p)
    print(f"lint: {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
