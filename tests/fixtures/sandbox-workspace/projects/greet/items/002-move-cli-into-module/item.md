---
id: "002"
title: Move the CLI into cli.py
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

# Move the CLI into cli.py

## Intent
Move argument parsing and `main()` from `greet.py` into a new `cli.py`, with its own tests, so `greet()` stays a plain function. The CLI's behavior doesn't change.

## Log
- {{today}}: created
