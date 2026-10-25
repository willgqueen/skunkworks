---
id: "002"
title: Reorganize the tests
kind: task
status: proposed
phase: define
size: M
parent: 
depends_on: []
repos: [target]
created: {{today}}
updated: {{today}}
---

# Reorganize the tests

## Intent
Replace `test_greet.py` with one test module per behavior (`test_greeting.py`, `test_shout.py`) sharing a `helpers.py`, without changing what the tests check.

## Log
- {{today}}: created
