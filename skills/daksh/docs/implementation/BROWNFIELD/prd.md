# BROWNFIELD — Product Requirements

This document specifies the product behavior for the BROWNFIELD module of Daksh. BROWNFIELD exists because Daksh was designed as a greenfield pipeline — every stage assumes a clean slate, an empty repo, a blank manifest. That assumption fails for the majority of real Divami engagements, which begin not with an empty directory but with an existing codebase, inherited docs, an active Jira board, and a team that already has habits. This PRD answers: what does the BROWNFIELD module do, for whom, and how do we know it's done? The TRD answers how. The full gap analysis this module addresses is in [brownfield-deficiencies.md](../../conversations/client/brownfield-deficiencies.md). This PRD implements UC-010 from `docs/business-requirements.md`.

---

## Scope

**In scope:**

- **Baseline scan** — detect an existing codebase at init time and produce `docs/baseline.md`
- **Inherited [stage](../../glossary#stage) mode** — per-stage `mode` field (`greenfield | inherited | delta`) so existing work doesn't have to be re-authored
- **Conventions block** — manifest section for discovered/declared project conventions (git, code, docs) that all downstream commands read
- **Org adapter** — manifest section for governance (configurable approval authority), Jira (existing epics, custom fields, workflow statuses), and team capacity
- **Discovery Record (DR-NNN)** — a new artifact type for legacy constraint discoveries, separate from spec-divergence change records

**Out of scope:**

- Automated static analysis or code quality scoring (baseline scan reads structure, not semantics)
- CI/CD enforcement or git hook integration
- Multi-tenant Jira configuration (one project key per manifest)
- Retroactive application to stages already `approved` before BROWNFIELD support shipped
- Automatic migration of pre-BROWNFIELD manifests (migration is a manual one-time step)

---

## User Stories

The five stories below map to the five architectural moves in the design doc. Each move is independently shippable; the stories are ordered by dependency, not by priority.

### US-BROWNFIELD-001 — Initialize Daksh on an existing repo

**Traces to:** UC-010, FR-013

As a **PTL or TL**, I want `/daksh init` to support three distinct initialization modes — greenfield, brownfield whole-project, and brownfield module-scoped — so that I can adopt Daksh at whatever entry point matches the project's current state.

The current single greenfield path (scaffold empty dirs, ask what you're building) produces fiction when run on an existing repo, and it's an all-or-nothing commitment that blocks module-level adoption. The three modes are:

| Mode | Flag | When to use |
|------|------|-------------|
| Greenfield | _(none)_ | No code exists yet — clean slate |
| Brownfield whole-project | `--brownfield` or prompted | Existing codebase, adopting Daksh for the full project |
| Brownfield module-scoped | `--module AUTH` | Existing codebase, adopting Daksh for one module only |

Whole-project brownfield runs the baseline scan (US-BROWNFIELD-002) before asking questions. Module-scoped brownfield runs a narrower scan covering only the specified module's directory and its declared dependencies.

---

### US-BROWNFIELD-002 — Produce a baseline snapshot

**Traces to:** UC-010, FR-014

As a **PTL or TL**, I want init to produce a baseline snapshot — `docs/baseline.md` for whole-project init, or `docs/implementation/[MODULE]/baseline.md` for module-scoped init — so that every downstream stage has a shared reference for inherited state rather than each stage reinventing its own discovery.

The baseline is not a spec — it is a map. "Here's what exists, where it lives, and what shape it's in." It is written once by the scan and patched by Discovery Records (US-BROWNFIELD-007) as new constraints are found.

**Scope by init mode:**

| Init mode | Baseline artifact | Scan coverage |
|-----------|------------------|---------------|
| Whole-project brownfield | `docs/baseline.md` | Full repo: all modules, all docs, git history, all conventions |
| Module-scoped brownfield | `docs/implementation/[MODULE]/baseline.md` | Module directory + declared dependencies only |

A module-scoped baseline is deliberately narrower — it does not infer the rest of the project and does not make claims about modules it didn't scan.

---

### US-BROWNFIELD-003 — Mark stages as inherited, delta, or greenfield

**Traces to:** UC-010, FR-015

As a **PTL**, I want each stage in the [manifest](../../glossary#manifest) to carry a `mode` field (`greenfield | inherited | delta`), so that I can accurately represent which parts of the pipeline are net-new, which already exist, and which are partially inherited with planned changes.

Without this, a PTL must either re-author docs for existing work (wasted effort, documentation fiction) or skip stages and accept broken gate chains. With this, inherited stages are auto-[approved](../../glossary#approval) at init and preflight treats them as valid predecessors. Delta stages get a two-part structure: "what exists" (from baseline) + "what's changing" (new work with traceability IDs).

---

### US-BROWNFIELD-004 — Adapt commands to discovered conventions

**Traces to:** UC-010

As a **TL or Engineer**, I want Daksh's impl commands to read the project's existing git and code conventions (branch naming, PR targets, test framework, indent style) from the manifest, so that new code written inside Daksh doesn't break PR reviews against the existing codebase.

The failure mode this prevents: engineer follows `references/python-guidelines.md` which says 2-space indent; existing 50k-LOC Python codebase uses 4-space; every PR gets a lint failure. The conventions block makes guidelines the fallback, not the mandate.

---

### US-BROWNFIELD-005 — Configure approval authority to match the org

**Traces to:** UC-010

As a **PTL**, I want to define which roles can approve which stages in the manifest (rather than accepting `approve.py`'s hardcoded PTL/TL map), so that the pipeline's governance matches the org's actual decision structure.

This matters when: a client's business owner must approve the PRD, an Architect must sign off on TRDs, or an external stakeholder must approve roadmap changes. None of these roles exist in the current hardcoded authority model. The `org.governance.stage_authority` map replaces the hardcoded map without removing the defaults.

---

### US-BROWNFIELD-006 — Bridge Daksh to an existing Jira project

**Traces to:** UC-010

As a **PTL**, I want `jira-sync.py` to place tasks under existing Jira epics (rather than creating new ones), respect the project's custom fields and workflow statuses, and validate sprint assignments against actual team capacity, so that Daksh enhances the existing Jira structure rather than orphaning it.

The current behavior creates `"{MODULE} Module"` epics unconditionally and pushes stories with hardcoded field names. In a brownfield project with active sprints, this creates duplicate epics, blows up the board, and ignores that the team is currently in Sprint 4.

---

### US-BROWNFIELD-007 — Raise a Discovery Record for legacy constraints

**Traces to:** UC-010

As an **Engineer**, I want a Discovery Record (DR-NNN) artifact type that I can create when I find a constraint in existing code — rather than forcing a legacy constraint discovery into the Change Record format — so that the distinction between "spec vs. reality" (CR) and "no spec, just reality" (DR) is preserved in the audit trail.

The two situations require different responses: a CR triggers a spec revision; a DR triggers a baseline update. Conflating them corrupts the feedback loop.

---

### US-BROWNFIELD-008 — View a risk report instead of hitting a gate block

**Traces to:** UC-010

As a **PTL**, I want to see a risk report of all missing approvals, stale hashes, and pipeline inconsistencies — rather than being hard-blocked by a gate I can't yet satisfy — so that I can make an informed decision about proceeding rather than being forced to stop.

The current model treats missing approvals as blockers. On a brownfield project, stages may be inherited or partially approved for legitimate reasons. Blocking on them doesn't improve quality — it just makes Daksh unusable for teams mid-project. Naveen's framing in the March 30 internal review was precise: *"I don't want approval to be a blocker. Approval process should be there."* The record matters; the hard stop doesn't.

This is the broadest story in this module: it touches the gate enforcement model across the entire pipeline, not just brownfield stages.

---

### US-BROWNFIELD-009 — Adopt Daksh one module at a time

**Traces to:** UC-010

As a **TL**, I want to run `/daksh init --module AUTH` to bring a single module of an existing project into Daksh without scaffolding or registering the rest of the codebase, so that I can introduce process discipline incrementally without requiring a whole-project commitment.

The current init path is all-or-nothing: scaffold the full directory tree, register all modules, commit to the whole pipeline. For a team mid-Sprint 4 on a live project, that bar is too high. Module-scoped init makes "start using Daksh on new work" a viable first step.

---

## Business Rules

The rules below constrain implementation choices that TRD must enforce.

### BR-BROWNFIELD-001 — Inherited stages are auto-approved at init

Stages marked `mode: inherited` must be automatically set to `status: approved` at init time. No manual approval command is required. Their `output` points to the relevant section of `docs/baseline.md`, and `doc_hash` is computed from that section. Preflight must treat `inherited` stages as valid predecessors for downstream stages.

*Why:* Requiring manual approval of "the past" is both meaningless (there's nothing to review, no decision to make) and blocking (it would prevent the pipeline from starting). The approval gate exists to verify human judgment on new decisions, not to acknowledge inherited reality.

### BR-BROWNFIELD-002 — Delta stages carry two-part documents

A `delta` stage must produce a document with two clearly separated sections:
1. "Inherited state" — references baseline.md, no traceability IDs
2. "What's changing" — net-new work with full UC/FR/US/TASK IDs

[Traceability](../../glossary#traceability-chain) IDs (`UC-`, `FR-`, `US-`, `TASK-`) are only assigned to items in the "what's changing" section. Inherited work is described by reference, not re-tagged.

*Why:* Assigning traceability IDs to inherited work implies Daksh authored it, which is false. False traceability is worse than no traceability — it makes the audit trail unreliable.

### BR-BROWNFIELD-003 — Conventions block takes precedence over guideline defaults

When `manifest.conventions.code` exists, all coding guideline references (`references/python-guidelines.md`, `references/typescript-guidelines.md`) must defer to it for: indentation, naming conventions, test framework, linter, and import style. The guidelines apply only when `conventions.code` is absent.

*Why:* Guidelines are defaults for greenfield. On a brownfield project, "follow your guidelines" and "match the existing codebase" are often in conflict. The existing codebase wins — it's the contract that PR reviews enforce.

### BR-BROWNFIELD-004 — DR-NNN is not a CR-NNN

A Discovery Record must not be created using the Change Record format. DRs reference code (file paths, module behaviors); CRs reference spec documents. A DR does not require a Daksh-authored spec to exist. A DR must not be routed through `change.py` — it requires its own scaffold script or template. The prefix `DR-` must be distinct from `CR-`.

*Why:* If legacy constraint discoveries are filed as CRs, the manifest treats them as spec failures, expects a spec revision, and blocks approval until a document that doesn't exist is "patched." Wrong artifact type → wrong resolution path → wasted effort.

### BR-BROWNFIELD-006 — Approval gates warn, they do not hard-block

Missing approvals must produce a risk entry in the pipeline risk report, not a hard stop that prevents the engineer from proceeding. The risk report surfaces: which stages are unapproved, which doc hashes are stale, and which gates are incomplete. The engineer or PTL decides whether to proceed with acknowledged risk.

Exception: `impl done` on a task that belongs to an unapproved CR must still warn, but the warning must be overridable with explicit acknowledgement (`--accept-risk`). The record of acknowledgement is written to the manifest.

*Why:* Hard gates work for greenfield projects where approval timelines are predictable. In brownfield, inherited stages, partial retrospective approvals, and mid-sprint onboarding make hard gates punishing without improving quality. The audit trail (risk report + acknowledgements) provides the accountability without the blockage.

### BR-BROWNFIELD-007 — Module-scoped init is valid and self-contained

Running `/daksh init --module AUTH` must produce a valid, self-contained manifest that registers only the AUTH module and only the stages relevant to it. All other modules are absent from the manifest. Subsequent stages (`prd AUTH`, `trd AUTH`, etc.) must function without error on a module-scoped manifest.

A module-scoped manifest may later be merged into a full project manifest, but it must never be required to be. Module-scoped adoption is a first-class path, not a workaround.

*Why:* Whole-project init on a live brownfield project requires a PTL to stop the team, audit everything, and commit to a pipeline for work that's already done. Module-scoped init lets a TL adopt Daksh on new work without waiting for organizational alignment on the old work.

### BR-BROWNFIELD-005 — Jira sync checks existing epics before creating

`jira-sync.py` must check `manifest.org.jira.existing_epics` before creating any new Jira epic for a module. If the module maps to an existing epic key (e.g., `"AUTH": "PROJ-42"`), tasks must be created under that epic. A new epic is created only when no mapping exists.

*Why:* Creating a second `AUTH Module` epic in an active Jira project is destructive. Existing sprint plans reference `PROJ-42`; a duplicate orphans those sprint relationships.

---

## Acceptance Criteria

Each AC is the client sign-off criterion for its parent story. These are Given/When/Then.

### AC-BROWNFIELD-001 — Three init mode paths

**Traces to:** US-BROWNFIELD-001, FR-013

**Path A — Greenfield (existing behavior):**
- **Given** an empty repo (no package files, no `src/`, no existing code)
- **When** `/daksh init` is run with no flags
- **Then** the existing greenfield flow runs unchanged

**Path B — Brownfield whole-project:**
- **Given** an existing repo with one or more of: `package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`, `src/`, `lib/`, or `app/` directories
- **When** `/daksh init` is run (or `/daksh init --brownfield`)
- **Then** the user is prompted: "This looks like an existing project. Initialize in brownfield mode? (y/n)"
- **And** if `y` or `--brownfield`: the full baseline scan runs before any questions are asked
- **And** the resulting manifest contains all inferred modules and global stages (00, 10, 20, 30)

**Path C — Brownfield module-scoped:**
- **Given** any repo state (empty or existing)
- **When** `/daksh init --module AUTH` is run
- **Then** no brownfield detection prompt is shown
- **And** no full baseline scan runs — only a narrower scan of the AUTH module directory
- **And** the resulting manifest contains only AUTH stages; global stages are absent
- **And** the output confirms: "Module-scoped pipeline initialized for AUTH. Run `/daksh init` (no flag) to initialize the full project later."

---

### AC-BROWNFIELD-002a — Whole-project baseline scan coverage

**Traces to:** US-BROWNFIELD-002, FR-014

- **Given** whole-project brownfield init is active
- **When** the scan runs
- **Then** `docs/baseline.md` is produced containing at minimum: tech stack (from package files), inferred module boundaries (from top-level directory structure), existing doc locations (READMEs, `docs/`, OpenAPI specs), git branch naming pattern, and detected conventions (test framework, linter, CI config)
- **And** each discovered item is tagged with its source (e.g., `source: package.json`, `source: git-history`)
- **And** the scan completes in under 30 seconds on a repo with ≤100k LOC
- **And** `manifest.modules` is pre-populated with all inferred modules (user can confirm or correct)

### AC-BROWNFIELD-002b — Module-scoped baseline scan coverage

**Traces to:** US-BROWNFIELD-002, FR-014

- **Given** module-scoped brownfield init is active (e.g., `--module AUTH`)
- **When** the scan runs
- **Then** `docs/implementation/AUTH/baseline.md` is produced containing: the AUTH module directory's tech files, test framework, linter config, any existing docs in `docs/implementation/AUTH/` or linked from it, and declared external dependencies (imports, go.mod, etc.)
- **And** the scan does **not** infer or describe other modules
- **And** `manifest.conventions` is pre-populated only with values discoverable from the AUTH module scope
- **And** all scan-derived values carry `"source": "baseline-scan"` in the manifest

### AC-BROWNFIELD-002c — Manifest pre-population (both modes)

**Traces to:** US-BROWNFIELD-002, FR-014

- **Given** either baseline scan has completed
- **When** the manifest is written
- **Then** `manifest.conventions` is pre-populated with discovered values
- **And** all scan-derived values carry `"source": "baseline-scan"` in the manifest
- **And** user-declared overrides carry `"source": "user-declared"`

---

### AC-BROWNFIELD-003a — Inherited stage auto-approval

**Traces to:** US-BROWNFIELD-003, FR-015, BR-BROWNFIELD-001

- **Given** a stage is marked `mode: inherited` in the manifest
- **When** init completes
- **Then** that stage has `status: approved` and `doc_hash` computed from its `inherited_ref` in `baseline.md`
- **And** `/daksh preflight [next-stage]` passes the prior-stage gate check for that stage
- **And** `/daksh approve [inherited-stage]` exits with an informational message: "This stage is inherited — no approval needed"

### AC-BROWNFIELD-003b — Delta stage document structure

**Traces to:** US-BROWNFIELD-003, BR-BROWNFIELD-002

- **Given** a stage is marked `mode: delta`
- **When** the stage is run
- **Then** the stage output contains a clearly marked "Inherited state" section (prose reference, no IDs) and a "What's changing" section (with UC/FR/US/TASK IDs for new work only)
- **And** `manifest.traceability` contains entries only for IDs in the "what's changing" section

---

### AC-BROWNFIELD-004 — Conventions block governs impl commands

**Traces to:** US-BROWNFIELD-004, BR-BROWNFIELD-003

- **Given** `manifest.conventions.git.branch_template` is set (e.g., `"feat/{module}/{task-slug}"`)
- **When** `/daksh impl start TASK-AUTH-001` runs
- **Then** the git branch created matches that template (e.g., `feat/auth/task-auth-001`), not the Daksh default
- **And** if `manifest.conventions.code.indent` is `"4-space"`, new Python files created in the task branch use 4-space indentation, regardless of what `references/python-guidelines.md` specifies

---

### AC-BROWNFIELD-005 — Configurable approval authority

**Traces to:** US-BROWNFIELD-005

- **Given** `manifest.org.governance.stage_authority` is defined with e.g. `"40a": ["PTL", "Client"]`
- **When** `/daksh approve prd AUTH --approver "Ravi"` is run and Ravi has role `Client` in the roster
- **Then** the approval is accepted and recorded
- **And** if `manifest.org.governance.stage_authority` is absent, `approve.py` falls back to the existing hardcoded PTL/TL map

---

### AC-BROWNFIELD-006a — Jira epic bridging

**Traces to:** US-BROWNFIELD-006, BR-BROWNFIELD-005

- **Given** `manifest.org.jira.existing_epics` maps `"AUTH"` to `"PROJ-42"`
- **When** `/daksh jira push --module AUTH` runs
- **Then** tasks are created as child stories under `PROJ-42`, not under a new epic
- **And** no new `"AUTH Module"` epic is created in Jira

### AC-BROWNFIELD-006b — Capacity-aware sprint assignment

**Traces to:** US-BROWNFIELD-006

- **Given** `manifest.org.capacity` specifies: `current_sprint: 4`, `velocity_per_engineer: 10`, `team_allocation.AUTH.engineers: 2`
- **When** stage 40c sizes AUTH tasks into sprints
- **Then** Daksh validates that sprint assignments don't exceed `20 pts/sprint` for AUTH
- **And** if the task list exceeds capacity, Daksh warns: "AUTH work requires N sprints at current velocity. Adjust task list or extend timeline."
- **And** no tasks are assigned to sprints ≤ `current_sprint` (already started)

---

### AC-BROWNFIELD-008 — Risk report replaces hard gate blocks

**Traces to:** US-BROWNFIELD-008, BR-BROWNFIELD-006

- **Given** a stage gate is not satisfied (missing approval, stale hash, or unapproved CR)
- **When** the engineer runs the next stage or `/daksh preflight`
- **Then** a risk report is printed listing every gate gap: stage, missing approver, hash status, blocking CR if any
- **And** the engineer is asked: "Proceed with acknowledged risk? (y/n)"
- **And** if `y`: execution continues and a risk acknowledgement entry is written to the manifest with the approver name, date, and listed gaps
- **And** if `n`: execution stops with no manifest change
- **And** `/daksh tend` surfaces all unresolved risk acknowledgements as a separate audit category ("Pending approvals with acknowledged risk: N")

---

### AC-BROWNFIELD-009 — Module-scoped init

**Traces to:** US-BROWNFIELD-009, BR-BROWNFIELD-007

- **Given** an existing repo with no Daksh manifest
- **When** `/daksh init --module AUTH` is run
- **Then** a valid `docs/.daksh/manifest.json` is created containing only the AUTH module and its stage entries (`40a+40b:AUTH`, `40c:AUTH`, `50:AUTH`)
- **And** `docs/implementation/AUTH/` and `docs/implementation/AUTH/change-records/` are scaffolded
- **And** global stages (00, 10, 20, 30) are absent from the manifest — no stubs, no placeholders
- **And** running `/daksh prd AUTH` succeeds on this module-scoped manifest without error
- **And** a subsequent `/daksh init` (full project init) on the same repo detects the existing module-scoped manifest and offers to merge rather than overwrite

---

### AC-BROWNFIELD-007 — Discovery Records

**Traces to:** US-BROWNFIELD-007, BR-BROWNFIELD-004

- **Given** an engineer running `/daksh impl start TASK-AUTH-001` finds a legacy constraint in existing code
- **When** they raise a Discovery Record
- **Then** a `DR-NNN.md` file is scaffolded in `docs/implementation/AUTH/change-records/`
- **And** the DR uses the DR template (not the CR template): sections are "What we found", "Where it lives" (code paths), "Impact on current work", "Impact on baseline", "Proposed path forward"
- **And** `manifest.change_records` records the DR under `DR-NNN` (distinct from `CR-NNN`)
- **And** `/daksh tend` surfaces open DRs as a distinct audit category from open CRs

---

## Data Contract

This module is an extension of Daksh itself — its inputs are the existing filesystem and the manifest it helps create.

**Consumes:**

| Source | What | Used by |
|--------|------|---------|
| Filesystem | Package manifests (`package.json`, `pyproject.toml`, etc.) | Baseline scan → tech stack detection |
| Filesystem | Directory structure, git history, linter/CI config | Baseline scan → module and convention detection |
| Filesystem | Existing `docs/`, READMEs, OpenAPI specs | Baseline scan → doc location mapping |
| User input | Confirmation/correction of scan results | init Q&A |
| Jira API (optional) | Existing epic keys, custom fields, workflow statuses | Org adapter → Jira bridging |

**Produces:**

| Artifact | Type | Consumed by |
|----------|------|-------------|
| `docs/baseline.md` | Document | All stages (inherited and delta stages reference it) |
| `manifest.conventions` | Manifest field | impl commands (git ops, coding guidelines), tend (codebase audit) |
| `manifest.org` | Manifest field | approve.py (governance), jira-sync.py (bridging), 40c (capacity) |
| `manifest.stages[*].mode` | Manifest field | preflight (gate validation), approve.py (auto-approval), all stages |
| `DR-NNN.md` | Artifact | tend (open DR audit), baseline.md (patches), sprint planning |
| `manifest.risk_acknowledgements` | Manifest field | tend (pending risk audit), preflight (gate gap visibility) |

**Cross-module contracts this module introduces:**

- `manifest.conventions` is a read contract. Any command that performs git operations or writes code must read it before acting.
- `manifest.org.governance.stage_authority` is an override contract. `approve.py` must prefer it over hardcoded role maps when present.
- `docs/baseline.md` is a shared reference. Inherited and delta stages reference it by section; they must not duplicate its content.

---

## Resolved Decisions

These were open questions at PRD draft time. They are resolved here so the TRD has firm decisions to implement.

1. **Brownfield detection threshold** — Trigger brownfield prompt if the repo contains any of: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `composer.json`; OR any of `src/`, `lib/`, `app/` directories with at least one file; OR a git history with ≥ 5 commits. All three checks are OR-joined. If any matches, the user sees the prompt. TRD must implement this exact heuristic in `init.py`.

2. **Baseline doc hash** — Inherited stages hash a named section of `baseline.md`, not the whole file. Sections are delimited by HTML comments: `<!-- section:stage-00 -->` … `<!-- /section:stage-00 -->`. `approve.py` extracts the text between the markers and hashes that substring. Changes to other sections do not invalidate inherited stage approvals. If the section marker is missing, `approve.py` exits with an error. TRD must specify the marker naming convention.

3. **DR approval gate** — Discovery Records are **advisory**. They are surfaced by `/daksh tend` as a distinct category ("Open Discovery Records: N") but do not block task closure or stage approval. Rationale: DRs represent found reality, not spec failure. Blocking on found reality recreates the hard-gate problem BR-BROWNFIELD-006 explicitly rejects.

4. **Conventions block population order** — **Manifest wins over scan.** If `manifest.conventions` already has a value for a field, the scan does not overwrite it. If the scan finds a value for a field not yet in the manifest, it adds it with `"source": "baseline-scan"`. If the scan finds a value that differs from an existing manifest value, it prints a warning: `"Scan found [X] for [field]; manifest has [Y]. Keeping manifest value."` No interactive merge prompt — silent manifest-wins, visible warning.

5. **Migration for pre-BROWNFIELD manifests** — `/daksh tend` warns when it detects a manifest missing `conventions`, `org`, or stage `mode` fields. The warning names exactly which fields are absent. No new command — `tend --fix` adds `"conventions": {}`, `"org": {}`, and `"mode": "greenfield"` to all existing approved stages. Manual edits are always allowed and take precedence.

6. **Risk acknowledgement expiry** — An acknowledgement becomes **stale** when the doc hash it covered has since changed. `preflight.py` checks: for each acknowledgement in `manifest.risk_register`, if the current hash of the referenced document differs from the hash at acknowledgement time, the entry is marked `"status": "stale"` and a new WARN is raised. Stale entries are not deleted — they remain as an audit trail. A fresh acknowledgement replaces them.

7. **Module-scoped manifest merge** — Module-scoped stage keys are already namespaced by module (`40a+40b:AUTH`), so they merge without collision into a full project manifest. Traceability IDs are prefixed by module (`TASK-AUTH-001`), so they also merge cleanly. The only conflict case is a stage key that exists in both manifests with different statuses (e.g., `40a+40b:AUTH` is `approved` in the module manifest but `pending_approval` in the full manifest). Resolution rule: **higher status wins** (`approved` > `pending_approval` > `not_started`). TRD must implement a `merge` subcommand on `init.py` that applies this rule and prompts the user to confirm any status upgrades.

---

## Approval

Approved by: Yeshwanth
Role:        PTL
Date:        2026-03-30
Hash:        47c869ed926b…
