# ci scenarios

Run per [docs/testing.md](../../docs/testing.md).

## I1. Adopt the standard CI

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`
- **Run:** `/ci ../target`
- **Expect:** a read-only inspection (Python stack, default branch `main`, no workflows), then an item through new-item in the `greet` project whose Intent records the stack, that nothing exists, and that deliver adds `.github/workflows/ci.yml` from `ci/templates/ci.yml` and `renovate.json`. It's sized L (CI config is deploy and infra config, a risk area), so it starts in discover.
- **Answer:** new-item's "start the first phase?": "not now".

Requiring `ci-ok` in a ruleset and a real CI run need a GitHub remote (item 038).
