"""Run every automated check: unit tests, the skills lint and the docs check.
Run before every commit. Usage: python3 -I scripts/test.py
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STEPS = [
    ["python3", "-I", "-m", "unittest", "discover", "-s", "tests", "-t", "."],
    ["python3", "-I", "scripts/lint_skills.py"],
    ["python3", "-I", "scripts/check_docs.py"],
]

failed = [s for s in STEPS if subprocess.run(s, cwd=ROOT).returncode]
print("all checks passed" if not failed else f"{len(failed)} step(s) failed")
sys.exit(1 if failed else 0)
