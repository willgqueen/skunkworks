# Language and framework selection

For choosing, or challenging, a language, framework or runtime. Decide against the problem, record the evidence, and check volatile facts live.

## Check facts live, never recall them

Versions, LTS and EOL dates, licenses, download and maintainer counts, and release cadence all change. Look them up at decision time and record "checked <date> at <URL>"; if you couldn't check, write "unverified".

| Fact | Check at |
|---|---|
| Supported versions, LTS, EOL | https://endoflife.date (API: `https://endoflife.date/api/v1/products/<product>/`, fields like `isLts`, `eolFrom`, `isMaintained`) |
| Latest version, license, downloads, dependencies | The package registry (npm, PyPI, crates.io, Maven Central, pkg.go.dev) |
| Maintainers, activity, releases, governance | The project repo and its governance and SECURITY files |
| Known vulnerabilities | GitHub Advisories, OSV, the language's own advisory database |

## Criteria

Answer each with evidence, not opinion.

| Criterion | Question | Evidence |
|---|---|---|
| Team familiarity | Can the team ship and operate it within the deadline? | Prior projects; time to first production deploy in a spike |
| Ecosystem maturity | Do maintained libraries exist for what we need (auth, DB, queues, observability)? | A library per required capability; registry activity |
| Workload fit | Does it suit the workload (CPU, I/O, latency, concurrency, data size)? | A prototype or benchmark on our workload, not generic benchmarks |
| Licensing and governance | Can we use and ship it, and who controls its direction? | LICENSE and registry metadata; foundation or single vendor; license-change history |
| LTS and cadence | Is our version supported for the project's life, and can we afford upgrades? | endoflife.date windows; release policy; breaking-change history |
| Interoperability | Does it integrate with our systems, protocols and languages? | Client libraries, schema support, FFI or RPC; an integration spike |
| Deployment target | Does it run where we deploy? | A hello-world in the real target and CI |
| Security record | How often, and how well, are vulnerabilities fixed? | Advisory history, time to patch, signing and lockfiles |
| Community health | What happens if the main maintainer leaves? | Active maintainers, backing, release recency, issue response time |
| Hiring | Can we hire and train for it over the system's life? | Candidate pool, training time |

## Maturity rings

State trust with the Thoughtworks Technology Radar rings: **Adopt** (proven; the default), **Trial** (ready, less proven; low-risk use), **Assess** (spike only), **Caution** (avoid for new work, formerly "Hold"). Ring names verified at https://www.thoughtworks.com/radar/faq; the ratings are our own judgment, dated per context.

## Boring technology

From https://boringtechnology.club/: an organization has only a few innovation tokens. Mature tools have known failure modes and need less maintenance. The rule we apply is in [criteria.md](../criteria.md#building-blocks). Out of tokens means choosing the boring option, or retiring something first.

## Anti-patterns

- **Resume-driven or hype-driven choices:** tie every choice to a criterion and evidence.
- **Framework before problem:** write requirements and constraints first.
- **Recalled facts:** check live.
- **No exit path:** record a replacement and its migration cost.

## Checklist

1. Problem, workload and non-functional requirements written before any technology is named.
2. The candidates include the boring or incumbent option.
3. Every criterion answered with evidence, or marked unverified.
4. Volatile facts checked live, with date and URL.
5. The version's support window covers the planned life, or there's an upgrade plan.
6. A spike ran on the real target and integrations.
7. Innovation tokens counted and justified.
8. Maturity ring stated.
9. Community health, security record and hiring assessed.
10. Decision, rejected options and an exit path recorded, with a review date.
