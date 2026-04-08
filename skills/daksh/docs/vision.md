# Why Daksh — and Why Now

Daksh is Divami's process skill for AI-assisted software engineering. It exists because AI copilots are force multipliers — but they multiply whatever's already there. A disciplined team gets more disciplined; a chaotic team gets faster chaos. Divami (100 engineers, services firm, multiple concurrent client projects) needs the discipline side to win by default. Daksh encodes that discipline as a numbered, stage-gated methodology that runs inside the copilot itself — so the right way is the path of least resistance.

The timing is simple: copilot adoption at Divami is accelerating, and without a shared process embedded in the tools, every engineer will invent their own workflow. That's Conway's Law applied to AI tooling — the system mirrors the org, and right now the org has no shared language for how copilot-assisted work should flow.

## Vision Statement

Daksh is how we approach software engineering at Divami.

## Target Users

| Role | Before Daksh | After Daksh |
|------|-------------|-------------|
| **PTL (Project Tech Lead)** | Chases status across Gmail-Chat, Jira, Gmail, Whatsapp, Google-Docs. No single source of truth for what's approved, what's in flight, what's blocked. | Opens the manifest — sees every stage's status, approvals, and contracts in one place. Reviews substance, not status. |
| **TL (Tech Lead)** | Receives vague specs, makes assumptions, discovers misalignment at code review. | Gets a TRD with justified design decisions that trace back to approved requirements. Knows what's decided vs. what's their call. |
| **Engineer** | Gets Jira tickets with no context. Doesn't know what decisions they can make. | Starts a session with `/daksh <task>` and gets a self-contained brief with decision budgets, acceptance criteria, and git workflow. |
| **Yeshwanth (Creator/Maintainer)** | Manually enforces process through reviews and reminders. | Daksh is self-sustaining — adopted because it's easier to use than skip, improved via PRs from the team. |

## Problem Statements

**1. Process knowledge lives in people's heads, not in the tools.**
Every PTL has a "how I run projects" mental model. None of them are written down. When a PTL is on leave, the project drifts. When a new PTL joins, they reinvent. Risk: institutional knowledge loss scales linearly with headcount.

**2. Copilots amplify whatever process (or lack thereof) already exists.**
An engineer with a clear spec and a copilot ships faster. An engineer with a vague ticket and a copilot ships wrong faster. The copilot doesn't know the difference. Risk: AI-assisted velocity without AI-assisted direction creates expensive rework.

**3. Documentation is written once and abandoned.**
Vision docs, BRDs, PRDs — they get written for kickoff and never updated. By sprint 3, the code and the docs have diverged. Nobody trusts the docs, so nobody reads them, so nobody updates them. Risk: the documentation death spiral makes specs actively misleading.

## Core Capabilities

1. **Stage-gated methodology** — named stages (`onboard`→`vision`→`brd`→`roadmap`→`prd`→`trd`→`tasks`→`impl`) with approval gates. Each stage produces one artifact that feeds the next.
2. **Traceability chain** — UC → FR → US → TASK. Every implementation task traces back to a user need. Orphan work gets flagged.
3. **Manifest as single source of truth** — `docs/.daksh/manifest.json` tracks state, hashes, approvals, and contracts across all stages.
4. **Embedded in the copilot** — runs as a skill inside Claude Code, Codex, etc. No separate UI, no server, no context switching.
5. **Self-contained task sessions** — `/daksh impl` gives an engineer everything they need for one task in one session: spec, decision budget, acceptance criteria, git workflow.
6. **Brownfield retrofit** — bring Daksh to an existing codebase through three modes: greenfield (clean slate), whole-project brownfield (baseline scan + inherited stage modes + org adapter), or module-scoped brownfield (`--module AUTH`, no full-project commitment required).
7. **Risk-report governance** — approval gates surface missing approvals and inconsistencies as a visible risk report rather than a hard block. The record exists; the team decides whether to proceed with acknowledged risk.
8. **Discovery Records** — a distinct artifact type (DR-NNN) for legacy constraint discoveries during implementation, separate from spec-divergence change records (CR-NNN). DRs feed back into the baseline and tend audit.

## Commands

| Command | What it does | Small project |
|---------|-------------|---------------|
| `/daksh init` | Initializes the pipeline — creates manifest, determines weight class, scaffolds `docs/` | — |
| `/daksh onboard` | Client onboarding — captures product context, user types, constraints, unvalidated assumptions | Combined with `vision` |
| `/daksh vision` | Translates client context into a locked product vision | Combined with `onboard` |
| `/daksh brd` | Decomposes vision into traceable use cases, functional and non-functional requirements, and acceptance criteria | — |
| `/daksh roadmap` | Sequences BRD into milestones, sprints, and cross-module contracts | — |
| `/daksh prd` | Module-level product spec — user stories, business rules, client sign-off criteria | Combined with `trd` |
| `/daksh trd` | Module-level technical design — architecture, data model, API contracts, tech choices | Combined with `prd` |
| `/daksh tasks` | Breaks TRD into Jira-ready tasks with decision budgets and acceptance criteria | — |
| `/daksh impl` | Execution session — one task, one engineer, self-contained brief with git workflow | — |
| `/daksh approve` | Records a gate approval with doc hash tied to the approver | 1 sign-off (vs 2) |
| `/daksh preflight` | Validates stage readiness — checks gates, skills, and context budget before running | — |
| `/daksh tend` | Health audit — flags stale hashes, orphan IDs, missing artifacts | Run at end of project |
| `/daksh jira` | Bidirectional Jira sync — push roadmap/tasks to Jira, pull status back | Optional |

## Scope

**In scope (day-1):**
- All 8 stages as named copilot commands: `onboard`, `vision`, `brd`, `roadmap`, `prd`, `trd`, `tasks`, `impl`
- Manifest tracking for stage state and approvals
- Filesystem-only operation — no external dependencies
- Internal rollout at Divami via dedicated communication channel

**In scope (near-term):**
- `/daksh approve` — structured approval workflow
- `/daksh preflight` — pre-stage validation checks
- `/daksh tend` — manifest maintenance and health checks
- `/daksh jira` — Jira ticket generation from roadmap output
- BROWNFIELD module — retrofit Daksh onto existing repos in three modes (whole-project or module-scoped), with baseline scan, inherited stage modes, conventions block, org adapter, risk-report governance, and Discovery Records

**Out of scope (not yet defined):**
- External client-facing approval workflows
- Automated Jira sync (planned, not required for day-1)
- CI/CD integration or git hooks for enforcement
- What Daksh will "never do" is an open question — the boundaries will
  emerge from real usage

## Leap-of-Faith Assumptions

Two beliefs that must hold for Daksh to succeed. If either is wrong, the product fails — not degrades, fails.

**1. Engineers will actually invoke Daksh stages rather than prompting the copilot freeform.** (Unvalidated)

The entire value proposition rests on adoption. Daksh only works if engineers choose to use it. The "easier to use than skip" bar hasn't been tested with real engineers yet. If invoking `/daksh` feels like overhead rather than shortcut, engineers will route around it — and a process tool that's routed around is worse than no tool at all, because leadership thinks the process exists.

**2. Doc-narrator and vyasa skills exist and work as dependencies.**
(Unvalidated)

Daksh's output quality depends on two skills it doesn't own. If they're broken or missing, every stage produces lower-quality documentation.  This is a dependency risk more than a kill risk — Daksh still functions, but its outputs lose the narrative quality that makes them worth reading instead of skimming.

> **Note:** Assumption #2 is load-bearing for quality but not for
> existence. If forced to pick one assumption to validate first,
> validate #1. A well-adopted Daksh with mediocre formatting beats a
> beautifully-formatted Daksh nobody uses.

## Success Metrics

**At handoff (Daksh is "ready"):**
- All 8 stages produce correct, traceable output when invoked (`/daksh onboard` through `/daksh impl`)
- Manifest accurately tracks state across stages
- At least one real Divami project has run `/daksh onboard` through `/daksh impl` end-to-end

**At adoption (Daksh is "working"):**
- Every new project starts with `/daksh init`
- Every engineer starts their session with `/daksh <task>`
- Engineers submit PRs to improve Daksh — the skill evolves with usage

## Open Questions

1. **How do we measure adoption?** Git hooks that detect `/daksh` invocations? Manifest audits? Self-reported? The success metrics above are aspirational — we need an observable proxy.
2. **What is Daksh's "never" list?** The out-of-scope boundary is currently undefined. Real usage will surface what Daksh should explicitly refuse to do.
3. **What's the minimum viable stage set for day-1?** All 8 stages, or a subset for teams already past planning (e.g., 40c + 50 only)?
4. **Who owns Daksh maintenance long-term?** Yeshwanth alone, or a rotating maintainer? Single-owner skills are single points of failure.
5. **Should stage gates enforce or advise?** Currently gates warn/block based on approval counts. Should Daksh ever hard-prevent proceeding, or always allow override with a warning?

## Approval

Approved by: Yeshwanth
Role:        PTL
Date:        2026-03-30
Hash:        ccb365b14341…
