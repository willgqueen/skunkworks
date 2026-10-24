"""Scope manifests and coverage checks for reviews (docs/criteria.md#complete-coverage).

Usage:
    python3 -I scripts/manifest.py list [--range BASE...HEAD | --all] [--repo PATH] > MANIFEST
    python3 -I scripts/manifest.py split MANIFEST --size N --out DIR
    python3 -I scripts/manifest.py check MANIFEST REPORTED [REPORTED...]

`list` prints every file in scope, one per line: the working tree against HEAD
(changed and untracked; every file when there's no commit yet) by default, a
commit range (use three dots for a PR: base...head), or every tracked file.
`split` writes chunk manifests for large scopes. `check` reads the covered files
from REPORTED files (one path per line, written by the main session, never passed
as arguments) and prints the coverage line and what's missing; exit 1 if
anything is missing or the manifest is empty.
"""
import argparse
import pathlib
import subprocess
import sys


class ScopeError(Exception):
    pass


class GitError(ScopeError):
    pass


def git(repo, *args):
    out = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if out.returncode:
        raise GitError(out.stderr.decode(errors="replace").strip())
    return [p.decode() for p in out.stdout.split(b"\0") if p]


def scope(repo, rng=None, everything=False):
    if everything:
        files = git(repo, "ls-files", "-z")
    elif rng:
        files = git(repo, "diff", "--name-only", "-z", rng)
    elif subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "-q", "HEAD"], capture_output=True).returncode:
        files = git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    else:
        files = git(repo, "diff", "--name-only", "-z", "HEAD") + git(repo, "ls-files", "-z", "--others", "--exclude-standard")
    bad = [f for f in files if "\n" in f or "\r" in f]
    if bad:
        raise ScopeError(f"file names with line breaks can't be listed safely: {bad!r}")
    return sorted(set(files))


def read_list(path):
    return [line.rstrip("\r") for line in pathlib.Path(path).read_text().split("\n") if line.rstrip("\r")]


def coverage(manifest, reported):
    """Coverage of a manifest by the reported files. An empty manifest is never complete."""
    manifest = sorted(set(manifest))
    missing = sorted(set(manifest) - set(reported))
    complete = bool(manifest) and not missing
    return f"coverage {len(manifest) - len(missing)}/{len(manifest)}", missing, complete


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    ls = sub.add_parser("list")
    which = ls.add_mutually_exclusive_group()
    which.add_argument("--range")
    which.add_argument("--all", action="store_true")
    ls.add_argument("--repo", default=".")
    sp = sub.add_parser("split")
    sp.add_argument("manifest")
    sp.add_argument("--size", type=int, required=True)
    sp.add_argument("--out", required=True)
    ck = sub.add_parser("check")
    ck.add_argument("manifest")
    ck.add_argument("reported", nargs="+")
    a = p.parse_args()
    try:
        if a.cmd == "list":
            print("\n".join(scope(pathlib.Path(a.repo), a.range, a.all)))
            return 0
        if a.cmd == "split":
            if a.size < 1:
                p.error("--size must be at least 1")
            files, out = read_list(a.manifest), pathlib.Path(a.out)
            out.mkdir(parents=True, exist_ok=True)
            for n, i in enumerate(range(0, len(files), a.size), 1):
                (out / f"chunk-{n:03}.txt").write_text("\n".join(files[i:i + a.size]) + "\n")
            print(f"{-(-len(files) // a.size)} chunks in {out}")
            return 0
        reported = [f for path in a.reported for f in read_list(path)]
        line, missing, complete = coverage(read_list(a.manifest), reported)
        print(line if missing or complete else f"{line} (empty manifest: nothing was in scope)")
        for f in missing:
            print(f"not covered: {f}")
        return 0 if complete else 1
    except ScopeError as err:
        sys.stderr.write(f"manifest: {err}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
