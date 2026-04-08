# What PREFLIGHT Does — and Why It Exists Before Every Stage

Without a pre-stage check, a user can invoke any Daksh [stage](../../glossary#stage) against stale approvals, missing input documents, or a dirty git state — and only discover the problem after burning a full context window on generation that will need to be redone. PREFLIGHT is the circuit breaker. It runs before every stage, reads the same manifest data the stage would read, and produces a pass/fail checklist so the user knows exactly what to fix before proceeding. For [stage](../../glossary#stage) 50 (impl) specifically, the stakes are higher — starting an implementation session against a stale [TRD](../../glossary#stage) or uncommitted local changes produces a [change record](../../glossary#change-record) before the first line of code ships. Preflight prevents that.

This PRD defines the user-facing behavior of `/daksh preflight <stage> [MODULE]`. The TRD (`trd.md`) defines how `scripts/preflight.py` implements it.

This document implements the roadmap at `../../implementation-roadmap.md`, milestone M1.

---

## Scope

**In scope:**
- `scripts/preflight.py` — the preflight script callable from any stage CONTEXT.md
- `/daksh preflight` — the standalone command for manual pre-invocation
- Check coverage for all 8 stages and the impl stage's additional git/hash checks
- `commands/preflight/CONTEXT.md` — the command entry point

**Out of scope:**
- Detecting whether `doc-narrator` or `vyasa` skills are installed (not scriptable from Python; deferred)
- Auto-fixing failed checks — preflight only reports, never mutates
- Integration with CI/CD or git hooks

---

## User Stories

### US-PREFLIGHT-001 — Pre-stage gate check for doc stages {#us-preflight-001}

As a PTL or TL, I can run `/daksh preflight <stage>` before invoking any document stage so that I see a clear pass/fail checklist of gate conditions and input doc availability before the stage consumes my context window.

**Traces to:** [UC-002](../../business-requirements.md) (Run a Pipeline Stage), FR-007

### US-PREFLIGHT-002 — Pre-impl safety check for engineers {#us-preflight-002}

As an engineer, I can run `/daksh preflight impl MODULE` before starting an implementation session so that I know all prerequisites are met: prior stage approved, TRD hash unchanged since approval, task dependencies done, and git working tree clean.

**Traces to:** [UC-005](../../business-requirements.md) (Implement a Task)

### US-PREFLIGHT-003 — Actionable failure messages {#us-preflight-003}

As any user, when preflight exits non-zero, I receive one clear message per failing check so that I know exactly what to fix — not just "something failed."

**Traces to:** [UC-002](../../business-requirements.md), [UC-005](../../business-requirements.md)

---

## Business Rules

### BR-PREFLIGHT-001 — No new gate conditions

Preflight enforces only the same conditions the stage itself enforces. It cannot block a stage that the stage would allow — it is a preview of the stage's own checks, run before context is loaded.

### BR-PREFLIGHT-002 — Impl stage gets additional checks

Stage 50 preflight runs the full base check suite plus: git working tree clean, all declared task dependencies done, and TRD/tasks doc hashes matching their manifest `doc_hash` (no post-approval drift). These are [hard stops](../../glossary#hard-stop) for impl — starting implementation on a stale spec is the fastest way to produce a [change record](../../glossary#change-record).

### BR-PREFLIGHT-003 — Script absence is not a hard stop

If `scripts/preflight.py` does not exist (the PREFLIGHT module has not yet been built), stages must still run. Stage CONTEXT.md files call preflight as a first step — this call must fail gracefully, not abort the session.

### BR-PREFLIGHT-004 — Output is structured and terse

Preflight output is a flat checklist: one line per check, status prefix `[PASS]` / `[FAIL]` / `[WARN]`, one-line explanation on failure. Final line: summary of pass/fail/warn counts and overall exit status.

---

## Acceptance Criteria

| ID | Scenario | Expected |
|----|---------|---------|
| AC-PREFLIGHT-001 | Stage `brd` invoked with vision not approved | Exits 1; `[FAIL] Prior stage (vision) approved: 0/1` |
| AC-PREFLIGHT-002 | All checks pass for any doc stage | Exits 0; every line shows `[PASS]`; summary: "All checks passed." |
| AC-PREFLIGHT-003 | Stage `impl AUTH` with dirty git working tree | Exits 1; `[FAIL] Git working tree clean: uncommitted changes detected` |
| AC-PREFLIGHT-004 | Stage `impl AUTH` with TRD edited after approval | Exits 1; `[FAIL] TRD hash matches manifest: file modified post-approval` |
| AC-PREFLIGHT-005 | Stage `impl AUTH` with a dependency task not done | Exits 1; `[FAIL] Dependency TASK-AUTH-003 not done` |
| AC-PREFLIGHT-006 | Missing output doc for prior stage | Exits 1; `[FAIL] Prior stage output missing: docs/vision.md not found` |
| AC-PREFLIGHT-007 | `scripts/preflight.py` does not exist | Stage session continues with a warning; does not abort |

---

## Data Contract

Preflight reads from:
- `docs/.daksh/manifest.json` — stage status, approvals, doc hashes, modules, weight class
- Prior stage output files — existence check + hash comparison
- Git working tree (impl only) — `git status --porcelain`

Preflight writes nothing. It is read-only.

---

## Open Questions

1. Should WARN exits (non-blocking issues) return exit code 0 or a distinct exit code (e.g. 2)? The TRD should decide — stage CONTEXT.md files currently treat any non-zero as "resolve before continuing."
2. For combined stages (`40a+40b`), which prior stage does preflight check? The roadmap approval, not the combined stage itself.

---

## Approval

Approved by: Yeshwanth
Role:        PTL
Date:        2026-03-28
Hash:        bceebb7252c0…
