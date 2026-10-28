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

## F2. No item named

- **Setup:** F1 done (002 is the only `status: active` item in greet).
- **Run:** `/define` in a session that has been working on greet.
- **Expect:** it resolves to 002 without asking and treats it as a revision (028 AC5).
- **Answer:** "add an AC: the test runner command is unchanged"; don't approve.
- **Expect:** define.md edited, not rewritten (F1's ACs kept, one added); `define reopened` then `define revised` logged; it stops at the gate.

## F3. Re-size trigger

- **Run:** `/define greet 002` with "also move the tests to a second repo".
- **Expect:** it recommends re-sizing to L, naming the condition (≥2 repos), and asks; `size` unchanged until the user agrees (028 AC5).
- **Answer:** "keep it M".
- **Expect:** no `re-sized` line; size still M.
