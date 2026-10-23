---
name: hq
description: The front door to all work. With no arguments, show the board of every open item, its next action and who it's waiting on. Given an item, run its next phase and carry on after each approved gate. Given a description of new work, create the item and start it. Also triages the inbox and records gate waivers the user gives explicitly. Use when the user asks what's next, for status, to continue or advance work, to start something new without naming a skill, or to triage the inbox.
argument-hint: "[<project> <item> | <description of new work> | inbox]"
---

# hq

Route work through the phase skills and keep the user oriented. hq decides **which skill runs next**; the phase skills do the work. It never duplicates their steps, and never gets past a gate without the user.

The routing is the *Next action* table in [docs/process.md](../../../docs/process.md#next-action), as implemented by [`scripts/board.py`](../../../scripts/board.py). Every condition (approval, waivers, parallel work) is defined in [docs/criteria.md](../../../docs/criteria.md). Apply them exactly.

## No arguments: the board

1. Run `python3 -I scripts/board.py` and show its output as is.
2. Below it, point out first what's **waiting on the user** (gates to answer, blocks, merges), then the item hq would advance next: the first item waiting on `claude`, in board order.
3. Ask what to advance. Don't start anything unprompted.

## An item: run it and carry on

1. Run `python3 -I scripts/board.py --item <project>/<id or slug>` to get its next action.
2. Act on it:
   - **Run `/<phase>`, revise, or resume `/deliver`:** invoke that skill with the Skill tool, passing `<project> <id>`.
   - **Waiting on the user:** say exactly what's needed (the open gate, the block's cause, the merge) and stop.
3. **Carry on:** when the user approves at a gate, after the phase skill has logged the approval, run step 1 again for the same item and continue. Stop when the item is done, when the board says it's waiting on `you` or `items`, or when the skill's own report says the next step isn't Claude's, even if the board disagrees. Report which phase is next before starting it.

## A description: new work

Run the **new-item** skill with the description, choosing the project as new-item does. When the user confirms the first phase, continue as for an item.

## `inbox`: triage

For each entry in `workspace/inbox.md`, in order, ask the user: **create** an item (through new-item, which removes the entry), **keep** it, or **drop** it (remove the entry). Batch up to four entries per question. End by showing the board.

## Waivers

Record a waiver only when the user explicitly asks to skip a gate ("skip to deliver", "waive develop"). For each phase being skipped, log `- <date>: <phase> waived: <the user's reason, or "user request">` in item.md, set `phase` to the next phase that isn't waived, and say which phases were waived.

Deliver's per-item authorization of outward actions can never be [waived](../../../docs/criteria.md#phase-state). If asked, say so and run deliver's normal approval.

## Several items at once

When the user asks to advance several items, gather context for the ones waiting on `claude` in parallel:
- give each item's research to `researcher` or Explore agents in the background, within the [parallel cap and fan-out rule](../../../docs/criteria.md#agents-and-parallelism), applying the model policy
- then run each item's phase skill in the main session, one at a time, passing along what the research found

Drafting phase docs and every gate stay in the main session, because the phase skills ask the user questions along the way.

## Never

- Take an outward action (commit, push, PR, merge) except through deliver and its per-item approval.
- Change an item's state except through the phase skills, new-item, or a waiver the user gave.
- Restate a rule from process.md or criteria.md. Link to it.
