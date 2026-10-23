# Agents

The roster of agents that skills hand work to, and how they run in parallel. The rules (model policy, parallel cap, when to fan out) are in [criteria.md](criteria.md#agents-and-parallelism). This page describes the agents.

## Roster

| Agent | Kind | Role | Default model · effort | Tools | Called by |
|---|---|---|---|---|---|
| [implementer](../.claude/agents/implementer.md) | custom | Builds one deliver task in a worktree, runs its checks, reports. Never commits. | sonnet · high | all | deliver |
| [reviewer](../.claude/agents/reviewer.md) | custom | Reviews a diff or PR against the ACs and design decisions; reports findings with failure scenarios. | opus · high | Read, Grep, Glob, Bash (read commands only, no tests) | deliver (until the review skill exists) |
| [verifier](../.claude/agents/verifier.md) | custom | Checks assigned ACs in a worktree; reports each as verified, failed or pending. | sonnet · medium | Read, Grep, Glob, Bash | deliver, in parallel groups |
| [researcher](../.claude/agents/researcher.md) | custom | Answers one research question from code, docs and the web, with sources. | sonnet · medium | Read, Grep, Glob, Bash, WebFetch, WebSearch | discover, develop |
| Explore | built-in | Fast read-only search across a codebase; returns conclusions. | built-in default | read-only | define, discover, develop, repo-context |
| Plan | built-in | Drafts implementation options for a broad design. | built-in default | read-only | develop |

L items and items that touch a risk area run custom agents on **opus** instead of their default (the calling skill passes the override). See the [model policy](criteria.md#agents-and-parallelism).

## Parallelism

Skills fan work out to parallel agents only when the [fan-out rule](criteria.md#agents-and-parallelism) allows, up to the parallel cap. In practice:

| Skill | Runs in parallel | Stays sequential |
|---|---|---|
| discover | Research questions (researcher, Explore) | The gate |
| develop | Research questions; Plan drafts | Decisions with the user, the gate |
| deliver | AC verification (verifier groups) | Tasks (one commit each, in order), push, PR, merge |

Agents started from the main session run in the background, and their results come back as notifications. The main session merges the results and owns every gate.

## Safety: no push or merge from subagents

[`.claude/hooks/guard-subagent-outward.sh`](../.claude/hooks/guard-subagent-outward.sh) is a PreToolUse hook registered in [`.claude/settings.json`](../.claude/settings.json). Its matcher covers Bash and every MCP tool.
- When a call comes from a subagent (the hook input has an `agent_id`), it blocks with exit code 2:
  - `git push` and `git merge` in any form (`git -C <path>`, env prefixes, absolute paths, inside `bash -c` or `$(…)`, on any line)
  - `gh pr merge`
  - `gh api` calls that merge, update refs or use a mutating method
  - MCP tools whose name mentions push, merge or refs
- If the hook can't read its input, or python3 is missing, it blocks (fails closed).
- Main-session calls have no `agent_id` and exit immediately, so deliver can still push and merge after its per-item approval.

It's a pattern guard, not a sandbox: it errs toward blocking, and a blocked subagent says so in its report. It can't see every way to reach a remote (for example, raw `curl` to an API). Item 013 standardizes MCP and external API use.

## Adding or changing an agent

1. Create or edit `.claude/agents/<name>.md` with `name`, `description`, `model`, `effort` and `tools`. Read-only roles get no Write or Edit.
2. Add it to the roster table above, and to [skills.md](skills.md) under the skills that call it.
3. Skills refer to the agent by name and apply the model policy; the only model they ever pass is the upgrade.

See [contributing.md](contributing.md) for the general process.
