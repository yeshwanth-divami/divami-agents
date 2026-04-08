# How preflight.py Works — Technical Design

`scripts/preflight.py` is a read-only diagnostic script. It takes a stage name and optional module, reads the [manifest](../../glossary#manifest), runs a check suite appropriate for that stage type, and prints a structured pass/fail table. Nothing is written. The only output is stdout and an exit code. The design is deliberately simple — this script runs before every Daksh stage, so it must be fast, dependency-free, and incapable of making things worse.

This TRD implements the PRD at `prd.md`.

---

## Scope

Design covers: `scripts/preflight.py`, `commands/preflight/CONTEXT.md`. Does not cover skill-detectability checks (deferred per PRD).

---

## Architecture

Single Python script, stdlib only. No third-party dependencies. Structure:

```
scripts/preflight.py
  main()              → arg parse → load manifest → run checks → print table → exit
  resolve_key()       → same logic as approve.py (share STAGE_MAP constant)
  run_checks()        → dispatches base_checks + impl_checks if stage == impl
  base_checks()       → manifest present, prior stage approved, prior output exists, hash match
  impl_checks()       → dependencies done, git clean
  print_table()       → formats checklist to stdout
```

The STAGE_MAP in preflight.py is a copy of the one in approve.py. Both are small and stable; sharing via import would create a coupling that's not worth the complexity for a two-file skill.

---

## Check Matrix

Every check has a severity: **HARD** (exits 1 on failure) or **WARN** (printed but exits 0).

| Check | Doc stages 00–40c | Impl stage 50 | Notes |
|-------|:-----------------:|:-------------:|-------|
| Manifest exists | HARD | HARD | `docs/.daksh/manifest.json` present and valid JSON |
| Stage registered in manifest | HARD | HARD | key exists in `manifest.stages` |
| Prior stage approved (count ≥ required) | HARD | HARD | reads `manifest.rules.approvals_per_gate` |
| Prior output doc exists on disk | WARN | HARD | path from prior stage's `manifest.stages[key].output` |
| Prior doc hash matches manifest `doc_hash` | WARN | HARD | sha256 of file vs stored hash — drift means post-approval edit |
| All task dependencies done | — | HARD | from task's `Depends on` field in tasks.md; checks manifest traceability |
| Git working tree clean | — | HARD | `git status --porcelain` returns empty |

**Exit code rules:**
- Any HARD failure → exit 1
- All HARDs pass, ≥1 WARN → exit 0 (stage CONTEXT.md files treat 0 as "proceed")
- All pass, no warnings → exit 0

This resolves PRD OQ-1: WARNs do not block; they are surfaced but stages proceed.

---

## Output Format

```
Preflight: brd
─────────────────────────────────────────────────
[PASS] Manifest exists
[PASS] Stage 20 registered in manifest
[PASS] Prior stage (10/vision) approved: 1/1
[WARN] docs/vision.md hash differs from approval hash (file modified post-approval)
[PASS] docs/vision.md exists on disk
─────────────────────────────────────────────────
Result: PASS with 1 warning. Stage may proceed.
```

```
Preflight: impl AUTH
─────────────────────────────────────────────────
[PASS] Manifest exists
[PASS] Stage 50:AUTH registered in manifest
[PASS] Prior stage (40c:AUTH/tasks) approved: 1/1
[PASS] docs/implementation/AUTH/tasks.md exists on disk
[PASS] docs/implementation/AUTH/trd.md hash matches manifest
[FAIL] Git working tree clean: 2 modified files (git status --porcelain)
[PASS] TASK-AUTH-003 dependency done
─────────────────────────────────────────────────
Result: BLOCKED — 1 hard failure. Resolve before proceeding.
```

---

## Script Interface

```
python scripts/preflight.py <stage> [MODULE]
```

Arguments mirror `approve.py` exactly. Same STAGE_MAP, same weight-class resolution. If manifest is missing, exits 1 immediately: `"ERROR: No Daksh pipeline found. Run /daksh init first."`

---

## commands/preflight/CONTEXT.md

Slim command file (same pattern as approve):

```
## Persona
Safety Inspector. Run the script, show output verbatim.

## Steps
1. Run from project root:
   python scripts/preflight.py <stage> [MODULE]
2. Show output verbatim.
3. If exit 0: "Preflight passed. Proceed with /daksh <stage>."
4. If exit 1: "Preflight blocked. Resolve the FAIL items above before continuing."
```

---

## Technology Choices

| Choice | Why |
|--------|-----|
| Python stdlib only | No install step. Consistent with approve.py. |
| `git status --porcelain` via `subprocess` | Single portable command; empty output = clean tree. |
| SHA-256 via `hashlib` | Identical to approve.py — hashes are comparable. |
| Flat checklist output (not JSON) | Read by a human in a terminal. JSON would require a consumer that doesn't exist. |

---

## Testing Strategy

Unit tests cover each check in isolation using mock manifest dicts and temp files. Integration test: run full preflight against the Daksh project's own manifest (self-hosting). No mocking of the manifest in integration tests — if the real manifest is wrong, the test should catch it.

---

## Open Questions

None. All PRD open questions resolved in this TRD.

---

## Approval

Approved by: Yeshwanth
Role:        PTL
Date:        2026-03-28
Hash:        bceebb7252c0…
