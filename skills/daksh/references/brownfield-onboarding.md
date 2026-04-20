# Brownfield Onboarding

An existing large project does not get to start clean. The code is deployed, the team has habits, the backlog is already mid-sprint, and the Jira board predates Daksh by months. The naive approach — "let's retrofit the whole project" — is the wrong hill to die on. Teams that try it produce neat documents that describe a fiction no one believes.

The right approach is modular adoption: bring one piece of new work fully inside Daksh, let the team feel what that's like, then expand.

> **Design principle:** this reference and the skill changes it describes should be written simultaneously. A spec without a matching CONTEXT.md is aspirational. A CONTEXT.md without a spec is undocumented. When adding brownfield features to Daksh, update both in the same commit.

---

## The Core Idea

Daksh is adopted at the **module boundary**, not the project boundary.

A brownfield project has two kinds of work running in parallel:

- **Existing work** — code already written, behaviors already shipped, docs that predate Daksh. Daksh does not rewrite these. It names them, points to them, and tracks risk against them.
- **New work** — the next module, the next feature area, the next sprint of meaningful scope. This is where Daksh starts. Fully. No shortcuts.

The first Daksh module is the proof of concept for the team. If it works, the next module comes in. The project is eventually inside Daksh, but it got there incrementally — not by a big-bang retrofit that nobody had time for.

---

## The Workflow

### Step 1 — Identify the entry point

Pick the next significant piece of new work: a new module, a major feature, a re-architecture of one service. It should be meaningful enough to justify the full Daksh cycle (PRD → TRD → tasks → impl) and bounded enough to complete in 2–4 sprints.

Do not pick a module that is 80% done. The entry point needs room to run.

### Step 2 — Module-level init

```
/daksh init --module [MODULE]
```

This creates the manifest with a single module registered, scaffolds `docs/implementation/[MODULE]/`, and sets up the stage skeleton for that module only. It does not touch the rest of the project.

Daksh infers the **stage mode** for each stage and confirms before writing
the manifest. The PTL does not need to know the greenfield/inherited/delta
distinction upfront — the LLM reads the available signals and proposes:

| Stage | Typical inference on a mid-project brownfield | How it's confirmed |
|---|---|---|
| `00` (client context) | `inherited` — brief / MOM / prior docs exist | LLM shows inference, PTL confirms |
| `10` (vision) | `inherited` — product vision predates Daksh | LLM shows inference, PTL confirms |
| `20` (BRD) | `inherited` or `delta` — depends on whether new module changes requirements | LLM asks one question if ambiguous |
| `30` (roadmap) | `delta` — existing sprint plan plus where this module fits | LLM shows inference, PTL confirms |
| `40a` (PRD) | `greenfield` — new module, no prior spec | LLM shows inference, PTL confirms |
| `40b` (TRD) | `greenfield` — new module, no prior tech spec | LLM shows inference, PTL confirms |
| `40c` (tasks) | `greenfield` — task list written by Daksh | LLM shows inference, PTL confirms |
| `50` (impl) | `greenfield` — implementation tracked by Daksh | LLM shows inference, PTL confirms |

After confirmation, inherited stages are auto-acknowledged. They are not
skipped — they are satisfied by pointing to the existing artifact via
`inherited_ref`. Preflight treats them as valid predecessors.

### Step 3 — Baseline the inherited risk

```
/daksh risk-profile --save
```

This produces the first risk report. Inherited stages show up as acknowledged risks, not flags. The report gives the PTL a clear picture of what Daksh is tracking vs. what it is trusting from prior work.

Approvals on inherited stages are non-blocking. They are recorded in the risk register, not enforced as gates. If the PTL wants to formally acknowledge the inherited context, they run:

```
/daksh risk-profile --accept-risk RISK-001 --acknowledged-by [NAME]
```

The acknowledgement persists. Future risk reports show it as acknowledged, not deleted.

### Step 4 — Write the delta spec

For delta stages, write only what is changing. The document has two parts:

1. **Inherited baseline** — a short reference to the existing artifact (file path or external link). One paragraph. No copy-paste.
2. **Delta** — what this module adds, changes, or removes. Full traceability (UC → FR → US → TASK) applies only to the delta section.

This keeps the document honest. A delta TRD that pastes the entire existing architecture is not a delta — it is a rewrite pretending to be a reference.

### Step 5 — Run the full Daksh cycle for the module

From here, the module runs exactly like a greenfield module:

```
/daksh prd [MODULE]
/daksh trd [MODULE]
/daksh tasks [MODULE]
/daksh impl start TASK-[MODULE]-001
```

Approvals are required at each gate. The rest of the project's inherited state is visible in the risk report but does not block this module's progression.

### Step 6 — Expand

Once the first module completes stage 50, the team has a reference point.  The next module onboards the same way. Over 3–5 sprints, the active work surface is inside Daksh even if the legacy core is not.

The legacy core gets onboarded only if and when it is touched — not by a scheduled cleanup sprint, but by the natural pressure of new work depending on old code. When that dependency surfaces (usually as a change record or a discovery record), the legacy module gets its own inherited-mode entry in the manifest.

---

## What Non-Blocking Approvals Look Like in Practice

The PTL runs `tend` at the start of each sprint. The health report shows:

- Green: stages with valid approvals and clean hashes
- Amber: inherited stages that are acknowledged but not formally approved
- Red: greenfield stages with missing approvals blocking downstream work

Red items block. Amber items are visible but do not block. The PTL decides whether to remediate amber items or carry them as acknowledged risk.

This model keeps the team moving without letting the pipeline degrade silently. The risk is visible at every tend cycle — it just does not stop the sprint.

---

## The Expansion Pattern

```
Sprint 1    MODULE-A fully onboarded (greenfield)
Sprint 2    MODULE-B onboarded; MODULE-A in impl
Sprint 3    MODULE-C onboarded; legacy-X inherited on first touch
Sprint N    Active work surface is fully inside Daksh
```

The project is never "done" onboarding. It is progressively inside Daksh as new work enters. Legacy code that is never touched is never formally onboarded — and that is fine. Daksh tracks risk on it, not ownership.

---

## What Is Not Supported Yet

As of the current Daksh version, the following steps in this guide require features not yet implemented:

- `--module` flag on `/daksh init`
- Stage `mode` field (`inherited`, `delta`, `greenfield`) in the manifest
- Auto-acknowledgement of inherited stages at init
- Non-blocking approval enforcement (risk register records, not hard gates)
- Discovery records (`DR-NNN`) for legacy constraint discoveries during impl

These are tracked in `docs/conversations/client/brownfield-deficiencies.md`
(gap analysis) and `docs/backlog.md` (implementation queue).
