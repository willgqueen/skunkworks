# Workspace

The workspace is the local, gitignored planning area at `workspace/`. Every skill that records context, decisions or plans reads and writes here, and only here.

## The containment rule

**Nothing from the workspace is ever written into another repo**, including its commit messages, PR text and branch names; item slugs and plain descriptions of the work are fine ([sensitive content](criteria.md#building-blocks)). When working on `~/repos/foo`, skills read foo's code and may change foo's code, but specs, plans, notes, findings and logs go to `workspace/projects/foo/`. Target repos only receive the deliverable itself: code, tests, and the docs that belong to that codebase.

Claude Code always runs from the skunkworks root, so skills refer to the workspace by the relative path `workspace/`. Target repos are reached as additional directories.

## Layout

```
workspace/
  inbox.md                    # raw ideas, not yet triaged
  projects/
    <project>/                # one per repo or idea; slug matches the repo folder name
      project.md              # what it is, repo path(s), stack, learned conventions
      architecture/
        overview.md           # what it is, C4 context and containers, top quality attributes
        decisions.md          # index of significant decisions, by item id
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

Every unit of work is an **item**, with the same folder shape whatever its size. Its `kind` (`initiative`, `feature`, `task` or `investigation`, in place of epic, feature, ticket and spike) is set by [criteria.md](criteria.md#kind). Nesting is done with the `parent` field, not nested folders, so items stay flat and easy to find.

The `item.md` frontmatter is defined by [templates/workspace/item.md](../templates/workspace/item.md).

## Phase docs

Each phase writes one file, and the next phase reads it. [templates.md](templates.md) lists what each holds; [process.md](process.md) says what each phase does.

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
