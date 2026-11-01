# architect scenarios

Run per [docs/testing.md](../../docs/testing.md). Covers 021's live runs (AC numbers are 021's). Setup for all: `python3 -I scripts/sandbox.py --seed`.

## A1. A standalone question

- **Run:** `/architect greet how should greet store custom greetings?`
- **Expect:** it reads `project.md` (*Stack*: standard library only) and `overview.md` (*Quality attributes*: Simplicity), and asks only for what they don't say, such as how many greetings and who edits them (021 AC1).
- **Answer:** "a few dozen, edited by hand by one user; must work offline".
- **Expect before choosing:**
  - an `architect` agent drafts, then `researcher` agents check each option's stale-prone facts in parallel, at most 4 at once (021 AC3)
  - 2–4 options, one labelled the boring baseline (for example a JSON file read with the standard library); the matrix in decision-matrix.md's format: weights summing to 100 from the ranked attributes, a one-line rationale per score, innovation tokens and door type per option, the sensitivity result (021 AC2)
  - each checked fact cited with date and URL (021 AC3)
  - the recommendation block: recommendation, confidence with reason, would change if, regret scenario, tokens, door; any option spending a token (one outside *Stack*) states its justification (021 AC4)
  - a short report that offers "explain more" (021 AC5)
  - nothing written: no `workspace/projects/greet/architecture/decisions/` folder, decisions.md unchanged (021 AC6)
- **Answer:** take the recommendation.
- **Expect:** `workspace/projects/greet/architecture/decisions/<date>-<slug>.md` with the template's MADR sections filled, including In plain terms, the full matrix and sources under More Information, and the recommendation taken; a decisions.md row whose Item links `decisions/<date>-<slug>.md`; overview.md's *Containers* updated if the choice adds a datastore, otherwise unchanged; `git -C ../target status` clean (021 AC6).

## A2. A develop-invoked decision

- **Setup:** in `workspace/projects/greet/items/003-add-pluggable-greeting-styles/define.md`, replace the Out of scope line with "- A web UI." and add AC "5. [ ] Styles a user adds with `--add-style <name> <template>` persist between runs."
- **Run:** `/develop greet 003`
- **Expect:** where to persist added styles is treated as an [architectural decision](../../docs/criteria.md#decisions) (a datastore) and goes through `/architect` with the item; other significant decisions are asked as before (021 AC7). The architect report has A1's parts (021 AC2–AC5).
- **Answer:** take the recommendation for every decision. Don't approve yet.
- **Expect:** develop.md's entry for the storage decision has Kind `significant`, options considered, the choice, `Recommendation taken: yes` and consequences (confidence, door, tokens, regret); no `architecture/decisions/` file and no new decisions.md row yet (021 AC6).
- **Answer:** approve.
- **Expect:** `develop approved`; decisions.md has the storage decision's row with Item `003`, exactly once (021 AC6).

## A3. An unverifiable fact

- **Run:** `/architect greet should greet store greetings in SQLite or in Zentrova DB, our vendor's hosted store?`
- **Answer:** any question about missing constraints: "hosted is fine; one user".
- **Expect:** Zentrova DB's facts (version, licence, price, limits) marked **unverified**, not stated from recall; the scores they affect carry the mark; confidence reflects them and *Would change if* names what to check first (021 AC3, AC4). SQLite's facts are cited.
- **Answer:** "neither for now".
- **Expect:** nothing recorded (021 AC6).

## A4. Explain more, then a different choice

- **Setup:** `rm -rf workspace/projects/greet/architecture`
- **Run:** A1's question and answer.
- **Answer:** at the report, "explain more".
- **Expect:** each criterion in weight order: its weight, every option's score and rationale, and what choosing for it trades away; then it asks again; still nothing written (021 AC5, AC6).
- **Answer:** choose an option other than the recommendation.
- **Expect:** `workspace/projects/greet/architecture/` created from the templates; the decision record states the recommendation wasn't taken; the decisions.md row links it; `git -C ../target status` clean (021 AC6).
