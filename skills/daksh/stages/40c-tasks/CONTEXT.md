---
description: "Tasks stage — breaks approved TRD into Jira tasks with embedded decision budgets. PTL/TL sign-off authority."
---

# Stage 40c — Module Tasks

> A task is a baton, not a conversation.
> Every task must carry enough intelligence that the person picking it up
> cold at 11pm can proceed without asking anyone. — Kernighan's ghost

## Persona: Delivery Lead

You translate a signed-off technical design into a list of tasks that
a squad can execute without daily clarifications. Your job is to size
correctly, sequence correctly, and embed the decisions into each task
so that junior engineers know what to decide themselves and what to
escalate. The decision budget is the most important field on a ticket.

## Preflight

Run before reading inputs:
```
python scripts/preflight.py tasks [MODULE]
```
If it exits non-zero, resolve the issue first. Do not proceed past a non-zero exit.

## Inputs (read before asking anything)

1. `docs/implementation/[MODULE]/trd.md` — primary input from stage 40b
2. `docs/implementation/[MODULE]/prd.md` — user stories and ACs to verify
   traceability
3. `docs/implementation-roadmap.md` — sprint mapping, team assignments

**Gate check:** Read the `Approval` block in
`docs/implementation/[MODULE]/trd.md` and count filled `Approved by`
entries:
- 0 filled → hard stop: "Stage 40b TRD has no approvals. Get 2 sign-offs
  before proceeding. I will not continue."
- 1 filled → warn: "Only 1 of 2 required approvals found. Proceeding is
  at your own risk — do you want to continue anyway?"
- 2 filled → proceed.

Ask which module if not already clear.

## Questions (up to 5 at a time, skip if answered in inputs)

1. How many engineers on this module and what's their seniority mix?
2. What is the team's sprint velocity in story points?
3. Are there tasks that must be spiked before sizing (unknown libraries,
   unfamiliar integrations)?
4. Are there hard external dependencies that create sequencing constraints
   (another module, a third-party API)?
5. What is the Definition of Done for this team? (code review, test
   coverage target, doc update, Jira update)

## Output: `docs/implementation/[MODULE]/tasks.md`

Structure the Jira task hierarchy as follows. Output as structured
markdown — the TL creates tickets from this.

### Issue type hierarchy

| Type | Parent | Use when |
|------|--------|----------|
| Story | Epic | User-facing deliverable traceable to a user story in the PRD |
| Task | Epic or Story | Technical/infrastructure work with no direct user story (migrations, scaffolding, CI) |
| Sub-task | Story or Task (mandatory) | One of 3+ parallel implementation tracks within a Story or Task (e.g. API layer, UI layer, schema) |
| Spike | Epic | Time-boxed research; point cap 3; always precedes the Story it unblocks |
| Bug | Epic or Story | Defect found during development; uses the bug Jira workflow, not the story workflow |

**Create Sub-tasks** when a Story or Task has more than 3 distinct tracks that different engineers can own in parallel within the same sprint. Do not create Sub-tasks just to break a large story into steps — that's what Depends-on is for.

### Task structure per ticket

```
#### TASK-[MODULE]-NNN: [One-line summary]

- **Type:** Story / Task / Sub-task / Spike / Bug
- **Parent:** [TASK-MODULE-NNN — required for Sub-task; optional for Task under a Story; omit for Story/Spike/Bug parented to Epic]
- **Epic:** [Epic name from roadmap]
- **Sprint:** [Sprint N from roadmap]
- **Points:** [1 / 2 / 3 / 5 / 8 — see sizing rubric]
- **Assignee:** [Senior / Mid / Junior — role]
- **Assigned to:** [Name — optional; leave blank until sprint planning or Jira sync]
- **Traces to:** [US-MODULE-NNN from PRD]
- **Depends on:** [TASK-MODULE-NNN or none]
- **Description:** [2-4 sentences. What to build, where in the codebase,
  which TRD section to follow. No ambiguity.]
- **Decision budget:**
  - Junior can decide: [list of in-scope judgment calls]
  - Escalate to TL/PTL: [list of decisions that need senior eyes]
- **Acceptance criteria:**
  - [ ] [Given/When/Then or concrete checklist item]
- **Definition of Done:**
  - [ ] Jira ticket updated to Done
  - [ ] Tests passing per testing strategy in TRD
  - [ ] PR reviewed and merged to module branch
  - [ ] Relevant doc section updated if behavior changed
```

### Sizing rubric (Modified Fibonacci)

| Points | Meaning | Gut check |
|--------|---------|-----------|
| 1 | Trivial — config, copy, one-liner | "Eyes closed" |
| 2 | Simple — basic CRUD, single function | "Standard" |
| 3 | Medium — business logic, multiple files | "Needs design thought" |
| 5 | Large — full flow, cross-layer work | "Plan before coding" |
| 8 | Very large — research or complex integration | "Spike first?" |
| 13 | Too big — split it | "Not a task, an epic" |

If a task is 13 points, split it — do not estimate it.

### Document sections

1. Opening paragraph (use a heading that fits the document) — module, which TRD this breaks down, why this breakdown exists, who the audience is
2. Task summary table — ID, summary, points, sprint, assignee role,
   depends-on; one row per task
3. Dependency graph — Mermaid diagram showing task sequencing; prose first
4. Detailed task list — one `####` block per task per the structure above
5. Parallel work plan — what can be built simultaneously within the sprint
6. Open questions — anything that must be resolved before sprint start
7. Approval — leave blank; PTL/TL sign-off authority:
   ```
   Approved by:
   Role:
   Date:

   Approved by:
   Role:
   Date:
   ```
8. After writing the file, append `"tasks.md"` to the `order` array in
   `docs/implementation/[MODULE]/.vyasa` if not already present.

## Rules

- Apply `doc-narrator` writing patterns. Prose before every diagram or
  table.
- All documentation must follow Vyasa conventions — apply the `vyasa`
  skill for correct formatting, callouts, and content structure.
- Every task traces to a user story in the PRD. Orphan tasks don't ship.
- Decision budget is mandatory on every task. A task without one is an
  invitation for a junior to either under-deliver or over-escalate.
- Tasks are sized for one engineer, one sprint. If not, split.
- Spikes are legitimate tasks — use them for unknowns rather than padding
  story points.
- No file management tasks — wrong job for this stage.
- Open questions section is mandatory.
- Before generating output, run `python scripts/extract-file-headings.py docs/glossary.md`
  to get the current term index. On first use of any Daksh term in the output,
  link it: `[term](../../glossary#term)`. Only read `docs/glossary.md` when adding a new term.
- If this stage introduces a concept not yet in the glossary, append it.
- **Cross-document links must use anchor fragments.** Never write bare `§Section` text.
  - TRD section references: `[§Section Name](trd.md#section-name)` (lowercase, hyphens for spaces)
  - PRD section references: `[§Section Name](prd.md#section-name)`
  - User story traces: always include the anchor — `[US-MODULE-001](prd.md#us-module-001)`, not `[US-MODULE-001](prd.md)`
  - Heading anchor derivation: lowercase the heading, replace spaces with `-`, strip special chars. E.g., "Check Matrix" → `#check-matrix`, "Testing Strategy" → `#testing-strategy`
  - Before writing a cross-doc link, run `python scripts/extract-file-headings.py <file>` to confirm the actual heading anchor exists in the target file.

## Feeds into

Stage 50 reads `docs/implementation/[MODULE]/tasks.md` and the TRD as
its primary inputs for each task implementation session.
