# ci scenarios

Run per [docs/testing.md](../../docs/testing.md).

## I1. Adopt the standard CI

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`
- **Run:** `/ci target`
- **Expect:** a read-only inspection (Python stack, default branch `main`, no workflows); an item through new-item whose Intent records the stack, that nothing exists, and that deliver adds `.github/workflows/ci.yml` from `ci/templates/python.yml` and `renovate.json`; sized by criteria.
- **Answer:** at deliver's approval, "Stop here".

Requiring `ci-ok` in a ruleset and a real CI run need a GitHub remote (item 025).
