---
id: "{{id}}"
title: {{title}}
kind: feature          # initiative | feature | task | investigation
status: proposed       # proposed | active | blocked | done | dropped
phase: discover        # discover | define | develop | deliver
size: M                # S | M | L: decides which phases run
parent:
depends_on: []       # ids that must be done first
repos: []             # repo folders this item touches
created: {{date}}
updated: {{date}}
---

# {{title}}

## Intent
<!-- One or two sentences: what and why. For S items this is the whole spec. -->

## Log
<!-- Dated, newest last: phase changes, gate approvals, key decisions. -->
- {{date}}: created
