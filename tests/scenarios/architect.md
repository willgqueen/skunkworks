# architect scenarios

Run per [docs/testing.md](../../docs/testing.md). Covers 021's live runs (AC numbers are 021's). Setup for all: `python3 -I scripts/sandbox.py --seed`.

## A1. A standalone question

- **Run:** `/architect greet how should greet store custom greetings?`
- **Expect:** it reads `project.md` (*Stack*: standard library only) and `overview.md` (*Quality attributes*: Simplicity), and asks only for what they don't say, such as how many greetings and who edits them (021 AC1).
- **Answer:** to every constraint or quality-attribute question: "a few dozen, edited by hand by one user; must work offline. Ranked: 1. Simplicity: adding a greeting is one edit to one file, under a minute; 2. Reliability: a malformed store gives a clear error, never a traceback; 3. Portability: runs on a fresh Python install with no extra packages".
- **Expect before choosing:**
  - an `architect` agent drafts, then `researcher` agents check the options' stale-prone facts in parallel, within the [cap](../../docs/criteria.md#agents-and-parallelism) (021 AC3)
  - 2–4 options, one labelled the boring baseline (for example a JSON file read with the standard library), each with its door type; the matrix in decision-matrix.md's format: weights summing to 100 from the ranked attributes, a one-line rationale per score, innovation tokens and door type per option, the sensitivity result (021 AC2)
  - each checked fact listed as "checked <date> at <URL>" (021 AC3)
  - the recommendation block: recommendation, confidence with reason, would change if, regret scenario, tokens, door; any option spending a token (one outside *Stack*) states its justification (021 AC4)
  - a short report that offers "explain more" (021 AC5)
  - nothing written: no `workspace/projects/greet/architecture/decisions/` folder, decisions.md unchanged (021 AC6)
- **Answer:** take the recommendation.
- **Expect:** `workspace/projects/greet/architecture/decisions/<date>-<slug>.md` (slug kebab-case, at most five words) with the template's MADR sections filled, including In plain terms, the full matrix and the sources under More Information, and the recommendation taken; a decisions.md row whose Item links `decisions/<date>-<slug>.md`; overview.md's *Containers* has a [container diagram](../../docs/architecture/c4-diagrams.md) with greet and the chosen store as a data store (every option adds one); `git -C ../target status` clean (021 AC6).

## A2. A develop-invoked decision

- **Setup:** in `workspace/projects/greet/items/003-add-pluggable-greeting-styles/define.md`, add the *In scope* line "- `--add-style <name> <template>`; added styles persist between runs.", replace the Out of scope line with "- A web UI." and add AC "5. [ ] Styles a user adds with `--add-style <name> <template>` persist between runs."
- **Run:** `/develop greet 003`
- **Expect:** where to persist added styles is treated as an [architectural decision](../../docs/criteria.md#decisions) (a datastore) and goes through `/architect` with the item; other significant decisions are asked as before (021 AC7). The architect report has A1's parts (021 AC2–AC5).
- **Answer:** to every constraint or quality-attribute question: "standard library only; one user; offline. Ranked: 1. Simplicity: adding a style is one command and one entry in one file; 2. Durability: an added style is there after a restart, and a crash mid-write leaves the earlier styles intact". Take the recommendation for every decision. Don't approve yet.
- **Expect:** develop.md's entry for the storage decision has Kind `significant`, Drivers, options considered, the choice, `Recommendation taken: yes`, consequences (confidence, door, tokens, regret) and Sources; no `architecture/decisions/` file, no new decisions.md row and overview.md unchanged yet; the report says the row comes at approval (021 AC6).
- **Answer:** approve.
- **Expect:** `develop approved`; decisions.md has the storage decision's row with Item `003`, exactly once (021 AC6).

## A3. An unverifiable fact

- **Setup:** a fresh seed (no `workspace/projects/greet/architecture/decisions/`).
- **Run:** `/architect greet should greet store greetings in SQLite or in Zentrova DB, our vendor's hosted store?`
- **Answer:** any question about missing constraints: "hosted is fine; one user".
- **Expect:** Zentrova DB's facts (version, license, price, limits) marked **unverified**, not stated from recall; the scores they affect carry the mark; confidence reflects them and *Would change if* names what to check first (021 AC3, AC4). SQLite's facts are cited. Zentrova DB, outside *Stack*, spends an innovation token and states its justification (021 AC4).
- **Answer:** "neither for now".
- **Expect:** nothing recorded: no `architecture/decisions/` folder, decisions.md unchanged (021 AC6).

## A4. Explain more, then a different choice

- **Setup:** `rm -rf workspace/projects/greet/architecture`
- **Run:** A1's question, with A1's answer to every constraint or quality-attribute question.
- **Answer:** at the report, "explain more".
- **Expect:** each criterion in weight order: its weight, every option's score and rationale, and what choosing for it trades away; then it asks again; still nothing written (021 AC5, AC6).
- **Answer:** choose an option other than the recommendation.
- **Expect:** `workspace/projects/greet/architecture/` created with only `overview.md` and `decisions.md` from the templates, plus `decisions/`; the decision record states the recommendation wasn't taken; the decisions.md row links it; `git -C ../target status` clean (021 AC6).

## A5. Revise an architectural decision

- **Setup:** A2 done.
- **Run:** `/develop greet 003` with "switch the storage decision to its second option".
- **Expect:** `develop reopened`; `/architect` re-enters at the choice with the recorded options and matrix: no new draft, no researchers, no constraint questions (021 AC7).
- **Answer:** if asked, confirm the second option.
- **Expect:** develop.md still has one storage entry, replaced: the second option as its choice, `Recommendation taken: no`; the tasks it affects updated; `develop revised`; it stops at the gate (021 AC6).
- **Answer:** approve.
- **Expect:** `develop approved`; decisions.md's storage row for `003` shows the second option, updated, not duplicated (021 AC6).

## A6. An M item

- **Run:** `/architect greet 002 where should the test fixtures be stored?`
- **Expect:** it says 002 is an M item, which has no develop.md, and stops; nothing written: no `develop.md` in 002, `workspace/projects/greet/architecture/` unchanged (021 AC6).
