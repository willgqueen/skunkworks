# Skills

A reference for every skill in [`.claude/skills/`](../.claude/skills/). Each one is invoked as `/<name>`, and Claude also picks one up on its own when a request matches its description. For task-based recipes, see [how-to.md](how-to.md). For the rules skills apply, see [process.md](process.md) and [criteria.md](criteria.md).

Every phase skill follows the same shape: **load → ground → work → write → update item → gate.** It stops at its gate until you approve.

## hq

The front door: shows the board and routes work to the other skills.

| | |
|---|---|
| **Use when** | You want status, what's next, to continue an item, to start new work without naming a skill, to triage the inbox, to see what changed (`ledger`), or to calibrate and tidy (`tidy`) |
| **Arguments** | none (board), `<project> <item>`, `<description of new work>`, `inbox`, `tidy`, or `ledger [range] [project]` |
| **Calls** | new-item, discover, define, develop, deliver |
| **Agents** | researcher and Explore, in parallel, when advancing several items or gathering `tidy` evidence |
| **Gate** | None of its own. It stops at every gate of the skills it runs, and carries on after you approve |

## new-item

Turns a description of work into a numbered item.

| | |
|---|---|
| **Use when** | New work comes up: a feature, bug, idea, question, or an inbox entry to triage |
| **Arguments** | `<project> <description>` |
| **Calls** | repo-context, when the project doesn't exist yet |
| **Gate** | None. It reports the kind, size and starting phase, then asks before starting |

## review

Strict, multi-agent code review against the [rubric](review-rubric.md).

| | |
|---|---|
| **Use when** | Deliver calls it before merge; or run it on any PR or diff |
| **Arguments** | none (the working tree), `--all [repo]` (whole codebase), `<PR>`, `<base>...<head> [repo]`, or `<project> <item>` |
| **Agents** | reviewer finders covering the rubric (scaled by size and risk), then a fresh reviewer refute pass |

## split

Checks whether work is too big for one item and proposes splitting it at natural seams.

| | |
|---|---|
| **Use when** | Called by new-item, discover, define and develop; or run it yourself on an item or a description |
| **Arguments** | `<project> <item>` or `<description>` |
| **Gate** | You choose: an initiative with children (default), sibling items, or keep it whole |

## integrate

Adds an MCP server or external API the standard way.

| | |
|---|---|
| **Use when** | Connecting a service, MCP server or API |
| **Arguments** | `<service or MCP server> [purpose]` |
| **Calls** | new-item |
| **Agents** | researcher |
| **Gate** | The item's own gates |

## ci

Sets up the [standard CI](ci.md) in a GitHub repo.

| | |
|---|---|
| **Use when** | A repo has no CI or non-standard CI; run again after adoption to require `ci-ok` |
| **Arguments** | `<repo>` |
| **Calls** | repo-context, new-item |
| **Gate** | The item's own gates, plus your approval per repo for the ruleset |

## repo-context

Builds or refreshes a project's `project.md` from a target repo, read-only.

| | |
|---|---|
| **Use when** | Starting on a repo, or when project.md is [stale](criteria.md#context) |
| **Arguments** | `<repo folder name or path> [project slug]` |
| **Agents** | Explore, for large repos |
| **Gate** | None |

## discover

The Discover phase: maps the problem without deciding anything.

| | |
|---|---|
| **Use when** | An L item or any investigation is in Discover |
| **Arguments** | `<project> <item>` |
| **Agents** | researcher and Explore, in parallel when the [fan-out rule](criteria.md#agents-and-parallelism) allows |
| **Gate** | You answer the open questions (answers are written inline as `→ <answer>`) and approve |

## define

The Define phase: the spec. Says what gets done and how we'll know.

| | |
|---|---|
| **Use when** | An item is in Define (M items start here) |
| **Arguments** | `<project> <item>` |
| **Asks** | Scope-changing [gaps](criteria.md#gaps), up to four at a time |
| **Gate** | Approve the spec. Next: develop (L) or deliver (M, investigations, initiatives) |

## develop

The Develop phase for L items: the design and the task list.

| | |
|---|---|
| **Use when** | An L feature or task has an approved spec |
| **Arguments** | `<project> <item>` |
| **Asks** | Every [significant decision](criteria.md#decisions), with options and a recommendation |
| **Agents** | researcher and Plan |
| **Gate** | Approve the design. Next: deliver |

## deliver

The Deliver phase: builds, verifies, publishes and closes. Resumable.

| | |
|---|---|
| **Use when** | An item is ready (see [readiness](../.claude/skills/deliver/SKILL.md)), or to resume one that's waiting |
| **Arguments** | `<project> <item>` |
| **Agents** | implementer (one per task, in sequence), verifier (in parallel groups); review through `/review` |
| **Gate** | One approval for the whole item, covering its outward actions but never a [host change](criteria.md#building-blocks). Merging follows the [merge rule](criteria.md#merge-rule) |

The full log vocabulary is in [workspace.md](workspace.md#log-vocabulary).
