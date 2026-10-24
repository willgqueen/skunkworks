# review scenarios

Run per [docs/testing.md](../../docs/testing.md). Covers 005's live runs (AC numbers are 005's) and 023's coverage scenario.

**Setup for R1–R4:** `python3 -I scripts/sandbox.py --seed`, then commit an untested bug on a branch:

```sh
git -C ../target checkout -qb bug
python3 - <<'PY'
import pathlib
p = pathlib.Path("../target/greet.py")
s = p.read_text()
s = s.replace('    parser.add_argument("--shout", action="store_true")\n',
              '    parser.add_argument("--shout", action="store_true")\n    parser.add_argument("--times", type=int, default=1)\n')
s = s.replace("    print(greet(args.name, args.shout))\n",
              "    for _ in range(args.times - 1):\n        print(greet(args.name, args.shout))\n")
p.write_text(s)
PY
git -C ../target commit -qam "feat: add --times"
git -C ../target checkout -q main
```

## R1. A range with a bug

- **Run:** `/review main...bug ../target` (it resolves the names to shas).
- **Expect:**
  - a folder `workspace/reviews/<date>-…/` with the manifest (`greet.py`), the saved diff and coverage lists
  - three finders in parallel (M scaling), then a fresh refute pass (AC3, AC4)
  - a Blocking finding: `--times` prints one greeting too few, untested; with file:line and a failure scenario
  - a table, most severe first, then coverage per dimension and `review: failed: <n> blocking @<sha> · coverage 1/1` (AC6)

## R2. Repo additions

- **Setup:** also add `../target/REVIEW.md` with "Flag every new CLI option that README doesn't document", committed on `bug`.
- **Run:** as R1.
- **Expect:** a finding citing REVIEW.md for the undocumented `--times` (AC8).

## R3. Re-review

- **Setup:** R1 done. Fix the loop (`range(args.times)`), add a test, commit on `bug`.
- **Run:** `/review main...bug ../target` again.
- **Expect:** only the commits after R1's sha reviewed, the earlier Blocking finding confirmed resolved, and `review: passed` (AC9).

## R4. Incomplete coverage

Covers 023 (a review whose finders skip files is incomplete, never passed).

- **Setup:** `chmod 000 ../target/greet.py` (finders read files with Read only, so they can't read it; git still diffs the commits).
- **Run:** `/review main...bug ../target`
- **Expect:** `greet.py` reported as not read, re-run at most twice, then `review: incomplete @<sha> · coverage 0/1`. Never `passed`, even with no findings.
- **After:** `chmod 644 ../target/greet.py`.
