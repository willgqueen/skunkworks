---
name: split
description: Check whether work is too big for one item and, if so, propose splitting it along natural seams into right-sized items, then apply the user's choice. Called by new-item, discover, define and develop with what each knows; also run directly.
argument-hint: <project> <item id or slug> | <description of new work>
---

# split

Apply [criteria.md#splitting](../../../docs/criteria.md#splitting) exactly.

## 1. Check

If the item is already an initiative, return: its children are checked when they're created.

Otherwise, using what the caller knows (a description, discover.md, the draft spec, or the task list), test the too-big caps and signals. If none hold, say "fits one item" in one line and return.

## 2. Propose

- Find the seams, in the criteria's order of preference. Never split by layer or activity.
- List the candidate items: title, kind, size, the seam it follows, one line of scope, and `depends_on` only where a re-cut can't remove it. Order them per the criteria, and detail only as far as the work's specificity allows.
- Name the cap or signal that fired.

Ask the user to choose:
- **an initiative with children** (the default)
- **sibling items**
- **keep it whole**

## 3. Apply

When **new-item** is the caller, no item exists yet: it creates the initiative, the siblings, or the single item as chosen, then logs the lines below in what it created.

- **Initiative:** set `kind: initiative` and `size: L`, and log `- <date>: re-kinded <old>→initiative: <signal>` (skip that line when new-item created it). Create each child with **new-item**, with `parent` and `depends_on` set, and list each child's id in define.md's Breakdown if it exists. Set `phase: deliver` if define is approved, otherwise `phase: define`. **The calling phase skill stops here:** an initiative's children carry their own design.
- **Siblings:** create each one with **new-item**, then narrow the original item's Intent (and define.md, if drafted) to what's left.
- **Keep whole:** change nothing.

Log `- <date>: split: <choice>` (`initiative`, `siblings <ids>` or `kept whole: <reason>`) and return to the caller.
