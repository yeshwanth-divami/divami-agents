---
name: workspace-anatomy
description: Naming conventions, folder structure, and file organization rules for ICM-compliant skill workspaces.
type: reference
---

# Workspace Anatomy

## Canonical Folder Structure

```
skill-name/                     ← skill directory (static, never per-run)
├── SKILL.md                    ← Layer 0: identity + routing table
├── references/                 ← Layer 3: stable knowledge, never per-run
│   ├── <domain-a>.md
│   └── <domain-b>.md
├── templates/                  ← Layer 4: per-run working artifacts with {{placeholders}}
│   ├── <artifact-a>.md
│   └── <artifact-b>.md
└── stages/                     ← optional: only for complex multi-stage skills
    ├── 01-<name>/
    │   └── CONTEXT.md
    └── 02-<name>/
        └── CONTEXT.md

<project-root>/                 ← user's project (per-run artifacts live here)
├── <stage-a>/                  ← semantic stage folder, defined by the skill
│   └── <codename>.md           ← intermediate file: edit surface + resumption artifact
├── <stage-b>/
│   └── <codename>.md
└── completed/                  ← finished work items, moved here by the skill on completion
    └── <codename>.md
```

`stages/` in the skill directory is optional. Use it only when a stage needs scoped context that doesn't belong in `references/`.

Stage folder names in the project are **semantic and skill-defined** — not generic numbered directories. They are declared in the skill's SKILL.md and are part of the skill's identity (e.g. `inception/`, `draft/`, `screenplay/` for a movie script skill). Every multi-stage skill must define them explicitly during Phase 2.

---

## Naming Rules

| Element | Convention | Example |
|---|---|---|
| Skill root folder | kebab-case | `pdf-summarizer` |
| Reference files | kebab-case, topic noun | `voice-guide.md`, `output-format.md` |
| Template files | kebab-case, describes artifact | `summary-output.md`, `stage-report.md` |
| Stage folders (in skill) | `NN-verb-noun` (numbered) | `01-extract`, `02-classify`, `03-write` |
| Stage folders (in project) | semantic noun, skill-defined | `inception/`, `draft/`, `completed/` |
| Codenames | kebab-case noun phrase, 2–4 words | `space-magic-fantasy`, `haunted-heist` |
| Placeholders in templates | `{{snake_case}}` | `{{project_name}}`, `{{target_audience}}` |

Stage folder names in the project are semantic — they reflect the skill's domain, not a generic pipeline numbering. The skill declares them; the user learns them.

---

## SKILL.md Routing Table (required)

Every SKILL.md must have a routing table. For multi-stage skills with codename-based commands, the table maps user commands to actions:

```markdown
## Stage Folders

| Stage | Folder | Meaning |
|---|---|---|
| 1 | `inception/` | Concept and premise established |
| 2 | `draft/` | First draft written |
| 3 | `screenplay/` | Full screenplay formatted |
| — | `completed/` | Work item finished and archived |

## Routing

| Command | Action |
|---|---|
| `create <description>` | Generate codename. Write `inception/<codename>.md`. Tell user the codename. |
| `draft <codename>` | Find `<codename>.md` in any stage folder. Read `stage` + `status`. If `needs-review`, surface open questions and stop. If `complete`, advance to next stage. |
| `list` | Scan all stage folders. Show each codename, its current stage, and status. |
| `complete <codename>` | Move `<codename>.md` to `completed/`. Confirm to user. |
```

The routing table is the machine-readable version of "mode detection." Commands are the skill's public API — design them to feel natural for the domain.

---

## Layer 3 Reference Files

Rules:
- Timeless. No run-specific data, no `{{placeholders}}`.
- One domain per file. If it covers two topics, split it.
- Must be readable standalone — assume no other file is loaded alongside it.
- Target: 300–1500 tokens each.

Bad: `all-conventions.md` (too broad)
Good: `tone-guide.md`, `output-schema.md`, `error-taxonomy.md`

---

## Layer 4 Template Files

Rules:
- Every variable piece of data is a `{{placeholder}}`.
- The structure is fixed; only placeholder values change per run.
- File name describes the artifact, not the stage that produces it.
- Target: 100–800 tokens each.

Bad: `stage1-output.md` (names the stage, not the artifact)
Good: `research-brief.md`, `spec-draft.md`

---

## What Does NOT Belong in a Skill Directory

- Completed run outputs — those go in the user's project, not the skill
- Git history artifacts
- Binaries, images, or anything not plain text
- Per-user configuration — that belongs in `CLAUDE.md` at the project root
