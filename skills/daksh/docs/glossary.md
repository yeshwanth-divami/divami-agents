# Glossary

Terms used across Daksh documents. When a term appears in any stage output, it means what's defined here — not what a cold reader might guess. Every term is a `###` heading so other documents can link directly to it: `[stage](glossary#stage)`, `[manifest](glossary#manifest)`, etc. Module-stage docs use `../../glossary#term`.

---

## Pipeline Structure

### Stage
A named phase of the Daksh pipeline. Each stage has one input (the previous stage's output), one output document, and an approval gate before the next stage can proceed. Stages 00–40c are [document stages](#document-stage); stage 50 is an [execution session](#execution-session).

### Document stage
Any stage that produces a document as its artifact (`onboard`, `vision`, `brd`, `roadmap`, `prd`, `trd`, `tasks`). Contrast with [execution session](#execution-session).

### Execution session
Stage 50 (`/daksh impl`). Produces code, a PR, and optionally a [change record](#change-record) — not a document. One task per session.

### Combined stage
Two stages merged into a single run for [small weight class](#weight-class) projects. Combinations: `onboard+vision` and `prd+trd`. The [manifest](#manifest) records them as `00+10` and `40a+40b:[MODULE]`.

### Weight class
Project classification — `small`, `medium`, or `large` — determined at init from timeline and module count. Controls approvals per [gate](#gate), whether stages are [combined](#combined-stage), whether open questions are mandatory, and how often `/daksh tend` runs. Set in the [manifest](#manifest); can be manually overridden.

### Module
A major feature area treated as an independent unit with its own PRD, TRD, tasks, and implementation. Identified by a short all-caps name (e.g., `AUTH`, `NOTIFY`). Modules are registered in the [manifest](#manifest) during `/daksh roadmap`.

---

## Manifest

### Manifest
The machine-readable pipeline state file at `docs/.daksh/manifest.json`. Every `/daksh` invocation reads it. Tracks [stage](#stage) status, approvals, [doc hashes](#doc-hash), [team roster](#roster), modules, [traceability](#traceability-chain), and [cross-module contracts](#cross-module-contract). Created by `/daksh init`; if it doesn't exist, no stage will run.

### Doc hash
SHA-256 digest of an output file, computed at the time the file is written or approved. Stored in the [manifest](#manifest). If the file changes after approval, the hash no longer matches — this is a [stale approval](#stale-approval).

### Stale approval
An approval whose [doc hash](#doc-hash) no longer matches the current file on disk. Detected by `/daksh tend`. Means someone approved a version that no longer exists.

### Stage status
The lifecycle state of a [stage](#stage) in the [manifest](#manifest): `not_started` → `in_progress` → `pending_approval` → `approved` (or `revision_needed`).

### Roster
The `team_roster` array in the [manifest](#manifest). Only people on the roster can approve [gates](#gate). The PTL manages the roster. Added at init; members can be added later via manifest edit + `/daksh tend`.

---

## Gates and Approvals

### Gate
The approval count check at the start of each [stage](#stage). Reads the prior stage's approval count from the [manifest](#manifest): 0 approvals = [hard stop](#hard-stop), fewer than required = warning, met = proceed. The gate is what makes stages sequential by contract, not just by convention.

### Approval
A recorded sign-off in the [manifest](#manifest): approver name, role, date, and the [doc hash](#doc-hash) at approval time. Required before the next stage can proceed. [Small weight class](#weight-class) requires 1; medium and large require 2.

### Approval gate
The block at the bottom of every stage output document where approvers fill in their name, role, and date. Reading this block is how the next stage counts approvals.

### Hard stop
A [gate](#gate) outcome where the system refuses to proceed. Triggered when 0 approvals are found on the prior stage. Cannot be overridden by "proceed anyway" — requires actual sign-off.

---

## Traceability

### Traceability chain
The lineage from business need to code: [UC](#uc) → [FR](#fr) → [US](#us) → [TASK](#task). Every implementation task must be traceable back to a use case. Tracked in `manifest.traceability`. Gaps are reported by `/daksh tend`.

### UC
Use Case. Top-level user need. Identified as `UC-001`, `UC-002`, etc. Defined in the BRD (`/daksh brd`). Every [functional requirement](#fr) must reference a UC.

### FR
Functional Requirement. A specific, testable product behavior that implements part of a [UC](#uc). Identified as `FR-001`, `FR-002`, etc. Defined in the BRD. Every [user story](#us) must reference an FR.

### NFR
Non-Functional Requirement. A constraint on how the system behaves — performance, security, reliability, maintainability. Not traced to a [UC](#uc), but must be satisfied by TRD design choices.

### US
User Story. Module-level expression of a user need: "As a [role], I want [action] so that [outcome]." Identified as `US-[MODULE]-001`. Traces to a [UC](#uc) and [FR](#fr). Defined in the PRD.

### TASK
A unit of implementation work for one engineer in one sprint. Identified as `TASK-[MODULE]-001`. Traces to a [US](#us). Defined in the tasks breakdown. Carried into stage 50 as the session brief.

### Orphan
A traceability ID with a missing required link — an [FR](#fr) with no [UC](#uc) parent, a [TASK](#task) with no [US](#us) parent, or a UC with no FR children. Orphans are flagged by `/daksh tend` and represent either missing work or misregistered IDs.

---

## Implementation

### Decision budget
A per-[TASK](#task) field specifying exactly what the engineer can decide independently vs. what must be escalated to TL or PTL. Prevents both under-delivery (waiting for permission on trivial choices) and over-delivery (making architectural decisions unilaterally). Mandatory on every task.

### Change record
A structured document raised via `/daksh change [MODULE]` when implementation reality diverges from the spec. Written to `docs/implementation/[MODULE]/change-records/CR-NNN.md`. Contains what was specified, what reality showed, impact, proposed resolution, and a change summary listing every doc mutation. The change command patches affected planning docs, marks them `pending_approval`, creates a change task, and registers the CR in `manifest.change_records`. The engineer cannot proceed past the divergence until `/daksh approve CR-NNN` resolves the change set. A project with zero change records either had perfect foresight or never looked hard enough.

### Change record tier
The highest-upstream document a [change record](#change-record) touches: `tasks`, `trd`, `prd`, `brd`, or `roadmap`. Stored in `manifest.change_records[CR-NNN].tier`. Determines which roles can approve the CR — the further upstream the change reaches, the heavier the [gate](#gate).

### Definition of Done
The four conditions that must all be true before a task is marked Done: Jira ticket updated, tests passing, PR reviewed and merged, docs updated if behavior changed.

### Cross-module contract
A formal interface agreement between two modules — who produces what, who consumes it, and what the shape is. Defined in `/daksh roadmap`, tracked in `manifest.contracts`. Changes must be approved by the PTL and may trigger downstream revision.

---

## Document Quality

### Doc-narrator
The writing skill that Daksh stages invoke before generating output. Enforces prose-before-diagrams, context seeds, open questions sections, narrative structure, and glossary linking. An output written without doc-narrator patterns is harder to read cold.

### Vyasa conventions
Formatting and structure rules from the `vyasa` skill: callout syntax, heading hierarchy, sidebar ordering via `.vyasa`, Mermaid diagram rules, and content structure. All Daksh outputs must follow Vyasa conventions to render correctly in the Vyasa doc viewer.

### Context seed
The opening paragraph of a stage document — 3–5 sentences that orient a cold reader: what this document is, why it exists, who it's for, and why now. Every stage output starts with one. The heading is chosen to fit the document, not prescribed.

### Leap-of-faith assumption
An unvalidated belief that the product depends on. If wrong, the product fails — not degrades. Mandatory section in the vision document. Unvalidated assumptions dressed as decisions are kindling.

---

## Commands

### init
`/daksh init` — the pipeline bootstrapper. Creates the [manifest](#manifest), determines [weight class](#weight-class), scaffolds directories including `docs/glossary.md`. Must run before any stage.

### tend
`/daksh tend` — health audit. Hashes all output files and compares to [manifest](#manifest), checks for [orphan](#orphan) traceability IDs, flags [stale approvals](#stale-approval), identifies missing artifacts. Run frequency depends on weight class.

### change
`/daksh change [MODULE]` — change intake and re-planning command. Creates a [change record](#change-record), patches affected planning docs, marks them `pending_approval`, creates a change task, and registers the CR in the [manifest](#manifest). Does not execute — execution happens later via `/daksh impl`. The only sanctioned way to create change records; hand-written CRs bypass governance.

### preflight
`/daksh preflight` — pre-stage validation. Checks that required skills are available, [gate](#gate) conditions are met, no documents are `pending_approval` from open [change records](#change-record), and context budget is within limits before a stage runs.
