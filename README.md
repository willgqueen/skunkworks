# skunkworks

Named for Lockheed's Skunk Works, which was famous for keeping paperwork to a minimum. This one writes everything down.

A control center for software work. Claude Code runs from this repo and takes ideas through discovery, specs, design and delivery in any repo under `~/repos`, the same way every time: tracked as items, decided at gates you approve, and documented as it goes.

## Quick start

```sh
git clone https://github.com/willgqueen/skunkworks ~/repos/skunkworks
cd ~/repos/skunkworks
mkdir -p workspace/projects workspace/archive workspace/worktrees && touch workspace/inbox.md
claude
```

Then:
- `/hq` shows every open item and what's next
- `/repo-context <repo>` maps a repo you'll work on
- `/hq <description>` starts new work and walks it through its phases

The full walkthrough is in [docs/getting-started.md](docs/getting-started.md).

## Skills

| Skill | What it does |
|---|---|
| `/hq` | The front door: the board, routing, carrying items through their phases, inbox triage, waivers, `ledger`, `tidy` |
| `/new-item` | Turns a description into a numbered item with kind, size and first phase |
| `/review` | Strict multi-agent code review with a verdict |
| `/split` | Proposes splitting work that's too big into right-sized items |
| `/integrate` | Adds an MCP server or API with credentials, access and guards |
| `/ci` | Sets up the standard CI, with one required `ci-ok` check |
| `/repo-context` | Maps a target repo into its project.md, read-only |
| `/discover` | Maps the problem: context, options, open questions |
| `/define` | Writes the spec: goal, scope, acceptance criteria |
| `/develop` | Designs L items with you: decisions, ordered tasks, risks |
| `/deliver` | Builds in a worktree, verifies, opens the PR, reviews, merges per the rules, closes |

Details for each: [docs/skills.md](docs/skills.md).

## Docs

| Doc | For |
|---|---|
| [getting-started.md](docs/getting-started.md) | A walkthrough of one item, start to finish |
| [how-to.md](docs/how-to.md) | Recipes for everyday tasks |
| [skills.md](docs/skills.md) | Reference for every skill |
| [agents.md](docs/agents.md) | The agent roster, parallelism, and the guard on subagents |
| [ci.md](docs/ci.md) | The standard CI and its shared workflows |
| [integrations.md](docs/integrations.md) | MCP servers and APIs: registry and rules |
| [architecture/](docs/architecture/) | Architecture reference guides |
| [templates.md](docs/templates.md) | Every template and who uses it |
| [review-rubric.md](docs/review-rubric.md) | What reviews check, severities, verdict |
| [process.md](docs/process.md) | The method: phases, gates, sizing, next actions |
| [criteria.md](docs/criteria.md) | Every rule and threshold, and how they're calibrated |
| [workspace.md](docs/workspace.md) | The local planning workspace and the log vocabulary |
| [contributing.md](docs/contributing.md) | How to change this repo |
| [testing.md](docs/testing.md) | Automated checks, and testing skills by hand in a sandbox |
| [vision.md](docs/vision.md) | What this repo is for, in the owner's words |

## Setup

1. Clone this repo into the folder that holds your other repos (for example `~/repos`): Claude Code gets read access to that whole folder, so never clone it into your home folder. Start Claude Code from here: `cd ~/repos/skunkworks && claude`. Skills, agents and hooks in `.claude/` load automatically.
2. Repos next to this one (in `~/repos`) are reachable through `.claude/settings.json`. For a repo elsewhere, run `/add-dir <path>` in the session.
3. On a fresh clone, create the workspace:

   ```sh
   mkdir -p workspace/projects workspace/archive workspace/worktrees && touch workspace/inbox.md
   ```

4. Requirements: Claude Code ≥ 2.1.295 (for the guard's fail-closed setting), `git`, `python3`, and `gh` (authenticated) for repos with a GitHub remote.

## License

[MIT](LICENSE)
