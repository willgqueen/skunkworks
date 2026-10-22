# Process

The working method: a **Double Diamond outer frame** with a **spec-driven file per phase**, scaled by size so small work skips the heavy steps.

## Phases

| Phase | Diamond | Mode | Question | Output |
|---|---|---|---|---|
| Discover | 1 | Diverge | What's really going on? | `discover.md` |
| Define | 1 | Converge | What exactly will we solve, and how will we know? | `define.md` |
| Develop | 2 | Diverge, then converge | How should we build it? | `develop.md` |
| Deliver | 2 | Converge | Build it, verify it, ship it | `deliver.md` + code |

Each phase ends at a **gate**: the user approves the phase doc before the next phase starts. A gate can be waived explicitly ("skip to deliver").

## Sizing

Every item is sized when it's created. The size picks the path:

| Size | Typical work | Phases |
|---|---|---|
| S | Typo, small bug fix, config tweak | Deliver (a one-line intent in `item.md`) |
| M | Clear feature or bug with a known approach | Define → Deliver (light Develop inside `define.md`) |
| L | Ambiguous, cross-cutting or risky work | Discover → Define → Develop → Deliver |

An `investigation` runs Discover → Define (the question and what would answer it), then ends with findings in `deliver.md` and no code.

When work turns out bigger than its size, re-size it and back up to the missing phase rather than pushing on.

## Why this combination

- Double Diamond keeps problem exploration apart from solution work, which matters most for ambiguous items.
- A file per phase gives agents a stable handoff: each phase reads the previous file instead of relying on chat history.
- Sizing keeps the process from slowing down routine work.

Other methods considered: Shape Up (its *appetite* idea may be borrowed later as an effort budget per item), and RFC/ADR-only flows (ADRs are kept inside `develop.md`).

## Building blocks

The toolkit is built bottom-up:

1. **Foundation**: project `.claude/` setup, workspace, templates, this process. *(done)*
2. **Atomic skills**: one job each, e.g. understand a repo, write a spec, plan, implement a task, test, review, open a PR.
3. **Phase commands**: chain atomic skills for one phase and stop at its gate.
4. **Orchestrator**: one entry point that creates or resumes an item, sizes it, and routes it.
