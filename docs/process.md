# Process

The working method: a **Double Diamond outer frame** with a **spec-driven file per phase**, scaled by size so small work skips the heavy steps.

## Phases

| Phase | Diamond | Mode | Question | Output |
|---|---|---|---|---|
| Discover | 1 | Diverge | What's really going on? | `discover.md` |
| Define | 1 | Converge | What exactly will we solve, and how will we know? | `define.md` |
| Develop | 2 | Diverge, then converge | How should we build it? | `develop.md` |
| Deliver | 2 | Converge | Build it, verify it, ship it | `deliver.md` + code |

Each phase ends at a **gate**: the user approves the phase doc before the next phase starts. A gate can be waived explicitly ("skip to deliver").

## Sizing

Every item is sized when it's created, using the rules in [criteria.md](criteria.md#size). The size picks the path:

| Size | Typical work | Phases |
|---|---|---|
| S | Typo, small bug fix, config tweak | Deliver (a one-line intent in `item.md`) |
| M | Clear feature or bug with a known approach | Define → Deliver (light Develop inside `define.md`) |
| L | Ambiguous, cross-cutting or risky work | Discover → Define → Develop → Deliver |

An `initiative` runs Discover → Define (its breakdown into child items) → Deliver, where it closes once its children are done. Its children carry their own design.

An `investigation` runs Discover → Define (the question and what would answer it), then ends with findings in `deliver.md` and no code.

When work turns out bigger than its size, re-size it and back up to the missing phase rather than pushing on. When it's too big for one item, new-item, discover, define and develop propose a split ([split](skills.md#split), [criteria.md](criteria.md#splitting)).

## Next action

Every open item's next step follows from its `item.md`: the frontmatter, plus the latest [log line](workspace.md#log-vocabulary) for its current phase. [`scripts/board.py`](../scripts/board.py) implements this table, and `/hq` uses it.

| State | Next action | Waiting on |
|---|---|---|
| `status: blocked` | Resolve the logged cause, then resume | you |
| `status: done` or `dropped` | None (not shown on the board) | |
| Current phase not drafted yet | Run that phase's skill | claude |
| Latest line for the phase is `reopened` | Revise the phase doc | claude |
| Latest line is `drafted` or `revised` | Answer and approve the gate | you |
| Latest line is `approved` or `waived` | Run the next phase for the item's size and kind (see [Sizing](#sizing)) | claude |
| Phase deliver, latest deliver line is `waiting on you: …` | What that line says | you |
| Phase deliver, latest deliver line is `waiting on items: …` | Wait for those items | items |
| Phase deliver, no `deliver authorized` | Run deliver: plan, then one approval | claude |
| Phase deliver, latest deliver line is `review: incomplete …` | Finish the review | claude |
| Phase deliver, latest deliver line is `review: failed: …` | Fix the findings (resume deliver), or accept them | you |
| Phase deliver, latest deliver line is `review: passed …` | Merge, or resume deliver | you |
| Phase deliver, otherwise | Resume deliver | claude |

Two overrides: an item whose `depends_on` items aren't done or dropped waits on **items**, and an initiative's row adds `children: <done>/<total>`. The board orders items blocked → waiting on you → active → proposed, with children nested under their initiative.

## Phase skill steps

Steps shared by `/discover`, `/define` and `/develop` (`/deliver` uses *Resolve the item*); each skill links here and names its own steps. `<phase>` is the skill's phase.

### Resolve the item

Resolve the item from `<project> <id or slug>`. If no item is named and exactly one item in the conversation's project has `status: active`, use it; otherwise list the candidates and ask.

### Revision

If `<phase>` is already [drafted](criteria.md#phase-state), this is a [revision](criteria.md#phase-state): if it was approved, log `<phase> reopened` first. Apply the user's feedback to the existing doc instead of rewriting it, redoing the skill's grounding and drafting steps only where the feedback needs it, then go to the skill's update-the-item step.

### Size check

If the phase's work hits a [re-size trigger](criteria.md#size), recommend re-sizing in your report and name the condition. Don't change the size without the user's agreement; when they agree, log it in the format criteria.md gives.

### Update the item

In `item.md`, set `phase: <phase>`, `status: active` and `updated`, then add a log line: `- <date>: <phase> drafted` (or `<phase> revised`).

## Why this combination

- Double Diamond keeps problem exploration apart from solution work, which matters most for ambiguous items.
- A file per phase gives agents a stable handoff: each phase reads the previous file instead of relying on chat history.
- Sizing keeps the process from slowing down routine work.

Other methods considered: Shape Up (its *appetite* idea may be borrowed later as an effort budget per item), and RFC/ADR-only flows (ADRs are kept inside `develop.md`, and each project indexes its significant decisions in `architecture/decisions.md`).

## Building blocks

The toolkit is built bottom-up:

1. **Foundation**: project `.claude/` setup, workspace, templates, this process. *(done)*
2. **Atomic skills**: one job each, e.g. understand a repo, write a spec, plan, implement a task, test, review, open a PR.
3. **Phase commands**: chain atomic skills for one phase and stop at its gate.
4. **Orchestrator**: `/hq`, one entry point that shows the board, creates or resumes an item, and routes it through its phases.
