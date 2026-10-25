# define scenarios

Run per [docs/testing.md](../../docs/testing.md). Setup for all: `python3 -I scripts/sandbox.py --seed`.

## F1. Spec an M item

- **Run:** `/define greet 002`
- **Expect before the gate:**
  - any scope-changing gap is asked, not guessed; minor gaps (for example what `helpers.py` holds) become Assumptions
  - define.md has Goal, In and Out of scope, checkable numbered ACs, Assumptions and a short Approach (M)
  - the split check runs ("fits one item") (016 AC2); `define drafted` logged; it stops at the gate
- **Answer:** to any scope question, "only reorganize the existing tests"; then approve, and "not now" to starting deliver.
- **Expect:** `define approved`, `phase: deliver`; the board's next action is `/deliver`.
