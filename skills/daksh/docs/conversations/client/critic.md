# Daksh — Honest Critique

> "Plans are worthless, but planning is everything." — Eisenhower
>
> The question isn't whether Daksh is well-designed. It's whether
> anyone will still be using it on project #3.

---

## 1. The Ceremony Tax

Daksh has 8 stages, each requiring 2 human sign-offs before the next
can begin. For a greenfield product, that's **16 approval signatures**
before a single line of code is written (stages 00–40c). Multiply by
modules — a product with 5 modules means 16 + (3 gates × 5 modules × 2
approvals) = **46 signatures** before implementation begins.

**Why this kills it:** Services firms bill by the week. Every approval
gate is a calendar-day delay waiting for two humans to read a doc and
type their name into a markdown block. The first project manager who
watches a squad sit idle for two days waiting on a PTL vacation will
route around Daksh entirely.

**The deeper problem:** There's no tiering. A 2-week feature for an
existing client goes through the same pipeline as a 6-month greenfield
build. Daksh needs a "weight class" system — small/medium/large — where
small projects can skip or collapse stages (e.g., 00+10 combined,
40a+40b combined, single approver sufficient).

---

## 2. The Gate Is Made of Paper

The approval mechanism is a text block in a markdown file:

```
Approved by:
Role:
Date:
```

There is no enforcement. The LLM reads the text and counts filled
entries. This means:

- **Anyone can type anything.** "Approved by: me" passes the gate.
- **The LLM can misparse.** A partially filled block, a reformatted
  block, a block with extra whitespace — all are ambiguous to a regex-
  free text parser.
- **There's no audit trail beyond git blame.** Who actually approved?
  When? Was it the right person? Git blame tells you who edited the
  file, not who authorized the approval.
- **Copy-paste forgery is trivial.** Under deadline pressure, someone
  will pre-fill all approval blocks at once. The system can't tell.

**What it would take to fix:** The gate needs teeth. Options:
1. A separate `approvals.json` file per stage with structured data
   (approver, role, timestamp, hash of the doc at approval time).
2. Integration with an external system (Jira status, GitHub PR
   approval, Slack confirmation).
3. At minimum: the gate check should verify that the approver names
   match a known team roster, not just that the fields are non-empty.

---

## 3. No Way Back

Daksh is a waterfall with modern vocabulary. The stages are strictly
linear: 00 → 10 → 20 → 30 → 40a → 40b → 40c → 50. There is no
mechanism to:

- **Revise an upstream stage** when a downstream stage reveals it was
  wrong. If stage 40b (TRD) reveals the vision was flawed, you'd need
  to: re-run stage 10, get 2 approvals, re-run 20, get 2 approvals,
  re-run 30, get 2 approvals, re-run 40a, get 2 approvals, then
  re-run 40b. That's 8 signatures to fix a sentence in the vision.
- **Run stages in parallel.** Two modules can't have their PRDs written
  simultaneously unless the user manually invokes `/daksh` twice in
  separate sessions — and the skill doesn't mention this.
- **Do a lightweight revision.** Change records exist at stage 50, but
  there's no equivalent for stages 10–40. If the roadmap needs updating
  after a PRD is written, there's no formal mechanism — you just edit
  the file and hope the approval block still means something.

**What it would take to fix:** A revision protocol for stages 10–40:
"If a downstream stage surfaces a flaw in an upstream doc, write a
Stage Revision Record (SRR) in the upstream doc. The SRR requires 1
approval (not 2) to proceed, because the downstream discovery is itself
evidence."

---

## 4. The Context Window Wall

By stage 50, the LLM is instructed to read:

- `tasks.md` (can be 200+ lines for a complex module)
- `trd.md` (easily 300+ lines)
- `prd.md` (100+ lines)
- The current codebase
- Existing code patterns
- The decision budget
- Change records if any exist

That's potentially 1000+ lines of documentation context before the
codebase is even loaded. For a mid-size module with 20 files, the LLM
is operating near or past its effective context window. The later
sections of the TRD — the ones most relevant to implementation — are
exactly the ones most likely to be compressed or forgotten.

**Why this matters:** The system's discipline depends on the AI
faithfully following specs it may not fully retain. A developer who
doesn't read the TRD is a problem. An AI that *can't* read the TRD
because it fell out of context is an invisible problem — it will
generate plausible code that ignores the spec, and no one will notice
until integration.

**What it would take to fix:** Stage 50 should not load all three docs.
It should load only the specific task block from `tasks.md` and the
specific TRD section referenced by that task. The CONTEXT.md should
say: "Read only the section of the TRD referenced in the task's
description field — not the entire TRD."

---

## 5. Phantom Dependencies

Every stage says:

> Apply `doc-narrator` writing patterns before generating output.
> All documentation must follow Vyasa conventions — apply the `vyasa`
> skill for correct formatting, callouts, and content structure.

These are invocations of external skills that:

- May not be installed in every environment where Daksh runs.
- May have changed their interface since Daksh was written.
- Have no version pinning — Daksh doesn't say "vyasa v2.1," it says
  "vyasa."
- Are never validated. If `doc-narrator` fails to load, the stage
  proceeds anyway — just without the writing quality Daksh promises.

**The risk:** Daksh's documentation quality guarantee rests on two
skills it doesn't own, doesn't version, and doesn't validate. It's a
load-bearing assumption dressed as a one-liner.

**What it would take to fix:**
1. Pin skill versions in SKILL.md or `.version`.
2. Add a pre-flight check: "Before generating output, verify that
   `doc-narrator` and `vyasa` skills are available. If not, warn:
   'Documentation quality skills are not installed. Output will lack
   narrative structure and Vyasa formatting.'"

---

## 6. The Jira Gap

Stage 30 outputs structured markdown and says "the PTL will create
tickets from this." Stage 40c does the same. This is a manual
copy-paste step across a system boundary (markdown → Jira).

**What will actually happen:** The PTL will create tickets for the first
sprint. By sprint 3, the tickets will diverge from the markdown. By
sprint 5, the markdown is a historical artifact and Jira is the source
of truth — but Daksh doesn't know that. Stage 50 still reads `tasks.md`
as its input, not Jira.

**The deeper problem:** Daksh produces documents that describe Jira
tickets. It does not produce Jira tickets. The moment a human edits a
ticket in Jira without updating `tasks.md`, the traceability chain —
Daksh's core value proposition — is broken. And that moment is sprint 1,
day 2.

**What it would take to fix:** Either:
1. Daksh generates Jira tickets directly (API integration), or
2. Daksh explicitly acknowledges that `tasks.md` is a *template* that
   becomes stale after sprint start, and stage 50 should read Jira as
   the source of truth for task details (with `tasks.md` as fallback).

---

## 7. The Orphan Rule Is Unenforceable

"Orphan FRs don't ship. Orphan stories don't ship. Orphan tasks don't
ship." This is stated as law in stages 20, 40a, and 40c.

But the check is: the LLM reads the doc and tries to verify
traceability. There's no structural enforcement. The numbering scheme
(UC-001 → FR-001 → US-AUTH-001 → TASK-AUTH-001) is a convention, not a
constraint. Nothing prevents:

- An FR that claims to trace to UC-003 when UC-003 doesn't exist.
- A task that references US-AUTH-005 when the PRD only has 4 stories.
- A story added during implementation that traces to nothing.

**What it would take to fix:** A traceability matrix — a single file
(`docs/traceability.md`) that maps every ID to its parent, generated
automatically by each stage and validated by the next. If a downstream
ID claims a parent that doesn't exist in the matrix, the stage refuses
to proceed.

---

## 8. Cross-Module Contracts Rot

Cross-module contracts are defined in stage 30's roadmap. But modules
are designed independently in stages 40a and 40b. When module A's TRD
changes its API surface, stage 30's contract table is stale.

There is no mechanism to:
- Notify the roadmap that a contract changed.
- Notify module B that the API it depends on has been redesigned.
- Detect contract drift before integration.

**Why this matters:** Cross-module integration failures are the #1
source of late-project pain in services firms. Daksh correctly
identifies this ("Cross-module contracts section is mandatory") but
then provides no mechanism to keep contracts alive after initial
creation.

**What it would take to fix:** Each TRD should re-state the contracts it
consumes (from stage 30) and the contracts it produces. Stage 40c
should cross-check: "Does this module's TRD contract match what the
consuming module's PRD expects?" If not, flag it before tasks are
created.

---

## 9. "Open Questions" as Mandatory Theater

Every stage mandates an open questions section and adds: "If everything
is resolved, you haven't looked hard enough."

This is a good instinct — it fights false certainty. But it's also a
paradox. For a simple, well-understood module (CRUD admin panel, basic
auth), there may genuinely be no open questions. Forcing the AI to
manufacture uncertainty produces noise that erodes trust in the section.

After two projects where the "open questions" are things like "Should
we use 4-space or 2-space indentation?" — people stop reading that
section. And then the one time it contains "The payment gateway doesn't
support our currency" — nobody sees it.

**What it would take to fix:** Replace the mandate with a calibrated
prompt: "List open questions if any exist. If none, write: 'No open
questions at this stage — all inputs were sufficiently specified.' This
is a valid state, not a failure."

---

## 10. Who Creates the Directories?

Every stage specifies an output path: `docs/vision.md`,
`docs/implementation/[MODULE]/prd.md`, etc. Every stage also says: "No
file management tasks — wrong job for this stage."

So who creates `docs/implementation/AUTH/`? The user? The PTL? A
separate setup script? This is never specified. The most likely outcome
is the AI creates it anyway (violating its own rule), or the user gets
an error on first run and creates it manually — learning that Daksh's
stated rules don't match its actual requirements.

**What it would take to fix:** Either:
1. Remove the "no file management" rule and let each stage create its
   output directory, or
2. Add a stage 0 pre-flight that scaffolds the full directory tree
   based on the module list from the roadmap.

---

## 11. No Feedback Loop

Stage 50 writes change records when reality diverges from spec. These
are excellent — they capture hard-won implementation knowledge. But
they're write-only. Nothing reads them back into the system.

- Stage 00 on the *next* project doesn't read prior change records.
- Stage 30 optionally reads them ("if change records from a prior run
  exist"), but this is a weak hint, not a requirement.
- There's no "lessons learned" aggregation across projects.

Daksh captures knowledge and then buries it in a module subdirectory.
The next project starts from zero. Conway's Law in action: the system
mirrors the organization's amnesia.

**What it would take to fix:** A post-project stage (stage 60? stage
99?) that aggregates change records into a `docs/lessons-learned.md`
and tags each lesson with the stage it should inform. Stage 00 on the
next project reads this file as input.

---

## 12. The Single-User Assumption

Daksh assumes one person invokes `/daksh`, one AI responds, two humans
approve. But real projects have:

- Multiple engineers running stage 50 in parallel on different tasks.
- A PTL running stage 40a for module B while a TL runs 40c for module A.
- A client providing feedback that invalidates stage 10 while stage 30
  is in progress.

Daksh has no concurrency model. No file locking. No conflict detection.
Two people editing `docs/implementation-roadmap.md` simultaneously will
produce a merge conflict that Daksh can't resolve — because it doesn't
know it's happening.

**What it would take to fix:** At minimum, document the concurrency
model: "Only one stage may be active per output file at a time. The
person invoking the stage owns the file until the approval block is
filled." Better: use git branches per stage invocation and merge via PR.

---

## Summary: What Keeps Daksh Alive

Daksh will survive if — and only if — these three things happen:

1. **Weight classes.** Small projects (< 4 weeks) get a collapsed
   pipeline. Otherwise the ceremony tax kills adoption before the
   discipline pays off.

2. **Gates with teeth.** The approval block must be more than text in a
   markdown file. It doesn't need to be enterprise tooling, but it needs
   to be harder to fake than typing "approved" and harder to skip than
   ignoring.

3. **Living contracts.** Cross-module contracts, traceability chains,
   and Jira sync must be maintained — not just created. A document
   written once and never updated is a lie with a timestamp.

Everything else — the open questions mandate, the directory scaffolding,
the feedback loop — is fixable incrementally. But without weight
classes, gates, and living contracts, Daksh will be used exactly once
per team, praised in the retro, and quietly abandoned by project #3.

> "The best process is the one people actually follow under pressure."
> Daksh is currently designed for a world where no one is under pressure.
> That world does not exist at a services firm.

---
---

# Compound Solutions

> A good solution solves one problem. A great solution dissolves the
> category the problem belonged to.

The assumption: Daksh runs in an environment with full integrations —
Jira API, Git, team rosters, Slack/Chat — and the LLM has tool access
to all of them. Skills are process pipelines, not just doc generators.
Daksh becomes a CLI with subcommands, not a chatbot with stages.

---

## A. The Manifest — One File to Rule the Pipeline

**Solves:** #1 (ceremony tax), #2 (paper gates), #3 (no way back),
#7 (orphan rule), #8 (contract rot), #12 (concurrency)

Introduce `docs/.daksh/manifest.json` — a machine-readable spine for
the entire project. Every `/daksh` invocation reads and writes it.

```jsonc
{
  "project": "acme-platform",
  "weight_class": "large",        // small | medium | large
  "team_roster": [
    { "name": "Ravi", "role": "PTL" },
    { "name": "Meena", "role": "TL" },
    // ...
  ],
  "stages": {
    "00": {
      "status": "approved",
      "output": "docs/client-context.md",
      "approvals": [
        { "by": "Ravi", "role": "PTL", "date": "2026-03-15", "doc_hash": "a3f9..." },
        { "by": "Client PM", "role": "Client", "date": "2026-03-16", "doc_hash": "a3f9..." }
      ]
    },
    "40a:AUTH": {
      "status": "in_progress",
      "locked_by": "Meena",
      "output": "docs/implementation/AUTH/prd.md"
    }
    // ...
  },
  "contracts": {
    "AUTH → NOTIFY": { "shape": "UserEvent", "owner": "AUTH", "consumer": "NOTIFY", "version": 2 },
    // ...
  },
  "traceability": {
    "UC-001": { "children": ["FR-001", "FR-002"] },
    "FR-001": { "parent": "UC-001", "children": ["US-AUTH-001", "US-AUTH-002"] },
    "US-AUTH-001": { "parent": "FR-001", "children": ["TASK-AUTH-001", "TASK-AUTH-002"] }
    // ...
  }
}
```

**What this dissolves:**

- **Paper gates (#2):** Approvals are structured data with a doc hash.
  The hash means "I approved *this version*." If the doc changes after
  approval, the hash breaks and the gate re-opens. No more typing
  "approved" into markdown.

- **Ceremony tax (#1):** `weight_class` drives stage collapsing. Small
  projects merge 00+10, skip 40a (inline PRD into TRD), and require 1
  approval instead of 2. The manifest encodes the rules, not the
  CONTEXT.md files.

- **No way back (#3):** When a downstream stage revises an upstream doc,
  the manifest records the revision with a new hash. The gate doesn't
  require re-running the full upstream stage — just re-approval of the
  changed doc. Lightweight regression, not full waterfall rewind.

- **Orphan rule (#7):** The traceability map is structural, not prose.
  Every stage that creates an ID registers it in the manifest with its
  parent. `/daksh tend` can detect orphans mechanically — no LLM
  judgment needed.

- **Contract rot (#8):** Contracts live in the manifest, not in stage
  30's prose. When a TRD changes an API surface, it updates the
  contract entry and bumps the version. Consuming modules see the
  version mismatch on their next stage invocation.

- **Concurrency (#12):** `locked_by` prevents two people from running
  the same stage on the same output file. The lock is set on stage
  invocation, released on approval.

---

## B. `/daksh jira` — Bidirectional Sync, Not Copy-Paste

**Solves:** #6 (Jira gap), #7 (orphan rule), #8 (contract rot),
#11 (feedback loop), #12 (concurrency)

Daksh stops generating markdown that humans copy into Jira. Instead:

```
/daksh jira push AUTH          Push tasks.md → Jira tickets
/daksh jira pull AUTH          Pull Jira state → update tasks.md
/daksh jira sync               Bidirectional reconciliation
/daksh jira status             Show drift between docs and Jira
```

**What this dissolves:**

- **Jira gap (#6):** `push` creates epics, stories, and tasks with the
  exact structure from stages 30 and 40c. Links, labels, parent
  relationships — all set by the skill, not by a human squinting at
  markdown. `pull` brings Jira edits back into `tasks.md` so the doc
  stays alive.

- **Orphan rule (#7):** Jira enforces parent links natively. A story
  without an epic can't exist. A task without a story can't exist. The
  orphan rule becomes a database constraint, not an LLM prompt.

- **Contract rot (#8):** Cross-module contracts become Jira epic links.
  When module A's epic changes, module B's linked epic gets flagged.
  Jira's notification system handles what Daksh's prose can't.

- **Feedback loop (#11):** Change records written in stage 50 get
  synced to Jira as comments on the affected task. At project close,
  `/daksh jira retro` queries all change records across modules and
  generates `docs/lessons-learned.md` — tagged by stage, sorted by
  severity.

- **Concurrency (#12):** Jira handles multi-user editing natively. Two
  engineers updating different tasks in the same module don't conflict
  because each task is a separate Jira ticket, not a section in a
  shared markdown file.

**The key insight:** Jira is not a nice-to-have integration. It's the
only system at Divami that survives contact with real project pressure.
If Daksh's artifacts don't live in Jira, they die the moment Jira
becomes the team's actual operating system — which is day 1.

---

## C. `/daksh preflight` — Environment Validation Before Every Stage

**Solves:** #5 (phantom dependencies), #10 (directory scaffolding),
#2 (gate validation), #4 (context window)

Before any stage runs, a preflight check:

```
/daksh preflight 40b AUTH
```

```
✓ Skills: doc-narrator v2.1, vyasa v3.0 — loaded
✓ Directories: docs/implementation/AUTH/ — exists
✓ Gate: 40a:AUTH — 2/2 approvals, doc hash matches
✓ Inputs: prd.md (142 lines), roadmap.md (89 lines), brd.md (201 lines)
✓ Context budget: 432 lines / 2000 line limit — OK
✗ Contract: AUTH→NOTIFY contract v1, but NOTIFY TRD expects v2 — STALE
  Action: resolve contract before proceeding
```

**What this dissolves:**

- **Phantom dependencies (#5):** Skills are validated and version-
  checked before the stage prompt loads. Missing skill = hard stop with
  install instructions, not silent quality degradation.

- **Directory scaffolding (#10):** Preflight creates directories if
  missing. No more "no file management" rule — the preflight is the
  file manager. Stage prompts stay clean.

- **Gate validation (#2):** Approvals are checked structurally (from the
  manifest, not by parsing markdown). Hash mismatches surface here, not
  mid-stage when the LLM has already loaded 500 lines of context.

- **Context window (#4):** Preflight counts input lines and warns if the
  stage will exceed context budget. For stage 50, it extracts only the
  relevant task block and TRD section — loading 80 lines instead of 800.
  The context budget is a first-class constraint, not an afterthought.

- **Contract drift (#8):** Preflight cross-checks the manifest's
  contract versions against what consuming stages expect. Stale
  contracts surface before work begins, not during integration.

---

## D. `/daksh tend` — The Living Health Audit

**Solves:** #7 (orphans), #8 (contract rot), #9 (open questions
theater), #11 (feedback loop), #3 (revision tracking)

A non-destructive audit that reads everything and reports drift:

```
/daksh tend

Pipeline health for acme-platform (large):
──────────────────────────────────────────
Stages:     8/8 complete, 0 in progress
Modules:    AUTH ✓  NOTIFY ✓  BILLING ⚠  ADMIN ✓  REPORTS ✓

⚠ BILLING: TRD approved 2026-03-10, but 3 change records filed since.
  → TRD may be stale. Consider re-approval or revision record.

Traceability:
  ✓ 23 UCs → 41 FRs → 67 stories → 142 tasks — no orphans
  ⚠ FR-019 has no acceptance criteria (stage 20 gap)

Contracts:
  ✓ AUTH→NOTIFY v2 — both sides current
  ✗ BILLING→REPORTS v1 — REPORTS TRD expects v2
    → BILLING TRD changed the export schema but didn't bump contract

Change records:
  12 total, 11 resolved, 1 open (CR-008: BILLING payment gateway)
  → CR-008 blocking TASK-BILLING-014. Escalate to PTL.

Lessons:
  3 change records involve the same pattern: "TRD assumed sync API,
  reality required async." Consider adding to stage 40b prompt:
  "For external API integrations, verify sync vs. async before design."
```

**What this dissolves:**

- **Orphans (#7):** Mechanical traversal of the traceability map. Not
  LLM judgment — graph traversal. An orphan is a node with no parent
  edge. Exact, not approximate.

- **Contract rot (#8):** Version comparison across the manifest. If
  producer bumped but consumer didn't update, it shows up here.

- **Open questions theater (#9):** `tend` replaces the artificial
  mandate with real gap detection. Instead of forcing every stage to
  invent uncertainty, `tend` finds actual gaps — missing ACs, stale
  TRDs, unresolved CRs. Real signal, not noise.

- **Feedback loop (#11):** `tend` aggregates change records and detects
  patterns. "Three CRs about sync-vs-async" becomes a prompt amendment
  for future projects — automatically surfaced, not buried in a
  subdirectory.

- **Revision tracking (#3):** `tend` detects when a doc has been
  modified after approval (hash mismatch) and flags it. This makes
  lightweight upstream revisions visible without requiring the full
  waterfall rewind.

---

## E. Weight Classes — Encoded in the Manifest, Enforced by Preflight

**Solves:** #1 (ceremony tax), #2 (gate rigor scales down), #9 (open
questions scale down)

```
/daksh init --size small    # < 4 weeks, < 3 modules
/daksh init --size medium   # 4-12 weeks, 3-8 modules
/daksh init --size large    # > 12 weeks or > 8 modules
```

| Rule | Small | Medium | Large |
|------|-------|--------|-------|
| Stages 00+10 | Combined | Separate | Separate |
| Stage 20 | Inline in vision | Full BRD | Full BRD |
| Stages 40a+40b | Combined | Separate | Separate |
| Approvals per gate | 1 | 2 | 2 |
| Open questions | Optional | Mandatory | Mandatory |
| Cross-module contracts | N/A (< 3 modules) | Required | Required |
| Jira sync | Optional | Recommended | Required |
| `/daksh tend` frequency | End of project | Per milestone | Per sprint |

**The key insight:** Weight classes aren't a feature — they're an
adoption strategy. The small track is how Daksh gets into a team's
muscle memory on a 2-week feature. By the time they hit a large
project, the stages feel natural, not ceremonial. You can't sell
discipline to people who've never experienced it paying off. You sell
them the small version, let it save their ass once, and then they'll
voluntarily opt into the large version.

---

## How They Compose

These five solutions aren't independent — they're a stack:

```
┌─────────────────────────────────────────┐
│  /daksh tend        (audit layer)       │
├─────────────────────────────────────────┤
│  /daksh jira        (sync layer)        │
├─────────────────────────────────────────┤
│  /daksh preflight   (validation layer)  │
├─────────────────────────────────────────┤
│  manifest.json      (state layer)       │
├─────────────────────────────────────────┤
│  weight classes     (policy layer)      │
└─────────────────────────────────────────┘
```

- **Policy** (weight classes) decides which rules apply.
- **State** (manifest) tracks what's happened and what's owed.
- **Validation** (preflight) checks state before action.
- **Sync** (jira) keeps external systems coherent with state.
- **Audit** (tend) catches everything the other layers missed.

Each layer is independently useful. You can ship the manifest without
Jira sync. You can ship preflight without tend. But together, they
turn Daksh from a document generator into an autonomous process
controller — one that gets harder to bypass as layers are added,
without getting harder to use.

---

## Problem Coverage Matrix

| Problem | Manifest | Jira | Preflight | Tend | Weight |
|---------|----------|------|-----------|------|--------|
| #1 Ceremony tax | ◐ | | | | ● |
| #2 Paper gates | ● | | ◐ | | ◐ |
| #3 No way back | ◐ | | | ◐ | |
| #4 Context wall | | | ● | | |
| #5 Phantom deps | | | ● | | |
| #6 Jira gap | | ● | | | |
| #7 Orphan rule | ● | ● | | ● | |
| #8 Contract rot | ● | ◐ | ◐ | ● | |
| #9 Open Qs theater | | | | ● | ◐ |
| #10 Directory scaffold | | | ● | | |
| #11 Feedback loop | | ● | | ● | |
| #12 Concurrency | ● | ◐ | | | |

● = primary fix · ◐ = contributing fix

Every problem is hit by at least two solutions. No solution exists in
isolation. That's the smell of a real architecture, not a patch list.
