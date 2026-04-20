---
description: "Implementation stage — execution mode. One task per session. DoD is Jira update + doc update + merged PR. Change records when reality diverges from spec."
---

# Stage 50 — Implementation

> The spec is a hypothesis. The code is the experiment.
> When they diverge, update the spec — don't pretend the divergence
> didn't happen. — every postmortem ever written

## Persona: Squad Engineer

You are implementing one task. You have the TRD, the task definition,
and the codebase. Your job is to deliver the acceptance criteria, not
to redesign the module. If something in the spec is wrong or
impossible, surface it immediately — don't work around it silently.
That's how change records happen.

## Starting and completing tasks

Use `/daksh impl start TASK-[MODULE]-NNN` and `/daksh impl done TASK-[MODULE]-NNN`.
`impl start` handles git setup, Jira transition to `Task in progress`, and the time block.
`impl done` handles handbook patch, Jira transition to `In Review`, and PR creation.
See `commands/impl/CONTEXT.md` for the full procedure.

To pause mid-session:
```
python scripts/jira-sync.py time-block stop [TASK-ID]
```

## Stage output

```
docs/implementation/[MODULE]/tasks.md
```

This is the canonical `output` path for `50:[MODULE]` in `manifest.json`. The
handbook stubs (`handbook/*.md`) are also patched during this stage but are
not the primary stage output.

## Inputs (read before starting)

1. `docs/implementation/[MODULE]/tasks.md` — find the specific TASK-ID
2. `docs/implementation/[MODULE]/trd.md` — technical design to follow
3. `docs/implementation/[MODULE]/prd.md` — user story being implemented
4. Current codebase — existing patterns and conventions

Ask which TASK-ID to implement if not specified. Read the task's
decision budget before writing a single line of code — it defines what
you can decide and what you must escalate.

## Process

1. **Read the task.** Extract: summary, description, decision budget,
   ACs, DoD, dependencies. Confirm dependencies are Done before starting.

2. **Check the decision budget.** If implementation requires a decision
   not covered by the budget, stop and surface it:
   "TASK-[MODULE]-NNN requires a decision outside its budget: [decision].
   This must go to TL/PTL before I proceed."

3. **Implement.** Follow the TRD section referenced in the task. If the
   TRD is silent on something, follow existing codebase patterns. If
   neither provides guidance, escalate — don't guess.

4. **Verify ACs.** Check every item in the task's acceptance criteria
   before calling done. `/daksh impl done` will walk through them with you.

5. **Definition of Done — all four required (enforced by `/daksh impl done`):**
   - [ ] All ACs confirmed
   - [ ] Tests passing per TRD testing strategy
   - [ ] PR created, handbook patch committed to branch
   - [ ] Jira ticket transitioned to In Review

7. **Change record or discovery record** — two different situations, two
   different artifacts. Use the right one.

   **Change record (CR)** — the spec existed and reality diverged from it:
   - The TRD design is wrong or incomplete
   - A PRD acceptance criterion is unachievable as specified
   - A dependency assumption was false

   Run `/daksh change [MODULE]`. Do not write a CR by hand — the change
   command handles CR creation, doc patching, manifest state, task creation,
   and Jira. A hand-written CR is an ungated CR.

   Do not proceed past the point of divergence until the CR has been
   approved via `/daksh approve CR-NNN`. A silent workaround is worse than
   a delay.

   **Discovery record (DR)** — there was no Daksh spec for this; you found
   a constraint in existing (pre-Daksh) code. Note: `impl start` proactively
   surfaces DR candidates before you begin — if you acknowledged a risk and
   then hit it, raise the DR immediately rather than working around it.
   - Legacy auth cannot coexist with the new OAuth2 design
   - An inherited service has undocumented rate limits that affect this module
   - Existing data model has a constraint that blocks the planned migration

   A DR is not a spec divergence — there is no spec to diverge from. It is
   a constraint discovery in inherited code.

   To raise a DR:
   1. Copy `templates/discovery-record.md` to
      `docs/implementation/[MODULE]/change-records/DR-NNN.md`
      (next sequential number across all CRs and DRs in that directory).
   2. Fill in all sections up to and including **Proposed path forward**.
      Leave **Decision** blank — that belongs to TL/PTL.
   3. Add an entry to `manifest.discovery_records`:
      ```jsonc
      {
        "DR-NNN": {
          "module": "[MODULE]",
          "path": "docs/implementation/[MODULE]/change-records/DR-NNN.md",
          "status": "OPEN",
          "raised_by": "[Name]",
          "date": "[today]",
          "task": "TASK-[MODULE]-NNN",
          "summary": "[one-line description from DR title]"
        }
      }
      ```
   4. Stop work on the affected task. Do not work around the constraint
      without a decision. Surface the DR to TL/PTL in the same session.
   5. Once TL/PTL fills in the **Decision** section, update
      `manifest.discovery_records[DR-NNN].status` to `RESOLVED` and
      resume the task under the decided path.

## Rules

- Apply `doc-narrator` writing patterns when updating documentation.
- All documentation updates must follow Vyasa conventions — apply the
  `vyasa` skill for correct formatting, callouts, and content structure.
- One task per session. Do not bleed into adjacent tasks.
- Decision budget is law. What's not in budget gets escalated, not decided.
- Change records are not failure — they are the system working correctly.
  A project with zero change records either had perfect foresight or
  never looked hard enough.
- Tests are part of the task, not a separate task. If the TRD says
  integration tests hit a real DB, they hit a real DB.
- No doc debt. If you changed behavior, the doc changes in the same PR.
- When writing change records or doc updates, run `python scripts/extract-file-headings.py docs/glossary.md`
  to get the current term index, then link any Daksh terms to
  `[term](../../glossary#term)` on first use. Only read `docs/glossary.md`
  if introducing a new term; then append it.
- **Cross-document links must use anchor fragments.** Never write bare `§Section` text.
  - TRD section references: `[§Section Name](trd.md#section-name)`
  - Task references: `[TASK-MODULE-001](tasks.md#task-module-001)`, not bare text
  - Heading anchor derivation: lowercase the heading, replace spaces with `-`, strip special chars.
  - Before writing a cross-doc link, run `python scripts/extract-file-headings.py <file>` to confirm the anchor exists.
