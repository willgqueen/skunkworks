import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import manifest  # noqa: E402

SCRIPT = ROOT / "scripts/manifest.py"


def sh(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


class Scope(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        sh(self.repo, "init", "-q")
        sh(self.repo, "config", "user.email", "t@example.com")
        sh(self.repo, "config", "user.name", "t")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text="x"):
        (self.repo / name).write_text(text)

    def test_no_head_lists_everything(self):
        self.write("a.py")
        self.assertEqual(manifest.scope(self.repo), ["a.py"])

    def test_working_tree_includes_untracked_and_unicode(self):
        self.write("a.py")
        sh(self.repo, "add", ".")
        sh(self.repo, "commit", "-qm", "init")
        self.write("a.py", "changed")
        self.write("café notes.md")
        self.assertEqual(manifest.scope(self.repo), ["a.py", "café notes.md"])

    def test_three_dot_range_excludes_base_changes(self):
        self.write("a.py")
        sh(self.repo, "add", ".")
        sh(self.repo, "commit", "-qm", "init")
        sh(self.repo, "checkout", "-qb", "feat")
        self.write("feat.py")
        sh(self.repo, "add", ".")
        sh(self.repo, "commit", "-qm", "feat")
        sh(self.repo, "checkout", "-q", "-")
        self.write("base.py")
        sh(self.repo, "add", ".")
        sh(self.repo, "commit", "-qm", "base")
        base = subprocess.run(["git", "-C", str(self.repo), "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
        self.assertEqual(manifest.scope(self.repo, f"{base}...feat"), ["feat.py"])

    def test_line_breaks_in_names_are_refused(self):
        self.write("x\nREADME.md")
        with self.assertRaises(manifest.ScopeError):
            manifest.scope(self.repo)

    def test_not_a_repo_is_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(manifest.GitError):
                manifest.scope(pathlib.Path(d))


class Coverage(unittest.TestCase):
    def test_full_and_partial(self):
        self.assertEqual(manifest.coverage(["a", "b"], ["b", "a", "x"]), ("coverage 2/2", [], True))
        self.assertEqual(manifest.coverage(["a", "a", "b"], ["a"]), ("coverage 1/2", ["b"], False))

    def test_empty_manifest_is_never_complete(self):
        self.assertFalse(manifest.coverage([], [])[2])

    def test_check_reads_reported_files_and_exits(self):
        with tempfile.TemporaryDirectory() as d:
            m, r = pathlib.Path(d, "m.txt"), pathlib.Path(d, "r.txt")
            m.write_text("a.py\nx$(touch pwned).md\n")
            r.write_text("a.py\n")
            run = lambda: subprocess.run([sys.executable, "-I", str(SCRIPT), "check", str(m), str(r)],
                                         capture_output=True, text=True)
            out = run()
            self.assertEqual(out.returncode, 1)
            self.assertIn("not covered: x$(touch pwned).md", out.stdout)
            r.write_text("a.py\nx$(touch pwned).md\n")
            self.assertEqual(run().returncode, 0)

    def test_check_cli_rejects_empty_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            m, r = pathlib.Path(d, "m.txt"), pathlib.Path(d, "r.txt")
            m.write_text("")
            r.write_text("")
            out = subprocess.run([sys.executable, "-I", str(SCRIPT), "check", str(m), str(r)], capture_output=True, text=True)
            self.assertEqual(out.returncode, 1)
            self.assertIn("empty manifest", out.stdout)

    def test_split_chunks_cover_everything_once(self):
        with tempfile.TemporaryDirectory() as d:
            m = pathlib.Path(d, "m.txt")
            m.write_text("".join(f"f{i}.py\n" for i in range(7)))
            subprocess.run([sys.executable, "-I", str(SCRIPT), "split", str(m), "--size", "3", "--out", f"{d}/c"], check=True,
                           capture_output=True)
            chunks = sorted(pathlib.Path(d, "c").glob("chunk-*.txt"))
            self.assertEqual([len(manifest.read_list(c)) for c in chunks], [3, 3, 1])
            self.assertEqual(sorted(f for c in chunks for f in manifest.read_list(c)), sorted(manifest.read_list(m)))
            bad = subprocess.run([sys.executable, "-I", str(SCRIPT), "split", str(m), "--size", "0", "--out", f"{d}/z"],
                                 capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)


if __name__ == "__main__":
    unittest.main()
