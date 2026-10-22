# sandbox

A control center for taking software work from idea to merged code in a standard way. Claude Code runs from this repo and works on other repos from here.

- Vision: [docs/vision.md](docs/vision.md)
- Method: [docs/process.md](docs/process.md)
- Local planning workspace: [docs/workspace.md](docs/workspace.md)

## Setup

1. Start Claude Code from this folder: `cd ~/repos/sandbox && claude`. Skills and agents in `.claude/` load automatically.
2. Repos under `~/repos` are reachable through `.claude/settings.json`. For a repo elsewhere, run `/add-dir <path>` in the session.
3. On a fresh clone, create the workspace:

   ```sh
   mkdir -p workspace/projects workspace/archive && touch workspace/inbox.md
   ```
