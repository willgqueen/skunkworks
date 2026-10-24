# Infrastructure checklist

Use at design time. Answer each question in a sentence, or "n/a, because …".

## Well-Architected pillars

The six pillars of the AWS Well-Architected Framework (verified: https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html). The questions are provider-neutral and our own wording.

**Operational excellence**
- Can we deploy, roll back and observe it without heroics (CI/CD, logs, metrics, alerts)?
- Does every alert have a runbook and an owner?
- Are changes small and reversible, and do incidents get reviewed?

**Security**
- Is access least-privilege, with no shared or long-lived credentials?
- Is data encrypted in transit and at rest, and where do the keys live?
- Where are the trust boundaries, and is untrusted input validated at each?
- Are secrets out of code and images, and dependencies scanned?

**Reliability**
- What are the targets (SLO, RTO, RPO), and does the design meet them?
- What are the single points of failure?
- Are backup, restore and failover tested?
- Do timeouts, retries with backoff and load shedding contain dependency failures?

**Performance efficiency**
- What are the latency and throughput targets, and how are they measured?
- Is each component's compute and storage chosen for its workload?
- How does it scale, and where's the first bottleneck?

**Cost optimization**
- Who owns the bill, and is spend attributable per service?
- Is capacity right-sized, with idle resources shut down and a budget alert?
- What drives cost (compute, egress, storage, per-request), and how does it grow?

**Sustainability**
- Is utilization high, or are we over-provisioning?
- Can batch work be scheduled or reduced, and is there a retention policy?

## Twelve factors

Titles verified at https://12factor.net/; the one-line checks are our paraphrase (unverified against each factor page).

1. **Codebase:** one repo per deployable app, many deploys.
2. **Dependencies:** declared and isolated; nothing implicit from the host.
3. **Config:** environment config lives in the environment, not the code.
4. **Backing services:** databases, queues and caches are attached resources, swappable by config.
5. **Build, release, run:** separate stages; releases immutable and versioned.
6. **Processes:** stateless and share-nothing; state in backing services.
7. **Port binding:** self-contained; serves by binding a port.
8. **Concurrency:** scale out through processes.
9. **Disposability:** fast start, graceful shutdown, crash-safe.
10. **Dev/prod parity:** keep environments as similar as possible.
11. **Logs:** an event stream to stdout; the platform routes it.
12. **Admin processes:** one-off tasks run from the same release and config.

## Managed or self-hosted

| | Managed | Self-hosted |
|---|---|---|
| Operational burden | Low: patching, HA and backups handled | High: upgrades, on-call, capacity |
| Cost | Higher unit price, less staff time | Lower at scale, more staff time |
| Control | Limited | Full |
| Lock-in | Higher with proprietary APIs; lower with standard ones (Postgres, S3 API, Kubernetes) | Low, but you're locked into your own operations |
| Exit cost | Egress, rewrites, retraining | Still work, but under your control |

Default to managed unless control, compliance or unit cost at scale justify the burden. Record the decision and the exit path. (General guidance; unverified.)

## Cost model

Prices change: check the vendor's pricing page or calculator, and record the date.

```
Assumptions (per month): users, requests, GB stored, GB egress, job-hours
Unit costs (URL + date): compute $/hr, storage $/GB, egress $/GB, per-request, support %
Estimate: each line = quantity × unit cost; total = sum + buffer (e.g. 20%)
Sensitivity: total at 0.5× and 2× usage; the largest driver
```

## Infrastructure as code

Fit statements unverified; confirm against each project's docs.
- **Terraform / OpenTofu:** declarative HCL, a large provider ecosystem, multi-cloud. Terraform is BSL-licensed; OpenTofu is the open-source fork.
- **Pulumi:** general-purpose languages; fits teams that want loops, types and tests in infrastructure code.
- **AWS CDK:** general-purpose languages compiled to CloudFormation; AWS only.

Whichever you use: remote, locked state; plans reviewed in CI; never apply by hand.
