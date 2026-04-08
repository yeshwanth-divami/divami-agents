# Stage 2 — Narrative

> Shape excavated facts into a story arc: Situation, Approach, Outcome.

---

## Inputs

| Type | Path | Purpose |
|---|---|---|
| Layer 3 | `references/narrative-guide.md` | Story arc, tone rules, audience adaptation |
| Layer 3 | `references/doc-narrator-rules.md` | Writing patterns |
| Layer 4 | `templates/narrative.md` | Output structure |
| Layer 4 | `docs/use-case/excavation.md` | Raw facts from Stage 1 |

*Load only what is listed here. Do not load excavation-guide or final template.*

---

## Process

Consume the reviewed excavation file. Shape raw facts into the three-act use case arc (Situation, Approach, Outcome) following the narrative guide. Write prose, not bullets. Adapt tone for a mixed audience: technical enough for a CTO, clear enough for procurement. Build a Key Decisions table from the most pivotal choices found in the excavation.

### Constraints
- Do not add facts not present in the excavation file. If the story needs more, flag it as an open question.
- Situation section must use the client's language for their pain (from excavation quotes/problem).
- Every metric stated must come from the excavation file's outcomes section.
- Each section must end by creating the question the next section answers.
- Do not start sections with "In this section we will..." — just start.
- Cut hollow adjectives. Replace with specific claims.

---

## Outputs

| File | Format | Content |
|---|---|---|
| `docs/use-case/narrative.md` | Markdown | Story draft with Situation, Approach, Outcome, Key Decisions |

**Resumption artifact:** `docs/use-case/narrative.md` — written before yielding control.

---

## Human Review Gate

**Verify before proceeding to polish:**
- Story arc flows: Situation creates the "how?" question, Approach creates the "did it work?" question, Outcome answers it
- No facts appear that weren't in the excavation (nothing invented)
- Tone works for mixed audience — a CTO nods, a PM doesn't squint
- Key Decisions table has 3-5 real decisions with genuine alternatives
- Open questions from excavation are either resolved or carried forward

**If wrong:** Edit `docs/use-case/narrative.md` directly. Restructure sections, adjust tone, add missing context. Set `status: needs-review` if edits need agent re-examination.
