# ci scenarios

Run per [docs/testing.md](../../docs/testing.md).

## I1. Adopt the standard CI

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`
- **Run:** `/ci ../target`
- **Expect:** a read-only inspection (Python stack, default branch `main`, no workflows) and no signal questions (adopt never asks), then an item through new-item in the `greet` project whose Intent records the stack, that nothing exists, and that deliver adds `.github/workflows/ci.yml` from `ci/templates/ci.yml` and `renovate.json`. It's sized L (CI config is deploy and infra config, a risk area), so it starts in discover. No pointer to [Own](../../.claude/skills/ci/SKILL.md#own), since no ownership signal holds.
- **Answer:** new-item's "start the first phase?": "not now".

Requiring `ci-ok` in a ruleset and a real CI run need a GitHub remote (item 038).

## I2. Own the CI

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`; then, from `DEST/skunkworks`, `git remote add origin <url>` with your real skunkworks checkout's origin (`git -C <checkout> remote get-url origin`; the sandbox copy has none) and `git -C DEST/skunkworks remote set-url --push origin DISABLED`, which blocks pushes through git; refuse any `gh` write in `DEST/skunkworks`. Then in `../target` add `.github/workflows/ci.yml` from `ci/templates/ci.yml` with `STACK` python, `OWNER` that URL's owner, `SHA` ci-v1's commit (`git rev-parse 'ci-v1^{commit}'` in your real checkout), `VERSION` ci-v1 and `DEFAULT_BRANCH` main, plus `with:` on `checks` overriding `lint: "ruff check ."`, `test: "python -m unittest"` and `audit: ""`; commit and push.
- **Run:** `/ci ../target own`
- **Expect:** a read-only inspection that finds the standard caller pinned at ci-v1 and its SHA, and no Renovate or Dependabot; a question on each of the two [signals](../../docs/criteria.md#building-blocks) the repo shows no evidence for.
- **Answer:** "no" to the stage needing secrets or an `environment`; "no" to its own CI maintainers.
- **Expect:** a report that the stage-commands signal holds and the other two don't; a question whether to own CI in target.
- **Answer:** "yes"
- **Expect:** an item through new-item in `greet` whose Intent names the ci-v1 pin, the highest `ci-v<n>` on origin and its commit from `git ls-remote --tags` against origin, the Releases entries after ci-v1, the files to copy into `.github/workflows/` (`ci-python.yml`, `ci-workflow-lint.yml`, `ci-gate.yml`), each of the three `uses:` lines to rewire to `./.github/workflows/<file>`, that neither Renovate nor Dependabot covers `.github/workflows` so Renovate is added, and that the ruleset is unchanged. It's sized L, so it starts in discover. Nothing changes in target, and no ruleset call is made.
- **Answer:** new-item's "start the first phase?": "not now".

## I3. Own with no signal

- **Setup:** I2's Setup without the `with:` overrides.
- **Run:** `/ci ../target own`
- **Expect:** I2's two signal questions.
- **Answer:** "no" to each.
- **Expect:** the report says no signal holds and asks whether to proceed anyway.
- **Answer:** "no"
- **Expect:** no item; nothing changes in target.

## I4. Adopt with an ownership signal

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`, then in `../target` add `.github/workflows/ci.yml`:

  ```yaml
  name: CI
  on:
    pull_request:
    push:
      branches: [main]
  permissions:
    contents: read
  jobs:
    test:
      runs-on: ubuntu-latest
      timeout-minutes: 8
      steps:
        - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
          with:
            persist-credentials: false
        - run: python -m unittest
          env:
            GREET_API_TOKEN: ${{ secrets.GREET_API_TOKEN }}
  ```

  Commit and push.
- **Run:** `/ci ../target`
- **Expect:** I1's inspection, plus the existing `ci.yml` and its `test` job; no signal questions. The stage-needing-secrets [signal](../../docs/criteria.md#building-blocks) named (`test` runs `python -m unittest` with `GREET_API_TOKEN` in its env), with a pointer to `/ci ../target own` for after adoption; then I1's item, its Intent also recording the existing `ci.yml` and what happens to it.
- **Answer:** new-item's "start the first phase?": "not now".

## I5. Own without the standard CI

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`
- **Run:** `/ci ../target own`
- **Expect:** says target isn't on the standard CI and offers Adopt; no signal questions.
- **Answer:** "no"
- **Expect:** no item; nothing changes in target.

## I6. Own when it already owns

- **Setup:** `python3 -I scripts/sandbox.py --seed --remote`, then in `../target` add `.github/workflows/ci.yml` from `ci/templates/ci.yml` with `STACK` python and `DEFAULT_BRANCH` main, each `uses:` set to `./.github/workflows/<file>` (no `@SHA # VERSION`), and copy `ci-python.yml`, `ci-workflow-lint.yml` and `ci-gate.yml` from `.github/workflows/` beside it; commit and push.
- **Run:** `/ci ../target own`
- **Expect:** says target already owns its CI; no signal questions, no item, nothing changes in target.

## I7. Adopt when it already owns

- **Setup:** I6's Setup.
- **Run:** `/ci ../target`
- **Expect:** says target already owns its CI; no signal questions and no item; nothing changes in target.

## I8. Own with a pin disagreement

- **Setup:** I2's Setup, with the `workflow-lint` line's SHA set to the commit of a later `ci-v<n>` (`git rev-parse 'ci-v<n>^{commit}'` in your real checkout), its comment left at ci-v1.
- **Run:** `/ci ../target own`
- **Answer:** I2's answers.
- **Expect:** I2's item, its Intent also recording that the `workflow-lint` line's SHA disagrees with the other two and with its `# ci-v1` comment.

## I9. Own when the latest-release lookup fails or finds no tag

- **Setup:** I2's Setup, except origin is your real origin URL with `-missing` appended to the repo name (a repo that doesn't exist, so the lookup fails; `git remote add origin <that URL>` from `DEST/skunkworks`, then the same push-disabling `set-url`), with `OWNER` the real origin's owner so the owner check passes, and `SHA` any commit. For the no-tag case, use a GitHub repo you own without `ci-v*` tags instead.
- **Run:** `/ci ../target own`
- **Answer:** I2's answers through the "own CI?" question.
- **Expect:** the latest-release lookup (`git ls-remote --tags` against origin) fails or finds no tag, so it stops and says so; no item; nothing changes in target.

## I10. Own with a caller owner that differs from origin's

- **Setup:** I2's Setup, with `OWNER` in `ci.yml` set to an owner other than origin's.
- **Run:** `/ci ../target own`
- **Expect:** says target isn't on the standard CI and offers Adopt; no signal questions.
- **Answer:** "no"
- **Expect:** no item; nothing changes in target.

## I11. Adopt with a separate deploy workflow

- **Setup:** I4's Setup, but the `test` job has no `env`, and add `.github/workflows/deploy.yml` (commit and push):

  ```yaml
  name: Deploy
  on:
    push:
      branches: [main]
  permissions:
    contents: read
  concurrency:
    group: deploy
  jobs:
    deploy:
      runs-on: ubuntu-latest
      timeout-minutes: 8
      environment: production
      steps:
        - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
          with:
            persist-credentials: false
        - run: python greet.py deploy
  ```
- **Run:** `/ci ../target`
- **Expect:** I1's inspection, plus both workflows; no signal questions and no signal named (the `environment` is in a separate deploy workflow, which doesn't count), so no pointer to Own; then I1's item, its Intent also recording the existing `ci.yml` and `deploy.yml` and what happens to each.
- **Answer:** new-item's "start the first phase?": "not now".

## I12. Adopt when it already owns, with a GitHub remote

- **Setup:** I6's Setup, with target on a GitHub remote where `ci-ok / ok` has passed on `main` (item 038).
- **Run:** `/ci ../target`
- **Expect:** I7's report, then Require ci-ok's question about the ruleset.
- **Answer:** "no"
- **Expect:** no ruleset call; the result reported (there's no item to log in); nothing changes in target.

Delivering I2's item needs a GitHub remote, as I1's ruleset does.
