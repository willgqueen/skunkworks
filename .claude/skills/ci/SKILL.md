---
name: ci
description: Set up the standard CI (docs/ci.md) in a GitHub repo through a normal item - detect the stack and existing CI, deliver a caller workflow with the ci-ok gate and Renovate config, then (with approval) require ci-ok in a ruleset; or, with own, move a repo onto its own copy of the shared workflows. Use when a repo has no CI, non-standard CI, has outgrown the shared CI, or the user asks to set up, fix or own CI.
argument-hint: <repo folder name or path> [own]
---

# ci

Follow [docs/ci.md](../../../docs/ci.md).

## Adopt

1. **Inspect** the repo, read-only (repo-context first if it has no project.md): its stack, its default branch, its existing workflows and required checks, and its own lint/test/build commands. If the [CI ownership](../../../docs/criteria.md#building-blocks) signals already hold, name them and say the repo can [own](#own) its CI once this adoption is done.
2. **Create the item** with **new-item**, recording in its Intent the stack, what exists and what changes. Size it by [criteria.md](../../../docs/criteria.md#size).
3. Deliver adds:
   - `.github/workflows/ci.yml` from `ci/templates/ci.yml`, filling `STACK` (python, node, go or rust), `OWNER` (skunkworks' GitHub owner), `SHA` and `VERSION` (the latest `ci-v<n>` tag and its commit), and `DEFAULT_BRANCH`; the repo's own commands go in as `with:` overrides where they differ
   - `renovate.json` from the template, unless the repo already has Renovate or Dependabot for actions
   - existing CI kept, replaced or merged into the standard, as the item's spec says

## Require ci-ok

Run `/ci <repo>` again once the adoption item is done and `ci-ok / ok` has passed on the default branch. Ask the user, for this repo, before adding a ruleset that requires `ci-ok / ok` from GitHub Actions (`integration_id` 15368) on the default branch, through `gh api` from the main session. Never add it without that approval. Log the result in the adoption item.

## Own

`/ci <repo> own`, per [docs/ci.md](../../../docs/ci.md#owning-your-ci):

1. **Inspect** the repo, read-only. It must already call the standard CI; if not, say so and offer [Adopt](#adopt). Read the pinned SHA and `ci-v<n>` tag from its caller's `uses:` lines.
2. **Test the [CI ownership](../../../docs/criteria.md#building-blocks) signals** and report which hold, or that none do. Ask the user whether to own CI in this repo (with none holding, whether to proceed anyway); stop if not.
3. **Create the item** with **new-item**, recording in its Intent the tag and SHA, the three files to copy into `.github/workflows/` (the stack workflow, `ci-workflow-lint.yml`, `ci-gate.yml`), each `uses:` line to rewire to `./.github/workflows/<file>`, and that the ruleset is unchanged. Size it by [criteria.md](../../../docs/criteria.md#size).
4. Deliver copies the files at that tag and rewires the caller in one PR. Never edit the ruleset on this path.
