---
name: define
description: Run the Define phase for a workspace item. Turn its intent (and discover.md, if any) into a spec in define.md with goal, scope, acceptance criteria and assumptions, then stop for approval. Use when an item is in or entering the define phase, when the user asks to spec, scope or define a piece of work, or to revise an existing define.md.
argument-hint: <project> <item id or slug>
---

# define

Write the item's spec in `define.md`, following [docs/process.md](../../../docs/process.md). This phase decides **what** is done and **how we'll know it's done**. Deliver verifies its acceptance criteria one by one, so they must be checkable.

Every condition below (sizes, gaps, approval) is defined in [docs/criteria.md](../../../docs/criteria.md). Apply those definitions exactly.

## 1. Load the item

- [Resolve the item](../../../docs/process.md#resolve-the-item).
- Read `project.md`, `item.md`, and `discover.md` if it exists.
- Check that the item belongs here:
  - **S**: define isn't needed. Say so, and offer to re-size if the user disagrees.
  - **L with no [approved](../../../docs/criteria.md#phase-state) discover.md**: point out that Discover was skipped and ask whether to continue anyway.
- If define is already drafted, it's a [revision](../../../docs/process.md#revision) (log `define reopened` if it was approved; grounding and drafting are steps 2–3, update the item is step 5).

## 2. Ground it in the code

For items with repos, read the code the work will touch (read-only): the current behavior, its entry points, the existing tests, and nearby patterns. Use an Explore subagent when [criteria.md](../../../docs/criteria.md#context) says to. The goal is a spec that matches how the system actually works, not a design. Implementation choices belong in develop, or in the M approach section.

## 3. Close the gaps

List what's ambiguous, then sort it:
- **[Scope-changing gap](../../../docs/criteria.md#gaps):** ask the user. Ask all of these at once (at most four questions), each with concrete options and a recommended one.
- **[Minor gap](../../../docs/criteria.md#gaps):** take the default and record it under *Assumptions*.

Never invent requirements the user didn't ask for. If something would be nice to have, put it under *Out of scope*, or mention it in your report.

## 4. Write define.md

Start from [the template](../../../templates/workspace/define.md) if the file doesn't exist.

- **Goal:** the outcome in one or two sentences, from the user's point of view.
- **In / Out of scope:** concrete bullets. *Out of scope* is where tempting adjacent work goes, so later phases don't pick it up.
- **Acceptance criteria:** observable behavior, each one a [checkable criterion](../../../docs/criteria.md#work-units). Cover the main path, the important error and edge cases, and "existing behavior X is unchanged" where there's regression risk. Avoid vague words like "fast", "clean" or "robust" unless they come with a measure.
- **Assumptions:** see step 3.
- **Approach (M only):** a few bullets on which files or modules change and how, plus the test strategy. Leave this section out for L items.

By kind:
- **investigation:** the goal is the question. *Acceptance criteria* list the sub-questions that must be answered and the evidence that counts (benchmarks, code references, docs). *Approach* is how to find out.
- **initiative:** after the criteria, add a `## Breakdown` section listing the child items, each with a working title, kind, size and one line of scope. Children are created at the gate, not now.

Run the **split** skill on the draft spec.

**Size check:** if the spec hits a re-size trigger, follow [Size check](../../../docs/process.md#size-check).

## 5. Update the item

[Update the item](../../../docs/process.md#update-the-item) with phase `define` (log `define drafted` or `define revised`).

## 6. Gate

Report the path to define.md, the goal, how many acceptance criteria there are, the main scope decisions, and every assumption. Ask the user to approve the spec or request changes. **Stop here.**

When the user approves:
- Add the log line `- <date>: define approved` and set `phase` to the next phase: **develop** for L features and tasks, **deliver** for M items, investigations and initiatives.
- **initiative:** offer to create each Breakdown child that doesn't have an id yet with the **new-item** skill, setting this item as its `parent`.
- Ask whether to start the next phase.
