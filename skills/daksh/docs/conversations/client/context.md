# Daksh Redesign — Full Conversation Record

## Who and What

**Yeshwanth** is building Daksh — a structured AI-assisted product development lifecycle
skill for **Divami**, a 100-engineer software services firm. Divami builds products for
clients end-to-end: discovery → delivery. Daksh is the discipline layer that prevents
the typical failure modes at each stage.

Daksh's two north stars:
1. **Highest documentation standards** — technically accurate AND consumable. The
   doc-narrator skill and its "write for the junior reading this cold at 11pm" principle
   is the benchmark.
2. **Tight coupling of docs + code + Jira tickets throughout the software lifecycle.**
   Every artifact must trace back to something real and forward to something actionable.

---

## The Origin Problem

The original Daksh was a "chatmode" format skill — a flat prompt file per stage with no
gates, no lineage, no approval mechanism, and no theory behind the stage design. Stages
were essentially "ask some questions and generate a doc." There was also a combined
40-module stage that was an escape hatch bypassing all tollgates.

Yeshwanth's goal: convert Daksh to ICM format (Interpretable Context Methodology) —
filesystem-based, layered, one-stage-one-job, with human review gates between every
stage. The redesign was grounded in theory: filmmaking (locked script before shoot),
NASA (phase gates), double diamond (diverge/converge), Lean Startup (validated learning).

---

## Yeshwanth's Philosophies and Demands

**On discipline:**
"I'm assuming discipline will come if we create good Daksh modes. The skill should be
so good it's easier to use than not use."

**On Agile's failure modes:**
Yeshwanth is skeptical of Agile in the AI age. Specifically: Agile's flexibility becomes
an excuse for no discipline. He'd read Eric Reis' *The Lean Startup* and was interested
in what's worth preserving from it (validated learning, build-measure-learn) vs. what
breaks down at scale or in a services context.

**On the role of Daksh vs. engineers:**
Daksh should generate Jira tickets (not just consume them). Tickets carry embedded
**decision budgets** — pre-classifying which decisions are junior-scoped vs. need
TL/PTL eyes. This prevents both under-escalation and over-escalation.

**On approval gates:**
- 0 approvals: hard stop. No exceptions.
- 1 approval: warn and ask if they want to proceed at their own risk.
- 2 approvals: proceed.
This came from a specific demand: "make the gates verify with 2 people instead of 1."

**On doc quality:**
"The document you wrote yesterday is already lying to someone." Yeshwanth added the
"Zen of Daksh" section to SKILL.md as a set of design principles, not decorations.

**On token efficiency:**
Yeshwanth explicitly called out that drafting in chat before writing to file doubles
token output. Correction: write directly to the file, let him review there.

**On invented paths:**
When I wrote `prior-project/docs/implementation/` in stage 30, Yeshwanth caught it
immediately: "who made-up path with no convention behind it? if it was you — why?"
Correct convention: `docs/implementation/[MODULE]/change-records/` — always the same
tree, PTL drops files there before running the stage.

**On vyasa references:**
Don't copy doc-narrator or vyasa files into the skill. Reference the skill by name.
Daksh invokes those skills, it doesn't own their content.

---

## My Pushbacks

**On the 40-all-in-one stage:**
I flagged that the combined `40-module/CONTEXT.md` was an escape hatch that bypassed
tollgates. It had to die. We kept only 40a/40b/40c.

**On "phase N" scoping in 40a/40b:**
The old PRD and TRD stages had a "Phase 1 / Phase 2+" scoping ceremony — present 3-4
options, wait for selection. I killed this in the rewrite. It was a consultant's hedge,
not a discipline. One PRD per module. One TRD per module. If scope changes, write a
change record.

**On the `prior-project` ghost path:**
I wrote it, I caught it after Yeshwanth called it out, I fixed it. The lesson: invented
paths are the same as invented facts — they propagate silently until someone hits a wall.

---

## Key Design Decisions Made

### Stage structure
```
00 — Client Onboarding        → docs/client-context.md
10 — Vision                   → docs/vision.md
20 — Business Requirements    → docs/business-requirements.md
30 — Roadmap                  → docs/implementation-roadmap.md + Jira epics/sprints/stories
40a — Module PRD              → docs/implementation/[MODULE]/prd.md
40b — Module TRD              → docs/implementation/[MODULE]/trd.md
40c — Module Tasks            → docs/implementation/[MODULE]/tasks.md
50  — Implementation          → code + PR + doc update + change record if needed
```

### Approval gate pattern
Every output doc ends with a 2-slot approval block. The next stage reads and counts
filled entries before doing anything. The block lives in the output doc itself — not a
separate file.

### Decision budget (40c and 50)
Every Jira task has a `Decision budget` field:
- Junior can decide: [list]
- Escalate to TL/PTL: [list]

This is the mechanism that makes execution mode safe for a mixed-seniority squad.

### Change records (50)
When reality diverges from the TRD during implementation:
1. Stop at the point of divergence.
2. Write `docs/implementation/[MODULE]/change-records/CR-NNN.md`.
3. Do not proceed until TL/PTL fills in the Decision field.

"A project with zero change records either had perfect foresight or never looked hard enough."

### Cross-module contracts (30)
The roadmap stage produces a mandatory cross-module contracts section. This surfaces
integration surfaces owned at PTL level — which team produces, which consumes, what the
contract is.

### Orphan rule
Orphan FRs don't ship (stage 20). Orphan stories don't ship (stage 40a). Orphan tasks
don't ship (stage 40c). Everything must trace to something upstream.

### Numbering discipline
UC-001, FR-001, AC-001 at stage 20. US-[MODULE]-001, BR-[MODULE]-001, AC-[MODULE]-001
at stage 40a. TASK-[MODULE]-001 at stage 40c.

---

## The Zen of Daksh (lives in SKILL.md)

> Docs are read by deaf ears and blind eyes. Give context at every junction.
> The document you wrote yesterday is already lying to someone.
> Structure without narrative is a skeleton without a body.
> Every enumeration deserves a "why these and nothing else."
> The baton carries no conversation. Write as if you won't be there.
> A polished wrong document is more dangerous than a rough right one.
> If you can't explain why, don't explain what.
> The decision is the artifact. The document is its trace.
> Unvalidated assumptions dressed as decisions are kindling.
> Write for the junior reading this cold at 11pm. If they can follow it, the senior will too.

---

## Files Written / Location

All stage files live at `/Users/yeshwanth/.codex/skills/daksh/stages/`.

```
00-client-onboarding/CONTEXT.md    ✅ written
10-vision/CONTEXT.md               ✅ written
20-business/CONTEXT.md             ✅ written
30-roadmap/CONTEXT.md              ✅ written (ghost path fixed)
40a-prd/CONTEXT.md                 ✅ written
40b-trd/CONTEXT.md                 ✅ written
40c-tasks/CONTEXT.md               ✅ written
50-implementation/CONTEXT.md       ✅ written (overwrote old)
```

Old `40-module/` directory deleted. SKILL.md routing table updated. Only one copy
of SKILL.md exists (at `.codex/skills/daksh/SKILL.md`) — no sync issue.

---

## Pending

No outstanding items. All stages written, routing updated, dead files cleaned up.

---

## References / Influences Cited

- Eric Reis — *The Lean Startup* (validated learning, build-measure-learn)
- Fred Brooks — *The Mythical Man-Month* (plan to throw one away; coordination cost)
- Brian Kernighan — "build intelligence into the message" (self-contained tickets)
- NASA phase gates — approval gates design
- Double diamond model — diverge/converge structure
- Conway's Law — org structure mirrors system structure (background, not explicit)
