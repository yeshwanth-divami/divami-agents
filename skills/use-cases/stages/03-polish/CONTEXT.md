# Stage 3 — Polish

> Tighten the narrative into a publishable use case. No open questions survive this stage.

---

## Inputs

| Type | Path | Purpose |
|---|---|---|
| Layer 3 | `references/narrative-guide.md` | Tone rules + polish-stage additions |
| Layer 3 | `references/use-case-anatomy.md` | Structural validation — all mandatory sections present |
| Layer 3 | `references/doc-narrator-rules.md` | Writing patterns |
| Layer 4 | `templates/final.md` | Output structure |
| Layer 4 | `docs/use-case/narrative.md` | Story draft from Stage 2 |

*Load only what is listed here. Do not load excavation-guide or excavation template.*

---

## Process

Consume the reviewed narrative. Produce the final publishable document. Add a Summary block (3-4 sentences, proposal-quotable). Tighten all prose — cut 20%, every sentence earns its place. Ensure metrics are prominent and all verified. Resolve or remove all open questions — nothing unresolved survives into the final. Format cleanly for publication: no internal references, no skill metadata visible to external readers (frontmatter is for the skill, not the audience).

### Constraints
- No open questions in the final output. Resolve them or ask the user before proceeding.
- Every metric must have a verified source by this point, or be removed.
- Do not add new facts. Only refine what exists in the narrative.
- Summary block must be self-contained — quotable in a proposal without reading the rest.
- Client Voice section is included only if real quotes exist. Do not fabricate.
- Frontmatter stays for the skill's use, but the document body reads as standalone.
- **Strip internal implementation labels.** Any validation stage code (e.g. MDV0, ODV4), internal acronym, architecture abbreviation, or configuration parameter (e.g. temperature, timeout) that appears in the narrative must be translated to plain English before publishing. Test: would a non-technical executive understand this term without explanation? If not, replace it.
- **Client Voice test.** Before including a quote, ask: is this direct testimony about pain experienced or outcome achieved? Meeting summaries, coordination chatter, and design feedback do not qualify. If the section has no qualifying quotes, omit it entirely — do not pad.
- **Architecture diagram accuracy.** Before drawing or finalizing an architecture diagram, read the actual agent/orchestration source files (not just docs) to verify agent count, data flow, and component roles. A diagram that misrepresents the system is worse than no diagram.

---

## Outputs

| File | Format | Content |
|---|---|---|
| `docs/use-case/final.md` | Markdown | Publishable use case document |

**Resumption artifact:** `docs/use-case/final.md` — written before yielding control.

---

## Human Review Gate

**Verify before considering complete:**
- Summary block works standalone — paste it into a proposal and it makes sense
- No open questions remain
- All metrics have sources or have been removed
- Prose is tight — no hollow adjectives, no nominalizations, no filler
- Key Decisions table shows genuine judgment, not obvious choices
- Client Voice quotes are direct testimony about pain or outcome — not process discussion, design feedback, or meeting summaries (or section is omitted)
- No internal implementation labels remain — every stage code, acronym, or parameter is in plain English
- Architecture diagram reflects actual source code structure, not the narrative description
- Document reads as proof of competence, not a portfolio piece

**If wrong:** Edit `docs/use-case/final.md` directly. This is the last gate — get it right.
