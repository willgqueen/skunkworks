# ci scenarios

Run per [docs/testing.md](../../docs/testing.md).

## I1. Adopt the standard CI

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`
- **Run:** `/ci ../target`
- **Expect:** a read-only inspection (Python stack, default branch `main`, no workflows), then an item through new-item in the `greet` project whose Intent records the stack, that nothing exists, and that deliver adds `.github/workflows/ci.yml` from `ci/templates/ci.yml` and `renovate.json`. It's sized L (CI config is deploy and infra config, a risk area), so it starts in discover.
- **Answer:** new-item's "start the first phase?": "not now".

Requiring `ci-ok` in a ruleset and a real CI run need a GitHub remote (item 038).

## I2. Own the CI

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`, then in `../target` add `.github/workflows/ci.yml` from `ci/templates/ci.yml` with `STACK` python, `OWNER` skunkworks' GitHub owner, `SHA` ci-v2's commit (`git rev-parse ci-v2` here), `VERSION` ci-v2 and `DEFAULT_BRANCH` main, plus `with:` on `checks` overriding `lint: "ruff check ."`, `test: "python -m unittest"` and `audit: ""`; commit and push.
- **Run:** `/ci ../target own`
- **Expect:** a read-only inspection that finds the standard caller pinned at ci-v2 and its SHA; a report that the "overrides most stage commands" [signal](../../docs/criteria.md#building-blocks) holds and the other two don't; a question whether to own CI in target.
- **Answer:** "yes"
- **Expect:** an item through new-item in `greet` whose Intent names ci-v2 and its SHA, the files to copy into `.github/workflows/` (`ci-python.yml`, `ci-workflow-lint.yml`, `ci-gate.yml`), each of the three `uses:` lines to rewire to `./.github/workflows/<file>`, and that the ruleset is unchanged. It's sized L, so it starts in discover. Nothing changes in target, and no ruleset call is made.
- **Answer:** new-item's "start the first phase?": "not now".

## I3. Own with no signal

- **Setup:** I2's Setup without the `with:` overrides.
- **Run:** `/ci ../target own`
- **Expect:** the report says no signal holds and asks whether to proceed anyway.
- **Answer:** "no"
- **Expect:** no item; nothing changes in target.

Delivering I2's item needs a GitHub remote, as I1's ruleset does.
