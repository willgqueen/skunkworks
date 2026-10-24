# develop scenarios

Run per [docs/testing.md](../../docs/testing.md). Setup for all: `python3 -I scripts/sandbox.py --seed`.

## V1. Design an L item

Covers 001 (fresh-session behavioral run).

- **Run:** `/develop greet 003`
- **Expect:**
  - develop.md has an Approach grounded in `greet.py`, Decisions, an ordered task list, and Risks
  - at least one significant decision (for example a registry dict or subclasses) is asked with options and a recommendation; minor ones are recorded with `Kind: minor`
  - every AC (1–4) is served by a task (`Serves: AC<n>`)
  - `develop drafted` logged; it stops at the gate
- **Answer:** pick the recommended option, then approve.
- **Expect:** the decision recorded with `Recommendation taken: yes`, `develop approved`, `phase: deliver`.
