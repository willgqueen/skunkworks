# new-item scenarios

Run per [docs/testing.md](../../docs/testing.md). Setup for all: `python3 -I scripts/sandbox.py --seed`.

## N1. An S item

- **Run:** `/new-item greet add a test that greet() handles an empty name`
- **Expect:** item `010-…` with `kind: task`, `size: S`, `phase: deliver`, `status: proposed`, `repos: [target]`, an Intent with no invented requirements, and deliver.md from the template. The report names the deciding size condition and asks before starting.
- **Answer:** "not now".
- **Expect:** nothing else runs.

## N2. Too thin to size

- **Run:** `/new-item greet make it better`
- **Expect:** one question, no item created.

## N3. A risk area makes it L

- **Run:** `/new-item greet add a --times N flag that repeats the greeting`
- **Expect:** `size: L` because a CLI flag is a public interface (a risk area), `phase: discover` with discover.md; the split check says it fits one item.
- **Answer:** "not now".
