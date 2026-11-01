---
name: architect
description: Answer one architecture question (stack, datastore, service boundary, infrastructure) with 2–4 options including a boring baseline, a weighted decision matrix with live-checked facts, and a recommendation with confidence and reversibility. The user chooses, then the decision is recorded in the item's develop.md or, standalone, in the project's architecture folder. Use when develop meets an architectural decision, or when the user asks an architecture or technology-choice question about a project.
argument-hint: <project> [<item>] <question>
---

# architect

Decide one architecture question the way [docs/architecture/](../../../docs/architecture/README.md) says. develop runs it for every [architectural decision](../../../docs/criteria.md#decisions); it also runs standalone.

Every condition below (architectural and significant decisions, boring technology, agents and the model policy) is defined in [docs/criteria.md](../../../docs/criteria.md). Apply those definitions exactly. It never writes into a target repo.

## 1. Load

- Read `workspace/projects/<project>/project.md`, and `architecture/overview.md` and `architecture/decisions.md` if they exist.
- With an item, [resolve it](../../../docs/process.md#resolve-the-item) and read its `define.md` and `develop.md`.

## 2. Constraints and quality attributes

From the question, project.md (*Stack* is the boring baseline's starting point), overview.md's *Quality attributes* and the item's docs, collect:
- the constraints (stack, team, deadline, budget, hosting, what's out of scope)
- the quality attributes, ranked, each with a testable scenario ([quality-attributes.md](../../../docs/architecture/quality-attributes.md))

Ask the user only for what's missing.

## 3. Draft

Give the `architect` agent the question, the constraints, the ranked attributes, project.md *Stack* and the docs/architecture/ guides that apply, applying the model policy. Check its *Coverage* line ([complete coverage](../../../docs/criteria.md#complete-coverage)).

## 4. Check facts

Give each option's *Facts to check* to one `researcher`, in parallel within the [cap](../../../docs/criteria.md#agents-and-parallelism), applying the model policy. Each fact comes back with "checked <date> at <URL>" or is marked **unverified**, never stated from recall ([guide](../../../docs/architecture/language-and-framework-selection.md#check-facts-live-never-recall-them)).

Correct the matrix from the results: rescore what a checked fact changes, keep each unverified fact's mark on the score it affects, and re-run the sensitivity check and the recommendation if anything moved.

## 5. Report

Concise by default:
- the options, one line each, with the baseline labelled
- the matrix in [decision-matrix.md](../../../docs/architecture/decision-matrix.md)'s format, with unverified facts marked
- its recommendation block
- each innovation token's justification ([boring technology first](../../../docs/criteria.md#building-blocks))

Ask the user to choose an option, and offer "explain more". On "explain more", walk each criterion in weight order: its weight, each option's score and rationale, and what choosing for it trades away. Then ask again.

## 6. Choose

The user chooses. Nothing is recorded before that.

## 7. Record

Create `workspace/projects/<project>/architecture/` from [templates/workspace/architecture/](../../../templates/workspace/architecture/) if it's missing.

- **With an item:** write the decision entry in develop.md (start from [the template](../../../templates/workspace/develop.md) if it doesn't exist): Kind `significant`, context, options considered, choice, Recommendation taken yes/no, and consequences (confidence, door, tokens and their justification, regret scenario). Leave its decisions.md row to develop's gate.
- **Standalone:** write `architecture/decisions/<date>-<slug>.md` from [the template](../../../templates/workspace/architecture/decision.md), mapping the matrix to its sections as [decision-matrix.md](../../../docs/architecture/decision-matrix.md#as-an-adr-madr) says, with [In plain terms](../../../docs/process.md#in-plain-terms) and whether the recommendation was taken. Add a decisions.md row: Date, Decision, Choice, and Item a link to `decisions/<date>-<slug>.md`.

Update overview.md's *Context*, *Containers* or *Quality attributes* where the decision changes them. Report the paths written.
