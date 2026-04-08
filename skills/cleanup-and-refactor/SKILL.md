---
name: cleanup-and-refactor
description: Cleans up working feature code after iterative chat-driven development. Use when code now works but contains dead paths, duplicate logic, or refactor debt from back-and-forth implementation. Produces a narrowed cleanup plan, one verification pass, and a commit-ready summary.
argument-hint: "[feature scope, repo state, or cleanup goal]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Cleanup And Refactor

This skill is the janitor after the renovation. Once a feature is working, it trims abandoned code, removes waste from iterative edits, applies bounded refactors inside the validated scope, runs one focused verification pass, and leaves a concise summary of what is safe to commit.

---

## Core Principle

> Preserve the working behavior, cut the scaffolding. Refactor only where the code became messy during feature discovery, not as an excuse to redesign the building.

---

## On Startup

Read `references/trigger-and-scope.md` before doing anything else.

---

## Workflow

### Phase 1 — Confirm Scope

Identify the working feature scope, the files touched during the chat, and the expected verification boundary.

### Phase 2 — Remove Waste

Delete dead code, abandoned branches, duplicate helpers, commented leftovers, and temporary structure that no longer serves the working implementation.

### Phase 3 — Refactor Safely

Tighten names, boundaries, and shared logic only inside the active scope and only when the refactor reduces risk or repetition.

### Phase 4 — Verify Once

Run the narrowest relevant test or validation pass one time, then capture the cleanup result and remaining risks.

## Routing

| Input signal | Load |
|---|---|
| "clean this up", "refactor this mess", or working code after feature churn | `references/trigger-and-scope.md` + `references/cleanup-heuristics.md` |
| Need guardrails before touching structure | `references/refactor-guardrails.md` |
| Need to choose or report verification | `references/verification-strategy.md` + `templates/verification-note.md` |
| Need final handoff output | `references/reporting-standard.md` + `templates/cleanup-report.md` |
