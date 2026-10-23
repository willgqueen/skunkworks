# Criteria

The single source for every condition that skills and the process branch on. Skills link here instead of restating rules. Change a definition here, and every skill that uses it follows.

Numbers marked *(provisional)* are starting guesses. They must be calibrated against real work; see [Calibration](#calibration).

## Building blocks

- **Public interface:** anything used from outside the module or repo that changes it: HTTP/RPC endpoints, CLI commands, flags and output, a library's exported API, config and env var formats, DB schema, event and message formats, on-disk file formats. Internal functions don't count.
- **Risk area:** stored data (schema, migrations, data backfills), auth, permissions and secrets, payments or money, deletion of user data, deploy and infra config, public interfaces.
- **Hard to reverse:** undoing it takes more than reverting the commit. Data has been written or migrated, others already depend on a published interface, there are external side effects (a deploy, a release, sent messages), or other code will be built on top of the choice (framework, datastore, core abstraction).
- **Sensitive content:** never allowed in commit messages, PR text, branch names or code comments in a target repo:
  - secrets: keys, tokens, passwords, connection strings
  - personal data about anyone other than the author's own attribution
  - local machine details: absolute home paths, hostnames
  - internal URLs

  Item slugs and plain descriptions of the work are fine.

## Size

Check for L first, then S. Anything else is M.

- **L** if *any* of these hold:
  - acceptance criteria can't be written yet (the problem is unclear)
  - there are ≥2 workable approaches with real trade-offs
  - it spans ≥2 modules or ≥2 repos
  - it touches a risk area
  - it needs a new dependency, service or infrastructure
  - it will likely take more than ~6 tasks *(provisional)*
- **S** if *all* of these hold:
  - the files can be named: ≤3 files in one module *(provisional)*
  - the change fits in one sentence
  - no new dependencies
  - no risk area
  - one commit
- **M:** everything else.
- An initiative is always L.

**Too thin to size:** you can't say what changes or roughly where. Ask one question; don't guess.

**Re-size trigger:** at any phase, an L condition appears on an S or M item, no L condition holds any longer for an L item, or all S conditions turn out to hold for an M item. Recommend re-sizing; only change the size with the user's agreement, and log it as `- <date>: re-sized <old>→<new>: <condition that triggered it>`.

## Kind

Kind is the type of work, regardless of size.

- **investigation:** what's delivered is a written answer, not code.
- **initiative:** needs ≥2 items that could each ship on their own.
- **task:** no new intended behavior: a bug fix that restores intended behavior, a chore, a refactor, a dependency bump.
- **feature:** new or changed intended behavior.

## Decisions

- **Significant decision** (ask the user, with options and a recommendation) if *any* of these hold:
  - it's hard to reverse
  - it touches a public interface or risk area
  - there are ≥2 workable options and the choice changes other tasks or what the user sees
  - it brings in a dependency, pattern or abstraction the repo doesn't already use
- **Minor decision** (decide and record): follows an existing repo pattern, stays inside one task, and is cheap to change later.
- When it's unclear which applies, treat it as significant.

## Gaps

- **Scope-changing gap** (ask the user): the answer would add or remove an acceptance criterion, move something in or out of scope, or touch a risk area.
- **Minor gap** (take the default and record it as an assumption): a repo convention or standard practice settles it, and guessing wrong costs ≤1 task of rework.

## Work units

- **Task** (in a plan): one concern, one commit, tests pass afterwards, has its own check, reviewable in one sitting: ~300 changed lines as a guide *(provisional)*.
- **Checkable criterion:** gets a pass/fail answer from a test, a command with expected output, or a specific observation.

## Phase state

- **Phase approved:** `item.md`'s log has a `- <date>: <phase> approved` line with no later `<phase> reopened` line. Approval comes only from the user.
- **Phase drafted:** the log has a `<phase> drafted` line. A phase doc that only holds template text (as new-item creates it) is not drafted.
- **Revision:** running a phase skill on a phase that's already drafted. If that phase was approved, log `- <date>: <phase> reopened` first, so the old approval no longer counts.

## Definitions of done

An item is done when the rule for its **kind** is met, finished the way its **repo setup** requires.

### By kind

- **Code item** (feature, task):
  - every task committed
  - every acceptance criterion verified or [deferred](#deferring-a-check)
  - review passed, or its findings resolved or explicitly accepted by the user
  - merged into the default branch
  - worktree removed, item archived
- **Investigation:** every question in define.md answered in deliver.md's *Outcome*, with evidence that meets define.md's standard, plus a recommendation. Recommended follow-up work is proposed as items.
- **Initiative:** every child item is done or dropped, and the initiative's own acceptance criteria are verified.

### By repo setup

| Setup | Finish |
|---|---|
| Remote + CI | Push, open PR, review, CI green, merge per the [merge rule](#merge-rule) |
| Remote, no CI | Push, open PR, review, local checks green, merge per the merge rule |
| Local only | No push or PR; review the branch diff, local checks green, merge locally per the merge rule |

- **CI green:** every required check on the PR passes.
- **Local checks:** the test, lint and build commands listed in project.md's *Commands*, where they exist.

### Merge rule

Deliver merges only when **all** of these hold. Otherwise it stops and the user merges.
- project.md's *Merge policy* is `auto` (the default is `manual`)
- review passed: findings resolved by fixes. Findings the user accepted without a fix mean the user merges.
- local checks and CI (where there is CI) are green
- the item touches no [risk area](#building-blocks)

### Deferring a check

- A check may be deferred only when it **can't be run in the current environment**, because it needs a tool, service, session or person that isn't available. A failing or slow check is never deferred.
- Move it to a named follow-up item: an existing one whose scope covers it, or a new one made with new-item. Log `check deferred to <NNN>: <check>` in the original item, and add the check to the follow-up's define.md (or to its Intent, if it isn't defined yet).
- Any other pending check keeps the item open.

## Context

- **Stale project.md:** last refreshed more than 30 days ago *(provisional)*, or the current work found it wrong.
- **Use an Explore subagent:** the survey would take more than ~10 file reads *(provisional)*, or the code is spread across areas you can't locate up front.

## Calibration

The provisional numbers above are guesses until they're tested against sustained use. Calibrate them using completed items as evidence, not intuition.

**When:** after 10 items have reached `done` since the last calibration *(provisional)*, or whenever the same re-size trigger has fired 3 times. Skills that see either condition suggest calibrating; they don't calibrate on their own.

**Evidence** (from `workspace/projects/*/items/` and `workspace/archive/`):
- Starting size vs. final size, and the `re-sized` log lines with their triggers
- Actual task count in `deliver.md` against the ~6-task L threshold
- Files and lines changed per task and per item (from the PRs or commits linked in `deliver.md`)
- Decisions the user overrode or questions they found unnecessary (from the `develop.md` decisions and the item logs)
- Explore subagent use, and project.md refreshes that turned out to be needed or not

**How:** propose each change to a number, citing the items that support it, and let the user approve. Record approved changes below. Definitions without a number can be recalibrated the same way when the evidence shows they misclassify work.

### Calibration history

| Date | Change | Evidence |
|---|---|---|
| 2026-10-23 | Initial values set | None yet: starting guesses |
