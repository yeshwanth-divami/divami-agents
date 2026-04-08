# Client Context — Daksh

## Why Daksh Exists

Daksh is an internal process skill for Divami, a 100-engineer software
services firm. It structures the entire product development lifecycle —
from client onboarding through implementation — as a series of gated
[stages](glossary#stage), each producing a specific artifact that feeds the next. The
trigger: AI copilots amplify both discipline and chaos equally, and
Divami needs the discipline side to win by default. Daksh is the
answer to "how do we make the right way the easy way?"

## Product Summary

Daksh is a numbered, stage-by-stage methodology implemented as an ICM
skill (Interpretable Context Methodology). It runs inside AI coding
assistants (Claude Code, Codex, etc.) and guides engineers through:

1. **Client onboarding** — capture context before work begins
2. **Vision → Business Requirements → Roadmap** — strategic documents
   with [traceability](glossary#traceability-chain) ([UC](glossary#uc) → [FR](glossary#fr) → [US](glossary#us) → [TASK](glossary#task))
3. **Module-level PRD → TRD → Tasks** — per-module deep specs
4. **Implementation** — one task per session, with [change records](glossary#change-record) and
   git workflow

Each stage has an [approval gate](glossary#approval-gate). A [manifest](glossary#manifest) (`docs/.daksh/manifest.json`)
tracks state, [doc hashes](glossary#doc-hash), [approvals](glossary#approval), contracts, and traceability across all
stages.

## User Types

| Role | Primary Pain |
|------|-------------|
| **PTL (Project Tech Lead)** | No visibility into whether docs are current, complete, or approved. Spends time chasing status instead of reviewing substance. |
| **TL (Tech Lead)** | Receives vague specs, makes assumptions during implementation, discovers misalignment too late. Needs specs that are both precise and navigable. |
| **Engineer** | Gets Jira tickets with no context. Doesn't know what decisions they can make vs. what needs escalation. Needs self-contained tasks with [decision budgets](glossary#decision-budget). |
| **Yeshwanth (Creator/Maintainer)** | Needs Daksh to be self-sustaining — adopted because it's easier to use than skip, improved via PRs from the team. |

## Constraints

1. **Token budget** — Each stage must fit in a single copilot context
   window. No stage can require reading more than ~3 prior documents.
2. **No external dependencies at launch** — Jira sync, approval
   automation are planned but not required for day-1 value.
3. **Progressive rollout** — Whatever is ready ships. No big-bang release.
   Engineers start using available stages immediately.
4. **Skill, not app** — Daksh runs inside existing AI tools. No separate
   UI, no server, no database. The filesystem is the database.
5. **Internal only** — Client is Divami. No external client approval
   workflows needed initially.
6. **Greenfield assumption (retrofitted via CR-001)** — the initial pipeline
   assumed projects start at stage zero. The BROWNFIELD module adds three
   init modes: `greenfield` (default), whole-project brownfield
   (`--brownfield`), and module-scoped brownfield (`--module AUTH`). Each
   mode produces different baseline artifacts and sets different inherited
   stage states in the manifest. Teams do not have to commit to a
   whole-project retrofit to get process discipline on new work.
7. **Gates must not block forward progress** — approval gates are
   informational, not hard blockers. Missing approvals or inconsistencies
   surface as a visible risk report; teams may proceed with acknowledged
   risk (`--accept-risk`). Hard enforcement is out of scope until real usage
   proves a gate is worth the friction.

## Tools & Integrations

| Tool | Config | Value |
|------|--------|-------|
| Jira | Project key | TBD — set before first `/daksh approve tasks` |
| Jira | Board ID | TBD — set before first `/daksh approve tasks` |

> Both values belong in `manifest.jira.project_key` and `manifest.jira.board_id`. Set them once; every subsequent `approve tasks` auto-pushes to Jira.

## Unvalidated Assumptions

1. **Engineers will actually invoke Daksh stages** rather than prompting
   the copilot freeform. The "easier to use than skip" bar hasn't been
   tested with real engineers yet.
2. **The manifest won't become a merge conflict magnet** when multiple
   people work on different modules concurrently.
3. **Doc-narrator and vyasa skills exist and work** — Daksh references
   them but doesn't own them. If they're broken, Daksh output quality
   drops.
4. **One task per session (stage 50) is practical** — Engineers may
   resist the constraint if tasks are trivially small or if context
   switching between sessions is expensive.
5. **PRs to Daksh will actually happen** — The assumption that engineers
   will improve the skill requires both motivation and understanding of
   ICM format.
6. **Brownfield adoption works as designed** — The BROWNFIELD module's
   retrofit flow (scan existing repo → map to stage outputs → fill gaps)
   hasn't been tested on a real existing project. Three init modes exist;
   none have been validated in the field.
7. **Teams will trust a risk report instead of a hard gate** — the
   non-blocking approval model assumes teams read the risk report and make
   an informed call. If teams ignore it and proceed blindly, the governance
   model degrades to theater. The `--accept-risk` escape hatch is useful
   only if the report it bypasses is actually read.
8. **Module-scoped adoption creates enough value on its own** — a team
   that adopts Daksh for one new module while the rest of the project is
   unmanaged may get partial benefit but also mismatched artifacts. The
   assumption is that partial is better than none; this hasn't been tested.
9. **Discovery Records (DR-NNN) will be raised faithfully** — the
   DR artifact type only works if engineers actually raise DRs when they
   hit legacy constraints, rather than silently working around them.
   Adoption of a new artifact type is a behavior change, not a tooling
   change.

## Open Questions

1. How do we measure adoption? Git hook that detects `/daksh` invocations?
   Manifest audit? Honor system?
2. What's the minimum viable stage set for day-1? All 8 stages, or a
   subset (e.g., 40c + 50 only for teams already past planning)?
3. Who owns Daksh maintenance long-term? Yeshwanth alone, or a rotating
   maintainer?
4. Should Daksh enforce stage ordering, or just warn? Strict gates vs.
   advisory gates.

## Approval

Approved by: Yeshwanth
Role:        PTL
Date:        2026-03-30
Hash:        ccb365b14341…
