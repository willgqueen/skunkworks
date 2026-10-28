---
name: repo-context
description: Build or refresh a project's project.md and architecture overview in the workspace from a target repo. Use when starting work on a repo for the first time, when project.md is missing or stale, or when the user asks to learn, map or summarize a repo.
argument-hint: <repo folder name or path> [project slug]
---

# repo-context

Read a target repo and record what future work needs to know in `workspace/projects/<project>/project.md` and its `architecture/` folder. The target repo is **read-only** for this skill.

## 1. Resolve the repo and project

- A bare name means `../<name>`, a repo next to this one (usually `~/repos/<name>`); otherwise use the path given. Resolve it to an absolute path. Confirm it exists and note whether it is a git repo.
- If the path isn't next to this repo and isn't reachable, ask the user to run `/add-dir <path>`.
- The project slug defaults to the repo folder name. If the user names an existing project, add this repo to that project instead (a project can span several repos).

## 2. Gather

Read, don't execute. Skip anything that doesn't exist.

- `README*`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING*`, `docs/` index
- Manifests: `package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`, `build.gradle*`, `*.csproj`, `Dockerfile`, `docker-compose*`
- Task runners and CI: `Makefile`, `justfile`, `Taskfile*`, `.github/workflows/`, other CI config
- Lint and format config, to note the conventions it enforces
- Top-level tree (two levels, ignoring `node_modules`, `.git`, build output)
- Git: `git -C <repo> remote -v`, the default branch, and `git -C <repo> log --oneline -15`

When [criteria.md](../../../docs/criteria.md#context) says to use an Explore subagent, hand the survey to one and ask for conclusions only.

Never install dependencies, run builds or tests, or modify anything in the target repo.

## 3. Write project.md and the architecture folder

- **New project:** create `workspace/projects/<project>/` and `items/`, then fill [templates/workspace/project.md](../../../templates/workspace/project.md).
- **Existing project** (refresh it when it's [stale](../../../docs/criteria.md#context) or the user asks): rewrite the factual sections from what you just gathered, but keep every entry under *Conventions learned* and the existing *Merge policy*. New projects start with `manual`; only the user changes it. Add new conventions there only when the repo states them (for example, in CLAUDE.md or lint config).
- **Architecture:** if `workspace/projects/<project>/architecture/` is missing (a new project, or one made before it existed), create `overview.md` and `decisions.md` from [templates/workspace/architecture/](../../../templates/workspace/architecture/), filling *What it is* and, only as far as the repo shows, *Context* and *Containers* (services in docker-compose, external APIs named in config). If it exists, rewrite only *What it is*; keep the other sections, which develop writes from approved designs that may not be built yet. Never touch `decisions.md` rows.

Guidelines:
- **Commands** are exact and copied from the repo (scripts, Makefile targets, CI steps). If a command is inferred rather than stated, mark it `(inferred)`.
- Keep it short: it's loaded at the start of every item, so it should be skimmable in under a minute.
- Set the *Last refreshed* date.

## 4. Report

Give the paths to project.md and the architecture folder, a two-line summary of the repo, and anything notable: no tests found, no CI, uncommitted changes, an unclear entry point.
