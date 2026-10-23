---
name: new-item
description: Create a new work item (initiative, feature, task or investigation) in the workspace, choose its kind and size, and set up its starting phase doc. Use when the user describes new work to do, a bug, an idea to pursue, a question to investigate, or asks to triage something from the inbox.
argument-hint: <project> <description of the work>
---

# new-item

Turn a description of work into a numbered item under `workspace/projects/<project>/items/`, following [docs/workspace.md](../../../docs/workspace.md) and [docs/process.md](../../../docs/process.md). This skill only sets up the item. It does not start phase work.

## 1. Resolve the project

- Use the project the user names. If none is named, infer it from the conversation; if that's ambiguous, list the projects in `workspace/projects/` and ask.
- If the project doesn't exist yet:
  - If a matching repo exists (`~/repos/<project>` or a path the user gave), run the **repo-context** skill first.
  - If it's an idea with no repo yet, create `workspace/projects/<project>/items/` and a `project.md` from the template, with *Repos* set to "none yet".
- Read `project.md` before going on.

## 2. Classify

Apply the rules in [docs/criteria.md](../../../docs/criteria.md) exactly. Don't restate or loosen them here.

- **Kind:** [criteria.md#kind](../../../docs/criteria.md#kind). For an initiative, create only the initiative, and list candidate children in its Intent.
- **Size:** [criteria.md#size](../../../docs/criteria.md#size). Check the L conditions first, then S. In the report, name the condition that decided the size. If the description is [too thin to size](../../../docs/criteria.md#size), ask one question.

**Starting phase**

| Item | Starts in |
|---|---|
| S | deliver |
| M | define |
| L, investigation | discover |

## 3. Create

1. **ID:** the highest `NNN` across `workspace/projects/<project>/items/` and `workspace/archive/<project>/`, plus one, zero-padded to three digits. Start at `001`.
2. **Slug:** kebab-case, at most five words, taken from the title.
3. **Title:** short and imperative ("Add retry to webhook sender").
4. Create `items/<NNN>-<slug>/` with:
   - `item.md` from [the template](../../../templates/workspace/item.md). Fill all fields. Use `status: proposed`, today's date, and in `repos` the repo folders this will touch (usually all of the project's repos, if it has only one). Write a one- or two-sentence *Intent* that captures what the user asked for and why. Don't invent requirements.
   - The starting phase's doc from its template, with the title filled in and any details the user already gave placed in the right sections. Leave the rest as template prompts.
5. If the user named a parent initiative, set `parent` and add a log line to the parent's `item.md`: `- <date>: child <NNN> <title> added`.
6. If the item came from `workspace/inbox.md`, remove that line from the inbox.

## 4. Report

Give the item path, kind, size and starting phase, and the criteria condition that decided the size. Then ask whether to start the first phase. Don't start it unprompted.

If [calibration is due](../../../docs/criteria.md#calibration) (10 items `done` since the last date in the calibration history, or the same re-size trigger logged 3 times), say so in one line.
