# repo-context scenarios

Run per [docs/testing.md](../../docs/testing.md).

## C1. New project

- **Setup:** `python3 -I scripts/sandbox.py` (no seed)
- **Run:** `/repo-context target greet`
- **Expect:** `workspace/projects/greet/project.md` from the template, with the test command copied from target's CLAUDE.md (`python3 -m unittest`), `Merge policy` `manual`, and a *Last refreshed* date; `items/` created; `git -C ../target status` clean and nothing run in the target.

## C2. Refresh keeps what's learned

- **Setup:** `python3 -I scripts/sandbox.py --seed`; add "- Keep `greet()` pure." under *Conventions learned* and set `Merge policy` to `auto` in `workspace/projects/greet/project.md`.
- **Run:** `/repo-context target greet`
- **Expect:** factual sections rewritten; the convention and `auto` kept.
