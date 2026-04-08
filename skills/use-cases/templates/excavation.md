---
name: excavation-template
description: Template for the excavation stage output — raw facts extracted from project artifacts.
type: template
---

# Template: excavation.md

```markdown
---
skill: use-cases
stage: excavation
status: complete
---

{{context_seed}}

## What This Stage Produced

{{prose_narrative — describe what artifacts were explored, what was found, what was surprising or notable, what gaps remain. 1-2 paragraphs.}}

## Client Problem

{{client_problem — their words for the pain, who was affected, business cost of the status quo}}

## Constraints

{{constraints — budget, timeline, regulatory, legacy systems, what the team could NOT do}}

## Approach Taken

{{approach — methodology, key decisions, tools/frameworks chosen and why, what was explicitly rejected}}

## Tech Stack

{{tech_stack — languages, frameworks, databases, infrastructure, notable libraries}}

## Outcomes / Metrics

{{outcomes — measurable results with sources. Flag any metric without a clear source.}}

## Notable Quotes

{{quotes — direct quotes from clients or stakeholders, with speaker role noted}}

## Open Questions

{{open_questions — gaps in the evidence, metrics needing verification, attribution needed. Write "None." if empty.}}
```
