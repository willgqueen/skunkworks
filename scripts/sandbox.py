"""Create a throwaway sandbox for manual skill tests (docs/testing.md).

Usage: python3 -I scripts/sandbox.py [DEST] [--remote]

DEST (absent or empty; default: a new temp folder) gets:
    skunkworks/  a copy of this working tree (tracked and new files, so
                 uncommitted skill changes are tested), as a fresh git repo,
                 with an empty workspace and access to DEST only
    target/      a git repo from tests/fixtures/target-repo/, branch main
    remote.git/  with --remote: a local bare repo, target's origin

Start the test session with: cd DEST/skunkworks && claude
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests/fixtures/target-repo"
# Fixed identity, so sandbox commits never depend on (or leak) the user's git config.
IDENTITY = ["-c", "user.name=sandbox", "-c", "user.email=sandbox@example.invalid", "-c", "commit.gpgsign=false"]


def git(repo, *args):
    subprocess.run(["git", *IDENTITY, "-C", str(repo), *args], check=True, capture_output=True)


def commit_all(repo, message):
    git(repo, "init", "-q", "-b", "main")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)


def copy_skunkworks(dest):
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z", "-co", "--exclude-standard"],
                         check=True, capture_output=True).stdout
    for rel in (p.decode() for p in out.split(b"\0") if p):
        src = ROOT / rel
        if src.is_file():  # skips tracked files deleted in the working tree
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / rel)
    settings = dest / ".claude/settings.json"
    data = json.loads(settings.read_text())
    data["permissions"]["additionalDirectories"] = [str(dest.parent)]
    settings.write_text(json.dumps(data, indent=2) + "\n")
    for sub in ("projects", "archive", "reviews", "worktrees"):
        (dest / "workspace" / sub).mkdir(parents=True)
    (dest / "workspace/inbox.md").write_text("# Inbox\n\nRaw, unsorted ideas. Triage into a project item when ready.\n")
    commit_all(dest, "chore: sandbox copy")


def create(dest, remote=False):
    dest = dest.resolve()
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"sandbox: {dest} is not empty")
    dest.mkdir(parents=True, exist_ok=True)
    copy_skunkworks(dest / "skunkworks")
    target = dest / "target"
    shutil.copytree(FIXTURE, target, ignore=shutil.ignore_patterns("__pycache__"))
    commit_all(target, "chore: initial commit")
    if remote:
        git(dest, "init", "-q", "--bare", "-b", "main", "remote.git")
        git(target, "remote", "add", "origin", str(dest / "remote.git"))
        git(target, "push", "-q", "-u", "origin", "main")
    return dest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dest", nargs="?", type=pathlib.Path)
    parser.add_argument("--remote", action="store_true", help="add a local bare remote as target's origin")
    args = parser.parse_args(argv)
    dest = create(args.dest or pathlib.Path(tempfile.mkdtemp(prefix="skw-")), args.remote)
    print(f"sandbox ready: cd {dest / 'skunkworks'} && claude")


if __name__ == "__main__":
    sys.exit(main())
