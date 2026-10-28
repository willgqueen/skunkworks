# Getting started

One piece of work, from opening a session to merged code. For specific questions, see [how-to.md](how-to.md).

## 1. Open a session

```sh
cd ~/repos/skunkworks && claude
```

On a fresh clone, create the workspace first ([README](../README.md#setup)). Repos next to this one (in `~/repos`) are reachable; for one elsewhere, run `/add-dir <path>`.

## 2. See where things stand

`/hq` shows every open item, its next action, and whether it waits on **you** or **claude**. Nothing starts until you say what to advance.

## 3. Map a repo

`/repo-context my-api` reads `~/repos/my-api` without changing it and writes `workspace/projects/my-api/project.md` (and an architecture overview), which every later step reads.

## 4. Start the work

`/hq Add rate limiting to the public endpoints` creates a numbered item with a [kind](criteria.md#kind) and [size](criteria.md#size), and asks before starting its first phase. Say yes, and hq runs the [phases](process.md) in order: discover (the problem and open questions), define (the spec), develop (the design), deliver. It stops at each gate for your approval and carries on after it. Smaller items skip phases.

## 5. Deliver

Deliver shows one plan and asks for **one approval** for its commits, push, PR and review. It builds in a worktree (`workspace/worktrees/my-api/<branch>`), so your checkout is untouched, verifies every acceptance criterion, opens the PR and reviews it. You merge (unless the [merge rule](criteria.md#merge-rule) lets Claude), then run `/hq my-api 001` to close it. If something fails, the item is marked **blocked** with the cause and nothing is pushed past it.

## 6. Pick up later

Everything lives in files. In a new session, `/hq` shows where each item stands, and `/hq my-api 001` resumes it.

Next: [how-to.md](how-to.md) for everything else, [skills.md](skills.md) for each skill, [process.md](process.md) and [criteria.md](criteria.md) for the rules.
