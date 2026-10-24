# Decision matrix

Compare 2–4 options against weighted criteria. The matrix structures judgment; it doesn't replace it.

## Template

Criteria come from the ranked [quality attributes](quality-attributes.md), plus cost and delivery. Weights sum to 100; scores are 1–5 (5 best), each with a one-line rationale. Total = Σ(weight × score) / 100.

| Criterion | Weight | A | B | C: boring baseline |
|---|---|---|---|---|
| Latency scenario met | 30 | 4 | 5 | 3 |
| Operable by the current team | 25 | 2 | 3 | 5 |
| Time to deliver | 20 | 3 | 3 | 4 |
| Cost | 15 | 3 | 2 | 4 |
| Reversibility | 10 | 2 | 3 | 5 |
| **Total** | **100** | **2.95** | **3.45** | **4.05** |
| Innovation tokens spent | | 1 | 1 | 0 |

- Set the weights before scoring.
- Score one criterion across all options before the next.
- **Sensitivity:** if moving one weight by 10 flips the winner, call it a tie.
- If the winner contradicts your gut, find out why before accepting either.

## Required

- **A boring baseline:** the most established option the team already runs, or the simplest thing that could work. Novel options must beat it clearly ([boring technology](../criteria.md#building-blocks)).
- **Reversibility:** label each option a two-way door (cheap to undo; decide fast) or a one-way door (data model, public API, lock-in; analyse more). Score 5 = undone in days, 1 = permanent. One-way doors via Bezos's 2015 shareholder letter (unverified).
- **Innovation tokens** spent per option (https://boringtechnology.club/).

## Recommendation

```
Recommendation: <option> (X.X vs next Y.Y)
Confidence: high | medium | low: <reason>
Would change if: <assumption> → <other option> wins
Regret scenario: <how this looks bad in 12 months; exit path and cost>
Innovation tokens: N · Door: one-way | two-way
```

- **High:** a clear margin, stable under sensitivity, backed by a spike or benchmark.
- **Medium:** a reasonable margin, some scores are judgment.
- **Low:** near tie or key unknowns; say what to test first.

## As an ADR (MADR)

Sections verified at https://adr.github.io/madr/.

| Matrix | MADR section |
|---|---|
| Problem and top scenarios | Context and Problem Statement |
| Criteria and weights | Decision Drivers |
| Options, with the baseline | Considered Options |
| Winner, confidence, justification | Decision Outcome |
| Regret, tokens, door, trade-offs | Consequences |
| Assumptions and how to check them | Confirmation |
| Per-option rationale | Pros and Cons of the Options |
| Full table, sensitivity | More Information |

Revisit the ADR when a listed assumption breaks.
