# review scenarios

Run per [docs/testing.md](../../docs/testing.md). Covers 005's live runs (AC numbers are 005's; `<project> <item>` input runs in deliver L1, a PR needs item 025) and 023's coverage scenario.

Setup for R1–R2: `python3 -I scripts/sandbox.py --seed`, then add a repo rule on `main` and an untested bug on branch `bug`, left checked out:

```sh
printf '# Review\n\n- Flag every CLI option that README.md does not document.\n' > ../target/REVIEW.md
git -C ../target add REVIEW.md && git -C ../target commit -qm "docs: add review rules"
git -C ../target checkout -qb bug
python3 -I - <<'PY'
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
```

## R1. A range with a bug

- **Run:** `/review main...bug ../target` (it resolves the names to shas).
- **Expect:**
  - a folder `workspace/reviews/<date>-…/` with the manifest (`greet.py`), the saved diff and coverage lists
  - the diff adds a CLI flag (a risk area), so one finder per dimension, in waves within the parallel cap, then a fresh refute pass (AC3, AC4)
  - a Blocking finding: `--times` prints one greeting too few, untested; with file:line and a failure scenario
  - a finding citing REVIEW.md for the undocumented `--times` (AC8)
  - one row per issue, even when several finders report it (AC5); nits within the nit cap and never blocking; Pre-existing issues (for example `main()` had no tests) listed separately (AC7)
  - a table, most severe first, then coverage per dimension and `review: failed: <n> blocking @<sha> · coverage 1/1` (AC6)

## R2. Re-review

- **Setup:** R1 done. Fix the loop, test it and document the option:
  ```sh
  sed -i.bak 's/range(args.times - 1)/range(args.times)/' ../target/greet.py && rm ../target/greet.py.bak
  printf '\n\nclass Times(unittest.TestCase):\n    def test_times(self):\n        from contextlib import redirect_stdout\n        from io import StringIO\n        from greet import main\n        out = StringIO()\n        with redirect_stdout(out):\n            main(["Ada", "--times", "2"])\n        self.assertEqual(out.getvalue(), "Hello, Ada!\\nHello, Ada!\\n")\n' >> ../target/test_greet.py
  printf '\n`--times N` repeats the greeting N times.\n' >> ../target/README.md
  git -C ../target commit -qam "fix: print --times greetings"
  ```
- **Run:** `/review main...bug ../target`
- **Expect:** only the commits after R1's sha reviewed, each earlier Blocking finding confirmed resolved, and `review: passed @<sha> · coverage <n>/<n>` (AC9).

## R3. Incomplete coverage

Covers 023 (a review whose finders skip files is incomplete, never passed). A whole-codebase review reads files whole, so an unreadable file can't be covered from a diff.

- **Setup:** `python3 -I scripts/sandbox.py --seed`, then `chmod 000 ../target/greet.py`.
- **Run:** `/review --all ../target`
- **Expect:** `greet.py` reported as not read, re-run up to the re-run limit, then `review: incomplete @<sha> · coverage <n-1>/<n>`. Never `passed`, even with no findings. Then `chmod 644 ../target/greet.py`.
