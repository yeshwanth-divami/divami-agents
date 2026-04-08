---
description: "Create a gated change set when implementation reality diverges from spec, and percolate the change upward through all affected planning documents."
---

# Command: /daksh change

## Syntax
```
/daksh change [MODULE]
/daksh cr [MODULE]
```

## Persona
Change Planner. Capture the divergence, trace its impact upward through the entire document hierarchy, and create a gated change set that keeps every layer honest. A change that only patches TRD but leaves the BRD lying is not a complete change. You re-plan — you do not execute.

## Pre-checks

1. Read `docs/.daksh/manifest.json`. Check `change_records` for any OPEN CRs
   whose `touched_docs` overlap with the docs you expect to modify. If overlap
   exists, warn: "[doc] is pending approval from [CR-ID]. Approve or resolve
   that CR before raising a new change against the same document." Let the
   engineer decide whether to proceed or resolve the overlap first.

## Steps

1. **Read the full module spec stack:** `tasks.md`, `trd.md`, `prd.md` for the module. Understand current state before asking anything.

2. **Ask only for missing facts:** divergence, impact, proposed resolution, raised-by. If affected tasks are ambiguous, ask for confirmation.

3. **Percolation analysis — mandatory before scaffolding.**

   Read upstream docs in order: `prd.md` → `docs/business-requirements.md` → `docs/implementation-roadmap.md` → `docs/vision.md` → `docs/client-context.md`.

   For each upstream document, ask: *does this change invalidate, extend, or contradict anything in that document?*

   Build the full `touched_docs` list bottom-up:

   | Layer | Touch if… |
   |-------|-----------|
   | `tasks.md` | Tasks are added, removed, or reordered |
   | `trd.md` | Technical design, APIs, or data model changes |
   | `prd.md` | User stories, business rules, or ACs change |
   | `business-requirements.md` | A UC, FR, or scope boundary changes |
   | `implementation-roadmap.md` | Module scope, sprint plan, or cross-module contracts change |
   | `vision.md` | A core capability, problem statement, or scope changes |
   | `client-context.md` | A constraint, assumption, or user type changes |

   Stop ascending when a layer is genuinely unaffected. But lean toward inclusion — a false positive is cheaper than a stale upstream doc.

   The highest touched layer determines the tier and approval authority. Do not artificially cap the tier.

4. **Run `change.py` to scaffold the CR and update manifest state:**

   ```bash
   python scripts/change.py \
     --module [MODULE] \
     --title "[One-line description]" \
     --raised-by "[Name]" \
     --touched-docs "[comma-separated doc paths, all layers]" \
     [--tier TIER] \
     [--affected-tasks "TASK-X-001,TASK-X-003"]
   ```

   The script will:
   - Check for overlapping open CRs (warns, does not block)
   - Allocate the next `CR-NNN`
   - Scaffold the CR document at `docs/implementation/[MODULE]/change-records/CR-NNN.md`
   - Mark **all** touched stages as `pending_approval` in the manifest (including upstream stages)
   - Allocate a change task ID (`TASK-[MODULE]-NNN`)
   - Add the CR to `manifest.change_records` and the change task to `manifest.traceability`
   - Git commit the scaffold + manifest

5. **Fill in the CR document.** Write the narrative for: What was specified, What reality showed, Impact, Proposed resolution.

6. **Produce the full change summary before touching any doc.** Work top-down (upstream first), listing the specific sections that will change at each layer and why:

   ```
   ### Changes to docs/vision.md
   - §Core Capabilities: add capability for [X]

   ### Changes to docs/business-requirements.md
   - §Use Cases: add UC-NNN / extend UC-NNN with FR-NNN

   ### Changes to docs/implementation/[MODULE]/prd.md
   - §User Stories: add US-[MODULE]-NNN
   - §Business Rules: add BR-[MODULE]-NNN

   ### Changes to docs/implementation/[MODULE]/trd.md
   - §Data Model: add field [X] to [entity]

   ### Changes to docs/implementation/[MODULE]/tasks.md
   - New task: TASK-[MODULE]-NNN (change task for CR-NNN)
   ```

   Write this into the CR's `## Change Summary` section. This is the contract — nothing gets patched that isn't listed here.

7. **Apply patches top-down (upstream first).** For each document in the change summary, apply only the listed changes. Do not reorganize, reformat, or "improve" untouched sections.

   The following mutations require explicit confirmation before proceeding:
   - Removing a UC, FR, or user story (prefer marking as `deprecated` with rationale)
   - Removing tasks (prefer marking as `cancelled` with rationale)
   - Changing ACs on tasks already `In Progress` in Jira

8. `change.py` has already appended a skeleton change task to `tasks.md`.
   Review it and refine if needed. Do **not** create a duplicate entry.

9. Do **not** push the change task to Jira yet. The Jira push happens when
   `/daksh approve CR-NNN` resolves the change set.

10. If `docs/implementation/[MODULE]/.vyasa` exists and does not include
    `"change-records"` in `order`, append it.

11. Git commit the filled CR, all patched docs (all layers), and updated tasks.md.

12. Tell the user:
    "Change set written. Touched layers: [list]. Run `/daksh approve CR-NNN` before
    `/daksh impl start [change-task-id]`."

## Approval Authority

The `tier` field determines who can approve the CR. The further upstream the
change reaches, the heavier the gate:

| Highest doc touched | Tier value | Required approver |
|---|---|---|
| `tasks.md` only | `tasks` | TL |
| TRD | `trd` | TL or PTL |
| PRD | `prd` | PTL |
| BRD or roadmap | `brd` / `roadmap` | PTL + Client |

`approve.py` enforces this via the `tier` field in `manifest.change_records`.

## Rules

- This command is the **only** way to create change records. Stage 50's
  CONTEXT.md redirects engineers here. Hand-written CRs bypass governance.
- Apply `doc-narrator` writing patterns when patching planning docs.
- All documentation updates must follow Vyasa conventions.
- When writing CRs or doc updates, run `python scripts/extract-file-headings.py docs/glossary.md`
  to get the current term index, then link Daksh terms on first use.
