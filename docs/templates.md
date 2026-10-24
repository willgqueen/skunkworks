# Templates

Files that skills copy when they create something. Placeholders look like `{{title}}`, and comments (`<!-- … -->`) explain what goes in each section. Skills replace placeholders and fill sections; they don't change a template's structure. To change the structure, edit the template; see [contributing.md](contributing.md).

## Workspace templates

In [`templates/workspace/`](../templates/workspace/). These end up in the gitignored [workspace](workspace.md).

| Template | Becomes | Created by | Holds |
|---|---|---|---|
| [project.md](../templates/workspace/project.md) | `projects/<project>/project.md` | repo-context, new-item | What the project is, repos, stack, commands, layout, merge policy, conventions learned |
| [item.md](../templates/workspace/item.md) | `items/<NNN>-<slug>/item.md` | new-item | Frontmatter (kind, status, phase, size, parent, repos, dates), Intent, Log |
| [discover.md](../templates/workspace/discover.md) | the item's `discover.md` | new-item, discover | Problem, Context, Options seen, Open questions |
| [define.md](../templates/workspace/define.md) | the item's `define.md` | new-item, define | Goal, scope, acceptance criteria, assumptions, approach (M) |
| [develop.md](../templates/workspace/develop.md) | the item's `develop.md` | develop | Approach, decisions, tasks with the ACs they serve, risks |
| [deliver.md](../templates/workspace/deliver.md) | the item's `deliver.md` | new-item (S items), deliver | Plan, tasks, progress, verification per AC, review, CI, outcome |

new-item creates only the starting phase's doc. Later phase skills create theirs when they run.

## CI templates

[`ci/templates/`](../ci/templates/) holds the caller workflows and Renovate config that `/ci` copies into target repos ([docs/ci.md](ci.md)). Their placeholders are `OWNER`, `SHA`, `VERSION` and `DEFAULT_BRANCH`.

## Repo templates

In [`templates/repo/`](../templates/repo/). These shape what goes **into target repos**. A repo's own conventions (CLAUDE.md, CONTRIBUTING, commitlint config, `.github/pull_request_template.md`) always override them. Both are checked against [sensitive content](criteria.md#building-blocks) before use.

| Template | Used for | Used by |
|---|---|---|
| [commit.md](../templates/repo/commit.md) | Commit messages: `<type>(<scope>): <summary>`, a body saying why, the attribution trailer | deliver |
| [pull-request.md](../templates/repo/pull-request.md) | PR descriptions: Summary, Changes, Verification, Notes | deliver |
