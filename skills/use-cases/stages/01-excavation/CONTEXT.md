# Stage 1 — Excavation

> Extract raw facts from project artifacts. Archaeology, not invention.

---

## Inputs

| Type | Path | Purpose |
|---|---|---|
| Layer 3 | `references/excavation-guide.md` | Where to dig and what to extract |
| Layer 3 | `references/doc-narrator-rules.md` | Writing patterns for the output file |
| Layer 4 | `templates/excavation.md` | Output structure |
| Repo | Project root | Source code, docs, transcripts, configs |
| External | Google Docs (if user provides) | PRDs, proposals, client feedback |

*Load only what is listed here. Do not load narrative-guide or final template.*

---

## Process

Explore the project repo broadly: README, docs, source code structure, dependency files, commit history, transcripts, and any Google Docs the user provides access to. For each extraction category in the excavation guide (client problem, constraints, approach, tech stack, outcomes, quotes), find and record raw facts with their source artifacts. Do not synthesize into narrative — that is the next stage's job.

### Constraints
- Never invent facts. Every claim must trace to a specific artifact.
- Preserve the client's own language when found in transcripts or docs.
- Flag any metric that lacks a clear source as an open question.
- Flag any quote that lacks attribution (speaker role) as an open question.
- Cast a wide net first — read broadly, then categorize.

---

## Outputs

| File | Format | Content |
|---|---|---|
| `docs/use-case/excavation.md` | Markdown | Raw facts organized by category, with source references |

**Resumption artifact:** `docs/use-case/excavation.md` — written before yielding control. Its `stage` and `status` frontmatter are the source of truth.

---

## Human Review Gate

**Verify before proceeding to narrate:**
- Each extraction category has at least some content (empty categories = missed artifacts)
- Client problem is stated in business terms, not just technical
- Metrics have sources noted, or are flagged as open questions
- No invented facts — everything traces to an artifact
- Open questions capture all gaps you noticed

**If wrong:** Edit `docs/use-case/excavation.md` directly. Add missing facts, correct errors, fill in metrics you know. Set `status: needs-review` if you want the agent to re-examine before proceeding.
