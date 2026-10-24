# Review rubric

What `/review` checks, how findings are graded, and how the verdict is reached. A target repo can add checks through its own REVIEW.md or CLAUDE.md, but can't remove a Blocking check.

## Dimensions

Each dimension is a finder's brief; smaller reviews group them ([scaling](criteria.md#agents-and-parallelism)). Check the change, plus the code it touches, against:

### Correctness
- Does what the acceptance criteria and design decisions say, on the main path and the edge cases (empty, null, limits, errors).
- No regressions in behavior the change didn't mean to alter.
- Error handling: failures are caught where they can be handled, surfaced where they can't, and never silently swallowed.
- Concurrency and ordering: races, shared state, retries, idempotency.

### Design and consistency
- Fits the existing architecture and the design decisions; no unnecessary new abstraction or dependency.
- Matches the repo's conventions (CLAUDE.md, linters, surrounding code).
- No duplication of existing code that could be reused.
- Succinct: no redundant comments, padded docs or restated rules ([CLAUDE.md](../CLAUDE.md#rules)).

### Tests
- New or changed behavior has tests that would fail without the change.
- Tests check behavior, not implementation details; no flaky timing or ordering.
- Acceptance criteria that tests can cover are covered.

### Security
- Input validation and output encoding at trust boundaries; no injection (SQL, shell, path, template).
- AuthN/AuthZ checks on every new path; least privilege.
- No secrets, credentials or [sensitive content](criteria.md#building-blocks) in code, config, logs or messages.
- Dependencies: new ones are justified and maintained.

### Performance and reliability
- No accidental quadratic work, N+1 queries, unbounded memory or blocking calls on hot paths.
- Timeouts, retries with backoff, and resource cleanup where the code talks to the outside world.

### Compatibility and docs
- [Public interfaces](criteria.md#building-blocks) change compatibly, or the break is intended, versioned and documented.
- Data migrations are reversible or explicitly one-way, with a plan.
- Docs, changelogs and comments that describe changed behavior are updated.

## Severity

| Severity | Meaning | Blocks |
|---|---|---|
| **Blocking** | A defect introduced by the change: wrong behavior, a broken acceptance criterion, a security hole, missing tests for changed behavior, a broken public interface | Yes |
| **Non-blocking** | A real improvement worth making, but the change is acceptable without it | No |
| **Nit** | Minor polish, up to the [nit cap](criteria.md#agents-and-parallelism); drop the rest | No |
| **Pre-existing** | A real problem the change didn't introduce. Reported separately; worth an item | No |

Every finding needs a file:line. Blocking and Non-blocking findings also need a concrete failure scenario. A finding without what it needs is dropped.

## Verdict

- `review: passed @<sha> · coverage <covered>/<total>`: every file covered by every applicable dimension, and no Blocking findings at the reviewed head.
- `review: failed: <n> blocking @<sha> · coverage <covered>/<total>`: any Blocking finding.
- `review: incomplete @<sha> · coverage <covered>/<total>`: some file wasn't covered by an applicable dimension, or the scope was empty ([complete coverage](criteria.md#complete-coverage)). Never passes, and **takes precedence over `failed`**: Blocking findings are still listed, but the verdict is incomplete until coverage is.

`<sha>` is the reviewed head, or `no commit` in a repo without one.

User-accepted Blocking findings don't make a review pass; they mean the user merges ([merge rule](criteria.md#merge-rule)).
