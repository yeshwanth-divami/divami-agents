---
name: narrative-guide
description: Story arc structure, tone calibration, and audience adaptation rules for shaping excavated facts into a publishable use case narrative.
type: reference
---

# Narrative Guide

A use case follows the oldest story arc: a world with a problem, a journey through the solution, and a transformed world at the end. The facts were excavated. Now they become a story.

---

## Story Arc

### Act 1 — Situation (The World Before)

Open with the client's pain. Not your interpretation of it — their experience of it. Use their language if you have quotes.

Structure:
1. Who is the client? (industry, scale — enough to place them, anonymized if needed)
2. What was the problem? (business terms, not technical)
3. What was at stake? (cost of inaction)

This section earns trust. If a reader's own pain shows up here, they stay.

### Act 2 — Approach (The Journey)

Not a feature list. A narrative of decisions. The reader should understand *why* at every turn.

Structure:
1. What was the first thing you understood that others might have missed?
2. What methodology did you use and why was it right for this problem?
3. What were the pivotal decisions? (tech choices, architecture, scope tradeoffs)
4. What did you explicitly choose NOT to do, and why?
5. **System entry point:** what is the primary input and why that specific input over alternatives?
6. **Agent architecture:** single agent or multiple? If multiple, name them and their roles. Explicitly distinguish sequential architectural generations from concurrent running components — leadership confuses these.
7. **Why the key mechanism exists:** for any central pattern (e.g. runbooks, validation pipeline, event loop), explain the cost of NOT having it, not just what it enables. "Without runbooks, every new diagnostic pattern requires a developer and a deployment" lands harder than "runbooks allow domain experts to extend the system."

The "chose not to" is often the most persuasive part. It shows judgment, not just execution.

### Act 3 — Outcome (The World After)

Lead with numbers. Metrics first, qualitative impact second.

Structure:
1. Measurable results (before/after, with units and timeframes)
2. Business impact (what changed for the client's business, not just their codebase)
3. Client reaction (quotes if available)

---

## Tone Rules

The audience is mixed: CTOs, PMs, procurement. The tone must satisfy all three.

| Audience | What they want | How to deliver |
|---|---|---|
| CTO / Technical Lead | Evidence of technical judgment | Show decision rationale,<br/>not just the decision.<br/>Name tradeoffs. |
| Product Manager | Evidence of process discipline | Show methodology,<br/>scope management,<br/>stakeholder handling. |
| Procurement / Leadership | Evidence of reliability<br/>and measurable ROI | Lead with metrics.<br/>Use business language.<br/>Show risk awareness. |

**Calibration principle:** Write at a level where a CTO nods and a PM doesn't squint. Technical depth goes in the Approach section; business impact leads the Situation and Outcome.

---

## Tone Anti-patterns

| Don't | Do |
|---|---|
| "We leveraged cutting-edge AI" | "We used GPT-4 to classify<br/>support tickets by urgency" |
| "Our team delivered a<br/>world-class solution" | "Response time dropped<br/>from 3s to 200ms" |
| "The client was thrilled" | Quote the client directly |
| "We built a robust,<br/>scalable platform" | "The system handles<br/>10x the original load<br/>without infrastructure changes" |

Every hollow adjective is a missed opportunity to state a specific claim.

---

## Prose Rules

Inherited from doc-narrator:

- **Prose before structure.** Tell the story, then show the table.
- **One sentence, one idea.** If a sentence has "and" connecting two unrelated claims, split it.
- **No nominalizations.** "We improved performance" not "performance improvement was achieved."
- **Context seed every document.** A reader opening this cold must understand it without reading anything else.
- **Analogies where they clarify.** If you can make a technical decision tangible with a one-sentence analogy, do it.

---

## Section Transitions

Each section must end by creating the question the next section answers.

- Situation ends with: "This is what needed to change." (Reader asks: "How?")
- Approach ends with: "This is what we built and why." (Reader asks: "Did it work?")
- Outcome answers: "Here's the proof."

Never start a section with "In this section we will..." — just start.

---

## Polish-Stage Additions

When advancing from narrative to final:

1. **Summary block** — 3-4 sentences at the top. Industry, problem, solution, headline metric. This is what gets quoted in proposals.
2. **Key Decisions table** — 3-5 rows. Decision | Alternative | Why. Shows judgment.
3. **Tighten prose** — cut 20%. Every sentence must earn its place.
4. **Verify all metrics** have sources. Unflagged metrics in the final doc are claims you're publishing.
5. **Format for publication** — clean markdown, no internal references, no open questions (resolve or remove).
6. **System architecture diagram** — include a visual of how the system works. Read the actual agent/orchestration source files before drawing it -- do not rely on the narrative description alone. Verify agent count, data flow, and component roles from code. A wrong diagram is worse than none.
7. **Define all jargon on first use** — any term from the Domain Glossary must be defined the first time it appears. If a term needs more than one clause to explain, it belongs in a callout or footnote, not mid-sentence.
8. **Strip internal implementation labels** — validation stage codes, architecture acronyms, configuration parameters, and internal naming conventions must be replaced with plain English before the final doc. The test: would a non-technical executive understand this term without a glossary? If not, replace it.
