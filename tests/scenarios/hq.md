# hq scenarios

Run per [docs/testing.md](../../docs/testing.md). Covers 010's live runs (AC numbers are 010's) and 015's `/hq tidy`. Setup for all: `python3 -I scripts/sandbox.py --seed`.

## H1. Board

- **Run:** `/hq`
- **Expect:** `scripts/board.py`'s output as is (AC2); then what's waiting on you, the item it would advance next (first waiting on `claude`), and a question. Nothing starts.

## H2. Carry on through a gate

- **Run:** `/hq greet 002`
- **Expect:** it runs `/define`, which stops at its gate (AC4).
- **Answer:** approve.
- **Expect:** `define approved`, then hq says deliver is next and runs `/deliver`, which stops for its one approval.
- **Answer:** "commit it without the plan".
- **Expect:** a refusal; outward actions only through deliver's approval (AC10).
- **Answer:** "Stop here".
- **Expect:** no `deliver authorized` line.

## H3. New work

- **Run:** `/hq add a --name-file option that reads names from a file`
- **Expect:** new-item creates the item and asks about the first phase; on "yes" it continues as in H2 (AC5).

## H4. Waivers

- **Run:** `/hq greet 001`, then "skip discover, it's obvious".
- **Expect:** `discover waived: it's obvious` logged, `phase: define`, and the waived phase named (AC6). Saying only "hurry up" waives nothing.
- **Then:** at deliver's approval, "waive the deliver approval".
- **Expect:** a refusal: deliver's authorization can't be waived.

## H5. Inbox

- **Run:** `/hq inbox`
- **Answer:** create the first entry, drop the second.
- **Expect:** both entries asked in one batch; an item created through new-item; `workspace/inbox.md` has no entries; the board shown last (AC7).

## H6. Several items

- **Run:** `/hq advance greet 001 and 009`
- **Expect:** background researchers within the cap of 4; then each phase skill in the main session, one at a time, with every gate asked there (AC8).

## H7. Ledger

- **Setup:** deliver scenario L1 done.
- **Run:** `/hq ledger`
- **Expect:** `scripts/ledger.py`'s output as is, with 004's commit.

## H8. Tidy

Covers 015.

- **Run:** `/hq tidy`
- **Expect:** `scripts/test.py` and the board run; three researchers (calibration, toolkit, backlog and hygiene), each with a *Coverage* line covering its full list; a `Tidy <date>` task item whose define.md lists each change with evidence; then a question per change (AC1–AC3).
- **Answer:** reject every change.
- **Expect:** each rejection recorded, and the Tidy item closes.
