# Workspace

The workspace is the local, gitignored planning area at `workspace/`. Every skill that records context, decisions or plans reads and writes here, and only here.

## The containment rule

**Nothing from the workspace is ever written into another repo.** When working on `~/repos/foo`, skills read foo's code and may change foo's code, but specs, plans, notes, findings and logs go to `workspace/projects/foo/`. Target repos only receive the deliverable itself: code, tests, and the docs that belong to that codebase.

Claude Code always runs from the skunkworks root, so skills refer to the workspace by the relative path `workspace/`. Target repos are reached as additional directories.

## Layout

```
workspace/
  inbox.md                    # raw ideas, not yet triaged
  projects/
    <project>/                # one per repo or idea; slug matches the repo folder name
      project.md              # what it is, repo path(s), stack, learned conventions
      items/
        <NNN>-<slug>/         # one unit of work, numbered per project
          item.md             # metadata, summary, status log
          discover.md         # phase docs: created only when the phase is used
          define.md
          develop.md
          deliver.md
          notes/              # research, scratch, raw material
  archive/
    <project>/<NNN>-<slug>/   # done or dropped items, moved here intact
  reviews/
    <date>-<scope>[-n]/       # one per /review: manifest, chunks, coverage lists, saved diff and PR text; item reviews are removed when the item closes
  worktrees/
    <repo>/<branch>/          # git worktrees deliver creates per item; removed at close
```

A project doesn't need a repo yet. An idea can become a project first and gain a repo later.

## Items

Every unit of work is an **item**, with the same folder shape whatever its size. Its `kind` replaces the corporate epic/feature/ticket/spike split. Kind is the type of work, regardless of size; the exact rules are in [criteria.md](criteria.md#kind).

| Kind | Use for | Usually ends with |
|---|---|---|
| `initiative` | A multi-item effort; groups child items | All children done |
| `feature` | New capability or a meaningful change in behavior | Merged code |
| `task` | No new intended behavior: a bug fix, chore, refactor or dependency bump | Merged code |
| `investigation` | A question to answer before committing to work | Findings and a recommendation |

Nesting is done with the `parent` field, not nested folders, so items stay flat and easy to find.

### `item.md` frontmatter

```yaml
id: "007"
title: Short imperative title
kind: feature          # initiative | feature | task | investigation
status: active         # proposed | active | blocked | done | dropped
phase: define          # discover | define | develop | deliver
size: M                # S | M | L — decides which phases run (see process.md)
parent:                # id of the parent initiative, if any
depends_on: []         # ids that must be done first (keep rare)
repos: []              # repo folder names this item touches
created: 2026-10-21
updated: 2026-10-21
```

## Phase docs

Each phase writes one file, and the next phase reads it. See [process.md](process.md) for what each phase does. Templates live in [templates/workspace/](../templates/workspace/).

| File | Phase | Contains |
|---|---|---|
| `discover.md` | Discover | Problem, context, constraints, open questions, options seen |
| `define.md` | Define | Spec: goal, scope, non-goals, acceptance criteria |
| `develop.md` | Develop | Approach, design decisions (ADR-style), task breakdown |
| `deliver.md` | Deliver | Task checklist, progress log, PR links, outcome |

## Log vocabulary

`item.md`'s log is the item's state history. Skills write these lines (newest last) and read them to resume:

| Line | Written by |
|---|---|
| `created` | new-item |
| `<planning phase> drafted` / `<planning phase> revised` | discover, define, develop |
| `<phase> reopened` | the phase skill, when revising an approved phase |
| `<phase> waived: <reason>` | hq, only when the user explicitly waives a gate |
| `discover answers: <summary>` | discover, whenever the user answers open questions |
| `<phase> approved` | the phase skill, on the user's approval |
| `re-sized <old>→<new>: <condition>` | any skill, on the user's agreement |
| `deliver authorized: <actions>` | deliver |
| `task <n> committed <sha> · <files> files, +<added>/-<deleted>` | deliver |
| `blocked: <cause>` / `unblocked: <how>` | deliver |
| `check deferred to <NNN>: <check>` | deliver, in both items |
| `PR opened <url>` | deliver |
| `review: <verdict>` | review; the [verdict](review-rubric.md#verdict) line |
| `merged <sha>` | deliver |
| `split: <choice>` / `re-kinded <old>→initiative: <signal>` | split |
| `child <NNN> added: <title>` / `child <NNN> done` | new-item, deliver (in the parent) |
| `waiting on you: <what>` / `waiting on items: <ids>` | deliver, at any stop where the next step isn't Claude's |
| `host change approved: <what> at <where> via <how>` | deliver, when the user approves a [host change](criteria.md#building-blocks) |
| `ledger: <note>` | anyone: an optional note for the change ledger |
| `done` | deliver |

Free-form lines are fine for anything else worth recording.
