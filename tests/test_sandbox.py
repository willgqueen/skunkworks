import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import sandbox  # noqa: E402


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


class Sandbox(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dest = sandbox.create(pathlib.Path(cls.tmp.name) / "sbx", remote=True)
        cls.local = sandbox.create(pathlib.Path(cls.tmp.name) / "local")
        cls.seeded = sandbox.create(pathlib.Path(cls.tmp.name) / "seeded", seeded=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_skunkworks_copy(self):
        sk = self.dest / "skunkworks"
        self.assertTrue((sk / ".claude/skills/hq/SKILL.md").is_file())
        self.assertTrue((sk / "scripts/sandbox.py").is_file())
        self.assertEqual(git(sk, "status", "--porcelain"), "")
        settings = json.loads((sk / ".claude/settings.json").read_text())
        self.assertEqual(settings["permissions"]["additionalDirectories"], [str(self.dest)])
        self.assertIn("PreToolUse", settings["hooks"])

    def test_empty_workspace(self):
        ws = self.dest / "skunkworks/workspace"
        self.assertEqual(sorted(p.name for p in ws.iterdir()), ["archive", "inbox.md", "projects", "reviews", "worktrees"])
        self.assertEqual(list((ws / "projects").iterdir()), [])

    def test_target_repo(self):
        target = self.dest / "target"
        self.assertEqual(git(target, "branch", "--show-current"), "main")
        self.assertEqual(git(target, "status", "--porcelain"), "")
        tests = subprocess.run([sys.executable, "-I", "-m", "unittest"], cwd=target, capture_output=True)
        self.assertEqual(tests.returncode, 0, tests.stderr)

    def test_remote(self):
        target = self.dest / "target"
        self.assertEqual(git(target, "remote"), "origin")
        self.assertEqual(git(self.dest / "remote.git", "rev-parse", "main"), git(target, "rev-parse", "HEAD"))

    def test_without_remote(self):
        self.assertEqual(git(self.local / "target", "remote"), "")
        self.assertFalse((self.local / "remote.git").exists())

    def test_seeded_workspace(self):
        ws = self.seeded / "skunkworks/workspace"
        texts = [p.read_text() for p in ws.rglob("*.md")]
        self.assertFalse([t for t in texts if "{{" in t])
        self.assertIn(str(self.seeded / "target"), (ws / "projects/greet/project.md").read_text())
        self.assertTrue((ws / "projects/skunkworks/items").is_dir())
        board = subprocess.run([sys.executable, "-I", "scripts/board.py"], cwd=self.seeded / "skunkworks",
                               capture_output=True, text=True, check=True).stdout
        for line in ["| 003 | Add pluggable greeting styles |", "Run /develop", "children: 2/2", "Inbox: 2 entries"]:
            self.assertIn(line, board)

    def test_refuses_non_empty_dest(self):
        with self.assertRaises(SystemExit):
            sandbox.create(self.dest)


if __name__ == "__main__":
    unittest.main()
