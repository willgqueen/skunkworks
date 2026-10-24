import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import ledger  # noqa: E402

FIXTURE = ROOT / "tests/fixtures/workspace"


class Ledger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = {i["id"]: i for i in ledger.entries(FIXTURE)}

    def test_one_entry_per_task_and_merge(self):
        self.assertEqual(self.items["040"]["changes"], [
            ("2026-10-02", "Add backoff helper", "aaa1111"),
            ("2026-10-02", "Retry webhook sends", "bbb2222"),
            ("2026-10-03", "Merged", "ccc3333")])

    def test_decisions_and_notes(self):
        self.assertEqual(self.items["040"]["decisions"], ["Backoff library"])
        self.assertEqual(self.items["040"]["notes"], ["first use of backoff helper"])

    def test_done_item_without_commits_falls_back(self):
        self.assertEqual(self.items["034"]["changes"], [("2026-10-23", "Done", "")])

    def test_bootstrap_item_uses_outcome_and_done_suffix(self):
        self.assertEqual(self.items["041"]["changes"], [("2026-10-05", "Shipped in PR 9.", "")])

    def test_task_sha_not_doubled(self):
        # Task 1 is ticked as "Add backoff helper (aaa1111)" in the fixture.
        self.assertEqual(self.items["040"]["changes"][0], ("2026-10-02", "Add backoff helper", "aaa1111"))
        self.assertNotIn("(aaa1111) (aaa1111)", ledger.render([self.items["040"]]))

    def test_sensitive_patterns(self):
        for line in ["sk-ant-api03-abcdefghijklmnopqrst", "github_pat_11ABCDEFGHIJKLMNOPQRSTU", "ghs_abcdefghijklmnopqrstuv",
                     "glpat-abcdefghijklmnopqrstu", "password=hunter2", "Bearer abcdefghijklmnop", "~/notes",
                     "/var/folders/x", "host devbox.local", "https://wiki.corp.internal/x", "a@b.com",
                     "-----BEGIN RSA PRIVATE KEY", "eyJhbGciOiJIUzI1.eyJzdWIiOiIxMjM0.sig"]:
            with self.subTest(line=line):
                self.assertTrue(ledger.SENSITIVE.search(line))
        for line in ["Add retry to webhook sender", "Raise limit to 1000000", "PR 7 merged (ccc3333)",
                     "loading .env.local per server", ".claude/settings.local.json", "actions/checkout@4.1.0"]:
            with self.subTest(line=line):
                self.assertFalse(ledger.SENSITIVE.search(line))

    def test_heading_shows_repos(self):
        self.assertIn("· api, web · 041 Bootstrap item", ledger.render(list(self.items.values())))

    def test_changelog_filters_project_and_refuses_sensitive(self):
        import tempfile, pathlib as pl
        with tempfile.TemporaryDirectory() as d:
            out = pl.Path(d, "CHANGELOG.md")
            items = [dict(self.items["040"], project="skunkworks"), self.items["041"]]
            self.assertEqual(ledger.write_changelog(items, out), [])
            text = out.read_text()
            self.assertIn("040 Add retry", text)
            self.assertNotIn("041", text)
            leaky = [dict(self.items["040"], project="skunkworks", notes=["see /Users/someone/notes"])]
            out.unlink()
            self.assertTrue(ledger.write_changelog(leaky, out))
            self.assertTrue(ledger.write_changelog([self.items["041"]], out))  # no skunkworks entries
            self.assertFalse(out.exists())

    def test_range_and_project_filters(self):
        out = ledger.render(list(self.items.values()), since="2026-10-03", project="p")
        self.assertIn("Merged (ccc3333)", out)
        self.assertNotIn("aaa1111", out)
        self.assertEqual(ledger.render(list(self.items.values()), project="other"), "No changes in range.")


if __name__ == "__main__":
    unittest.main()
