# What JIRA Does — and Why Daksh Talks to Jira

Daksh is the source of truth for what gets built and why. Jira is where Divami's teams track execution. Without a bridge, PTLs manually copy task breakdowns into Jira — a slow, error-prone handoff that drifts within days. The JIRA [module](../../glossary#module) closes that gap: a PTL runs `/daksh jira push` and the full epic/sprint/story hierarchy lands in Jira automatically, keyed to the same [TASK](../../glossary#task) IDs that live in `tasks.md`. When engineers mark stories done in Jira, `/daksh jira pull` reflects that status back — without overwriting a single line of task content. The module also surfaces a name-filtered task view so engineers can ask Daksh "what's mine?" and get a direct answer after sprint planning.

This PRD defines the user-facing behavior of the JIRA module. The TRD (`trd.md`) defines how `scripts/jira-sync.py` and the `commands/jira/CONTEXT.md` implement it.

This document implements the roadmap at `../../implementation-roadmap.md`, milestone M2.

---

## Scope

**In scope:**
- `scripts/jira-sync.py` — push, pull, status subcommands
- `commands/jira/CONTEXT.md` — routes `/daksh jira` invocations to the script
- Enhancement to `scripts/list-tasks.py` — `--name`, `--sprint`, `--open` flags with `user_map` support
- `manifest.jira.ticket_map` — TASK ID → Jira issue key mapping
- `manifest.jira.user_map` — Daksh roster name → Jira display name mapping

- Time block tracking per task — start on `/daksh impl`, stop via `/daksh impl MODULE time-block stop TASK-ID`; logs to Jira Work Log and `manifest.traceability`

**Explicitly out of scope:**
- Creating Jira boards or projects from scratch — `project_key` and `board_id` must exist before push
- Real-time or webhook-based sync — this is a pull-on-demand model
- Content sync from Jira back to `tasks.md` — description, ACs, and decision budget are Daksh-owned; pull touches status only
- Jira field mapping beyond the epic > sprint > story hierarchy (no custom fields, no components, no labels)
- Slack or email notifications on sync events

---

## User Stories

### US-JIRA-001 — Push task breakdown to Jira

As a PTL, I can run `/daksh jira push` to create Jira epics, sprints, and stories from the roadmap and all `tasks.md` files so that the team can track execution in Jira without re-entering the breakdown manually.

**Traces to:** [UC-004](../../business-requirements.md) (Run a Module Document Stage — Jira sync alternate flow), Sprint 2

### US-JIRA-002 — Pull Jira status back into Daksh

As a PTL, I can run `/daksh jira pull` to sync done status from Jira back into `tasks.md` and `manifest.traceability` so that Daksh's health view stays current without manual manifest edits.

**Traces to:** [UC-004](../../business-requirements.md) (Jira sync alternate flow), Sprint 2

### US-JIRA-004 — Track time blocks per task for velocity reporting

As an engineer, I can start a time block automatically when I begin an impl session and stop it explicitly when I pause or finish, so that my actual working time is logged in both Jira and Daksh without manual timesheet entry.

**Traces to:** [UC-005](../../business-requirements.md) (Implement a Task), Sprint 2

### US-JIRA-003 — List tasks assigned to a named engineer

As an engineer, I can run `/daksh list-my-tasks --name "Alice"` to see only my assigned tasks across all modules so that I don't have to scan every `tasks.md` to find what I own.

**Traces to:** [UC-004.5](../../business-requirements.md) (List Tasks for an Engineer), Sprint 3

---

## Business Rules

### BR-JIRA-001 — Hierarchy mapping is fixed

Push maps exactly: each Daksh [module](../../glossary#module) becomes a Jira Epic; each Sprint label in `tasks.md` becomes a Jira Sprint on the configured board; each task becomes a Jira Story linked to its Epic and placed in its Sprint. No other hierarchy levels are created. If a module name collides with an existing Epic summary in the project, push warns and skips creation — it does not overwrite existing Epics.

### BR-JIRA-002 — Pull is status-only

Pull reads Jira issue status for each key in `manifest.jira.ticket_map` and updates two things: the Status column in the task summary table of the corresponding `tasks.md`, and the `manifest.traceability` entry for that task. Pull never touches task descriptions, ACs, decision budgets, or assigned names in `tasks.md`. Content is Daksh-owned; Jira owns execution status.

### BR-JIRA-003 — Push is idempotent

If `manifest.jira.ticket_map` already contains an entry for a given TASK ID, push skips that task. A PTL who re-runs push after a partial failure picks up from where it left off. To force recreation of existing tickets, pass `--force` — this updates ticket content but does not create duplicates (it uses the stored key to update, not create).

### BR-JIRA-004 — Auth via environment variables only

The script reads `JIRA_SERVER`, `JIRA_EMAIL`, and `JIRA_TOKEN` from the environment. If any are missing, the script exits 1 immediately with a message naming which variable is absent. No credentials are read from files, manifest, or any other source. No token ever appears in output or manifest.

### BR-JIRA-006 — Time blocks are per-task, multi-block, write-to-both

A time block starts when an engineer begins an impl session (`/daksh impl MODULE TASK-ID`) and stops when they explicitly pause (`/daksh impl MODULE time-block stop TASK-ID`). One task can accumulate multiple blocks across multiple sessions. Each completed block (start + end) is logged immediately to Jira as a work log entry (`add_worklog`) and persisted in `manifest.traceability[TASK-ID].time_blocks`. A `jira_worklog_id` is stored per block to prevent duplicate submissions on re-run. An open block (start recorded, no end yet) is never submitted to Jira — only closed blocks are logged. If an engineer starts a new impl session while a block is already open, the open block is closed first with the current timestamp and logged before the new one opens.

### BR-JIRA-005 — Name resolution requires user confirmation

When an engineer runs `/daksh list-my-tasks --name "Alice"`, Daksh checks `manifest.jira.user_map` for a confirmed mapping. If none exists, the Daksh session proposes the closest matching name from the `Assigned to` fields in `tasks.md` and asks the engineer to confirm. Only on confirmation is the mapping written to `manifest.jira.user_map` for reuse. The script `list-tasks.py` itself does exact-string filtering only — the LLM-assisted resolution happens at the session level.

---

## Acceptance Criteria

| ID | Scenario | Expected |
|----|---------|---------|
| AC-JIRA-001 | `/daksh jira push` on a project with 2 modules and 3 tasks each | 2 Epics + 1 Sprint + 6 Stories created in Jira; all 6 TASK IDs present in `manifest.jira.ticket_map` |
| AC-JIRA-002 | Re-run push after AC-JIRA-001 (no --force) | No new tickets created; output: "N tasks already in ticket_map — skipped" |
| AC-JIRA-003 | `/daksh jira pull` after 2 stories marked Done in Jira | Status column in `tasks.md` updated to "Done" for those 2 tasks; `manifest.traceability` updated |
| AC-JIRA-004 | Pull runs on a task whose description was manually edited in Jira | Description in `tasks.md` unchanged; only status updated |
| AC-JIRA-005 | `JIRA_TOKEN` not set in environment | Exit 1: `"ERROR: JIRA_TOKEN not set. Export it before running jira-sync."` |
| AC-JIRA-006 | `/daksh list-my-tasks --name "Alice"` with Alice in `user_map` | Filtered table showing only Alice's tasks; no tasks from other assignees |
| AC-JIRA-007 | `/daksh jira status` with no prior push | Output: "No tickets in ticket_map. Run /daksh jira push first." |
| AC-JIRA-008 | Push with missing `manifest.jira.project_key` | Exit 1: `"ERROR: manifest.jira.project_key not set. Edit manifest.json before push."` |
| AC-JIRA-009 | Engineer starts impl session for TASK-PREFLIGHT-001 | `manifest.traceability["TASK-PREFLIGHT-001"].time_blocks` gains `{"start": "<ISO timestamp>", "end": null}` |
| AC-JIRA-010 | Engineer runs time-block stop for TASK-PREFLIGHT-001 | Open block `end` is filled; Jira work log entry created; `jira_worklog_id` stored in block |
| AC-JIRA-011 | Engineer starts a second impl session while a block is already open | Open block auto-closed with current timestamp before new block opens; Jira work log created for closed block |
| AC-JIRA-012 | Task not in `ticket_map` when time-block stop runs | Warn: "TASK-ID not in ticket_map — time block saved locally but not logged to Jira. Run /daksh jira push first." Exit 0. |

---

## Data Contract

The JIRA module reads from:
- `docs/.daksh/manifest.json` — modules, stage statuses, `manifest.jira` (project_key, board_id, ticket_map, user_map)
- `docs/implementation/*/tasks.md` — TASK IDs, summaries, epics, sprints, `Assigned to` fields
- Jira REST API — issue status for pull

The JIRA module writes to:
- `manifest.jira.ticket_map` — populated on push
- `manifest.jira.user_map` — populated on name confirmation
- `manifest.jira.synced_at` — updated on push and pull
- `manifest.traceability` — task status keyed by TASK ID, updated on pull
- `tasks.md` summary table, Status column — updated on pull (status only)

No cross-module contract with PREFLIGHT — they share no outputs.

---

## Open Questions

1. **project_key and board_id setup** — How does the PTL configure `manifest.jira.project_key` and `manifest.jira.board_id`? Options: (a) manual manifest edit before push, (b) a `jira-sync.py configure` subcommand that asks interactively. TRD should decide — leaning toward manual edit since this is a one-time setup for a small project.
2. **Done status mapping** — Which Jira status values count as "done" for pull? Default candidates: `["Done", "Closed", "Resolved"]`. Should this be hardcoded or configurable in `manifest.jira.done_statuses`? TRD should decide.

---

## Approval

Approved by: Yeshwanth
Role:        PTL
Date:        2026-03-28
Hash:        947e9297b2a6…
