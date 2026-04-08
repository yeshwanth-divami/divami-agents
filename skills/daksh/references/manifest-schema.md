# Daksh Manifest Schema

> The manifest is the machine-readable spine of the pipeline.
> Every `/daksh` invocation reads it. Most write to it.
> If the manifest doesn't know about it, it didn't happen.

The manifest lives at `docs/.daksh/manifest.json` in the project root
(not in the skill directory). It is created by `/daksh init` and
updated by every stage and command thereafter.

---

## Top-level fields

| Field | Type | Set by | Description |
|-------|------|--------|-------------|
| `project` | string | init | Project short name (kebab-case) |
| `description` | string | init | One-line project description |
| `client` | string | init | Client organization name |
| `created` | ISO date | init | Pipeline creation date |
| `daksh_version` | string | init | Daksh skill version at init time |
| `weight_class` | enum | init | `"small"` \| `"medium"` \| `"large"` |
| `weight_rationale` | string | init | Why this weight class was chosen |
| `rules` | object | init (computed) | Derived rules — see below |
| `team_roster` | array | init | Team members — see below |
| `modules` | array | stage 30 | Module short names, e.g. `["AUTH", "NOTIFY"]` |
| `stages` | object | init + stages | Stage status map — see below |
| `contracts` | object | stage 30+ | Cross-module contracts — see below |
| `traceability` | object | stages 20, 40a, 40c | ID lineage map — see below |
| `change_records` | object | `/daksh change` | Change record index — see below |
| `required_skills` | array | init | Skills that must be present, e.g. `["doc-narrator", "vyasa"]` |
| `jira` | object | `/daksh jira` | Jira sync state — see below |

---

## `rules` (computed from `weight_class`)

These are derived, not user-editable. Init computes them; stages read them.

| Field | small | medium | large |
|-------|-------|--------|-------|
| `stages_combined` | `["00+10", "40a+40b"]` | `[]` | `[]` |
| `approvals_per_gate` | `1` | `2` | `2` |
| `open_questions` | `"optional"` | `"mandatory"` | `"mandatory"` |
| `cross_module_contracts` | `false` | `true` | `true` |
| `jira_sync` | `"optional"` | `"recommended"` | `"required"` |
| `tend_frequency` | `"end_of_project"` | `"per_milestone"` | `"per_sprint"` |

---

## `team_roster` entries

```jsonc
{
  "name": "Ravi Kumar",
  "role": "PTL",          // PTL | TL | Engineer | Client | Stakeholder
  "email": "ravi@divami.com"
}
```

Only roster members can approve gates. The `role` field determines
which stages they can approve (e.g., Client can approve 00, 10, 40a;
PTL/TL can approve all stages).

---

## `stages` entries

Each key is a stage identifier: `"00"`, `"10"`, `"20"`, `"30"`,
`"40a:AUTH"`, `"40b:AUTH"`, `"40c:AUTH"`, `"50:AUTH"`.

For combined stages (small weight class): `"00+10"`, `"40a+40b:AUTH"`.

```jsonc
{
  "status": "not_started",   // not_started | in_progress | pending_approval | approved | revision_needed
  "output": "docs/client-context.md",
  "locked_by": null,          // Name of person running this stage, or null
  "doc_hash": null,           // SHA-256 of output file, set when stage completes
  "approvals": [],            // Array of approval objects (see below)
  "revision_history": []      // Array of revision objects (see below)
}
```

### Stage 50 (impl) output and approval contract

The `output` for `50:[MODULE]` must point to `docs/implementation/[MODULE]/tasks.md`
(the tasks document, not the `change-records/` directory). This is the binding
contract that defines what "done" looks like for the module sprint.

`approve.py` enforces a **completion precondition** before writing the approval
block: every `TASK-[MODULE]-NNN` entry in `manifest.traceability` must have
`status: done`. If any task is incomplete, the script exits 1 and lists the
blockers. This makes the approval semantically honest — you cannot stamp
`tasks.md` as implementation-complete unless the traceability map confirms it.

The `40c:[MODULE]` approval (from `/daksh tasks`) and the `50:[MODULE]` approval
are both over `tasks.md` but certify different things:
- `40c` approval = "I sign off on this task list as the implementation plan."
- `50` approval = "All tasks in this list are done and their traceability is verified."

The distinction is enforced by the precondition, not by document structure.

Stage `50:[MODULE]` `approved` status is the natural gate for stage 60 (handbook). Any
stage that preflight-checks `60:[MODULE]` will look for an approved `50:[MODULE]` prior
stage. Init must scaffold `50:[MODULE]` with `output` pointing at `tasks.md`, not at
the `change-records/` directory.

### Approval object

```jsonc
{
  "by": "Ravi Kumar",
  "role": "PTL",
  "date": "2026-03-15",
  "doc_hash": "a3f9c2..."    // SHA-256 at time of approval
}
```

The `doc_hash` ties the approval to a specific version. If the output
file changes after approval (hash mismatch), the approval is stale and
the gate should warn.

### Revision object

For lightweight upstream corrections (critic issue #3):

```jsonc
{
  "date": "2026-03-20",
  "reason": "TRD revealed vision scope was too broad",
  "triggered_by": "40b:AUTH",
  "prior_hash": "a3f9c2...",
  "new_hash": "b7d1e4...",
  "approved_by": "Ravi Kumar"
}
```

---

## `contracts` entries

Each key is a directional pair: `"AUTH->NOTIFY"`.

```jsonc
{
  "shape": "UserEvent",       // Name of the data shape or API surface
  "description": "Auth emits UserEvent on login/logout; Notify consumes for real-time alerts",
  "owner": "AUTH",            // Producing module
  "consumer": "NOTIFY",       // Consuming module
  "version": 1,               // Bumped when shape changes
  "defined_in": "30",         // Stage that defined this contract
  "last_updated_by": "40b:AUTH"  // Stage that last modified it
}
```

---

## `traceability` entries

Each key is an artifact ID: `"UC-001"`, `"FR-001"`, `"US-AUTH-001"`,
`"TASK-AUTH-001"`.

```jsonc
{
  "parent": "UC-001",         // null for top-level UCs
  "children": ["FR-001", "FR-002"],
  "stage": "20",              // Stage that created this entry
  "module": null               // null for stage 20 IDs, "AUTH" for module-scoped IDs
}
```

---

## `change_records` entries

Each key is a CR identifier: `"CR-001"`, `"CR-002"`, etc.

```jsonc
{
  "CR-001": {
    "module": "PREFLIGHT",
    "path": "docs/implementation/PREFLIGHT/change-records/CR-001.md",
    "status": "OPEN",              // OPEN | RESOLVED
    "raised_by": "Yeshwanth",
    "date": "2026-03-29",
    "tier": "trd",                 // Highest doc touched: tasks | trd | prd | brd | roadmap
    "touched_docs": [              // Every doc the CR modified
      "docs/implementation/PREFLIGHT/trd.md",
      "docs/implementation/PREFLIGHT/prd.md"
    ],
    "change_task": "TASK-PREFLIGHT-005",  // The new task created by /daksh change
    "change_summary": "...",       // One-line description from the CR title
    "approvals": []                // Array of {by, role, date} — accumulated by approve.py
  }
}
```

### Tier field

The `tier` records which is the highest-upstream document the CR touched.
`approve.py` uses it to determine required approval authority:

| `tier` value | Required approver |
|---|---|
| `tasks` | TL |
| `trd` | TL or PTL |
| `prd` | PTL |
| `brd` or `roadmap` | PTL + Client |

### Tier inference (fail-safe)

If a CR in the manifest has no `tier` field, `approve.py` infers it from
`touched_docs` basenames, choosing the **highest** (safest) tier:

| Basename | Tier |
|---|---|
| `tasks.md` | `tasks` |
| `trd.md` | `trd` |
| `prd.md` | `prd` |
| `brd.md` | `brd` |
| `roadmap.md` | `roadmap` |

If inference fails (no recognized basenames), `approve.py` **blocks** — it
will not silently default to the lightest tier.

### Approval accumulation

CR approval is incremental. Each call to `approve.py CR-NNN --approver <name>`
records one approval. The CR resolves only when:

1. Every required role slot is filled (see Tier field above — `brd`/`roadmap`
   need both PTL and Client).
2. Total approval count meets `rules.approvals_per_gate`.

Until both conditions are met, the CR stays `OPEN` and touched stages remain
`pending_approval`.

### Count-filling approvals

When all authority slots are satisfied but the approval count is still below
`approvals_per_gate`, additional approvals are accepted **only from roles
with authority for that tier** (i.e. the same roles listed in `CR_TIER_ROLES`).
This preserves the authority model — a TL cannot count-fill a `prd`-tier CR
because TL has no `prd` authority.

If the roster cannot supply enough distinct approvers with the required
authority, the script surfaces this as a governance constraint rather than
silently weakening the gate.

### Status values

- `OPEN` — change set written, docs marked `pending_approval`, accumulating approvals
- `RESOLVED` — all required approvals collected. Touched docs returned to `approved` status.

---

## `jira` object

```jsonc
{
  "project_key": "ACME",          // Jira project key, or null if not synced
  "board_id": null,                // Jira board ID, or null
  "synced_at": null,               // ISO datetime of last sync, or null
  "ticket_map": {},                // "TASK-AUTH-001" -> "ACME-142" mapping
  "user_map": {},                  // "Name" -> "jira-account-id" mapping
  "workflow_preset": "divami-engineering-jira-standard",  // or "custom"
  "done_statuses": ["Done", "Done - Not Reproducible", "Done - Not A Bug"],
                                   // Union of all workflow done_statuses — used by jira-sync pull
  "workflows": {
    "story": {
      "applies_to": ["Story", "Task", "Sub-task", "Spike"],
      "statuses": [...],           // Ordered list of valid status names
      "done_statuses": ["Done"],   // Which statuses count as done for this type
      "transitions": {             // status -> [allowed next statuses]
        "Open": ["To Do"],
        ...
      }
    },
    "bug": {
      "applies_to": ["Bug"],
      "statuses": [...],
      "done_statuses": ["Done", "Done - Not Reproducible", "Done - Not A Bug"],
      "transitions": { ... }
    }
  }
}
```

### `workflow_preset` values

| Value | Meaning |
|-------|---------|
| `"divami-engineering-jira-standard"` | Two-graph standard: story/task/sub-task/spike graph + bug graph. Populated by `/daksh init`. |
| `"custom"` | User-defined statuses. Transitions optional. |
| `null` | Jira not configured. `jira-sync pull` falls back to `done_statuses`. |

### Workflow resolution in `jira-sync`

`jira-sync pull` uses `jira.done_statuses` (the flat union field) for backward-compatible status detection.
`jira-sync transition` uses `jira.workflows[type].transitions` to validate that a transition is legal before calling the Jira API.

The top-level `done_statuses` must always equal the union of all per-workflow `done_statuses`. Re-computed automatically by `/daksh init` and whenever the manifest is edited via a daksh command.

---

## Hash computation

All `doc_hash` values are SHA-256 hex digests of the output file,
computed via:

```bash
shasum -a 256 <file> | cut -d' ' -f1
```

This makes hashes reproducible and verifiable outside the LLM.
