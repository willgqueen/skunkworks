---
name: architect
description: Answer one architecture question (stack, datastore, service boundary, infrastructure) with 2–4 options including a boring baseline, a weighted decision matrix with live-checked facts, and a recommendation with confidence and reversibility. The user chooses, then the decision is recorded in the item's develop.md or, standalone, in the project's architecture folder. Use when develop meets an architectural decision, or when the user asks an architecture or technology-choice question about a project.
argument-hint: <project> [<item>] <question>
---

# architect

Decide one architecture question the way [docs/architecture/](../../../docs/architecture/README.md) says. develop runs it for every [architectural decision](../../../docs/criteria.md#decisions); it also runs standalone.

Every condition below (architectural and significant decisions, boring technology, phase state, complete coverage, agents and the model policy) is defined in [docs/criteria.md](../../../docs/criteria.md). Apply those definitions exactly. It never writes into a target repo.

## 1. Load

- Read `workspace/projects/<project>/project.md`, and `architecture/overview.md` and `architecture/decisions.md` if they exist.
- With an item, [resolve it](../../../docs/process.md#resolve-the-item). It must be an L item whose develop isn't [approved](../../../docs/criteria.md#phase-state); otherwise say so and stop. An M item has no develop.md; an approved design is changed by revising it with `/develop`, which logs `develop reopened`. Read its `define.md` and `develop.md`.
- If this decision is already recorded (the item's develop.md entry, or a standalone record for the same question), it's a [re-run](#re-runs).

## 2. Constraints and quality attributes

From the question, project.md (*Stack* is the boring baseline's starting point), overview.md's *Quality attributes* and the item's docs, collect:
- the constraints (stack, team, deadline, budget, hosting, what's out of scope)
- the quality attributes, ranked, each with a testable scenario ([quality-attributes.md](../../../docs/architecture/quality-attributes.md))

Within one develop run, reuse the constraints and ranked attributes an earlier call recorded for the item (its entries' *Drivers*). Ask the user only for what's still missing.

## 3. Draft

Give the `architect` agent the question, the constraints, the ranked attributes, project.md *Stack* and the docs/architecture/ guides that apply, applying the model policy.

Check its output against [decision-matrix.md](../../../docs/architecture/decision-matrix.md)'s *Required* and *Recommendation*: a boring baseline, 2–4 options, weights summing to 100, the recommendation is the highest total, and its confidence fits the sensitivity result. Check its *Coverage* line. On a gap, re-run it with the gap named, up to the [re-run limit](../../../docs/criteria.md#complete-coverage); then report the result as incomplete.

## 4. Check facts

Give the *Facts to check* to `researcher` agents: one per option that has facts, each shared fact to only one of them. Run them in parallel within the [cap](../../../docs/criteria.md#agents-and-parallelism), applying the model policy. Each fact comes back with "checked <date> at <URL>" or is marked **unverified**, never stated from recall ([guide](../../../docs/architecture/language-and-framework-selection.md#check-facts-live-never-recall-them)). Check each researcher's *Coverage* line; any fact it doesn't account for is **unverified**.

Correct the matrix from the results: rescore what a checked fact changes, keep each unverified fact's mark on the score it affects, and re-run the sensitivity check and the recommendation if anything moved.

## 5. Report

Concise by default:
- the options, one line each, with the baseline labelled and each one's door type
- the matrix in [decision-matrix.md](../../../docs/architecture/decision-matrix.md)'s format, with unverified facts marked, and the sensitivity result
- its recommendation block
- each innovation token's justification ([boring technology first](../../../docs/criteria.md#building-blocks))
- each checked fact with "checked <date> at <URL>", and each unverified one

Ask the user to choose an option, and offer "explain more". On "explain more", walk each criterion in weight order: its weight, each option's score and rationale, and what choosing for it trades away. Then ask again.

## 6. Choose

The user chooses. Nothing is recorded before that. If they choose none, record nothing; within develop the decision stays open and develop asks how to proceed.

## 7. Record

If `workspace/projects/<project>/architecture/` is missing, create it with `overview.md` and `decisions.md` from [templates/workspace/architecture/](../../../templates/workspace/architecture/).

- **With an item:** write the decision entry in develop.md (start from [the template](../../../templates/workspace/develop.md) if it doesn't exist), replacing any existing entry for this decision: Kind `significant`, context, *Drivers* (constraints and ranked attributes with their weights), options considered (baseline labelled, each with its total), choice, Recommendation taken yes/no, consequences (confidence, door, tokens and their justification, regret scenario) and *Sources* (each checked fact's citation, unverified ones marked). Write nothing else: develop's gate adds the decisions.md row and updates overview.md when the design is approved.
- **Standalone:** write `architecture/decisions/<date>-<slug>.md` (slug: kebab-case, at most five words, from the question) from [the template](../../../templates/workspace/architecture/decision.md), mapping the matrix to its sections as [decision-matrix.md](../../../docs/architecture/decision-matrix.md#as-an-adr-madr) says, with [In plain terms](../../../docs/process.md#in-plain-terms), whether the recommendation was taken, and the sources in *More Information*. Add its decisions.md row: Date, Decision, Choice, and Item a link to `decisions/<date>-<slug>.md`. Update overview.md's *Context*, *Containers* or *Quality attributes* where the decision changes them.

Report the paths written; with an item, say that its decisions.md row comes at develop's approval.

## Re-runs

A re-run replaces, never appends: with an item, the develop.md entry for the decision; standalone, the same record and its decisions.md row. A changed choice among the recorded options re-enters at step 6 with the recorded options and matrix. Only changed constraints or attributes restart at step 2.
