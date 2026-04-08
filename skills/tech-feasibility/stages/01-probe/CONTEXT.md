# Stage 1 — Probe

> Read the idea, generate a batch of clarifying questions, assess answers, repeat until stop conditions are met.

---

## Inputs

| Type | Path | Purpose |
|---|---|---|
| Layer 3 | `references/probing-guide.md` | Five dimensions, batching rules, stop conditions |
| Layer 4 | User's idea text (from conversation) | The raw idea being assessed |

*Load only what is listed here. Do not load doc-structure.md or doc-narrator-rules.md at this stage.*

---

## Process

Read the user's idea and the probing guide. Identify which of the five dimensions (modality, output consumer, integration surface, regulatory constraints, scope boundary) are already answered by the idea text, which are partially answered, and which are unknown.

Generate a batch of questions covering the unresolved dimensions. Deliver all questions in a single message — never one question at a time. Number them so the user can answer selectively.

After the user responds: re-assess dimension coverage. If any dimensions remain unresolved and have not been explicitly waived, generate a second targeted batch covering only those dimensions. Make follow-up questions more specific than the first batch — use information from the previous answers to narrow the question.

Repeat until stop conditions in the probing guide are met.

### Constraints

- Never ask one question at a time. All questions for a round go in one message.
- Never re-ask a dimension that was explicitly waived by the user ("not relevant", "TBD", "doesn't matter").
- Never probe implementation details the user has not raised (database choice, team size, timeline, budget).
- Do not speculate or volunteer architecture opinions during probing — this stage collects, it does not analyse.
- Do not generate an outline or write the doc from this stage. Stop conditions must be met first.

---

## Outputs

No files are written in this stage. The output is the conversation — a sufficient set of answers covering the five dimensions.

When stop conditions are met, signal transition: "I have enough to write the outline. Moving to Phase 2."

---

## Human Review Gate

**Verify before proceeding to Phase 2:**
- All five dimensions are either answered or explicitly waived
- No dimension was answered with a contradiction (if so, ask one clarifying question)

**If wrong:** Ask one targeted follow-up. Do not restart the batch from scratch.
