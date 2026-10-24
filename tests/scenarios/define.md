# define scenarios

Run per [docs/testing.md](../../docs/testing.md). Setup for all: `python3 -I scripts/sandbox.py --seed`.

## F1. Spec an M item

- **Run:** `/define greet 002`
- **Expect before the gate:**
  - a scope-changing gap is asked (for example whether `python3 greet.py` must keep working); a minor gap becomes an Assumption
  - define.md has Goal, In and Out of scope, checkable numbered ACs, Assumptions and a short Approach (M)
  - the split check runs ("fits one item"); `define drafted` logged; it stops at the gate
- **Answer:** "yes, `python3 greet.py` keeps working", then approve.
- **Expect:** `define approved`, `phase: deliver`; the board's next action is `/deliver`.
