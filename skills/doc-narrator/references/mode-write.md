# Mode: Write

Input: a component, flow, or decision to document.

**Ground rule:** Do not write about code you have not read. Read every file you will reference before writing.

Steps:
1. Write the context seed
2. For each section: prose narrative first, then a diagram slot that confirms it
3. Add an unresolved-decisions section for anything unresolved — see `writing-patterns.md` § Open Questions
4. Add a justification table or short justification subsection for every enumeration of fields, steps, or choices

Header rule:
- Do not copy reference labels like `Open Questions` or `Why these and nothing else?` verbatim into output unless the user explicitly wants those exact words.
- Rewrite headings so they sound native to the document, for example `Outstanding Decisions`, `Remaining Unknowns`, `Rationale`, `Design Tradeoffs`, or `Why This Shape`.

**Substance floor:** A section with fewer than 3 sentences is a stub. Flow sections must trace the full lifecycle, not summarise it. Optimise for the cold reader's understanding.

---

## Manual-First Writing

Trigger: the document is a handbook, manual, runbook, onboarding guide, or any "what should I do next?" document.

In this mode, optimise for next action, stop conditions, and recovery before concept expansion or deep-link navigation.

Steps:
1. Start with audience + goal
2. Put prerequisites before the workflow
3. Keep the main happy path complete in one place
4. Add "if blocked" guidance before any "go deeper" links
