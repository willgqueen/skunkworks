# new-item scenarios

Run per [docs/testing.md](../../docs/testing.md). Setup for all: `python3 -I scripts/sandbox.py --seed`.

## N1. An S item

- **Run:** `/new-item greet add a --times N flag that repeats the greeting`
- **Expect:** item `010-…` with `kind: feature`, `size: S`, `phase: deliver`, `status: proposed`, `repos: [target]`, an Intent with no invented requirements, and deliver.md from the template. The report names the deciding size condition and asks before starting.
- **Answer:** "not now".
- **Expect:** nothing else runs.

## N2. Too thin to size

- **Run:** `/new-item greet make it better`
- **Expect:** one question, no item created.
