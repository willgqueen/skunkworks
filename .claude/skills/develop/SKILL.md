---
name: develop
description: Run the Develop phase for an L workspace item. Turn its approved spec into develop.md, with the approach, design decisions made together with the user, an ordered task list that covers every acceptance criterion, and the risks. Then stop for approval. Use when an L item is in or entering the develop phase, when the user asks to design, architect or plan the implementation of an item, or to revise an existing develop.md.
argument-hint: <project> <item id or slug>
---

# develop

Write the item's design in `develop.md`, following [docs/process.md](../../../docs/process.md). This phase decides **how** the spec in `define.md` gets built. Deliver works through its task list in order.

Every condition below (sizes, significant vs. minor decisions, tasks, approval, Explore use) is defined in [docs/criteria.md](../../../docs/criteria.md). Apply those definitions exactly.

## 1. Load the item

- Resolve the item from `<project> <id or slug>`. If no item is named and exactly one item in the conversation's project has `status: active`, use it; otherwise list the candidates and ask.
- Read `project.md`, `item.md`, `discover.md` if it exists, and `define.md`.
- Check that the item belongs here:
  - **S or M**: Develop isn't needed. An M item's approach lives in define.md. Say so, offer to re-size if the user disagrees, and don't write develop.md.
  - **investigation**: Develop is skipped. It goes from define to deliver.
  - **L without an [approved](../../../docs/criteria.md#phase-state) define**: say so and ask whether to continue anyway.
- If `develop.md` already has content, this is a **revision**: apply the user's feedback to the existing doc, then go to step 6. If the feedback changes a decision, update the decision's record and every task it affects, so the doc stays consistent.

Refer to acceptance criteria as **AC1, AC2, …**, numbered by their order in define.md.

## 2. Ground it in the code

For each repo in `repos`, read that repo's `CLAUDE.md`, then the code the design will touch (read-only): the current structure, the patterns to follow, the test setup, and the places where the change has to fit in. Use an Explore subagent when [criteria.md](../../../docs/criteria.md#context) says to. Never write into a target repo in this phase.

## 3. Shape the approach

Draft the overall approach, then list every decision it depends on. Classify each one as [significant or minor](../../../docs/criteria.md#decisions); when it's unclear, treat it as significant.

For a broad design, a Plan subagent may draft the options. Its output is input to you, not the decision.

**Spec check:** if the design shows that define.md is wrong or incomplete (an acceptance criterion can't be met as written, something is missing, or the scope is unworkable), stop. Recommend a define revision and say exactly what needs to change. Don't edit define.md, and don't continue designing around the problem.

## 4. Decide with the user

- **Significant decisions:** put each one to the user with 2–3 options. Give each option its trade-offs, put the recommended option first, and mark it *(Recommended)*. Ask independent decisions together, at most four at a time. A decision that depends on an earlier one waits for that answer. Don't write a significant decision into develop.md until the user has chosen.
- **Minor decisions:** decide, following existing repo patterns, and record them. The user can still change them at the gate.

For every decision, record whether the user took the recommendation (`n/a` for minor ones). This feeds [calibration](../../../docs/criteria.md#calibration).

## 5. Write develop.md

Start from [the template](../../../templates/workspace/develop.md) if the file doesn't exist.

- **Approach:** the design as decided: what changes where, and how the pieces fit together.
- **Decisions:** one entry per decision, significant and minor, with its kind, context, options considered, choice, whether the recommendation was taken, and consequences.
- **Tasks:** ordered by dependency. Each one must be a [task](../../../docs/criteria.md#work-units), so split anything larger. Each task lists the ACs it serves. Before finishing, check coverage: every AC must be served by at least one task. If one isn't, add a task or go back to the spec check.
- **Risks:** what could go wrong, each with how it's mitigated or how we'll notice.

**Size check:** if the design hits a [re-size trigger](../../../docs/criteria.md#size), recommend re-sizing in your report and name the condition. Don't change the size without the user's agreement; when they agree, log it in the format criteria.md gives.

## 6. Update the item

In `item.md`, set `phase: develop`, `status: active` and `updated`, then add a log line: `- <date>: develop drafted` (or `develop revised`).

## 7. Gate

Report the path to develop.md, the approach in two or three lines, each decision with its choice, the number of tasks, and the risks. Ask the user to approve the design or request changes. **Stop here.**

When the user approves:
- Add the log line `- <date>: develop approved` and set `phase: deliver`.
- Ask whether to start Deliver.
