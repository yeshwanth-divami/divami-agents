---
name: intermediate-file-format
description: Format rules for ICM stage output files. These files are both edit surfaces (human can modify before next stage) and long-term artifacts resumable by codename. They follow doc-narrator conventions.
type: reference
---

# Intermediate File Format

Every stage in an ICM skill writes exactly one output file before yielding control. This file serves two purposes simultaneously:

1. **Edit surface** — a human can open it, read it, change it, and the next stage consumes the edited version
2. **Resumption artifact** — its frontmatter carries the current `stage`, so the skill can find it by codename and continue from wherever it left off

Because humans must be able to read and edit these files without context from any other document, they follow doc-narrator conventions.

---

## Required Structure

```markdown
---
skill: <skill-name>
codename: <codename>
stage: <stage-folder-name>
status: complete | needs-review
---

<context seed — 3–5 sentences. What skill is this? What codename is this?
What stage just ran? What did it produce? What will the next stage consume?>

## What This Stage Produced

<Prose narrative of the stage's output. Not a dump — a story. What was
the input? What transformation ran? What decisions were made or deferred?
Write for a reader who did not watch the stage execute.>

## Output

<Structured content — the actual artifact this stage produced.
Tables, lists, or structured text as appropriate to the skill.>

## Open Questions

<Any decisions deferred, ambiguities unresolved, or human choices needed
before the next stage should run. If none, write "None." — do not omit
the section. An empty section is a deliberate signal.>

1. **<Question>** — <options considered, why blocked, what unblocks it>
```

---

## Frontmatter Fields

| Field | Values | Purpose |
|---|---|---|
| `skill` | skill root folder name | Identifies which skill owns this file |
| `codename` | kebab-case noun phrase | The work item's identity across all stages |
| `stage` | semantic stage folder name (e.g. `inception`, `draft`) | Which stage produced this file; determines where it lives and what comes next |
| `status` | `complete` or `needs-review` | Human sets to `needs-review` when edits were made; skill checks this before proceeding |

---

## File Naming and Location

Each skill defines its own semantic stage folder names during design. Files live in those folders, named by codename:

```
<project-root>/
├── inception/
│   └── space-magic-fantasy.md     ← stage: inception, status: complete
├── draft/
│   └── space-magic-fantasy.md     ← stage: draft, status: needs-review
└── completed/
    └── galactic-heist.md          ← finished work items
```

The skill — not the user — decides what `inception/`, `draft/`, and `completed/` are called. These names are declared in the skill's SKILL.md and are part of the skill's identity.

A codename travels with the work item across stage folders. The file moves (or is copied) when the stage advances.

---

## Codename Generation

When a skill creates a new work item, it generates a codename from the user's input — a short, memorable, kebab-case noun phrase that the user can reference in future commands.

Rules:
- 2–4 words, kebab-case
- Derived from the input's essence, not a hash or timestamp
- Unique within the skill's project scope (check for collisions before writing)
- The skill tells the user the codename immediately after creating the file

Example: `/ms create star wars meets lord of the rings` → codename `space-magic-fantasy`, file written to `inception/space-magic-fantasy.md`.

---

## Resumption by Codename

When a skill receives a command referencing a codename (e.g. `/ms draft space-magic-fantasy`):

1. Search all stage folders for `<codename>.md`
2. Read its `stage` and `status` frontmatter
3. If `status: needs-review` — stop, surface the open questions, do not proceed
4. If `status: complete` — advance to the next stage and continue

No registry needed. The file's own frontmatter is the source of truth.

---

## Context Seed Rules (from doc-narrator)

The seed must answer:
1. What skill/pipeline is this? (one clause)
2. What codename is this work item? (one clause)
3. What stage just completed? (one sentence)
4. What did it produce, and what does the next stage expect? (one sentence)

**Bad seed:**
> Stage 2 output for the ms skill.

**Good seed:**
> The ms skill transforms a movie concept into a full screenplay through three stages.
> This is `space-magic-fantasy` — a story that blends Star Wars and Lord of the Rings.
> The `inception` stage just completed: it established genre, tone, protagonist arc, and
> central conflict. The `draft` stage will consume the Output block below to write Act 1.

---

## Prose Before Structure

The "What This Stage Produced" section must be prose — not a bullet list of what happened.

Bad:
```
- Generated concept
- Set tone to epic fantasy
- Defined protagonist
```

Good:
```
The inception stage mapped the collision between two genre traditions: Star Wars' mythic
hero journey set in a technological cosmos, and Lord of the Rings' grounded, tactile
secondary world. The central tension resolved as a story about a farm boy from a dying
star-system who must cross into a realm of ancient magic to retrieve an artifact that
neither world can destroy alone. Tone was set to epic and elegiac — heroic but costly.
```

---

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Output file is a raw JSON dump | Wrap in prose narrative; put structured data in the Output section |
| No context seed | Add one — a reader opening this file cold must understand it |
| Open Questions section omitted when there are none | Write "None." — the absence must be explicit |
| File written at end of pipeline only | Write after every stage, not just the last |
| Codename is a timestamp or hash | Generate a memorable noun phrase from the input |
| Status field not set | Always set — `complete` by default; human changes to `needs-review` |
