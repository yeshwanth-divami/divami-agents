---
name: narrative-template
description: Template for the narrative stage output — story draft shaped from excavated facts.
type: template
---

# Template: narrative.md

```markdown
---
skill: use-cases
stage: narrative
status: complete
---

{{context_seed}}

## What This Stage Produced

{{prose_narrative — how the raw facts were shaped into a story, what editorial decisions were made, what was cut and why. 1-2 paragraphs.}}

## Situation

{{situation — the world before the engagement. Client's pain in their language. Industry context. What was at stake. End by creating the question "How did they fix this?"}}

## Approach

{{approach — narrative of decisions, not a feature list. Why this stack, why this methodology, what tradeoffs, what was explicitly not done. End by creating the question "Did it work?"}}

## Outcome

{{outcome — metrics first, qualitative second. Before/after. Business language. Client quotes if available.}}

## Key Decisions

| Decision | Alternative Considered | Why This Choice |
|---|---|---|
| {{decision_1}} | {{alternative_1}} | {{rationale_1}} |
| {{decision_2}} | {{alternative_2}} | {{rationale_2}} |
| {{decision_3}} | {{alternative_3}} | {{rationale_3}} |

## Open Questions

{{open_questions — unresolved items from excavation, plus any new ones from narrative shaping. Write "None." if empty.}}
```
