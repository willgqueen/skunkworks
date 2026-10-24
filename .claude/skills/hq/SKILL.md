---
name: hq
description: The front door to all work. With no arguments, show the board of every open item, its next action and who it's waiting on. Given an item, run its next phase and carry on after each approved gate. Given a description of new work, create the item and start it. Also triages the inbox, records gate waivers the user gives explicitly, and runs the combined calibration and tidy pass. Use when the user asks what's next, for status, to continue or advance work, to start something new without naming a skill, to triage the inbox, what changed recently, or to calibrate or tidy.
argument-hint: "[<project> <item> | <description of new work> | inbox | tidy | ledger [range] [project]]"
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

## `ledger`: what changed

Run `python3 -I scripts/ledger.py` with `--since`, `--until` and `--project` as asked, and show the output as is.

## `tidy`: calibrate and consolidate

Run when the board says calibration is due, or on request. One pass covers [calibration](../../../docs/criteria.md#calibration) and consolidation.

1. **Gather evidence.** Run `python3 -I scripts/test.py` and the board yourself, then give each area to a `researcher` agent in parallel (within the cap), with that output and the archived items, review findings and item logs:
   - **calibration:** each *(provisional)* number in criteria.md against what completed items show
   - **toolkit:** contradicting or restated rules, overlapping skills or docs, unused templates or agents, verbosity
   - **backlog and hygiene:** overlapping, [stale](../../../docs/criteria.md#context) or mis-sized items; leftover worktrees; items stuck waiting
2. **Propose** with **new-item**: one task item, `Tidy <date>`, listing each change (adjust, merge, prune, restructure, expand) with its evidence in its define.md.
3. Ask the user to approve or reject each change. The Tidy item itself delivers the approved threshold changes (editing criteria.md and its calibration history). Every other approved change becomes its own item through new-item. The Tidy item closes when each proposal is applied, itemized or rejected.

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
