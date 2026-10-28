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

- **Setup:** F1 done.
- **Run:** `/define` in a session that has been working on greet.
- **Expect:** several items are `status: active` (002, 003, 005, 006), so it lists them and asks (028 AC5).
- **Answer:** "002"; then "add an AC: the test runner command is unchanged"; don't approve.
- **Expect:** it treats 002 as a revision.
- **Expect:** define.md edited, not rewritten (F1's ACs kept, one added); `define reopened` then `define revised` logged; it stops at the gate.

## F3. Re-size trigger

- **Run:** `/define greet 002` with "also switch the tests to pytest".
- **Expect:** it recommends re-sizing to L, naming the condition (a new dependency; the target uses unittest), and asks; `size` unchanged until the user agrees (028 AC5).
- **Answer:** to any scope question, "pytest only as the runner; keep the tests as they are"; to a split question, "keep it whole"; then "keep it M".
- **Expect:** no `re-sized` line; size still M.
