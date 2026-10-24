# deliver scenarios

Run per [docs/testing.md](../../docs/testing.md). Covers 003's AC2–AC4, AC6 and AC8–AC15; AC numbers below are 003's. `../target` is the sandbox's target repo.

## L1. S item, local only, end to end

- **Setup:** `python3 -I scripts/sandbox.py --seed`
- **Run:** `/deliver greet 004`
- **Expect the plan:** the definition of done (code item, local only), worktree `workspace/worktrees/target/feat/add-version-flag`, branch `feat/add-version-flag`, one task from the Intent, every outward action, and that you merge (`manual`). One question for approval (AC4).
- **Answer:** approve.
- **Expect:**
  - `deliver authorized:` logged once; no further approval asked
  - an implementer runs the task, deliver runs `python3 -m unittest` itself and makes one conventional commit with no sensitive content or workspace text (AC6)
  - the log line `task 1 committed <sha> · <files> files, +<added>/-<deleted>`
  - each AC verified by verifiers in *Verification*, ending `Coverage: n/n ACs` (AC9)
  - `/review` runs and logs its verdict; it stops with the branch ready for you to merge (AC12)
  - `git -C ../target status` is clean and still on `main`
- **Then:** `git -C ../target merge --no-ff feat/add-version-flag`, and `/deliver greet 004` again.
- **Expect:** it sees the merge, removes the worktree and branch, completes *Outcome*, archives the item, and offers *Conventions learned* additions (AC13).

## L2. Not ready

- **Setup:** `python3 -I scripts/sandbox.py --seed`
- **Run:** `/deliver greet 002`
- **Expect:** a refusal naming what's missing (define not approved), and no files changed (AC2).

## L3. Tasks from develop

- **Setup:** develop scenario V1 done.
- **Run:** `/deliver greet 003`, then answer "Stop here".
- **Expect:** deliver.md's tasks copied from develop.md, in order (AC3).

## L4. With a remote

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`
- **Run:** `/deliver greet 004`, approve.
- **Expect:** the branch pushed to `remote.git` (`git -C ../remote.git branch` lists it). A local bare remote isn't GitHub, so no PR or CI: record exactly how deliver handles that. The PR and CI parts of AC10–AC11 need a GitHub remote (item 025).

## L5. A failing check blocks

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`, then add a failing test to the target:
  ```sh
  printf 'import unittest\n\nclass Broken(unittest.TestCase):\n    def test_broken(self):\n        self.fail("seeded")\n' > ../target/test_broken.py
  git -C ../target add -A && git -C ../target commit -qm "test: seed a failure" && git -C ../target push -q
  ```
- **Run:** `/deliver greet 004`, approve.
- **Expect:** the failure sent back to the implementer once, then `status: blocked` with a `blocked:` log line naming the failure, nothing committed after it, nothing pushed (`git -C ../remote.git branch` lists only `main`) (AC8).

## L6. Investigation

- **Setup:** `python3 -I scripts/sandbox.py --seed`
- **Run:** `/deliver greet 005`, approve.
- **Expect:** no worktree or branch; *Outcome* answers both questions, citing lines and Python releases, with a recommendation; it offers follow-up items; the item is archived (AC14).

## L7. Initiative

- **Setup:** `python3 -I scripts/sandbox.py --seed`
- **Run:** `/deliver greet 006`, approve.
- **Expect:** both children found done in the archive, the initiative's ACs checked, *Outcome* summarizes the children, archived (AC15).
