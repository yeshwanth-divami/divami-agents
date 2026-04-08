---
name: doc-narrator-rules
description: Doc-narrator writing conventions distilled for use in the tech-feasibility skill. Context seed, prose-first, Why? tables, open questions, callout syntax, diagram rules.
type: reference
---

# Doc-Narrator Writing Rules

These are the structural conventions every feasibility document must follow. They are not style preferences — they are the rules that prevent readers from getting lost.

---

## Context Seed

Every document opens with a context seed: 3–5 sentences that make the document self-contained for a cold reader.

**Appears before any heading. Before any section. Before the title if there is one.**

The seed must answer:
1. What world does this document live in? (one sentence on the domain/problem space)
2. What is this specific document about?
3. What will the reader understand by the end?

**Bad:** "This document describes the feasibility of the Patient Information Collector."
**Good:** "A hospital consultation begins before the doctor enters the room. [continues to paint the scene, the system, and the reader's destination]"

**Test:** Cover the title. Show the seed to someone unfamiliar with the project. Can they read the document without confusion? If yes, the seed works.

---

## Prose Before Diagrams

Tell the story in prose before showing the diagram. The reader must know what they are about to see before they see it.

**Wrong:** Section heading → Mermaid diagram → explanation
**Right:** Section heading → prose walkthrough of the system → Mermaid diagram that confirms it

A diagram placed before its prose explanation is a puzzle, not a document.

---

## Open Questions Are First-Class

Unresolved decisions are documented explicitly in an `## Open Questions` section at the end of the document.

Each item:
- Numbered
- States the question clearly
- Names options under consideration (if known)
- States what unblocks it

Do not hide open questions in prose or comments. Do not omit them to make the doc look more complete.

---

## Why? Tables

For any table that enumerates outputs, fields, choices, or steps — follow with a Why? table that answers: **what breaks if this row is removed?**

If a row cannot answer that question, either the row is wrong or the table is incomplete.

**Format:**

| Output / Field / Choice | Why it cannot be dropped |
|---|---|
| `<item>` | What breaks without it — stated as a consequence, not a definition. |

Wrap long prose in table cells at ~8 words per visual line using literal `<br/>` to prevent horizontal scrolling.

---

## Callout Syntax

Use Obsidian-style callouts for important information that would interrupt the narrative:

```
> [!note]
> Content here.

> [!warning]
> Content here.

> [!tip]
> Content here.
```

Use `[!warning]` for safety-critical constraints (e.g., prompt injection risk, HIPAA requirements).
Use `[!note]` for important clarifications that sit outside the main flow.
Use `[!tip]` for debugging or operational guidance.

Do not use `///` callouts — they are not supported.

---

## Collapsibles for Deep Detail

Use `<details>` when technical depth is necessary but would interrupt the reading flow for most readers:

```markdown
<details>
<summary>Why option A over option B</summary>

Detail here...

</details>
```

Good candidates for collapsibles: implementation trade-offs between two similar options, deep technical justification for a design choice, exhaustive option lists.

---

## No TOC

Do not include a table of contents. Vyasa generates it automatically.

---

## Diagrams

- Use Mermaid (sequence, flowchart, C4 component, ER as appropriate).
- Use literal `<br/>` for line breaks inside Mermaid node labels.
- Diagrams confirm prose — they do not replace it.
- Every diagram must be preceded by at least one paragraph of prose that describes what it shows.

---

## Inline Links

Link to related documents at the natural moment in prose when the reader's curiosity about that document arises — not in a footer block.

**Right:** "...for how the RT Agent merges signals across sources, see the [RT Agent LLD](../lld/rt-agent/index.md)."
**Wrong:** A "Related Documents" footer block at the end of the file.
