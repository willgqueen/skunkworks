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
  - the recommendation block: recommendation, confidence with reason, would change if, regret scenario, tokens, door; the recommendation and confidence consistent with the sensitivity result (a flip under sensitivity is called a tie, with low confidence); any option spending a token (one outside *Stack*) states its justification (021 AC4)
  - a short report that offers "explain more" (021 AC5)
  - nothing written: no `workspace/projects/greet/architecture/decisions/` folder, decisions.md unchanged (021 AC6)
- **Answer:** take the recommendation.
- **Expect:** `workspace/projects/greet/architecture/decisions/<date>-<slug>.md` (slug kebab-case, at most five words) with the template's MADR sections filled, including In plain terms, the full matrix and the sources under More Information, and the recommendation taken; a decisions.md row whose Item links `decisions/<date>-<slug>.md`; overview.md's *Containers* updated with a [container diagram](../../docs/architecture/c4-diagrams.md) showing greet and the chosen store as a data store if the choice adds one, otherwise unchanged; `git -C ../target status` clean (021 AC6).
- **Run:** A1's question again, with A1's answers; take the recommendation.
- **Expect:** a re-run: the same record replaced and its decisions.md row replaced, not duplicated (021 AC6).

## A2. A develop-invoked decision

- **Setup:** in `workspace/projects/greet/items/003-add-pluggable-greeting-styles/define.md`, add the *In scope* line "- `--add-style <name> <template>`; added styles persist between runs.", replace the Out of scope line with "- A web UI." and add AC "5. [ ] Styles a user adds with `--add-style <name> <template>` persist between runs."
- **Run:** `/develop greet 003`
- **Expect:** where to persist added styles is treated as an [architectural decision](../../docs/criteria.md#decisions) (a datastore) and goes through `/architect` with the item; other significant decisions are asked as before (021 AC7). The architect report has A1's parts (021 AC2–AC5).
- **Answer:** to every constraint or quality-attribute question: "standard library only; one user; offline. Ranked: 1. Simplicity: adding a style is one command and one entry in one file; 2. Durability: an added style is there after a restart, and a crash mid-write leaves the earlier styles intact". Take the recommendation for every decision. Don't approve yet.
- **Expect:** develop.md's entry for the storage decision is a `### D<n>:` heading followed by the line - **Kind:** significant (bare, no backticks), then Drivers (constraints, ranked attributes, weights), options considered, the Matrix (every score with its rationale, the sensitivity result, each option's door and tokens, the recommendation's regret scenario), the choice, Recommendation taken: yes, consequences and Sources; no `architecture/decisions/` file, no new decisions.md row and overview.md unchanged yet; the report says the row comes at approval (021 AC6).
- **Answer:** approve.
- **Expect:** `develop approved`; decisions.md has the storage decision's row with Item `003`, exactly once (021 AC6).
- **Variant:** in a fresh seed with A2's setup and run, and A2's answers until the storage report, answer it with "none of these".
- **Expect:** no storage entry in develop.md; develop says the decision is still open and asks how to proceed (021 AC6).

## A3. An unverifiable fact

- **Setup:** a fresh seed (no `workspace/projects/greet/architecture/decisions/`).
- **Run:** `/architect greet should greet store greetings in SQLite or in Zentrova DB, our vendor's hosted store?`
- **Answer:** to every constraint or quality-attribute question: "hosted is fine; one user. Ranked: 1. Simplicity: adding a greeting is one edit, under a minute; 2. Reliability: an unreachable store gives a clear error, never a traceback".
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

- **Setup:** A2 done. Start a fresh Claude session in A2's sandbox.
- **Run:** `/develop greet 003` with "switch the storage decision to an option other than the current choice".
- **Expect:** `develop reopened`; `/architect` re-enters at the choice from the matrix recorded in develop.md: no new draft, no researchers, no constraint questions; the report states its sources' check dates (021 AC7; 041 AC6).
- **Answer:** if asked which, pick any recorded option other than the current choice.
- **Expect:** develop.md still has one storage entry, replaced: the new option as its choice, Recommendation taken: no, and its consequences rewritten for the new option from the recorded matrix (its door and tokens); the Approach and the tasks it affects updated; `develop revised`; it stops at the gate (021 AC6).
- **Answer:** approve.
- **Expect:** `develop approved`; decisions.md's storage row for `003` shows the new option: one row updated, not duplicated (021 AC6).

## A6. An M item

- **Run:** `/architect greet 002 where should the test fixtures be stored?`
- **Expect:** it hands to develop, which says Develop isn't needed for an M item and offers to re-size.
- **Answer:** "keep it M".
- **Expect:** it stops; nothing written: no `develop.md` in 002, `workspace/projects/greet/architecture/` unchanged (021 AC6).

## A7. An item call on an approved design

- **Setup:** A2 done, before A5 (or in a fresh sandbox through A2).
- **Run:** `/architect greet 003 should added styles be stored with shelve instead?` (if A2's matrix has `shelve`, name another standard-library option it lacks)
- **Expect:** it hands to develop with the question as feedback marked "from /architect"; develop logs `develop reopened` exactly once and routes the decision through `/architect`, which redrafts at step 3 with the recorded drivers, shown for confirmation: no other constraint questions, and `shelve` scored in the new matrix (021 AC7; 041 AC6).
- **Answer:** confirm the drivers; choose `shelve`.
- **Expect:** develop.md's storage entry replaced, not duplicated, and the Approach and affected tasks updated; `develop revised`; it stops at its gate; decisions.md unchanged until approval (021 AC6).

## A8. An initiative

- **Run:** `/architect greet 006 should the CLI use a terminal UI framework?`
- **Expect:** it hands to develop, whose check says Develop is skipped for an initiative, and stops; nothing written: no `develop.md` in 006, `workspace/projects/greet/architecture/` unchanged (021 AC6).

## A9. One active item, no item named

- **Setup:** in 005's and 006's `item.md`, set `status: proposed`, so 003 (an L with an approved define) is greet's only active item.
- **Run:** `/architect greet how should greet store custom greetings?`, with A1's answers; take the recommendation.
- **Expect:** a standalone record and decisions.md row as in A1, with no hand-off to develop; 003 untouched: no `develop.md`, `item.md` unchanged (021 AC6).

## A10. A new architectural decision on an item

- **Setup:** A2 done.
- **Run:** `/architect greet 003 should styles come from a separate greeting service rather than greet itself?`
- **Expect:** it hands to develop, which logs `develop reopened` and routes the question through `/architect`; it shows the storage *Drivers* for confirmation or asks for this concern's ranking, and never reuses them silently (021 AC7; 041 AC1).
- **Answer:** to every constraint or quality-attribute question: "one user, installs by copying the file. Ranked: 1. Simplicity: installing is one copy, under a minute; 2. Portability: runs on a fresh Python install with no extra packages". Take the recommendation.
- **Expect:** a new `### D<n>:` entry beside the storage one, which is unchanged; `develop revised`; it stops at its gate; decisions.md unchanged until approval (021 AC6).

## A11. A fresh-run hand-off

- **Setup:** a fresh seed with A2's setup; 003 has no `develop.md`.
- **Run:** `/architect greet 003 where should added styles persist?`
- **Expect:** it hands to develop with the question as feedback marked "from /architect"; develop drafts and takes the question up as an architectural decision through `/architect ... (from /develop)`, which doesn't hand back to develop again; it asks A2's constraint and attribute questions (041 AC3).
- **Answer:** as in A2's answers; take the recommendation.
- **Expect:** develop.md has the storage decision's `### D<n>:` entry as in A2; `develop drafted` is logged once; it stops at its gate (041 AC3).

## A12. Re-check a recorded fact

- **Setup:** A1 done.
- **Run:** `/architect greet re-check the facts in the recorded decision on greeting storage`
- **Expect:** a re-run that re-enters at step 4 with the recorded matrix: no new draft and no constraint questions; `researcher` agents re-check the facts; the report shows the matrix corrected where a fact moved, with new "checked <date> at <URL>" lines (041 AC6).
- **Answer:** take the recommendation.
- **Expect:** the same record and decisions.md row replaced, not duplicated.
