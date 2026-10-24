# Skills

A reference for every skill in [`.claude/skills/`](../.claude/skills/). Each one is invoked as `/<name>`, and Claude also picks one up on its own when a request matches its description. For task-based recipes, see [how-to.md](how-to.md). For the rules skills apply, see [process.md](process.md) and [criteria.md](criteria.md).

Every phase skill follows the same shape: **load → ground → work → write → update item → gate.** It stops at its gate until you approve.

## hq

The front door: shows the board and routes work to the other skills.

| | |
|---|---|
| **Use when** | You want status, what's next, to continue an item, to start new work without naming a skill, to triage the inbox, to see what changed (`ledger`), or to calibrate and tidy (`tidy`) |
| **Arguments** | none (board), `<project> <item>`, `<description of new work>`, `inbox`, `tidy`, or `ledger [range] [project]` |
| **Reads** | `scripts/board.py` and `scripts/ledger.py` output; for `tidy`, archived items and check output |
| **Writes** | Waiver lines and the inbox during triage. Everything else, including `tidy`'s changes, goes through the skills and items it creates |
| **Calls** | new-item, discover, define, develop, deliver |
| **Agents** | researcher and Explore, in parallel, when advancing several items or gathering `tidy` evidence |
| **Gate** | None of its own. It stops at every gate of the skills it runs, and carries on after you approve |

## new-item

Turns a description of work into a numbered item.

| | |
|---|---|
| **Use when** | New work comes up: a feature, bug, idea, question, or an inbox entry to triage |
| **Arguments** | `<project> <description>` |
| **Reads** | `project.md`; criteria.md for kind and size |
| **Writes** | `items/<NNN>-<slug>/item.md` and the starting phase's doc; the parent's log; the inbox |
| **Calls** | repo-context, when the project doesn't exist yet |
| **Gate** | None. It reports the kind, size and starting phase, then asks before starting |
| **Log lines** | `created`; in the parent, `child <NNN> added: <title>` |

## review

Strict, multi-agent code review against the [rubric](review-rubric.md).

| | |
|---|---|
| **Use when** | Deliver calls it before merge; or run it on any PR or diff |
| **Arguments** | none (the working tree), `<PR>`, `<base>..<head> [repo]`, or `<project> <item>` |
| **Reads** | The diff, the item's ACs and decisions, the repo's REVIEW.md and CLAUDE.md |
| **Writes** | For an item: deliver.md *Review* and the verdict log line |
| **Agents** | reviewer finders covering the rubric (scaled by size and risk), then a fresh reviewer refute pass |
| **Log lines** | `review: passed @<sha>` / `review: failed: <n> blocking @<sha>` |

## split

Checks whether work is too big for one item and proposes splitting it at natural seams.

| | |
|---|---|
| **Use when** | Called by new-item, discover, define and develop; or run it yourself on an item or a description |
| **Arguments** | `<project> <item>` or `<description>` |
| **Reads** | Whatever the caller knows: the description, discover.md, the draft spec, or the task list |
| **Writes** | Child or sibling items (through new-item); `kind`, Breakdown and log lines on the original |
| **Gate** | You choose: an initiative with children (default), sibling items, or keep it whole |
| **Log lines** | `split: <choice>`, `re-kinded <old>→initiative: <signal>` |

## integrate

Adds an MCP server or external API the standard way.

| | |
|---|---|
| **Use when** | Connecting a service, MCP server or API |
| **Arguments** | `<service or MCP server> [purpose]` |
| **Calls** | new-item |
| **Writes** | An item; deliver adds config, the allowlist entries and the [registry](integrations.md) row |
| **Agents** | researcher |
| **Gate** | The item's own gates |

## repo-context

Builds or refreshes a project's `project.md` from a target repo, read-only.

| | |
|---|---|
| **Use when** | Starting on a repo, or when project.md is [stale](criteria.md#context) |
| **Arguments** | `<repo folder name or path> [project slug]` |
| **Reads** | The repo's README, CLAUDE.md, manifests, CI, file tree, git info |
| **Writes** | `workspace/projects/<project>/project.md`, keeping *Conventions learned* and *Merge policy* |
| **Agents** | Explore, for large repos |
| **Gate** | None |

## discover

The Discover phase: maps the problem without deciding anything.

| | |
|---|---|
| **Use when** | An L item or any investigation is in Discover |
| **Arguments** | `<project> <item>` |
| **Reads** | `project.md`, `item.md`, the item's `notes/`, and the target code (read-only) |
| **Writes** | `discover.md`: Problem, Context, Options seen, Open questions |
| **Agents** | researcher and Explore, in parallel when the [fan-out rule](criteria.md#agents-and-parallelism) allows |
| **Gate** | You answer the open questions (answers are written inline as `→ <answer>`) and approve |
| **Log lines** | `discover drafted` / `revised` / `reopened`, `discover answers: <summary>`, `discover approved` |

## define

The Define phase: the spec. Says what gets done and how we'll know.

| | |
|---|---|
| **Use when** | An item is in Define (M items start here) |
| **Arguments** | `<project> <item>` |
| **Reads** | `project.md`, `item.md`, `discover.md`, the target code |
| **Writes** | `define.md`: Goal, scope, numbered acceptance criteria, Assumptions; Approach for M items; Breakdown for initiatives |
| **Asks** | Scope-changing [gaps](criteria.md#gaps), up to four at a time |
| **Gate** | Approve the spec. Next: develop (L) or deliver (M, investigations, initiatives) |
| **Log lines** | `define drafted` / `revised` / `reopened`, `define approved` |

## develop

The Develop phase for L items: the design and the task list.

| | |
|---|---|
| **Use when** | An L feature or task has an approved spec |
| **Arguments** | `<project> <item>` |
| **Reads** | Everything above plus `define.md` |
| **Writes** | `develop.md`: Approach, Decisions (each with whether you took the recommendation), ordered Tasks with the ACs they serve, Risks |
| **Asks** | Every [significant decision](criteria.md#decisions), with options and a recommendation |
| **Agents** | researcher and Plan |
| **Gate** | Approve the design. Next: deliver |
| **Log lines** | `develop drafted` / `revised` / `reopened`, `develop approved` |

## deliver

The Deliver phase: builds, verifies, publishes and closes. Resumable.

| | |
|---|---|
| **Use when** | An item is ready (see [readiness](../.claude/skills/deliver/SKILL.md)), or to resume one that's waiting |
| **Arguments** | `<project> <item>` |
| **Reads** | The item's phase docs, `project.md`, the target repo |
| **Writes** | Code in a worktree at `workspace/worktrees/<repo>/<branch>`; commits (for skunkworks, also CHANGELOG.md); a PR; `deliver.md` (Plan, Tasks, Verification, Review, CI, Outcome); then archives the item |
| **Agents** | implementer (one per task, in sequence), verifier (in parallel groups); review through `/review` |
| **Gate** | One approval for the whole item, covering its outward actions. Merging follows the [merge rule](criteria.md#merge-rule) |
| **Log lines** | `deliver authorized`, `task <n> committed <sha>`, `blocked` / `unblocked`, `check deferred to <NNN>`, `PR opened`, `review`, `merged`, `done` |

The full log vocabulary is in [workspace.md](workspace.md#log-vocabulary).
