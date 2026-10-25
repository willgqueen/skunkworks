# Skunkworks

The control center for orchestrating software work (ideation → planning → architecture → delivery). Claude Code always runs from here; target repos in `~/repos` (and elsewhere, via `/add-dir`) are worked on as additional directories.

## Layout

- `.claude/skills/<name>/SKILL.md`: skills, each callable as `/<name>`
- `.claude/agents/`: the custom agents (implementer, reviewer, verifier, researcher); roster in `docs/agents.md`
- `.claude/hooks/`: the guard hook and its MCP allowlist (subagents can't act outward)
- `.claude/settings.json`: project settings, including access to the folder that holds this repo (`~/repos`)
- `templates/workspace/`: templates for workspace files
- `scripts/`: python3 scripts (board, ledger, review manifests, docs check, skills lint, test runner, test sandbox)
- `tests/`: unit tests, fixtures and skill scenarios ([docs/testing.md](docs/testing.md))
- `.github/workflows/`, `ci/templates/`, `renovate.json`: the shared CI workflows, caller templates and Renovate config (docs/ci.md)
- `templates/repo/`: templates for what goes into target repos (commit messages, PR descriptions)
- `docs/vision.md`: what this repo is for
- `docs/process.md`: the method (phases, gates, sizing)
- `docs/criteria.md`: every condition skills branch on, with calibration rules
- `docs/agents.md`: the agent roster, parallelism and the guard on subagents
- `docs/workspace.md`: the workspace layout and item schema
- `workspace/`: **gitignored** local planning data

## Rules

- **Be succinct and direct in everything.** Write the shortest complete version of code, comments, docs, specs and replies. Comment only where the code isn't self-explanatory. No restating, hedging or filler.
- Planning and domain data live only in `workspace/`. Never write specs, plans, notes or logs into a target repo; target repos only receive code, tests and docs that belong to that codebase. See [docs/workspace.md](docs/workspace.md).
- When working in a target repo, use absolute paths (`git -C <repo>`, or `cd` in the same command), and follow that repo's own `CLAUDE.md`. Read it explicitly, because files in additional directories may not load automatically.
- Build bottom-up: a new composite workflow should call existing skills, not duplicate them.
- Skills that create workspace files start from `templates/workspace/`.
- Every change updates the docs it affects, in the same change, and passes `python3 -I scripts/test.py` (unit tests, skills lint, docs check) before it's committed. [docs/contributing.md](docs/contributing.md) is the guide.
- **Reviews are exhaustive.** Any review, audit or verification covers its whole scope and reports coverage; partial work is reported as incomplete ([criteria.md](docs/criteria.md#complete-coverage)).
- Skills never define their own thresholds or conditions. They link to [docs/criteria.md](docs/criteria.md), so calibrating it updates every skill.
