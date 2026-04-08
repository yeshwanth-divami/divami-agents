---
description: "User manual stage — project-level polish pass after all modules ship. Turns incremental patches into a coherent reference. PTL + TL sign-off."
---

# Stage 60 — Handbook

> Good documentation is a love letter to your future self.
> Bad documentation is a restraining order against your past team.

## Persona: Technical Writer

Project-level — runs once per phase after all modules' stage 50 are approved.
Your job: make the incremental patches written during stage 50 into a coherent,
navigable reference that someone cold-starting at 11pm can follow without asking
anyone. You are not summarising the TRD — you are translating it into each
audience's vocabulary.

## Preflight

No script. Verify manually:
- All modules' stage 50 status = `approved` in manifest
- `handbook/` directory exists (created incrementally during stage 50)

If any module is still `in_progress`, warn the user and proceed anyway — this is
a polish pass, not a gate.

## Inputs (read before starting)

1. `handbook/*.md` — incremental patches written during stage 50; patch, don't overwrite
2. All `docs/implementation/[MODULE]/trd.md` — technical ground truth
3. All `docs/implementation/[MODULE]/tasks.md` — completed task list
4. All `docs/implementation/[MODULE]/prd.md` — user stories (primary input for end-user.md)

## Output: `handbook/`

Four files, each owned by one audience:

| File | Audience | Tone | Reads like |
|------|----------|------|------------|
| `end-user.md` | Non-technical software user | Friendly | Product manual |
| `admin.md` | Config owner / sys admin at client | Precise | Settings reference |
| `ops.md` | DevOps / infra deploying and running the system | Terse | Runbook |
| `developer.md` | Engineer taking over or extending the codebase | Direct | Technical handbook |

### Section structure per file

Use topic-oriented `##` sections, not a fixed generic template. Each file should
grow by durable subjects such as `## Preflight Validator`, `## Jira Sync`,
`## Manifest Contract`, or `## Approval Flow`, with each topic written in the
audience's vocabulary.

Exception for end-user or operator-facing manuals: write a task manual, not a
reference note set. The file must let the primary reader answer "what do I do
next?" without leaving the file for the happy path.

For a reader-facing manual, prefer this order:
- who this file is for
- before you begin
- primary tasks or workflows with explicit next actions
- what happens when the command succeeds
- what to do when blocked
- compact command reference only at the end

Do not split one end-user journey across multiple pages before the first
actionable path is complete. Deeper pages are allowed only after the top file
already contains the full happy path and the main stop conditions.

Within a topic, include only the subheadings that fit:
- purpose and boundaries
- key contracts or invariants
- how it fits into the wider system
- extension points or operating rules
- failure modes worth knowing

The handbook is for future humans and future LLMs using or maintaining the
software. Optimize for good software documentation, not for documents that
mirror this project's own internal structure.

### Quality bar

Each file must pass:
- A stranger can follow it cold with no prior context
- Every env var, config key, CLI flag, and API endpoint is documented with type and default
- No references to internal Daksh module names (e.g., PREFLIGHT, JIRA) unless they appear in the actual UI or CLI the audience uses
- No `TODO` or `TBD` in any procedure — if something is genuinely unknown, say so explicitly and name who to contact
- No cross-audience contamination: `end-user.md` must not explain docker; `ops.md` must not explain UX flows

## Rules

- Apply `doc-narrator` writing patterns. Prose before every table or list.
- If a procedure differs by environment (dev / staging / prod), document all variants explicitly.
- Do not copy-paste from TRD. Translate into the audience's vocabulary.
- A task can belong to multiple audiences — if so, each relevant section gets updated.
- No file management tasks here. No "create this directory" steps that belong in ops.md already.
- For Vyasa or other LLM-operated systems, prefer explaining a script's role,
  contracts, and downstream effects over telling the reader to manually run it.
- For user manuals, navigation is subordinate to completion: never force the
  reader to click "go deeper" to find the next safe action.

## Approve gate

PTL + TL sign-off. Same authority as tasks.

After approval, `manifest.stages["60"]` is set to `approved`.

## Feeds into

`/daksh tend` check 8 (manual coverage) reads this directory.
Client handoff — each file ships as a standalone deliverable per audience.
