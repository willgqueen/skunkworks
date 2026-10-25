"""Create a throwaway sandbox for manual skill tests (docs/testing.md).

Usage: python3 -I scripts/sandbox.py [DEST] [--remote] [--seed]

DEST (absent or empty; default: a new temp folder) gets:
    skunkworks/  a copy of this working tree (tracked and new files, so
                 uncommitted skill changes are tested), as a fresh git repo,
                 with an empty workspace and access to DEST only
    target/      a git repo from tests/fixtures/target-repo/, branch main
    remote.git/  with --remote: a local bare repo, target's origin

--seed fills the workspace from tests/fixtures/sandbox-workspace/: a `greet`
project for target, items in the states the scenarios start from, and an inbox.

Start the test session with: cd DEST/skunkworks && claude
"""
import argparse
import datetime
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests/fixtures/target-repo"
SEED = ROOT / "tests/fixtures/sandbox-workspace"
# Repo-local settings, so sandbox commits (Claude's and the scenarios') never use
# or leak the user's identity, signing or global hooks.
LOCAL_CONFIG = {"user.name": "sandbox", "user.email": "sandbox@example.invalid",
                "commit.gpgsign": "false", "core.hooksPath": "/dev/null"}


# Without the caller's GIT_* variables (a git hook's GIT_INDEX_FILE would aim every
# call at the caller's repo), and in English, so errors read the same everywhere.
ENV = {**{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}, "LC_ALL": "C"}


def git(repo, *args):
    out = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=ENV)
    if out.returncode:
        raise SystemExit(f"sandbox: git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout


def commit_all(repo, message):
    git(repo, "init", "-q", "-b", "main")
    for key, value in LOCAL_CONFIG.items():
        git(repo, "config", key, value)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)


def copy_skunkworks(dest, root=ROOT):
    for rel in (p for p in git(root, "ls-files", "-z", "-co", "--exclude-standard").split("\0") if p):
        src = root / rel
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


def seed(dest):
    workspace = dest / "skunkworks/workspace"
    values = {"{{today}}": datetime.date.today().isoformat(), "{{target}}": str(dest / "target"),
              "{{skunkworks}}": str(dest / "skunkworks")}
    for src in SEED.rglob("*.md"):
        text = src.read_text()
        for key, value in values.items():
            text = text.replace(key, value)
        out = workspace / src.relative_to(SEED)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    for project in (workspace / "projects").iterdir():
        (project / "items").mkdir(exist_ok=True)


def create(dest, remote=False, seeded=False):
    dest = dest.resolve()
    try:
        dest.mkdir(parents=True)
        created = True
    except FileExistsError:
        created = False
        if not dest.is_dir() or any(dest.iterdir()):
            raise SystemExit(f"sandbox: {dest} is not an empty folder")
    try:
        copy_skunkworks(dest / "skunkworks")
        target = dest / "target"
        shutil.copytree(FIXTURE, target, ignore=shutil.ignore_patterns("__pycache__"))
        commit_all(target, "chore: initial commit")
        if remote:
            git(dest, "init", "-q", "--bare", "-b", "main", "remote.git")
            git(target, "remote", "add", "origin", str(dest / "remote.git"))
            git(target, "push", "-q", "-u", "origin", "main")
        if seeded:
            seed(dest)
    except BaseException:
        # Never leave a half-built sandbox; keep a folder the user made.
        for path in [dest] if created else list(dest.iterdir()):
            shutil.rmtree(path, ignore_errors=True)
        raise
    return dest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dest", nargs="?", type=pathlib.Path)
    parser.add_argument("--remote", action="store_true", help="add a local bare remote as target's origin")
    parser.add_argument("--seed", action="store_true", help="fill the workspace with the scenario fixtures")
    args = parser.parse_args(argv)
    dest = create(args.dest or pathlib.Path(tempfile.mkdtemp(prefix="skw-")), args.remote, args.seed)
    print(f"sandbox ready: cd {dest / 'skunkworks'} && claude")


if __name__ == "__main__":
    sys.exit(main())
