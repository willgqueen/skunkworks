# CI

The standard CI for GitHub repos. Adopt it in a repo with `/ci <repo>`.

## The one required check

Every repo's CI ends with a job named **`ci-ok`** that calls the shared gate ([`ci-gate.yml`](../.github/workflows/ci-gate.yml)). The gate fails if any other job failed or was cancelled, or if the run attempt took over 10 minutes from its first job's start (the first job's queue time and earlier attempts don't count). It's the only required status check, reported as **`ci-ok / ok`**, so deliver and the [merge rule](criteria.md#merge-rule) wait on one constant name in every repo. (Requiring the aggregate avoids two traps: skipped or path-filtered jobs leaving a required check pending forever, and matrix job names changing.)

## Stages

Lint and format (with typecheck), unit tests and a dependency audit, as parallel jobs, plus a lint of the workflows themselves ([`ci-workflow-lint.yml`](../.github/workflows/ci-workflow-lint.yml), actionlint). Integration tests and builds are added per repo, from [`ci/templates/extras/`](../ci/templates/extras/). Coverage is advisory. Secret scanning and push protection are repository settings, not jobs.

## Shared workflows

[`.github/workflows/`](../.github/workflows/) holds a reusable workflow per stack (`on: workflow_call`). Each sets up the toolchain with dependency caching, which a repo turns off with `cache: ""` (Python, JS/TS) or `cache: false` (Go, Rust), and runs commands a repo can override; an empty command skips the step, and a job whose commands are all empty is skipped:

| Stack | Lint | Typecheck | Test | Audit |
|---|---|---|---|---|
| Python ([ci-python](../.github/workflows/ci-python.yml)) | `ruff check`, `ruff format --check` | set per repo | `pytest` | `pip-audit` |
| JS/TS ([ci-node](../.github/workflows/ci-node.yml)) | `npm run lint` (if present) | `tsc --noEmit` (if tsconfig) | `npm test` | `npm audit --audit-level=high` |
| Go ([ci-go](../.github/workflows/ci-go.yml)) | `gofmt -l`, `go vet` | | `go test -race` | `govulncheck` |
| Rust ([ci-rust](../.github/workflows/ci-rust.yml)) | `cargo fmt --check`, `clippy -D warnings` | | `cargo test` | `cargo audit` (prebuilt) |

Setup actions look for lock files (and Go's `go.mod`) at the repo root; a repo with its code in a subfolder also sets `cache-dependency-path` (and `go-version-file`).

A repo calls them from a thin workflow made from [`ci/templates/`](../ci/templates/). Commands passed as inputs run as shell: pass only fixed text, never event data such as PR titles or branch names.

## Rules

- **Pin everything:** actions and shared workflows to full commit SHAs with the version in a comment; tools and toolchains to exact versions (the runner's own Go and pip are the exceptions). skunkworks tags each release of its shared workflows `ci-v<n>` (starting from `ci-v1`; deliver tags the merge commit of any item that changes them), and callers pin that tag's SHA; [Renovate](../ci/templates/renovate.json) (`helpers:pinGitHubActionDigests`) opens update PRs, in skunkworks itself too ([`renovate.json`](../renovate.json)).
- **Least privilege:** `permissions: contents: read` by default; the gate adds `actions: read`.
- **`persist-credentials: false`** on checkout; never `pull_request_target`.
- **`timeout-minutes`** on every job (8 for stage jobs, 2 for the gate, so the critical path stays within 10); **`concurrency`** cancels superseded PR runs.
- **Time budget:** as short as possible; put slow suites on a schedule.
- **Flaky tests:** quarantine and track them; bounded, reported retries only.
- **Branch protection:** a ruleset on the default branch requiring `ci-ok / ok` from GitHub Actions, set by `/ci` only with your approval per repo.
- **Use each language's standard tools**, exposed as the repo's own commands where it has them.
- `python3 -I scripts/test.py` checks these rules on the files here (pins, timeouts, permissions, the gate).

## Limits

GitHub only. Other repos call the shared workflows from the public skunkworks repo, so a fork made private must allow access from repositories owned by the same user in its Actions settings.
