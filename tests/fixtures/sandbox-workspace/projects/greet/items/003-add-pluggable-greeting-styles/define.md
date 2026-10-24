# Define: Add pluggable greeting styles

## Goal
A new greeting style can be added in one place, without changing `greet()` or the CLI code.

## In scope
- Styles plain, shout and formal; `--style <name>` on the CLI; `--shout` kept as an alias.

## Out of scope
- Styles loaded from outside the repo.

## Acceptance criteria
1. [ ] `python3 greet.py Ada --style formal` prints `Good day, Ada.`
2. [ ] `--shout` still works and equals `--style shout`.
3. [ ] Adding a style is one new entry in one place, shown in README.
4. [ ] `python3 -m unittest` passes, with a test per style.

## Assumptions
- Standard library only.
