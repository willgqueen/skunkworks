---
name: discover
description: Run the Discover phase for an L workspace item or an investigation. Map the problem before anything is decided (problem, context, options seen, open questions) in discover.md, then stop for approval and record the user's answers. Use when an L item or investigation is in or entering the discover phase, when the user asks to explore, research or understand a problem before committing to it, or to revise an existing discover.md.
argument-hint: <project> <item id or slug>
---

# discover

Write the item's discovery in `discover.md`, following [docs/process.md](../../../docs/process.md). This phase is divergent: it finds out **what's really going on** and lays out the possibilities. It doesn't decide. Define and Develop decide, using what this phase finds.

Every condition below (sizes, approval, Explore use, re-size) is defined in [docs/criteria.md](../../../docs/criteria.md). Apply those definitions exactly.

## 1. Load the item

- [Resolve the item](../../../docs/process.md#resolve-the-item).
- Read `project.md`, `item.md`, and anything in the item's `notes/` folder.
- Check that the item belongs here:
  - **Any investigation, or any L item** (including initiatives, which are always L): continue.
  - **S or M feature or task**: Discover isn't needed. Say so, and offer to re-size if the user disagrees.
- [Revision](../../../docs/process.md#revision) (log `discover reopened` if approved; redo steps 2–3, then go to step 5). A discover.md that only holds template text isn't drafted, so start at step 2.

## 2. Ground it

For each repo in `repos`, read its `CLAUDE.md`, then the code and docs around the problem (read-only): what exists today, how it behaves, prior attempts, constraints. Use an Explore subagent when [criteria.md](../../../docs/criteria.md#context) says to. When the research is big enough for a subagent ([criteria.md](../../../docs/criteria.md#context)), split it into independent questions (separate code areas, external docs). Give each to a `researcher` or Explore agent with the list of what it must cover. Check each researcher's *Coverage* line and re-run gaps ([complete coverage](../../../docs/criteria.md#complete-coverage)). Run them in parallel when the [fan-out rule](../../../docs/criteria.md#agents-and-parallelism) allows, applying the model policy. Never write into a target repo in this phase.

## 3. Map, don't decide

- **Problem:** what's wrong or missing, and for whom, stated without a solution.
- **Context:** facts that shape the work: relevant code and behavior, constraints (technical, time, dependencies), lessons from earlier items. Note sources.
- **Options seen:** the directions worth considering, each with its main trade-off. List them without choosing. For an investigation, options are the possible answers or lines of inquiry.
- **Open questions:** everything the user needs to answer before Define. Phrase each so it can be answered directly, and number them.

Anything that looks like a decision goes under *Options seen* or *Open questions*, never into the doc as settled. Don't invent requirements.

Run the **split** skill with what Discover found.

Work that turns up and is outside this item becomes a new item through the **new-item** skill. Mention it in the report; it doesn't become extra scope here.

[Size check](../../../docs/process.md#size-check) for Discover.

## 4. Write discover.md

Start from [the template](../../../templates/workspace/discover.md) if the file doesn't exist, and fill the four sections from step 3.

## 5. Update the item

[Update the item](../../../docs/process.md#update-the-item) with phase `discover` (log `discover drafted` or `discover revised`).

## 6. Gate

Report the path to discover.md, the problem in one or two lines, the options, and the numbered open questions. Ask the user to answer the questions and approve, or to request changes. **Stop here.**

**Whenever the user answers open questions** (all or some, with or without approval, alongside requested changes): write each answer next to its question in discover.md (`<question> → <answer>`) and log `- <date>: discover answers: <short summary>`. Answers never live only in chat.

When the user approves:
- Log `- <date>: discover approved` and set `phase: define`.
- Ask whether to start Define.
