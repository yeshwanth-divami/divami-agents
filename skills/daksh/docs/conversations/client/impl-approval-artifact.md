# What Does It Mean to Approve Implementation?

This document captures a design question that surfaced during the first completed
implementation sprint (PREFLIGHT module, 2026-03-29) and has not yet been resolved
in the schema or the approve script. The question is deceptively simple: when a team
lead approves stage 50, what are they approving?

> [!summary] Throughline
> Daksh distinguishes planning approval from execution approval for stages 00–40c.
> Stage 50 breaks that pattern: the current schema points `50:[MODULE]` output at
> `tasks.md` — the same document already approved at `40c`. This makes the two approvals
> structurally identical, which means either one of them is redundant or they are
> approving different things with the wrong artifact. The resolution depends on a
> design choice about what stage 50's approvable output should be.

---

## The Two Approvals That Look Like One

Daksh has two approvals in the module planning layer that both involve `tasks.md`:

**`40c:[MODULE]` approval** — run after `/daksh tasks`. The TL or PTL signs off on
the task breakdown: "This is the right list of tasks, correctly scoped, correctly
sequenced, with decision budgets and acceptance criteria I agree with." The document
being approved is `tasks.md` as a *plan*.

**`50:[MODULE]` approval** — run after the sprint. The TL or PTL signs off on
implementation: "The work described in tasks.md has been done. PRs are merged,
ACs were confirmed, handbook was patched, Jira reflects reality." The document
being approved is... also `tasks.md`.

When the PREFLIGHT sprint completed today and `/daksh approve impl PREFLIGHT` was
run, the script hashed `tasks.md`, appended an approval block, and wrote
`status: approved`. Structurally identical to what happened at `40c`. The only
difference was the person running the command knew they meant something different
by it.

That meaning difference is currently carried only in the approver's head.

---

## Why This Matters

A Daksh approval does two things: it creates an audit trail ("who certified this and
when") and it unblocks downstream stages ("preflight passes for the next stage").

If stage 50's approval is over `tasks.md`:

- **Audit trail** — it records that Yeshwanth certified something related to tasks
  on 2026-03-29. But certified *what*? That the plan was good (that was `40c`) or
  that the execution was complete?
- **Downstream gate** — currently nothing gates on `50:[MODULE]` being approved.
  Stage 60 (handbook) isn't present yet. There is no next stage that runs
  `preflight 60 PREFLIGHT` and checks for a stage 50 approval. So the gate has
  no active consumer right now.
- **Tend audits** — `/daksh tend` checks for stale docs. If `50:PREFLIGHT` is
  "approved" but the check only looks at `tasks.md`, tend cannot distinguish
  "all tasks done, sprint complete" from "task list approved, work not started."

---

## Three Possible Answers

### Option A: Stage 50 approval is a completion certificate over a new artifact

Generate `docs/implementation/[MODULE]/sprint-summary.md` at the end of the sprint
(possibly as part of `/daksh impl done` on the last task, or as a new
`/daksh impl close [MODULE]` command). The sprint summary records every task, its
Jira ticket, its PR link, whether ACs were confirmed, and the final traceability
state. Stage 50 approval signs off on this document.

**What this gets right:** The artifact specifically exists to certify completion.
It has no existence before the sprint ends. Approving it couldn't be confused with
approving the plan.

**What this costs:** New artifact, new command, new schema field. More surface
area in an already-complex system.

---

### Option B: Stage 50 approval gates on traceability state, not a document hash

`approve.py` is extended to check, before writing the approval block, that all
tasks in `manifest.traceability` for this module are `status: done`. If any are
not, the script exits 1: "Cannot approve: TASK-PREFLIGHT-003 is not done."

The approvable document stays `tasks.md`, but the script enforces a completion
precondition. The approval block in `tasks.md` now carries a verified meaning.

**What this gets right:** No new artifact. The precondition makes the approval
semantically meaningful because you can't get the stamp without the completion
state being verified. Simple to implement in `approve.py`.

**What this costs:** `tasks.md` is still the document, which still looks
identical to the `40c` approval. The hash will differ slightly (new block appended)
but the intent difference is invisible in the file itself.

---

### Option C: The intent difference is acceptable and the current design is correct

`40c` approval = "I approve this plan."
`50` approval = "I have reviewed the merged PRs and confirm the plan was executed."

Both happen to sign `tasks.md` because `tasks.md` is the binding contract that
defines what "done" looks like for this module. The approval block timestamp is
the record. The two approvals have different semantic weight even though they point
at the same document.

**What this gets right:** No changes required. It's how paper-based engineering
sign-off works — the same spec sheet gets a "reviewed" stamp and then a "completed"
stamp from the same signatory.

**What this costs:** The distinction is invisible to any automated system. Tend,
preflight, and the manifest schema cannot distinguish the two intents. Future
maintainers reading the manifest will see two approvals on `tasks.md` and not know
which is which without reading the conversation history.

---

## Decision — 2026-03-29

**Option B implemented.** Rationale from Yeshwanth:

> One thing I'd push back on: the doc says "currently nothing gates on
> 50:[MODULE]." That's fine now, but if you're building Daksh as a lifecycle
> system, stage 50 approval is the natural gate for stage 60 (handbook/ops).
> Designing it correctly now avoids retrofitting later. The cheapest time to
> fix a schema is before the second module uses it.

This is the correct framing. The gate *does* have a consumer — it just isn't
built yet. Designing a toothless gate now and retrofitting enforcement when
stage 60 arrives is exactly the kind of schema debt that compounds. The precondition
costs one function call in `approve.py` now and saves a backward-incompatible
schema change later.

### What was changed

1. **`scripts/approve.py`** — Added a completion precondition before the approval
   path for any key starting with `50:`. Scans `manifest.traceability` for all
   `TASK-[MODULE]-NNN` entries and exits 1 if any are not `done`. Lists the
   blocking task IDs.

2. **`references/manifest-schema.md`** — Documented the `50:[MODULE]` output
   contract (`tasks.md`, not `change-records/`), the approval semantics (completion
   vs planning), and the stage 60 gate dependency.

3. **`commands/approve/CONTEXT.md`** — Added the impl precondition note and the
   stage 60 gate note.

### What was NOT changed

- The artifact is still `tasks.md`. The precondition makes the approval
  semantically different from the `40c` approval without requiring a new document.
- No sprint summary artifact (Option A). The traceability state carries the
  completion evidence; a separate doc would duplicate it.

### Remaining gap

`/daksh init` scaffolds `50:[MODULE]` with `output: "docs/implementation/[MODULE]/change-records/"`.
This points at a directory, which breaks `approve.py`. The init command must be
updated to scaffold `50:[MODULE]` with `output: "docs/implementation/[MODULE]/tasks.md"`.
