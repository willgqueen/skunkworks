# CI

The standard CI for GitHub repos. Adopt it in a repo with `/ci <repo>`.

## The one required check

Every repo's CI ends with a job named **`ci-ok`** that calls the shared gate ([`ci-gate.yml`](../.github/workflows/ci-gate.yml)). The gate fails if any other job failed or was cancelled, or if the run attempt took over 10 minutes from the first job it ran (queue time, skipped jobs and jobs carried over from earlier attempts don't count). It's the only required status check, reported as **`ci-ok / ok`**, so deliver and the [merge rule](criteria.md#merge-rule) wait on one constant name in every repo. (Requiring the aggregate avoids two traps: skipped or path-filtered jobs leaving a required check pending forever, and matrix job names changing.)

## Stages

Lint and format (with typecheck), unit tests and a dependency audit, as parallel jobs, plus a lint of the workflows themselves ([`ci-workflow-lint.yml`](../.github/workflows/ci-workflow-lint.yml), actionlint). Integration tests and builds are added per repo, from [`ci/templates/extras/`](../ci/templates/extras/). Coverage is advisory. Secret scanning and push protection are repository settings, not jobs.

## Shared workflows

[`.github/workflows/`](../.github/workflows/) holds a reusable workflow per stack (`on: workflow_call`). Each sets up the toolchain with dependency caching, which a repo turns off with `cache: ""` (Python, JS/TS) or `cache: false` (Go, Rust), and runs commands a repo can override; an empty command skips the step, and a job whose stage commands (lint and typecheck, test, or audit) are all empty is skipped, even if `install` is set:

| Stack | Lint | Typecheck | Test | Audit |
|---|---|---|---|---|
| Python ([ci-python](../.github/workflows/ci-python.yml)) | `ruff check`, `ruff format --check` | set per repo | `pytest` | `pip-audit` |
| JS/TS ([ci-node](../.github/workflows/ci-node.yml)) | `npm run lint` (if present) | `tsc --noEmit` (if tsconfig) | `npm test` | `npm audit --audit-level=high` |
| Go ([ci-go](../.github/workflows/ci-go.yml)) | `gofmt -l`, `go vet` | | `go test -race` | `govulncheck` |
| Rust ([ci-rust](../.github/workflows/ci-rust.yml)) | `cargo fmt --check`, `clippy -D warnings` | | `cargo test` | `cargo audit` (prebuilt) |

Setup actions look for lock files (and Go's `go.mod`) at the repo root; a repo with its code in a subfolder also sets `cache-dependency-path` (and `go-version-file`).

A repo calls them from a thin workflow made from [`ci/templates/ci.yml`](../ci/templates/ci.yml), with `STACK` set to python, node, go or rust. Commands passed as inputs run as shell: pass only fixed text, never event data such as PR titles or branch names.

## Rules

- **Pin everything:** actions and shared workflows to full commit SHAs with the version in a comment; tools and toolchains to exact versions (the runner's own pip is the exception; govulncheck, which has no prebuilt releases, runs with `go run` and is verified by Go's checksum database); a downloaded tool is checked with `sha256sum -c` against its release's checksum. skunkworks tags each release of its shared workflows `ci-v<n>` (starting from `ci-v1`; deliver tags the merge commit of any item that changes them, and that item adds the release's entry under [Releases](#releases)), and callers of the shared workflows pin the tag's commit (`ci-v<n>^{commit}`); [Renovate](../ci/templates/renovate.json) (`helpers:pinGitHubActionDigests`) opens update PRs, in skunkworks itself too ([`renovate.json`](../renovate.json)).
- **Latest release:** the highest `ci-v<n>` by number, from `git ls-remote --tags` against skunkworks' own `origin`, never the caller's `OWNER`. Its commit is the peeled `^{}` line if there is one, else the tag's own line. If the command fails or finds no tag, stop.
- **Deploy and release stages** go in a separate workflow with its own concurrency group, never in `ci.yml`.
- **Least privilege:** `permissions: contents: read` by default; the gate adds `actions: read`.
- **`persist-credentials: false`** on checkout; never `pull_request_target`.
- **`timeout-minutes`** on every job (8 for stage jobs, 2 for the gate, so the critical path stays within 10); **`concurrency`** cancels superseded PR runs.
- **Time budget:** as short as possible; put slow suites on a schedule.
- **Flaky tests:** quarantine and track them; bounded, reported retries only.
- **Branch protection:** a ruleset on the default branch requiring `ci-ok / ok` from GitHub Actions, set by `/ci` only with your approval per repo.
- **Use each language's standard tools**, exposed as the repo's own commands where it has them.
- `python3 -I scripts/test.py` checks these rules on the files here (pins, downloads, timeouts, permissions, the gate).

## Owning your CI

A repo that has outgrown the shared workflows ([when](criteria.md#building-blocks)) takes them over with `/ci <repo> own`:

- Find the [latest release](#rules).
- Fetch that commit and copy the stack workflow, `ci-workflow-lint.yml` and `ci-gate.yml` from it, not from the local checkout or the repo's old pin, into the repo's `.github/workflows/`. The item lists the [Releases](#releases) entries since the pin, also read at that commit.
- In each copied workflow, the first line's docs/ci.md link becomes `From skunkworks ci-v<n> (<sha>)` and the rest stays. The rewired caller's first line is replaced whole with `# CI (owned). From skunkworks ci-v<n> (<sha>); rules: docs/ci.md#rules in skunkworks.`
- Call them by local path (`uses: ./.github/workflows/<file>`) and keep the `ci-ok` job: the check stays `ci-ok / ok` from GitHub Actions, so the ruleset doesn't change. The other [rules](#rules) carry over; a local `uses: ./` path needs no SHA.
- Keep deploy and release stages [separate](#rules).
- Add Renovate (from [`ci/templates/renovate.json`](../ci/templates/renovate.json)) when neither Renovate nor Dependabot covers `.github/workflows`.

From then on the repo maintains its own CI: its tool pins and checksums (Renovate only bumps actions), fixes from [Releases](#releases) ported by hand from its base, and the rules, enforced by its own review. skunkworks' releases no longer reach it.

## Limits

GitHub only. Other repos call the shared workflows from the public skunkworks repo, so a fork made private must allow access from repositories owned by the same user in its Actions settings.

## Releases

Callers of the shared workflows move to a release by changing the SHA and the `# ci-v<n>` comment on their three `uses:` lines.

- **ci-v2:** stage jobs with no stage command show as skipped (an install-only job no longer runs); actionlint comes from its checksum-verified release binary; the time budget counts only jobs the attempt ran, so skipped jobs and partial re-runs don't trip it.

