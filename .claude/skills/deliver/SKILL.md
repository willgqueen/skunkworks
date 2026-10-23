---
name: deliver
description: Run the Deliver phase for a workspace item. With one approval for the item, build its tasks in an isolated worktree of the target repo (one implementer subagent and one commit per task), verify every acceptance criterion, push, open a PR, review, merge when the merge rule allows, and close and archive the item. Investigations end with findings; initiatives close when their children are done. Resumable. Use when an item is ready for delivery, when the user asks to build, implement, ship or finish an item, or to resume one that is waiting.
argument-hint: <project> <item id or slug>
---

# deliver

Carry the item to its [definition of done](../../../docs/criteria.md#definitions-of-done), following [docs/process.md](../../../docs/process.md). `deliver.md` holds the state: every stage records its result there and in item.md's log, so running `/deliver` again picks up where the last run stopped.

Every condition below (readiness, definitions of done, merge rule, deferral, sensitive content, tasks, re-size) is defined in [docs/criteria.md](../../../docs/criteria.md). Apply those definitions exactly.

The target repo receives only code, tests and docs that belong to it. Nothing from the workspace goes into commits, PRs, branches or code.

## 1. Load and check readiness

- Resolve the item from `<project> <id or slug>`. If no item is named and exactly one item in the conversation's project has `status: active`, use it; otherwise list the candidates and ask.
- Read `project.md`, `item.md`, `define.md`, `develop.md` and `deliver.md`, where they exist.
- **Ready** means:
  - S: always
  - investigation and initiative, at any size: define [approved](../../../docs/criteria.md#phase-state)
  - M feature or task: define approved
  - L feature or task: develop approved

  If the item isn't ready, say what's missing and stop.
- **Resume:** if item.md's log has a `deliver authorized` line, find the first stage that isn't finished, using deliver.md and the log. Say where you're resuming and go there. Actions outside the authorized list still need a new approval.
- **Blocked:** if `status: blocked`, check that the logged cause is resolved before resuming. If it is, set `status: active` and log `- <date>: unblocked: <how>`. If it isn't, report it and stop.

Refer to acceptance criteria as **AC1, AC2, …**, numbered by their order in define.md.

## 2. Plan and approve

Investigations go to [step 8](#8-investigations), and initiatives to [step 9](#9-initiatives), after the approval in point 5. They skip the repo checks in points 1–2. A code item whose project has no repo can't be delivered: say so and stop.

1. **Context:** the item's kind, plus the repo setup:
   - remote: `git -C <repo> remote`
   - CI: `.github/workflows/` or other CI config

   Together these pick the definition of done.
2. **Prerequisites:** for a GitHub remote, run `gh auth status`. If it fails, say so and stop before planning, since pushing will need it.
3. **Fill deliver.md** from [the template](../../../templates/workspace/deliver.md):
   - **Plan:** the definition of done, worktree, branch and authorized actions.
   - **Tasks:** copied from develop.md (L), from define.md's approach (M), or one task from the Intent (S).
   - **Branch:** follow the repo's convention if its CLAUDE.md or CONTRIBUTING states one; otherwise `<type>/<slug>` (`feat` for features; `fix`, `chore` or `refactor` for tasks).
4. **Show the plan:** definition of done, worktree path, branch, tasks, and every outward action: commits, push, PR, review, and merge, saying whether the [merge rule](../../../docs/criteria.md#merge-rule) can allow deliver to merge or whether the user will.
5. **Ask for one approval for the whole item.** When given, log `- <date>: deliver authorized: <actions>` and set `status: active`, `phase: deliver` and `updated`. Don't ask again per commit.

## 3. Create the worktree

- Record `git -C <repo> status --porcelain` for the user's checkout in the Plan, as the *checkout baseline*, so resumed runs can compare against it too. Record it only once, on the first run.
- If there's a remote, `git -C <repo> fetch`. The base is the latest default branch (`origin/<default>` when there's a remote).
- Create the worktree, depending on what already exists:
  - **Neither exists:** `git -C <repo> worktree add <sandbox>/workspace/worktrees/<repo>/<branch> -b <branch> <base>`, then record the base sha in the Plan.
  - **Worktree exists** (an earlier run): reuse it.
  - **Branch exists without its worktree:** `git -C <repo> worktree add <path> <branch>`.

  In the last two cases, keep the base sha already in the Plan.

## 4. Build, one task at a time

For each unchecked task, in order:
1. **Implement:** start the `implementer` agent with:
   - the worktree path
   - the task and the ACs it serves
   - the check commands from project.md
   - the relevant approach and decisions
2. **Review the result:** read its report and `git -C <worktree> diff`. Confirm the change:
   - stays within the task and matches the approach
   - contains no workspace or [sensitive](../../../docs/criteria.md#building-blocks) content
   - leaves the user's checkout as it was (compare against the checkout baseline in the Plan)
3. **Check:** run the checks yourself in the worktree, and report the results faithfully. If they fail, send the failure output back to the implementer **once**. If they still fail, stop (see below).
4. **Commit:** one commit for the task, with the message following [templates/repo/commit.md](../../../templates/repo/commit.md) (repo conventions override it).
5. **Record:** tick the task in deliver.md with its sha, add a progress note, and log `- <date>: task <n> committed <sha>`.

**Stop the run** if a check is still failing, there's an unexpected blocker, the implementer reports the task can't be done as described, or a [re-size trigger](../../../docs/criteria.md#size) appears:
- set `status: blocked` and log `- <date>: blocked: <cause>` (for a re-size, recommend it and log it only when the user agrees)
- report the cause
- push nothing

## 5. Verify

For each AC, run its check and record the result in deliver.md's *Verification*:
- `verified: <how>`
- `pending: <why>`
- `deferred to <NNN>: <why it can't run here>`, only when the [deferral rule](../../../docs/criteria.md#deferring-a-check) allows it. Log the deferral in both items and add the check to the follow-up item.

A pending check that isn't deferred keeps the item open. Report it and stop; the next run resumes here.

## 6. Publish and review

- **Remote:**
  - push: `git -C <worktree> push -u origin <branch>`
  - open the PR with `gh pr create`, writing the body to a file first, following [templates/repo/pull-request.md](../../../templates/repo/pull-request.md) (a repo PR template overrides it)
  - log `- <date>: PR opened <url>`
- **Local only:** no push or PR. The review covers the branch diff.
- **Review:** run the **review** skill on the PR or the branch diff.
  - If the review skill doesn't exist, record review as pending in *Review*, never skipped. It can be deferred only under the deferral rule.
  - Fix findings as extra tasks through step 4, or record the user's explicit acceptance.
  - After fix commits, push again (remote), then re-run the review on the new changes and wait for CI again. Only the results for the final pushed head count.
  - Log `- <date>: review: <result>`.
- **CI:** if the repo has CI, wait for the PR's checks (for example, `gh pr checks <pr> --watch`, in the background) and record them in *CI*. A failing required check stops the run, as in step 4.

## 7. Merge and close

**Merge:** if the merge rule allows it, merge:
- **Remote:** use the repo's preferred method if it states one; otherwise a merge commit, which keeps the per-task commits.
- **Local only:** merge into the default branch in the user's checkout. Do this only if that checkout is on the default branch and clean; otherwise ask.

Log `- <date>: merged <sha>`.

If the merge rule doesn't allow it, report that the PR (or branch) is ready for the user to merge, and stop. The next run checks whether it was merged (`gh pr view <pr> --json state`, or `git -C <repo> branch --merged <default>`).

**Close**, once the definition of done is met:
1. Remove the worktree: `git -C <repo> worktree remove <path>`. Delete the local branch with `git -C <repo> branch -d <branch>`, which only works once it's merged.
2. Complete the *Outcome*. For code items, add the PR link and the merge sha. For investigations, keep the findings already written there. For initiatives, summarize the children and their outcomes.
3. Set `status: done`, log `- <date>: done`, and move the item folder to `workspace/archive/<project>/`.
4. If the item has a parent, log `- <date>: child <NNN> done` in the parent.
5. Offer additions to project.md's *Conventions learned* from what this item taught.

## 8. Investigations

No worktree, branch or PR. Research with read-only reads and commands. A scratch worktree is allowed for experiments; it's never committed, and it's removed afterwards.
- In *Outcome*, answer each of define.md's questions with evidence that meets its standard, then give a recommendation.
- Verify against define.md (step 5), and offer to create the recommended follow-up items with **new-item**.
- Close as in step 7, without the merge.

## 9. Initiatives

- Find the children: items whose `parent` is this id, in `items/` and `archive/`.
- If any are neither done nor dropped, list them with their phase and status, and stop.
- Otherwise, verify the initiative's own ACs (step 5) and close as in step 7, without the worktree or merge.

## Report

At every stop, give the item path, the stage reached, what was done (commits, PR, review, CI), the AC verification summary, and what happens next: who acts, and what running `/deliver` again will do.
