# discover scenarios

Run per [docs/testing.md](../../docs/testing.md). Setup for all: `python3 -I scripts/sandbox.py --seed`.

## D1. Map a problem, then approve

Covers 009 (fresh-session run).

- **Run:** `/discover greet 001`
- **Expect before the gate:**
  - discover.md has Problem, Context grounded in `greet.py`, at least two Options, and numbered Open questions
  - the split check runs and says it fits one item (016 AC2)
  - nothing is decided or recommended; the log has `discover drafted`; it stops at the gate
- **Answer:** answer question 1 only, without approving.
- **Expect:** `<question> → <answer>` in discover.md and a `discover answers:` log line; still not approved.
- **Answer:** answer the rest and approve.
- **Expect:** `discover approved`, `phase: define`.

## D2. Revise after approval

- **Setup:** D1 done.
- **Run:** `/discover greet 001` with "add an option: gettext catalogs".
- **Expect:** `discover reopened` logged first, the option added to the existing doc (not rewritten), then the gate again.
