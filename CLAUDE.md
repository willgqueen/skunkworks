# Sandbox

The control center for orchestrating software work (ideation → planning → architecture → delivery). Claude Code always runs from here; target repos in `~/repos` (and elsewhere, via `/add-dir`) are worked on as additional directories.

## Layout

- `.claude/skills/<name>/SKILL.md`: skills, each callable as `/<name>`
- `.claude/agents/`: subagent definitions
- `.claude/settings.json`: project settings, including access to `~/repos`
- `templates/workspace/`: templates for workspace files
- `docs/vision.md`: what this repo is for
- `docs/process.md`: the method (phases, gates, sizing)
- `docs/workspace.md`: the workspace layout and item schema
- `workspace/`: **gitignored** local planning data

## Rules

- Planning and domain data live only in `workspace/`. Never write specs, plans, notes or logs into a target repo; target repos only receive code, tests and docs that belong to that codebase. See [docs/workspace.md](docs/workspace.md).
- When working in a target repo, use absolute paths (`git -C <repo>`, or `cd` in the same command), and follow that repo's own `CLAUDE.md`. Read it explicitly, because files in additional directories may not load automatically.
- Build bottom-up: a new composite workflow should call existing skills, not duplicate them.
- Skills that create workspace files start from `templates/workspace/`.
