# Testing

Two layers: automated checks before every commit, and skill scenarios you run by hand in a sandbox.

## Automated checks

Run before every commit:

```sh
python3 -I scripts/test.py
```

It runs:
- the unit tests in `tests/` (board, ledger, manifests, sandbox, docs check, skills lint, guard hook), with fixtures in `tests/fixtures/`
- `scripts/lint_skills.py`: frontmatter, no model names in skills, log lines in the vocabulary, a scenario for every skill
- `scripts/check_docs.py`: links, anchors, and that every skill, agent and template is documented

`scripts/install-hooks.sh` installs it as a git pre-commit hook (optional).

Use each language's standard test framework: `unittest` for this repo's Python. Add a test with every script change; add a fixture case with every Next action rule change; update a skill's scenario with every change to what the skill does.

## Skill scenarios

Skills are tested by hand: you drive a fresh Claude Code session through a scenario in a throwaway sandbox, away from your real workspace, memory and repos. Your MCP connectors and `gh` login still work there, so scenarios only call read-only tools.

### 1. Create a sandbox

```sh
python3 -I scripts/sandbox.py [DEST] [--remote] [--seed]
```

| Folder | What it is |
|---|---|
| `DEST/skunkworks/` | A copy of this working tree (uncommitted changes included, so they're what's tested), with an empty workspace and access to `DEST` |
| `DEST/target/` | A tiny Python repo ([fixture](../tests/fixtures/target-repo/)), branch `main` |
| `DEST/remote.git/` | With `--remote`: a local bare repo, target's `origin`. It stands in for a remote but isn't GitHub, so PRs, CI and rulesets need a real GitHub repo |

`--seed` adds a `greet` project for the target, items in the states the scenarios start from, and an inbox ([fixture](../tests/fixtures/sandbox-workspace/)). `DEST` defaults to a new temp folder.

### 2. Start a fresh session

```sh
cd DEST/skunkworks && claude
```

If `claude` isn't on your PATH, open `DEST/skunkworks` with your editor's Claude Code instead. A new folder means a new session with fresh skills (loaded skills are [snapshots](contributing.md#known-caveats)) and no memory. Check that `/hq` shows the seeded board.

### 3. Run the scenario

Each file in [tests/scenarios/](../tests/scenarios/) has numbered scenarios with:
- **Setup:** the sandbox command (run here), then any extra steps (run from `DEST/skunkworks`)
- **Run:** what to type
- **Answer:** what to say at each question or gate
- **Expect:** the files, log lines and board state to check afterwards
- **Then:** a follow-up step, followed by its own **Expect**

Each scenario starts in a new sandbox, made by its own sandbox command or the file's "Setup for all", then runs any other Setup steps. A Setup that says "X done" instead continues in X's sandbox and session.

Give the answers as written. Anything the skill does that the scenario doesn't expect is a result too.

| Skill | Scenarios | Covers deferred checks from |
|---|---|---|
| hq | [hq.md](../tests/scenarios/hq.md) | 010, 015 |
| new-item | [new-item.md](../tests/scenarios/new-item.md) | |
| split | [split.md](../tests/scenarios/split.md) | 016 |
| discover | [discover.md](../tests/scenarios/discover.md) | 009, 016 |
| define | [define.md](../tests/scenarios/define.md) | |
| develop | [develop.md](../tests/scenarios/develop.md) | 001, 016 |
| deliver | [deliver.md](../tests/scenarios/deliver.md) | 003 |
| review | [review.md](../tests/scenarios/review.md) | 005, 023 |
| repo-context | [repo-context.md](../tests/scenarios/repo-context.md) | |
| ci | [ci.md](../tests/scenarios/ci.md) | |
| integrate | [integrate.md](../tests/scenarios/integrate.md) | 013 |

### 4. Record the result

Record it in the item being tested: the one changing the skill, or the one that deferred the check. Add one line per AC or check to its deliver.md *Verification*:

```
- AC3: verified: live, <date>, deliver L1: <what you saw> ($<cost>)
- AC8: failed: live, <date>, deliver L5: <what happened>
```

A failure becomes a fix through new-item. Delete the sandbox afterwards (`rm -rf DEST`).

### Budget

Each run has a [budget](criteria.md#testing). Check `/cost` at the end and put it in the result. If a run passes its budget, stop it and record it as incomplete.
