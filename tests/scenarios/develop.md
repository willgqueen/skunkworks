# develop scenarios

Run per [docs/testing.md](../../docs/testing.md). Covers 001's behavioral checks (AC numbers are 001's). Setup for all: `python3 -I scripts/sandbox.py --seed`.

## V1. Design an L item

- **Run:** `/develop greet 003`
- **Expect:**
  - develop.md has an Approach grounded in `greet.py` (read only; `git -C ../target status` clean), Decisions, an ordered task list, and Risks (AC6, AC8)
  - at least one significant decision (for example a registry dict or subclasses) is asked with options and a recommendation before it's written; minor ones are recorded with `Kind: minor` (AC7)
  - every AC of 003 (1–4) is served by a task (`Serves: AC<n>`) (AC9)
  - the split check runs (016 AC2); `develop drafted` logged; it stops at the gate (AC12)
- **Answer:** take each recommendation. Don't approve yet.
- **Expect:** each significant decision records `Recommendation taken: yes` (AC7).

## V2. Revise a draft

- **Setup:** V1 done.
- **Run:** `/develop greet 003` with "switch the first significant decision to its second option".
- **Expect:** the existing develop.md revised, not rewritten: that decision now records `Recommendation taken: no`, and every task it affects is updated; `develop revised` logged (AC7, AC11).
- **Answer:** approve.
- **Expect:** `develop approved`, `phase: deliver`, a row in `workspace/projects/greet/architecture/decisions.md` for the switched decision with Item `003` (022 AC3), and a question about starting deliver; answer "not now" (AC13).

## V3. L item without an approved define

- **Run:** `/develop greet 001`
- **Expect:** it says define isn't approved and asks whether to continue (AC4).
- **Answer:** "no".
- **Expect:** no develop.md written.

## V4. Not needed for M

- **Run:** `/develop greet 002`
- **Expect:** it says develop isn't needed for an M item (the approach lives in define.md) and offers re-sizing; no develop.md (AC5).
- **Answer:** "keep it M".

## V5. Define is wrong

- **Setup:** in `workspace/projects/greet/items/003-add-pluggable-greeting-styles/define.md`, add AC "5. [ ] The CLI's options don't change: no new flags."
- **Run:** `/develop greet 003`
- **Expect:** it finds AC5 contradicts AC1 (`--style`), stops, and recommends a define revision; define.md unchanged (AC10).
