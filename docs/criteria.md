# Criteria

The single source for every condition that skills and the process branch on. Skills link here instead of restating rules. Change a definition here, and every skill that uses it follows.

Numbers marked *(provisional)* are starting guesses. They must be calibrated against real work; see [Calibration](#calibration).

## Building blocks

- **Public interface:** anything used from outside the module or repo that changes it: HTTP/RPC endpoints, CLI commands, flags and output, a library's exported API, config and env var formats, DB schema, event and message formats, on-disk file formats. Internal functions don't count.
- **Risk area:** stored data (schema, migrations, data backfills), auth, permissions and secrets, payments or money, deletion of user data, deploy and infra config, public interfaces.
- **Hard to reverse:** undoing it takes more than reverting the commit. Data has been written or migrated, others already depend on a published interface, there are external side effects (a deploy, a release, sent messages), or other code will be built on top of the choice (framework, datastore, core abstraction).
- **Host change:** installing, upgrading or removing software, interpreters or packages outside a repo's own environment in its worktree (a project's venv or `node_modules` there doesn't count; a toolchain a check fetches by itself, such as rustup's or Go's, does), or changing system or user configuration (shell profiles, global git config, system settings). It needs the user's explicit approval of that specific change (what, and where); deliver's per-item authorization never covers one.
- **Boring technology first:** a language, datastore, framework or runtime not already in the project's stack (project.md *Stack*) spends an innovation token, of about three per project *(provisional)*. Each one must be justified by the product's real differentiator and recorded in the decision ([guide](architecture/language-and-framework-selection.md#boring-technology)).
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
  - it spans ≥2 repos, or ≥2 modules and changes a shared contract between them; uniform mechanical edits and docs-only changes don't count (skills and agents are code, not docs)
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

## Splitting

- **Too big for one item** (propose a split) if any of these hold:
  - more than ~8 tasks *(provisional)*
  - more than ~12 acceptance criteria *(provisional)*
  - ≥3 repos *(provisional)*
  - a too-big signal
- **Too-big signals:**
  - the work joins separate outcomes ("and", a list of workflows)
  - its acceptance criteria span distinct behaviors
  - no demoable state until the end
  - an unresolved unknown (split off an investigation)
  - parts that could be built in parallel
- **Seams**, preferred in this order:
  1. user-visible workflow paths
  2. interfaces or platforms
  3. data variations
  4. rules that can be deferred
  5. a skeleton, then flesh
  6. unknowns, as an investigation first
  7. replaceable pieces of an existing system
- **Never split** by layer (DB, API, UI) or by activity (design, build, test).
- **A good increment** is observable, leaves the system working, can be tested on its own, and depends on as little as possible.
- **Order:** a thin end-to-end skeleton first where the work needs one, then the riskiest parts. Re-cut to remove a dependency before recording it in `depends_on`.
- **Depth:** detail children only as far as the idea's specificity allows. Later slices can stay `proposed` with just an Intent.

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

- **Phase approved:** `item.md`'s log has a `- <date>: <phase> approved` or `- <date>: <phase> waived: <reason>` line with no later `<phase> reopened` line. Approval and waivers come only from the user.
- **Waived:** the user explicitly skipped a phase's gate. A waived phase counts as approved, and its doc may be left unwritten. Deliver's per-item authorization of outward actions (`deliver authorized`) can never be waived.
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
- **Investigation:** every question in define.md answered in deliver.md's *Outcome*, with evidence that meets define.md's standard, or [deferred](#deferring-a-check) when that evidence needs a tool that isn't available, plus a recommendation. Recommended follow-up work is proposed as items.
- **Initiative:** every child item is done or dropped, and the initiative's own acceptance criteria are verified.

### By repo setup

| Setup | Finish |
|---|---|
| Remote + CI | Push, open PR, review, CI green, merge per the [merge rule](#merge-rule) |
| Remote, no CI | Push, open PR, review, local checks green, merge per the merge rule |
| Local only | No push or PR; review the branch diff, local checks green, merge locally per the merge rule |

- **CI green:** every required check on the PR passes, and, in a repo with the [standard CI](ci.md), `ci-ok / ok` passes whether or not a ruleset requires it.
- **Local checks:** the test, lint and build commands listed in project.md's *Commands*, where they exist.

### Merge rule

Deliver merges only when **all** of these hold. Otherwise it stops and the user merges.
- project.md's *Merge policy* is `auto` (the default is `manual`)
- the latest [review](review-rubric.md#verdict) verdict, for the final pushed head, is `review: passed` (full coverage), and no Blocking finding was accepted without a fix
- local checks and CI (where there is CI) are green
- the item touches no [risk area](#building-blocks)

### Deferring a check

- A check may be deferred only when it **can't be run in the current environment**, because it needs a tool, service, session or person that isn't available. A failing or slow check is never deferred.
- Move it to a named follow-up item: an existing one whose scope covers it, or a new one made with new-item. Log `check deferred to <NNN>: <check>` in the original item, and add the check to the follow-up's define.md (or to its Intent, if it isn't defined yet).
- Any other pending check keeps the item open.

## Context

- **Stale item:** `proposed`, with no log line in the last 30 days *(provisional)*.
- **Stale project.md:** last refreshed more than 30 days ago *(provisional)*, or the current work found it wrong.
- **Use an Explore subagent:** the survey would take more than ~10 file reads *(provisional)*, or the code is spread across areas you can't locate up front.

## Testing

- **Scenario budget** ([testing.md](testing.md#skill-scenarios)): about **$1** for a smoke run (one scenario) and **$10** for a full run (every scenario) *(provisional)*.

## Complete coverage

Every review, audit, verification or research sweep:
1. **Builds a scope manifest first:** every file, AC or item in scope (`scripts/manifest.py list` for files).
2. **Accounts for every entry** before reporting: covered, or excluded with a stated reason.
3. **Reports coverage** as `<covered>/<total>`.

Anything less is **incomplete**, and is reported as incomplete, never as done or passed. An empty scope is reported as such, never as complete. Large scopes are split into chunks of about **40 files** per finder *(provisional)* and run in waves, never sampled or truncated. A missing entry gets at most **two re-runs** before the result is incomplete. `n/a` counts as covered only with a real reason (deleted, binary or generated, or the dimension doesn't apply, and why); "not reached" or "not read" means not covered.

## Agents and parallelism

The roster of agents, with each one's role, model, effort and tools, is in [agents.md](agents.md). Skills spawn only agents from the roster. The only model a skill ever passes is the upgrade below; otherwise the agent's frontmatter decides.

- **Model policy:** a custom agent's frontmatter sets its default model and effort. When a skill spawns an agent for an **L item** or an item that touches a **[risk area](#building-blocks)**, it passes `model: opus` for that run (a no-op for agents whose default is already opus). Built-in agents (Explore, Plan) keep their own defaults.
- **Parallel cap:** at most **4** agents running at once per skill *(provisional)*.
- **Fan out** only when all of these hold. Otherwise, work in sequence.
  - the pieces of work are independent: no shared files to edit, no ordering between them, and no shared build output, caches, ports or databases
  - none needs the user's input
  - the main session merges the results
- **Review scaling** (finders per review, *provisional*). A risk area takes precedence over size. Without an item (a PR, range or working tree), use M, or L if the diff touches a risk area.
  - S: one finder covering every dimension
  - M: three finders: correctness + tests; design and consistency + compatibility and docs; security + performance and reliability
  - L or a risk area: one finder per dimension, in waves up to the cap
- **Nit cap:** at most **5** [nits](review-rubric.md#severity) per review *(provisional)*; drop the rest.
- **Always sequential:** deliver's tasks (one commit per task, in dependency order) and every gate.
- **Outward actions:** subagents never act outward (push, merge, unlisted MCP tools); the [guard](agents.md#safety-subagents-cant-act-outward) enforces it. Commits are made by the main session.

## Calibration

The provisional numbers above are guesses until they're tested against sustained use. Calibrate them using completed items as evidence, not intuition.

**When:** after 10 items have reached `done` since the last calibration *(provisional)*, or whenever the same re-size trigger has fired 3 times. Skills that see either condition suggest calibrating; they don't calibrate on their own.

**Evidence** (from `workspace/projects/*/items/` and `workspace/archive/`):
- Starting size vs. final size, and the `re-sized` log lines with their triggers
- Actual task count in `deliver.md` against the ~6-task L threshold
- Files and lines changed per task and per item (from deliver's `task <n> committed` log lines)
- Decisions the user overrode or questions they found unnecessary (from the `develop.md` decisions and the item logs)
- Explore subagent use, and project.md refreshes that turned out to be needed or not
- Split proposals: how often a split was proposed, and how often you kept the work whole
- Agent runs per skill, the model used, and, for agents whose default isn't opus, whether upgraded runs found more (review findings, failed verifications) than default runs

**How:** run `/hq tidy`, which calibrates and consolidates in one pass. It proposes each change to a number, citing the items that support it, and lets the user approve. Record approved changes below. Definitions without a number can be recalibrated the same way when the evidence shows they misclassify work.

### Calibration history

| Date | Change | Evidence |
|---|---|---|
| 2026-10-23 | Initial values set | None yet: starting guesses |
| 2026-10-24 | L condition narrowed: ≥2 modules counts only with a shared contract between them; uniform mechanical edits and docs-only changes don't count | 011 (a mechanical rename) sized L while other multi-folder items were M; "module" was undefined (Tidy 024) |
| 2026-10-24 | Every provisional number kept | 15 items, all single-repo, one day, no splits or re-sizes: too little spread to move any number (Tidy 024) |
| 2026-10-24 | Deliver logs files and lines changed per task | No item recorded them, so the S file cap and the ~300-line task size couldn't be checked (Tidy 024) |
| 2026-10-24 | Nit cap (5) moved here from the review rubric | Calibration only sees numbers in this file (Tidy 024) |
| 2026-10-24 | L condition: skills and agents are code, not docs-only; scenario budget added | Tidy 024's open review point, decided in 019; budget from 004's discover (019) |
