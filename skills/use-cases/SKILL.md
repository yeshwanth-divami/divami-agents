---
name: use-cases
description: Excavate evidence from a finished project repo and turn it into a staged, publishable use-case narrative through extraction, story drafting, and final polish.
argument-hint: "excavate | narrate | polish | status"
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, Agent, WebFetch, TodoWrite
---

# Use Cases

A finished project leaves behind code, docs, transcripts, and scattered decisions. This skill excavates those artifacts and produces a publishable use case document — proof of competence disguised as a story.

Run this skill from inside the project repo. One use case per repo.

---

## Core Principle

> A use case proves three things: you understood the real problem, you had a method, and the outcome was measurable. Everything else is decoration.

---

## The Zen of Use Cases

```
The evidence already exists — your job is archaeology, not invention.
A use case that reads like a portfolio piece has failed. It must read like proof.
Situation before solution. Problem before process. Numbers before narrative.
If the client's pain isn't in the first paragraph, start over.
Quotes from real humans beat polished prose every time.
The hardest part is not writing — it's deciding what to leave out.
A use case without metrics is a testimonial. A testimonial without a story is an ad.
```

---

## On Startup

1. Read `references/use-case-anatomy.md` — understand what a use case proves.
2. Check if `docs/use-case/` exists and scan for existing stage files to determine current state.

---

## Stage Folders

All output lives in `docs/use-case/` at the project root. Files are named by stage, not codename — one use case per repo.

| Stage | File | Meaning |
|---|---|---|
| 1 | `docs/use-case/excavation.md` | Raw facts extracted from artifacts |
| 2 | `docs/use-case/narrative.md` | Story draft shaped from facts |
| 3 | `docs/use-case/final.md` | Polished, publishable document |

---

## Routing

| Command | Action |
|---|---|
| `excavate` | Read `references/excavation-guide.md`. Ingest repo artifacts (code, docs, transcripts). Write `docs/use-case/excavation.md`. |
| `narrate` | Read `references/narrative-guide.md`. Consume `excavation.md`. Write `docs/use-case/narrative.md`. |
| `polish` | Read `references/narrative-guide.md` (tone section). Consume `narrative.md`. Write `docs/use-case/final.md`. |
| `status` | Scan `docs/use-case/`. Show which stage files exist, their `stage` and `status` frontmatter. |

Before advancing a stage, check the previous stage file's `status`. If `needs-review`, stop and surface open questions. If `complete`, proceed.

---

## Workflow

### Phase 1 — Excavate

Read `stages/01-excavation/CONTEXT.md`. Load `references/excavation-guide.md`.

The agent explores the repo: README, docs, source code, commit history, transcripts, any Google Docs the user provides access to. It extracts raw facts into structured categories: client problem, constraints, approach taken, tech stack, architecture decisions, outcomes/metrics, and notable quotes.

Output: `docs/use-case/excavation.md`

The user reviews the extracted facts. They correct errors, fill gaps, add metrics or context the artifacts don't capture. They set `status: complete` when satisfied (or it defaults to `complete` if no edits needed).

### Phase 2 — Narrate

Read `stages/02-narrative/CONTEXT.md`. Load `references/narrative-guide.md`.

The agent consumes the reviewed excavation and shapes it into the classic use case arc: Situation, Approach, Outcome. It writes prose, not bullets. It adapts tone for a mixed audience (technical enough to satisfy a CTO, clear enough for procurement).

Output: `docs/use-case/narrative.md`

The user reviews the draft for accuracy, tone, and story arc. They may restructure sections or flag missing context.

### Phase 3 — Polish

Read `stages/03-polish/CONTEXT.md`. Load `references/narrative-guide.md` (tone section).

The agent takes the reviewed narrative and produces the final publishable document. It tightens prose, ensures metrics are prominent, adds a summary block, and formats for publication.

Output: `docs/use-case/final.md`

---

## Output Rules

- All output follows doc-narrator conventions: context seeds, prose-first, open questions as first-class sections.
- Load `references/doc-narrator-rules.md` at every stage for writing patterns.
- Never invent facts. Every claim must trace to an artifact found in the repo or provided by the user.
- Metrics without a source get flagged as open questions, not stated as fact.
- Quotes must be attributed or flagged for attribution.

---

## Reference Files

| Need | Read |
|---|---|
| What a use case proves, its sections | `references/use-case-anatomy.md` |
| How to extract facts from artifacts | `references/excavation-guide.md` |
| Story arc, tone, audience rules | `references/narrative-guide.md` |
| Doc-narrator writing patterns | `references/doc-narrator-rules.md` |
