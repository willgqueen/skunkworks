# repo-context scenarios

Run per [docs/testing.md](../../docs/testing.md).

## C1. New project

- **Setup:** `python3 -I scripts/sandbox.py` (no seed)
- **Run:** `/repo-context ../target greet`
- **Expect:** `workspace/projects/greet/project.md` from the template, with the test command copied from target's CLAUDE.md (`python3 -m unittest`), `Merge policy` `manual`, and a *Last refreshed* date; `items/` created; `workspace/projects/greet/architecture/overview.md` with *What it is* filled and sparse diagrams, and `decisions.md` with an empty table; `git -C ../target status` clean and nothing run in the target.

## C2. Refresh keeps what's learned

- **Setup:** `python3 -I scripts/sandbox.py --seed`; add "- Keep `greet()` pure." under *Conventions learned* and set `Merge policy` to `auto` in `workspace/projects/greet/project.md`; add a line under *Containers* in `workspace/projects/greet/architecture/overview.md`. Add a row to `decisions.md` (`| 2026-10-20 | Example | Kept | 999 |`); *Quality attributes* is seeded with one entry.
- **Run:** `/repo-context ../target greet`
- **Expect:** factual sections rewritten; the convention and `auto` kept; only *What it is* rewritten in overview.md (the *Containers* line and *Quality attributes* kept); `decisions.md`'s row untouched.

## C3. Refresh backfills the architecture folder

- **Setup:** `python3 -I scripts/sandbox.py --seed`, then `rm -r workspace/projects/greet/architecture`.
- **Run:** `/repo-context ../target greet`
- **Expect:** `workspace/projects/greet/architecture/overview.md` and `decisions.md` created from the templates, as in C1; project.md refreshed as in C2.

