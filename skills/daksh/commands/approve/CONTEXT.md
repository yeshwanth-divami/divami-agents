---
description: "Approve or flag for revision a Daksh stage gate."
---

# Command: /daksh approve

## Persona
Gate Keeper. Collect identity, run the script, show output verbatim.

## Syntax
```
/daksh approve <stage> [MODULE] [--revise]
/daksh approve CR-NNN
```
`stage`: `brd` · `roadmap` · `vision` · `onboard` · `prd` · `trd` · `tasks` · `impl`
`MODULE`: required for `prd`, `trd`, `tasks`, `impl`

## Steps

1. Identify the approver from the user's message. If not stated, ask: "Who is approving?"
2. If `--revise`, ask for a one-line reason if not provided.
3. If the target is `CR-NNN`, run from project root:
   ```
   python scripts/approve.py CR-NNN --approver "<name>"
   ```
   The script handles: tier-based authority check, approval block in the CR,
   status flip to RESOLVED, restoring all touched docs to `approved`, hashing,
   and git commit. Show output verbatim.
   If the script exits 0 **and** the CR status is now RESOLVED, read the CR's
   `module` field from `manifest.change_records[CR-NNN].module` and push:
   ```
   python scripts/jira-sync.py push --module <resolved-module>
   ```
   (The module is always available in the manifest — do not guess it from args.)
4. Otherwise, run from project root:
   ```
   python scripts/approve.py <stage> [MODULE] --approver "<name>" [--revise --reason "<reason>"]
   ```
5. Show the script output verbatim.
6. If stage is `tasks` and approve.py exited 0, auto-push to Jira:
   ```
   python scripts/jira-sync.py push --module MODULE
   ```
   Show output verbatim. If exit non-zero: "Jira push failed — tasks are approved but not yet in Jira. Run `/daksh jira push` manually after resolving the error."

**Stage `impl` precondition (enforced by the script):** `approve.py` will exit 1
if any `TASK-[MODULE]-NNN` in `manifest.traceability` is not `done`. Resolve each
blocker (mark tasks done via `/daksh impl done TASK-ID` or update traceability
directly if the task predates the traceability contract) before running the
approval again.

**Stage 60 gate:** `50:[MODULE]` approval is the upstream gate for stage 60
(handbook). Once `50:[MODULE]` is `approved`, `/daksh preflight 60 MODULE` will
pass the prior-stage check and the handbook stage can proceed.
