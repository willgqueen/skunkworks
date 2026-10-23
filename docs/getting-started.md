# Getting started

A walkthrough of one piece of work, from opening a session to merged code. It takes about ten minutes to read. For quick answers to specific questions, see [how-to.md](how-to.md).

## 1. Open a session in the sandbox

```sh
cd ~/repos/sandbox
claude
```

Everything loads from `.claude/`: the skills, the agents, and the hook that stops subagents from pushing or merging. Repos under `~/repos` are reachable from here; for a repo somewhere else, run `/add-dir <path>`.

On a fresh clone, create the workspace first (see the [README](../README.md#setup)).

## 2. See where things stand

```
/hq
```

The board lists every open item: what it is, which phase it's in, its next action, and whether it's waiting on **you** or on **claude**. Items waiting on you come first. Nothing starts until you say what to advance.

## 3. Map a repo you'll work on

```
/repo-context my-api
```

This reads `~/repos/my-api` (without changing it) and writes `workspace/projects/my-api/project.md`: what the repo is, its stack, its exact commands, its layout, and its merge policy (`manual` to start). Every later step reads this file.

## 4. Start a piece of work

Describe it, either to `/hq` or directly to `/new-item`:

```
/hq Add rate limiting to the public endpoints
```

new-item creates `workspace/projects/my-api/items/001-add-rate-limiting/` and decides:
- **Kind:** feature, task, investigation or initiative ([criteria.md](criteria.md#kind))
- **Size:** S, M or L, naming the condition that decided it ([criteria.md](criteria.md#size)). Here it's L, because public endpoints are a risk area.
- **First phase:** S starts in deliver, M in define, and L and investigations in discover.

It asks before starting the first phase.

## 5. Go through the phases

Say yes, and hq runs the phases in order, stopping at every gate:

| Phase | What happens | What you do at the gate |
|---|---|---|
| **Discover** | Claude researches the problem (with parallel research agents when it's big) and writes the problem, context, options and numbered open questions | Answer the questions and approve |
| **Define** | The spec: goal, scope, numbered acceptance criteria, assumptions. Claude asks you about anything that would change the scope | Approve the spec, or ask for changes |
| **Develop** | The design: each significant decision is put to you with options and a recommendation; then an ordered task list covering every acceptance criterion | Approve the design |
| **Deliver** | One plan for the whole item, then you give **one approval** for its commits, push, PR and review | Approve the plan; later, merge if the merge rule says you merge |

After each approval, hq carries straight on into the next phase. Each phase writes its own doc in the item folder, so you can read exactly what was decided, and so can a fresh session.

An M item skips Discover and Develop; an S item goes straight to Deliver.

## 6. Delivery

Deliver works in a git worktree (`workspace/worktrees/my-api/<branch>`), so your own checkout is never touched:
1. An `implementer` agent builds each task; Claude checks it, runs the repo's checks and makes one commit per task.
2. `verifier` agents check the acceptance criteria in parallel.
3. Claude pushes, opens the PR and runs a review.
4. If the [merge rule](criteria.md#merge-rule) allows it, Claude merges. Otherwise it tells you the PR is ready.
5. Once the [definition of done](criteria.md#definitions-of-done) is met, the worktree is removed and the item is archived.

If anything fails, the item is marked **blocked** with the cause, nothing is pushed past the failure, and `/hq` shows it at the top of the board.

## 7. Pick up later

Everything lives in files, so you can stop at any point. In a new session, `/hq` shows where every item stands, and `/hq my-api 001` resumes it from where it stopped.

## Where to go next

- [how-to.md](how-to.md): recipes for everything else (waiving a gate, revising an approved spec, unblocking, the inbox, merge policy, calibration)
- [skills.md](skills.md): each skill in detail
- [process.md](process.md): the method and the routing rules
- [criteria.md](criteria.md): every rule and threshold
