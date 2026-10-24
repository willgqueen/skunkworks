# split scenarios

Run per [docs/testing.md](../../docs/testing.md). Covers 016's live runs; AC numbers are 016's. Setup for all: `python3 -I scripts/sandbox.py --seed`.

## P1. Split into an initiative

- **Run:** `/split greet 009`
- **Expect:** the signal named (it joins separate outcomes); candidates with title, kind, size, seam and one line of scope, ordered with a thin skeleton first; no split by layer (DB, API, UI) or activity; `depends_on` only where it can't be cut; later slices left as Intent only; three choices with initiative the default (AC2, AC3, AC5, AC6, AC9, AC10).
- **Answer:** initiative.
- **Expect:** 009 becomes `kind: initiative`, `size: L`, logs `re-kinded feature→initiative: <signal>` and `split: initiative`; children created through new-item with `parent: "009"`; the board nests them with `children: 0/<n>`, and a child waiting on another shows `items` (AC4, AC7, AC8).

## P2. Siblings

- **Run:** `/split greet 009`, answer siblings.
- **Expect:** sibling items created, 009's Intent narrowed to what's left, `split: siblings <ids>` (AC4).

## P3. Keep whole

- **Run:** `/split greet 009`, answer keep whole ("one team, one release").
- **Expect:** nothing changes but `split: kept whole: one team, one release`.

## P4. Called by new-item

- **Run:** `/new-item greet a greeting web service with accounts, history, an admin UI and email reminders`
- **Expect:** new-item runs the split check and proposes the split before creating anything (AC2).

## P5. Fits one item

- **Run:** `/split greet 004`
- **Expect:** "fits one item" in one line; nothing changes.
