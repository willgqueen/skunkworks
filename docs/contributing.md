# Contributing

How to change this repo: its skills, agents, templates, rules, scripts and docs. Changes go through the same process as any other work: they're tracked as items in the `skunkworks` project, built through the phases, and reviewed before they're committed.

## The ground rules

Above all, be succinct: the shortest complete version, everywhere ([CLAUDE.md](../CLAUDE.md#rules)).

1. **Track it.** Every change starts as an item (`/new-item skunkworks <description>`), sized by [criteria.md](criteria.md#size), and goes through its phases and gates.
2. **One source for each rule.** Conditions and thresholds live in [criteria.md](criteria.md); routing lives in [process.md](process.md). Skills, agents and docs link to them and never restate them.
3. **Build bottom-up.** A new workflow calls existing skills and agents instead of copying their steps.
4. **Update the docs in the same change.** If you change what something does, update every doc that describes it: [skills.md](skills.md), [agents.md](agents.md), [templates.md](templates.md), [how-to.md](how-to.md), [getting-started.md](getting-started.md), the README, CLAUDE.md. Then run the docs check.
5. **Keep workspace data in the workspace.** Nothing from `workspace/` goes into a target repo, a commit message or a PR. See [workspace.md](workspace.md#the-containment-rule).

## Adding or changing a skill

1. Create `.claude/skills/<name>/SKILL.md` with frontmatter:
   - `name`: the command name
   - `description`: what it does and when to use it. Claude matches requests against this, so name the situations.
   - `argument-hint`: for example `<project> <item id or slug>`
2. Follow the shape of the existing phase skills: load → ground → work → write → update item → gate. Copy their wording for shared steps (resolving an item, revision mode, the gate).
3. Link every condition to criteria.md with relative links (`../../../docs/criteria.md#<section>`). Never write a threshold into a skill.
4. Use the [log vocabulary](workspace.md#log-vocabulary). If the skill needs a new log line, add it to that table in the same change.
5. Spawn only roster agents, and apply the [model policy](criteria.md#agents-and-parallelism).
6. Document it: an entry in [skills.md](skills.md), and in the README's skill list.

## Adding or changing an agent

See [agents.md](agents.md#adding-or-changing-an-agent). In short: a file in `.claude/agents/` with `name`, `description`, `model`, `effort` and `tools`; a row in the roster table; read-only roles get no Write or Edit.

## Adding or changing a template

Edit or add the file in `templates/workspace/` or `templates/repo/`, keep placeholders as `{{name}}`, update every skill that fills it, and update [templates.md](templates.md).

## Changing a rule or threshold

Edit [criteria.md](criteria.md) only. Every skill that links to the rule follows automatically. Changes to *(provisional)* numbers go through [calibration](criteria.md#calibration): a proposal citing completed items, approved by you, and recorded in the calibration history.

## Adding or changing a script

Scripts live in `scripts/`. They use python3 and the standard library only, and are run with `python3 -I`. A script that implements a rule from process.md or criteria.md cites the section it implements, and changes to that rule update the script in the same change.

## Reviewing a change

Before committing, review the change. Until the review skill (item 005) exists, run the built-in `/code-review` on the diff and fix or explicitly accept every finding. Record the result in the item's `deliver.md` *Review* section.

## Checking the docs

```sh
python3 -I scripts/check_docs.py
```

It checks every relative link and `#anchor` in the tracked markdown, and that every skill, agent and template has an entry in its reference doc. Run it before every commit that touches docs, skills, agents or templates.

## Known caveats

- **New skills register after a delay.** A skill written mid-session shows up a few minutes later, without a restart.
- **Loaded skills are snapshots.** Once a skill has loaded in a session, edits to its file don't reach that session. Test changed skills in a fresh session.
- **Hooks apply immediately.** Changes to hooks in `.claude/settings.json` take effect in the running session.
- **Commits in this repo** go straight to `main` while it has no remote. That's the bootstrap exception noted in each item's deliver.md.
