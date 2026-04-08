# Stage 3 — Write

> Generate the full feasibility analysis document from the confirmed outline, following doc-narrator conventions throughout.

---

## Inputs

| Type | Path | Purpose |
|---|---|---|
| Layer 3 | `references/doc-structure.md` | Section requirements — what each section must contain |
| Layer 3 | `references/doc-narrator-rules.md` | Writing conventions — seed, prose-first, Why? tables, callouts, diagrams |
| Layer 4 | `templates/feasibility-doc.md` | Output document skeleton |
| Layer 4 | Confirmed outline from Stage 2 | The agreed scope, sections, angles, and assumptions |

*Load all four. This is the only stage that loads doc-narrator-rules.md.*

---

## Process

Use the confirmed outline as the specification. Use doc-structure.md to meet the substance floor for each section. Use doc-narrator-rules.md for all writing decisions. Use the feasibility-doc template as the structural skeleton — fill every placeholder, leave none in the output.

**Apply `output_purpose` weighting before writing Build Order:**
- Client evaluation → write the spine statement in prose and the `flowchart LR` only. Do not write a Gantt diagram.
- Internal architecture review or implementation planning → write the full section: spine statement, flowchart, Gantt, and parallelism rules.

Write every section to its substance floor: no section fewer than 3 sentences. Trace the full lifecycle in "What the system must do" — do not summarise. Name each challenge in "What is hard" with its own subsection heading.

Generate the Mermaid diagram after writing the architecture prose — the diagram confirms what was just described, not the other way around.

Write the Why? table rows with `<br/>` wrapping at ~8 words per visual line to prevent horizontal scrolling.

Write the document to `tech-feasibility-analyses/<codename>/analysis.md`. The frontmatter must include `skill: tech-feasibility`, `codename`, `stage: analysis`, `status: complete`.

### Constraints

- The context seed appears before any heading. No exceptions.
- Prose before diagrams. The diagram must be preceded by at least one paragraph.
- No TOC — Vyasa generates it.
- No diagnostic language, speculation, or "this will definitely work" claims in any section.
- Open Questions must reflect genuine unknowns — do not fabricate resolvable questions to pad the section.
- Every Why? table row must answer: what breaks if this is removed? A row that defines the item instead of justifying it is wrong.
- Do not add sections not in the confirmed outline without telling the user.

---

## Outputs

| File | Format | Content |
|---|---|---|
| `tech-feasibility-analyses/<codename>/analysis.md` | Markdown | Complete feasibility analysis with ICM frontmatter |

After writing, state the file path (`tech-feasibility-analyses/<codename>/analysis.md`) and offer to adjust any section.

---

## Human Review Gate

**After writing:**
- Context seed present before any heading? If not, the file is malformed.
- Every section from the outline present? If a section is missing, it was skipped — add it.
- Mermaid diagram preceded by prose? If diagram comes first, fix the order.
- Why? table rows answer "what breaks", not "what it is"?
- All `{{placeholders}}` replaced? A stray placeholder in the output means the stage was incomplete.

**If the user requests a section change:** Edit in place using the Edit tool. Do not rewrite the whole document.

Before constructing `old_string` for any Edit call: Grep the target file for a short unique phrase (5–10 words) from the intended target location. Read the specific lines returned. Copy the exact character-for-character text — including typographic quotes (`"` `"` `'` `'`), em-dashes (`—`), and other non-ASCII characters. Do not rely on recalled text from a previous read. Files with long single-line paragraphs or typographic punctuation will silently fail a match if you guess.
