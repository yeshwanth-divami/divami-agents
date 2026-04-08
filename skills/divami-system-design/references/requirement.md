# Project Scoping Skill — Full Session Briefing

## Context

You are helping build a Claude Code SKILL.md system for a design and AI-led product engineering company (service model, not product). The company takes on client projects — SaaS platforms, enterprise modernization, deep tech products — and needs to produce accurate, defensible project scopes and effort estimates before a project kicks off. Currently this process is ad hoc, inconsistent, and person-dependent. The goal is to systematize it into a reusable, LLM-executable skill folder that any team member can invoke.

This is not a chatbot. This is a structured agentic skill that Claude Code will execute step-by-step using a defined pipeline, referencing firm-specific data, and producing client-deliverable outputs.

---

## What We Are Building

A folder-based SKILL.md system under `.claude/skills/project-scoping/` that executes a six-stage pipeline:

1. **Discovery** — Interrogates the user (BD/PM/tech lead) to extract all knowable project inputs
2. **Domain Decomposition** — Breaks the problem into bounded contexts, components, and system boundaries
3. **Architecture Selection** — Selects and justifies an architecture pattern; produces ADRs and C4 diagrams
4. **WBS Generation** — Produces a hierarchical work breakdown across all delivery layers
5. **Effort Estimation** — Generates PERT-ranged estimates per task/phase with risk-adjusted confidence levels
6. **SOW Formatting** — Assembles a client-facing scope document with assumptions, exclusions, and change control language

---

## Folder Structure

```
/Users/yeshwanth/.codex/skills/divami-system-design
  ├── SKILL.md
  ├── references/
  │   ├── estimation-benchmarks.md
  │   ├── rate-card.md
  │   ├── risk-multipliers.md
  │   └── architecture-patterns.md
  ├── subskills/
  │   ├── 01-discovery.md
  │   ├── 02-domain-decomposition.md
  │   ├── 03-architecture-selection.md
  │   ├── 04-wbs-generation.md
  │   ├── 05-effort-estimation.md
  │   └── 06-sow-formatter.md
  ├── templates/
  │   ├── requirements-doc.md
  │   ├── context-map.md
  │   ├── adr-template.md
  │   ├── wbs-template.md
  │   ├── estimate-sheet.md
  │   └── sow-template.md
  └── examples/
      ├── saas-dashboard-project/
      └── enterprise-integration/
```

---

## File-by-File Responsibilities

### `SKILL.md` — Orchestrator
- Declares the pipeline sequence
- Loads and passes outputs between subskills
- Enforces gate conditions: if any stage output is below confidence threshold or contains unresolved ambiguities, it halts and surfaces a clarification request before proceeding
- Accepts an optional `--stage` flag to run a single subskill in isolation
- Accepts an optional `--resume` flag to continue from a saved stage output

### `references/estimation-benchmarks.md`
- Historical velocity data per project type and delivery layer
- Format: project archetype → layer → low/mid/high effort range in person-days
- Populated with generic industry benchmarks initially; replaced with firm actuals over time
- Subskill 05 reads this as its primary calibration source

### `references/rate-card.md`
- Internal only; excluded from all client-facing outputs
- Maps roles to daily rates
- Used by the SOW formatter to compute pricing ranges from effort ranges
- Must be explicitly flagged as confidential; skill must never include rate card data in SOW output

### `references/risk-multipliers.md`
- Coefficient table: complexity factors → effort multipliers
- Example factors: greenfield vs. legacy migration, unclear requirements score, third-party API dependency count, regulatory compliance requirements, distributed team, first-time domain
- Format: factor → condition → multiplier range
- Subskill 05 applies these to raw WBS estimates

### `references/architecture-patterns.md`
- Catalog of architecture styles: modular monolith, microservices, event-driven, layered, CQRS/ES, BFF, etc.
- Each entry: pattern name → best-fit conditions → cost/complexity surface → known risks → team size requirements
- Subskill 03 uses this as a decision matrix

---

## Subskill Specifications

### `01-discovery.md`
**Input:** Raw client brief, meeting notes, RFP, or free-form description  
**Process:**
- Runs a structured interrogation across six dimensions:
  1. Functional scope (features, user types, key workflows)
  2. Non-functional requirements (scale, latency, availability, compliance)
  3. Integration surface (third-party APIs, legacy systems, data sources)
  4. Constraints (budget range, timeline, team, existing tech stack)
  5. Unknowns and risks (unclear areas, dependencies outside client control)
  6. Success criteria (what does done look like for the client)
- Flags every unanswered dimension as an open question
- Assigns a completeness score (0–100) to the discovery output
- Halts pipeline if completeness < 70

**Output:** Populates `templates/requirements-doc.md`

---

### `02-domain-decomposition.md`
**Input:** Completed requirements doc  
**Process:**
- Applies Event Storming concepts: identify domain events → group into aggregates → define bounded contexts
- Maps contexts to system boundaries (what is in scope vs. out of scope)
- Identifies shared kernels and integration points between contexts
- Produces a component inventory: name, responsibility, owns/consumes data, integration dependencies

**Output:** Populates `templates/context-map.md`

---

### `03-architecture-selection.md`
**Input:** Context map + non-functional requirements from requirements doc  
**Process:**
- Extracts top 3 driving architecture characteristics (e.g., scalability, maintainability, deployability)
- Scores each candidate pattern from `references/architecture-patterns.md` against driving characteristics
- Selects the highest-scoring pattern; documents runner-up and rejection rationale
- Produces one ADR per major architectural decision using `templates/adr-template.md`
- Generates C4 Level 1 (system context) and Level 2 (container) diagrams in Mermaid

**Output:** Populated ADRs + Mermaid diagrams + architecture summary section for SOW

---

### `04-wbs-generation.md`
**Input:** Context map + architecture selection output  
**Process:**
- Generates a hierarchical WBS across all delivery layers:
  - Frontend (component library, pages, state management, responsive/accessibility)
  - API layer (endpoints, auth, validation, error handling)
  - Data layer (schema design, migrations, query optimization)
  - Infrastructure (environments, CI/CD, IaC, monitoring)
  - Integrations (per third-party, per legacy system)
  - Auth & security
  - Testing (unit, integration, E2E, performance)
  - DevOps & deployment
  - Project management overhead
- Each WBS node: task name, layer, estimated complexity (S/M/L/XL), dependencies, owner role
- Explicitly lists exclusions: what is not in this WBS and why

**Output:** Populates `templates/wbs-template.md`

---

### `05-effort-estimation.md`
**Input:** WBS + risk multipliers from references + estimation benchmarks  
**Process:**
- Maps each WBS node complexity (S/M/L/XL) to person-day ranges from benchmarks
- Applies risk multipliers from `references/risk-multipliers.md` per identified risk factor
- Computes three estimates per phase using PERT formula: `E = (O + 4M + P) / 6`
  - O = optimistic, M = most likely, P = pessimistic
- Aggregates to phase-level and total-project-level ranges
- Assigns confidence level per phase (High / Medium / Low) based on discovery completeness and risk score
- Produces assumptions log: every estimate is traceable to a stated assumption
- Produces an exclusions log cross-referenced with WBS exclusions

**Output:** Populates `templates/estimate-sheet.md`

---

### `06-sow-formatter.md`
**Input:** All prior stage outputs  
**Process:**
- Assembles client-deliverable SOW using `templates/sow-template.md`
- Sections:
  1. Project Overview
  2. Scope of Work (derived from WBS, written in non-technical language)
  3. Out of Scope
  4. Technical Approach Summary (from architecture selection, simplified)
  5. Deliverables list with acceptance criteria
  6. Timeline (phased, with PERT ranges)
  7. Effort Estimate (ranged, with confidence levels)
  8. Assumptions
  9. Exclusions
  10. Change Control clause (boilerplate)
- Strips all internal data: rate card, internal benchmarks, risk coefficient values
- Flags any section where confidence is Low with a `[REQUIRES REVIEW]` marker

**Output:** Populates `templates/sow-template.md` as a complete document

---

## Pipeline Execution Logic (in SKILL.md)

```
1. Load client brief
2. Run 01-discovery → check completeness score
   - If < 70: surface open questions, halt, request input
   - If ≥ 70: proceed
3. Run 02-domain-decomposition
4. Run 03-architecture-selection
5. Run 04-wbs-generation
6. Run 05-effort-estimation
7. Run 06-sow-formatter
8. Output: SOW document + internal estimate sheet (separate)
```

Each stage writes its output to the corresponding template file before the next stage loads it. This makes every intermediate artifact inspectable and editable by a human before the pipeline continues.

---

## Design Principles

**Separation of internal and client-facing outputs**
The estimate sheet and SOW are always separate files. Rate card and risk coefficients never appear in client output.

**Every number is traceable**
Every effort figure in the estimate sheet references a WBS node, a benchmark source, and an applied risk multiplier. No magic numbers.

**Confidence is explicit**
Every phase carries an explicit confidence level. Low-confidence phases are marked for human review before the SOW is sent.

**The skill grows with the firm**
`references/estimation-benchmarks.md` is designed to be updated after every completed project. Over time it becomes the firm's proprietary calibration data — the primary moat of this system.

**Human gates, not full automation**
The pipeline halts at ambiguity rather than proceeding on assumptions. Scoping errors caught before a SOW is sent are free. Scoping errors caught during delivery are expensive.

---

## Theoretical Foundations

The skill is grounded in:
- **Domain-Driven Design** (Evans, Vernon) — for decomposition and boundary identification
- **Fundamentals of Software Architecture** (Richards & Ford) — for architecture characteristic identification, ADR structure, and C4 diagramming
- **Software Architecture: The Hard Parts** (Ford et al.) — for trade-off analysis driving architecture selection
- **Software Estimation: Demystifying the Black Art** (McConnell) — for PERT, benchmarking, and estimation heuristics
- **Agile Estimating and Planning** (Cohn) — for story-level sizing and velocity-based calibration
- **COSMIC Function Points** (ISO 19761) — as an optional sizing methodology for regulated or fixed-price contexts
- **C4 Model** (Simon Brown) — for architecture diagrams in client deliverables

---

## What to Build in This Session

When this briefing is provided to a new session, the task is:

1. Author each file in the folder structure above
2. Start with `SKILL.md` (orchestrator), then subskills in order, then templates, then references stubs
3. Each subskill must include: purpose, input contract, output contract, step-by-step process instructions, failure conditions, and a reference to its output template
4. Templates must include placeholder sections with field descriptions, not just blank headers
5. References must be authored as functional stubs with generic industry data that can be replaced with firm actuals
6. Examples directory is out of scope for this session — flagged for a future session after the core skill is validated on a real project

Build one file at a time. Confirm each file before proceeding to the next.