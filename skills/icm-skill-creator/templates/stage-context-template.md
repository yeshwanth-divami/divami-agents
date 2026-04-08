---
name: stage-context-template
description: Base template for a stage-level CONTEXT.md in an ICM skill. Use when a stage needs scoped context beyond what SKILL.md routing provides.
type: template
---

# Template: Stage CONTEXT.md

Replace all `{{placeholders}}`. Used only when a stage's context is too specific to live in a shared reference file.

---

```markdown
# Stage {{stage_number}} — {{stage_name}}

> One sentence: what transformation this stage performs.

---

## Inputs

| Type | Path | Purpose |
|---|---|---|
| Layer 3 | `references/{{reference_file}}.md` | {{what constraint or knowledge it provides}} |
| Layer 4 | `{{path/to/working/artifact}}` | {{what content it contains}} |

*Load only what is listed here. Do not load other files.*

---

## Process

{{One paragraph describing the single transformation.
State what changes. State what must NOT change.
Use active verbs: extract, classify, generate, validate, transform.}}

### Constraints
- {{Hard rule — what the agent must never do}}
- {{Hard rule — format or structural requirement}}
- {{Hard rule — what stays unchanged}}

---

## Outputs

| File | Format | Content |
|---|---|---|
| `{{output/path/artifact.md}}` | {{Markdown / JSON / plain text}} | {{what it contains}} |

Outputs are written to `{{stage_folder}}/output/`. Do not write outside this folder.

---

## Human Review Gate

**Verify before proceeding:**
- {{Specific thing to check — not "looks good" but "X field is populated", "Y section has at least N items"}}
- {{What a broken output looks like}}

**If wrong:** {{What to edit and where. Which file to change.}}
```
