import pathlib
import shutil
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_docs  # noqa: E402
import lint_skills  # noqa: E402

FIXTURES = ROOT / "tests/fixtures"
GOOD = (FIXTURES / "lint/.claude/skills/good/SKILL.md").read_text()


class CheckDocs(unittest.TestCase):
    root = FIXTURES / "docs"

    def test_broken_link_and_anchor(self):
        problems = check_docs.check_links([self.root / "docs/source.md"], self.root)
        self.assertEqual(sorted(p.split(" -> ")[1] for p in problems), ["nope.md", "target.md#nope"])

    def test_undocumented_skill_agent_template(self):
        problems = check_docs.check_coverage(self.root)
        self.assertEqual(len(problems), 3)
        for word in ("undocumented", "ghost", "orphan.md"):
            self.assertTrue(any(word in p for p in problems), word)

    def test_fixtures_excluded_from_repo_scan(self):
        self.assertFalse(any("tests/fixtures" in str(f) for f in check_docs.tracked_markdown()))


class LintSkills(unittest.TestCase):
    root = FIXTURES / "lint"

    def setUp(self):
        self.problems = lint_skills.lint(self.root)

    def found(self, text):
        return any(text in p for p in self.problems)

    def test_good_skill_passes(self):
        self.assertFalse(self.found("good:"))

    def test_missing_or_empty_frontmatter(self):
        self.assertTrue(self.found("nofront: frontmatter"))
        self.assertTrue(self.found("agent agent: frontmatter"))

    def test_agent_needs_tools(self):
        self.assertTrue(self.found("agent notools: frontmatter"))

    def test_model_name_any_case(self):
        self.assertTrue(self.found("model: names a model (Opus)"))

    def test_skill_needs_scenario(self):
        self.assertTrue(self.found("model: no scenario"))

    def test_log_lines_must_fully_match(self):
        self.assertTrue(self.found("define drafted extra junk"))
        self.assertTrue(self.found("bogus drafted"))

    def test_planning_phase_placeholder(self):
        self.assertTrue(self.found("badlog: log line not in the vocabulary: deliver drafted"))
        self.assertFalse(self.found("discover drafted"))

    def test_shared_steps_log_lines(self):
        self.assertTrue(self.found("process.md#phase-skill-steps: log line not in the vocabulary: <phase> written"))
        self.assertFalse(self.found("<phase> drafted"))
        self.assertFalse(self.found("outside the section"))

    def test_shared_steps_section_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "lint"
            shutil.copytree(self.root, root)
            (root / "docs/process.md").write_text("# Process\n\n## Other\n\nLog `bogus written`.\n")
            problems = lint_skills.lint(root)
        self.assertIn("process.md: no ## Phase skill steps section", problems)
        self.assertFalse(any("bogus written" in p for p in problems))

    def lint_with(self, **files):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "lint"
            shutil.copytree(self.root, root)
            for name, text in files.items():
                (root / name.replace("__", "/")).write_text(text)
            return lint_skills.lint(root)

    def test_fixture_within_budgets(self):
        self.assertFalse(self.found("budget"))
        self.assertFalse(self.found("over"))

    def test_skill_over_line_budget(self):
        problems = self.lint_with(**{".claude__skills__good__SKILL.md": GOOD + "x\n" * 5})
        self.assertIn("good: SKILL.md over 8 lines", problems)

    def test_description_over_char_budget(self):
        problems = self.lint_with(**{".claude__skills__good__SKILL.md": GOOD.replace("description: d", "description: " + "d" * 21)})
        self.assertIn("good: description over 20 characters", problems)

    def test_claude_md_over_line_budget(self):
        problems = self.lint_with(**{"CLAUDE.md": "x\n" * 4})
        self.assertIn("CLAUDE.md: over 3 lines", problems)

    def test_criteria_over_char_budget(self):
        problems = self.lint_with(**{"docs__criteria.md": (self.root / "docs/criteria.md").read_text() + "x" * 500})
        self.assertIn("docs/criteria.md: over 500 characters", problems)

    def test_unreadable_budget(self):
        problems = self.lint_with(**{"docs__criteria.md": "- **Size budgets:** none.\n"})
        for name in lint_skills.BUDGETS:
            self.assertIn(f"docs/criteria.md#context: can't read the {name} budget", problems)

    def test_budget_numbers_come_from_criteria(self):
        text = (self.root / "docs/criteria.md").read_text().replace("**3 lines**", "**30 lines**")
        problems = self.lint_with(**{"docs__criteria.md": text, "CLAUDE.md": "x\n" * 4})
        self.assertFalse(any(p.startswith("CLAUDE.md") for p in problems))

    def test_budget_with_thousands_separator(self):
        text = (self.root / "docs/criteria.md").read_text().replace("**500 characters**", "**1,500 characters**")
        self.assertFalse(any("criteria.md: over" in p for p in self.lint_with(**{"docs__criteria.md": text + "x" * 600})))


if __name__ == "__main__":
    unittest.main()
