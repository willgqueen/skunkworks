import importlib
import json
import os
import re
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import sandbox  # noqa: E402


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True,
                          env=sandbox.ENV).stdout.strip()


class Sandbox(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.dest = sandbox.create(pathlib.Path(cls.tmp.name) / "sbx", remote=True)
        cls.local = sandbox.create(pathlib.Path(cls.tmp.name) / "local")
        cls.seeded = sandbox.create(pathlib.Path(cls.tmp.name) / "seeded", seeded=True)

    def test_skunkworks_copy(self):
        sk = self.dest / "skunkworks"
        self.assertTrue((sk / ".claude/skills/hq/SKILL.md").is_file())
        self.assertTrue((sk / "scripts/sandbox.py").is_file())
        self.assertEqual(git(sk, "status", "--porcelain"), "")
        settings = json.loads((sk / ".claude/settings.json").read_text())
        self.assertEqual(settings["permissions"]["additionalDirectories"], [str(self.dest)])
        self.assertIn("PreToolUse", settings["hooks"])

    def test_copies_untracked_but_not_ignored_or_deleted(self):
        root, dest = pathlib.Path(self.tmp.name) / "src", pathlib.Path(self.tmp.name) / "copy"
        (root / ".claude").mkdir(parents=True)
        (root / ".claude/settings.json").write_text('{"permissions": {}}')
        (root / ".gitignore").write_text("secret.txt\n")
        (root / "gone.md").write_text("x")
        git(root, "init", "-q")
        git(root, "add", "-A")
        (root / "gone.md").unlink()
        (root / "new.md").write_text("x")
        (root / "secret.txt").write_text("x")
        sandbox.copy_skunkworks(dest, root)
        self.assertTrue((dest / "new.md").is_file())
        self.assertFalse((dest / "secret.txt").exists())
        self.assertFalse((dest / "gone.md").exists())

    def test_repo_local_identity(self):
        for repo in (self.dest / "skunkworks", self.dest / "target"):
            self.assertEqual(git(repo, "config", "--local", "user.email"), "sandbox@example.invalid")
            self.assertEqual(git(repo, "config", "--local", "core.hooksPath"), "/dev/null")

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
        starts = {"001": "Run /discover", "002": "Run /define", "003": "Run /develop", "004": "Run /deliver",
                  "005": "Run /deliver", "006": "children: 2/2", "009": "Run /discover"}
        rows = {m.group(1): line for line in board.splitlines() if (m := re.match(r"\| (?:↳ )*(\d{3}) \|", line))}
        self.assertEqual(sorted(rows), sorted(starts))
        for id, start in starts.items():
            self.assertIn(start, rows[id])
        self.assertIn("Inbox: 2 entries", board)

    def test_refuses_non_empty_dest(self):
        with self.assertRaises(SystemExit):
            sandbox.create(self.dest)

    def test_failure_removes_partial_dest(self):
        dest = pathlib.Path(self.tmp.name) / "broken"
        fixture, sandbox.FIXTURE = sandbox.FIXTURE, pathlib.Path(self.tmp.name) / "missing"
        try:
            with self.assertRaises(FileNotFoundError):
                sandbox.create(dest)
        finally:
            sandbox.FIXTURE = fixture
        self.assertFalse(dest.exists())

    def test_failure_keeps_users_empty_dest(self):
        dest = pathlib.Path(self.tmp.name) / "mine"
        dest.mkdir()
        fixture, sandbox.FIXTURE = sandbox.FIXTURE, pathlib.Path(self.tmp.name) / "missing"
        try:
            with self.assertRaises(FileNotFoundError):
                sandbox.create(dest)
        finally:
            sandbox.FIXTURE = fixture
        self.assertEqual(list(dest.iterdir()), [])

    def test_ignores_callers_git_variables(self):
        index = pathlib.Path(self.tmp.name) / "hook-index"
        try:
            with mock.patch.dict(os.environ, GIT_INDEX_FILE=str(index)):  # as a git pre-commit hook sets it
                importlib.reload(sandbox)
                dest = sandbox.create(pathlib.Path(self.tmp.name) / "hooked")
        finally:
            importlib.reload(sandbox)
        self.assertFalse(index.exists())
        self.assertEqual(git(dest / "target", "log", "--format=%s"), "chore: initial commit")

    def test_git_errors_show_stderr(self):
        with self.assertRaisesRegex(SystemExit, "not a git repository"):
            sandbox.git(pathlib.Path(self.tmp.name), "log")

    def test_refuses_file_dest(self):
        path = pathlib.Path(self.tmp.name) / "file"
        path.write_text("x")
        with self.assertRaises(SystemExit):
            sandbox.create(path)


if __name__ == "__main__":
    unittest.main()
