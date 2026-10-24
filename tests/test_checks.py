import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_docs  # noqa: E402
import lint_skills  # noqa: E402

FIXTURES = ROOT / "tests/fixtures"


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

    def test_model_name_any_case(self):
        self.assertTrue(self.found("model: names a model (Opus)"))

    def test_log_lines_must_fully_match(self):
        self.assertTrue(self.found("define drafted extra junk"))
        self.assertTrue(self.found("bogus drafted"))


if __name__ == "__main__":
    unittest.main()
