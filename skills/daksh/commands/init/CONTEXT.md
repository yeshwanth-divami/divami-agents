---
description: "Initialize Daksh pipeline — creates manifest, determines weight class,
scaffolds project directories, registers team roster."
---

# Command: /daksh init

> Every project begins with a shape. Init determines that shape
> before the first document is written.

## Persona: Delivery Strategist

You are setting up a new Daksh pipeline for a services engagement.
Your job is to determine the project's weight class, register the
team, and scaffold the directory tree so that every subsequent stage
has a home for its output.

## Inputs (read before asking anything)

1. Check if `docs/.daksh/manifest.json` already exists.
   - If it exists and any stage has `status != "not_started"`, warn:
     "A Daksh pipeline already exists with work in progress.
     Re-initializing will reset all stage status. Proceed? (y/n)"
   - If it exists and all stages are `not_started`, proceed silently.
2. Read `docs/conversations/client/` if it exists — extract project
   name, client name, timeline, team size from available context.
   Skip questions already answered by these documents.

## Questions (ask all applicable at once, skip if answered in inputs)

1. What is the project name and client name?
2. What is the estimated timeline? (< 4 weeks / 4-12 weeks / > 12 weeks)
3. How many modules or major feature areas do you expect? (< 3 / 3-8 / > 8)
   If modules are already known, list them (short names, e.g. AUTH, NOTIFY).
4. Who is the PTL? Name and email.
5. Who are the TLs? Names and emails.
6. Are there client-side approvers? Names and emails.

Do not ask more than 6 questions. Extract and confirm rather than
re-asking what's already in the client documents.

## Weight class determination

| Condition | Class |
|-----------|-------|
| < 4 weeks AND < 3 modules | small |
| 4-12 weeks AND 3-8 modules | medium |
| > 12 weeks OR > 8 modules | large |
| Ambiguous (e.g., 3 weeks but 5 modules) | Ask: "This could go either way. Small or medium?" |

The user can override: "treat this as large" always wins.

## Output

## Jira configuration

Ask only when `rules.jira_sync` is `"recommended"` or `"required"` (medium/large projects).
Add these as questions 7 and 8 (ask at the same time as questions 1–6 above):

7. Jira project key (e.g. `ACME`) and board ID?
8. Workflow: use `divami-engineering-jira-standard` (default) or define custom statuses?

**If divami-engineering-jira-standard** (default when not answered): set `workflow_preset:
"divami-engineering-jira-standard"` in the manifest. Copy the file
`templates/jira-workflow-divami-engineering-jira-standard.json` verbatim to
`docs/.daksh/jira-workflow.json`. The manifest's `done_statuses` must equal the union of
all per-workflow `done_statuses` in that file: `["Done", "Done - Not Reproducible", "Done - Not A Bug"]`.

**If custom**: set `workflow_preset: "custom"`, then ask:
- Statuses for stories/tasks/sub-tasks, and which count as done?
- Statuses for bugs, and which count as done?
- Do not ask for transition maps — they can add those by editing the manifest later.

If `jira_sync` is `"optional"` (small), leave `jira` fields at template defaults and skip questions 7–8.

---

### 1. Create `docs/.daksh/manifest.json`

Read the template at `templates/manifest-template.json` and the schema
at `references/manifest-schema.md`. Populate:

- **Project metadata** from answers.
- **`weight_class`** and **`weight_rationale`** from determination.
- **`rules`** computed from weight class:

  | Rule | small | medium | large |
  |------|-------|--------|-------|
  | `stages_combined` | `["00+10", "40a+40b"]` | `[]` | `[]` |
  | `approvals_per_gate` | `1` | `2` | `2` |
  | `open_questions` | `"optional"` | `"mandatory"` | `"mandatory"` |
  | `cross_module_contracts` | `false` | `true` | `true` |
  | `jira_sync` | `"optional"` | `"recommended"` | `"required"` |
  | `tend_frequency` | `"end_of_project"` | `"per_milestone"` | `"per_sprint"` |

- **`team_roster`** from answers.
- **`modules`** if known (otherwise empty — stage 30 populates this).
- **`stages`** skeleton based on weight class:

  **Medium/Large stage keys:**
  `00`, `10`, `20`, `30` — always present.
  Per module (if modules known): `40a:[MODULE]`, `40b:[MODULE]`,
  `40c:[MODULE]`, `50:[MODULE]`. Add project stage `60`.
  If modules not yet known: `00` through `30`, plus `60`.

  **Small stage keys:**
  `00+10` (combined), `20`, `30`.
  Per module: `40a+40b:[MODULE]`, `40c:[MODULE]`, `50:[MODULE]`.
  Add project stage `60`.

  Each stage entry starts as:
  ```json
  {
    "status": "not_started",
    "output": "<path from stage CONTEXT.md>",
    "locked_by": null,
    "doc_hash": null,
    "approvals": [],
    "revision_history": []
  }
  ```

  **Canonical output paths per stage key (use these exactly — do not derive):**

  | Stage key | `output` value |
  |---|---|
  | `00`, `00+10` | `docs/client-context.md` |
  | `10` | `docs/vision.md` |
  | `20` | `docs/business-requirements.md` |
  | `30` | `docs/implementation-roadmap.md` |
  | `40a:[M]`, `40a+40b:[M]` | `["docs/implementation/[M]/prd.md", "docs/implementation/[M]/trd.md"]` |
  | `40b:[M]` | `docs/implementation/[M]/trd.md` |
  | `40c:[M]` | `docs/implementation/[M]/tasks.md` |
  | `50:[M]` | `docs/implementation/[M]/tasks.md` |
  | `60` | `["handbook/end-user.md", "handbook/admin.md", "handbook/ops.md", "handbook/developer.md"]` |

  The `50:[M]` output is `tasks.md` — the same document as `40c:[M]`. The
  difference is what the approval certifies: `40c` approves the plan;
  `50` certifies all tasks in the plan are done (enforced by `approve.py`).
  **Never scaffold `50:[M]` with `change-records/` as the output.**

- **`contracts`**, **`traceability`** — empty objects.
- **`required_skills`** — `["doc-narrator", "vyasa"]`.
- **`jira`** — `project_key` and `board_id` from answers (null if skipped).
  `workflow_preset` and `workflows` populated per "Jira configuration" section above.
  `done_statuses` set to union of all per-workflow `done_statuses`.
- **`created`** — today's date.
- **`daksh_version`** — read from skill's `.version` file.

### 2. Scaffold directories

Create these directories if they don't exist:

```
docs/
├── .daksh/                  (manifest home)
├── conversations/
│   └── client/              (client input docs)
└── implementation/          (module output home)
handbook/                    (audience manuals, patched during stage 50)
```

If modules are known, also create:
```
docs/implementation/[MODULE]/              (per module)
docs/implementation/[MODULE]/change-records/
```

Also create these handbook stubs if they don't exist:

```
handbook/end-user.md
handbook/admin.md
handbook/ops.md
handbook/developer.md
```

These are not placeholders for later cleanup. They establish the narrative
shape that stage 50 and stage 60 will patch. Write them in `doc-narrator`
style: assume a junior reader is opening the file cold, give them one short
orientation paragraph before any structured section, and avoid leaving a file
as a bare stack of headings.

Each stub should contain these sections in order, with a one- to two-sentence
 seed paragraph under `# [Audience]` that explains what this manual is for,
 when to use it, and what it will eventually cover for that audience:

```md
# [Audience]

[Orientation paragraph for this audience.]

## Overview
## Prerequisites
## Core procedures
## Reference
## Troubleshooting
## Changelog
```

Under each section heading, add a single sentence that states the contract for
that section. Example: `## Core procedures` should say that the section will
hold the numbered workflows this audience performs most often. Do not add
`TODO`, `TBD`, or implementation fiction.

### 3. Scaffold `docs/.vyasa`

Create `docs/.vyasa` to control Vyasa sidebar ordering. Write the
following content — do not skip even if the files don't exist yet,
Vyasa ignores missing entries:

```toml
# Daksh pipeline document order — maintained by /daksh init and each stage.
# Add new entries here as stages complete. Vyasa displays docs in this order.
# glossary.md must always be last — do not insert entries after it.
order = [
  "client-context.md",
  "vision.md",
  "business-requirements.md",
  "implementation-roadmap.md",
  "implementation",
  "glossary.md",
]
folders_first = false
```

Also scaffold `docs/glossary.md` as an empty file with just the heading
`# Glossary` if it doesn't already exist.

If `docs/.vyasa` already exists, do not overwrite — append any missing
entries to the `order` array instead. `glossary.md` must always be the
last entry. If it exists but is not last, move it to the end.

### 4. Confirm to user

Display a summary — no more, no less:

```
Daksh pipeline initialized.
  Project:      [name]
  Client:       [client]
  Weight class: [class] ([rationale])
  Team:         [names and roles]
  Stages:       [stage sequence based on weight class]
  Approvals:    [N] per gate
  Modules:      [list or "TBD — stage 30 will register them"]
  Next step:    /daksh [first stage name]
```

## Rules

- Do not generate any project documents. Init creates structure, not
  content. No vision docs, no BRDs, no roadmaps.
- Write the manifest directly to disk. Do not draft it in chat first.
- If modules are known, register them now. If not, that's fine — stage
  30 will register them and init will not block on this.
- Weight class can always be changed later by editing the manifest
  directly. Init is not a one-way door.

## Feeds into

Every subsequent `/daksh` invocation reads `docs/.daksh/manifest.json`
as its first action. If the manifest doesn't exist, the system tells
the user to run `/daksh init`.
