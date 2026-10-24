# Quality attributes

Name, rank and specify the qualities a system needs before comparing designs. Pair with the [decision matrix](decision-matrix.md).

## ISO/IEC 25010:2023

Nine characteristics. The 2023 edition renamed Usability to Interaction capability and Portability to Flexibility, and added Safety. Names follow secondary sources; the standard's own text wasn't read (iso.org returned 403).

| Characteristic | Sub-characteristics | Ask |
|---|---|---|
| Functional suitability | completeness, correctness, appropriateness | Does it do the right things, correctly? |
| Performance efficiency | time behaviour, resource utilization, capacity | How fast, at what cost, up to what load? |
| Compatibility | co-existence, interoperability | Can it share an environment and exchange data? |
| Interaction capability | appropriateness recognizability, learnability, operability, user error protection, user engagement, inclusivity, user assistance, self-descriptiveness | Can the intended users, including those with diverse needs, use it without errors? |
| Reliability | faultlessness, availability, fault tolerance, recoverability | How often does it fail, and how does it recover? |
| Security | confidentiality, integrity, non-repudiation, accountability, authenticity, resistance | What must be kept out, unaltered or provable, and how does it withstand attack? |
| Maintainability | modularity, reusability, analysability, modifiability, testability | How cheaply can we find, change and verify a change? |
| Flexibility | adaptability, scalability, installability, replaceability | Can it adapt, scale, be installed and be replaced? |
| Safety | operational constraint, risk identification, fail safe, hazard warning, safe integration | Can it cause harm, and does it fail safely? |

## Ranking (ATAM utility tree)

1. List the business drivers.
2. Build a tree: quality attribute → refinement → concrete scenario.
3. Rate each scenario's business importance and difficulty: High, Medium or Low (from memory of the SEI report; unverified).
4. High importance and high difficulty drive the architecture.
5. Keep the top 3–5, and state what you'll trade away.

| Attribute | Refinement | Scenario | Importance | Difficulty |
|---|---|---|---|---|
| Performance | Latency | p95 search < 300 ms at 500 rps | H | M |
| Reliability | Recoverability | Region loss restored < 15 min, no data loss | H | H |
| Maintainability | Modifiability | Add a payment provider in < 3 dev-days | M | L |

## Scenario format

> **Source** does **stimulus** to **artifact** in **environment**; the system **responds**, measured by **measure**.

Example: an end user (source) submits checkout (stimulus) to the order service (artifact) at peak load, 500 rps (environment); the order is confirmed and stored (response), p95 < 300 ms and errors < 0.1% (measure). A scenario counts only if its measure is testable.

## Sources

- https://www.iso.org/standard/78176.html (catalogue; text not read)
- https://www.sonarsource.com/resources/library/iso-iec-25010-explained/, https://tnlab.org/en/iso-iec-250102023-square-product-quality-model/ (sub-characteristics)
- https://quality.arc42.org/articles/iso-25010-update-2023 (2023 changes)
- https://en.wikipedia.org/wiki/Architecture_tradeoff_analysis_method (ATAM steps)
