# How-to

Short recipes for everyday tasks. Each one names the command and what to expect. For a full walkthrough, see [getting-started.md](getting-started.md).

## Seeing what's going on

### See all open work and what's next
`/hq`. The board lists every open item with its next action and who it's waiting on, items waiting on you first. It ends with the inbox count, any stale items, and, when due, a calibration reminder. Outside a session: `python3 -I scripts/board.py`.

### See what changed
`/hq ledger` (or `python3 -I scripts/ledger.py --since 2026-10-01 --project <p>`): one entry per committed task or merge, grouped by item, with repos, significant decisions and any `ledger:` notes. Items closed without per-task commit lines get one unlinked entry from their Outcome. skunkworks' own changes are also in [CHANGELOG.md](../CHANGELOG.md).

### See one item in detail
Open its folder: `workspace/projects/<project>/items/<NNN>-<slug>/`. `item.md` has its state and log; each phase has its own doc. Or run `python3 -I scripts/board.py --item <project>/<NNN>`.

## Starting work

### Map a repo before working on it
`/repo-context <repo folder name or path>`. Writes `workspace/projects/<repo>/project.md`. Re-run it when the file is [stale](criteria.md#context).

### Start new work
`/hq <description>` or `/new-item <project> <description>`. You get a numbered item with its kind, size and first phase, and Claude asks before starting.

### Start a project that has no repo yet
`/new-item <new-project-name> <description>`. It creates the project with "Repos: none yet". Run `/repo-context` once the repo exists.

### Jot an idea down for later
Add a line starting with `- ` to `workspace/inbox.md`.

### Turn inbox ideas into items
`/hq inbox`. For each entry you choose: create an item, keep it, or drop it.

## Moving work forward

### Continue an item
`/hq <project> <NNN>`. It runs the item's next phase and carries on after each gate you approve.

### Run a specific phase yourself
`/discover`, `/define`, `/develop` or `/deliver`, each with `<project> <NNN>`. Each checks that the item is ready for it and says so if it isn't.

### Answer a gate
Reply in chat. Approve ("approved"), request changes, or answer the numbered questions (Discover). Answers are written into the phase doc, so they never live only in chat.

### Advance several items at once
Ask `/hq` to advance them. Research for each runs in parallel in the background; then each phase runs in turn in the main session, with its gate.

### Skip a gate
Say so explicitly, for example "skip to deliver" or "waive develop". hq logs `<phase> waived: <reason>`, and a waived phase counts as [approved](criteria.md#phase-state). Deliver's one approval for outward actions can't be waived.

### Change something after you approved it
Run the phase again, for example `/define <project> <NNN>`, and say what to change. The skill logs that the phase was reopened, so the old approval stops counting, revises the doc, and asks you to approve again.

### Split work that's too big
new-item, discover, define and develop propose a split on their own when work is [too big for one item](criteria.md#splitting). To ask for one, run `/split <project> <NNN>`. You choose: an initiative with children, sibling items, or keep it whole.

### Change an item's size
When a skill sees a [re-size trigger](criteria.md#size), it recommends one. You can also ask directly. Only you can agree to a re-size; it's logged with the condition that triggered it.

## Delivery

### Approve delivery
`/deliver <project> <NNN>` shows one plan (worktree, branch, tasks, definition of done, and every outward action). Your approval covers the whole item, except a [host change](criteria.md#building-blocks), which needs its own; you won't be asked per commit.

### Let Claude merge in a project
Set *Merge policy* to `auto` in `workspace/projects/<project>/project.md`. Claude then merges only when the [merge rule](criteria.md#merge-rule) holds. The default, `manual`, means you always merge.

### Merge it yourself, then close the item
Merge the PR (or branch), then run `/deliver <project> <NNN>` (or `/hq <project> <NNN>`). It confirms the merge, removes the worktree and archives the item.

### Unblock an item
The board shows the cause. Fix it, then run `/deliver <project> <NNN>`. Deliver checks that the cause is resolved, logs `unblocked`, and resumes.

### Find where deliver is building
`workspace/worktrees/<repo>/<branch>`. It's a normal git worktree of the target repo, and deliver removes it when the item closes.

## CI

### Set up CI in a repo
`/ci <repo>`. It creates an item that adds the [standard CI](ci.md), ending in one required check, `ci-ok`, and asks before requiring it on the default branch.

## Integrations

### Connect an MCP server or API
`/integrate <service>`. It creates an item that sets up the config, credentials (in `.env.local`, loaded per server), agent access and the allowlist, and adds it to the [registry](integrations.md).

## Keeping the toolkit honest

### Calibrate and tidy
When the board says calibration is due, run `/hq tidy`. In one pass it proposes calibration changes to *(provisional)* numbers in [criteria.md](criteria.md#calibration) and consolidation changes to the toolkit and backlog, each with evidence. You approve each one.

### Review a change
`/review` reviews your working tree; `/review --all [repo]` audits a whole codebase; `/review <PR>`, `/review <base>...<head>` or `/review <project> <NNN>` review the rest. It covers every file in scope, reports coverage, and ends with a verdict per the [rubric](review-rubric.md); a review that didn't cover everything says `incomplete`. To add checks for one repo, put them in its REVIEW.md or CLAUDE.md; they can add to the rubric but never remove Blocking checks.

### Run the checks
`python3 -I scripts/test.py`: unit tests, the skills lint and the docs check. Required before every commit. To test a skill by hand, see [testing.md](testing.md#skill-scenarios).

### Change a skill, agent, template or rule
Follow [contributing.md](contributing.md). It starts with `/new-item skunkworks <description>`, like any other work.
