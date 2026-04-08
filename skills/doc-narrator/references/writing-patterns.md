# Writing Patterns

The rules every doc-narrator document follows. These are not style preferences — they are the structural principles that prevent readers from getting lost and authors from falling into prerequisite regression.

The section titles in this file are pattern names for the skill author, not prescribed output headings. In generated documents, prefer natural, topic-specific headers over copied phrases from this reference.

---

## Context Seed

Every document opens with a context seed: 3–5 sentences that make the document self-contained for a reader who has never heard of this project. The seed appears before the table of contents, before any heading, before any diagram.

**What a context seed must answer:**
1. What world does this document live in? (one sentence on the product/system)
2. What is this specific document about? (one sentence on the component/decision/flow)
3. What will the reader understand by the end? (one sentence on the outcome of reading)
4. If a neighbouring system appears in this doc — what is it, in one clause? (inline, not a link)

**The test:** Cover the title and show the seed to someone who has never seen this project. Can they read the document without confusion? If yes, the seed works.

**What a context seed is not:**
- A link to a prerequisite: `> See data-flow-understanding.md first` — this is the disease, not the cure
- A generic opener: "This document describes the technical design of..." — this says nothing
- A list of what the document contains — that is a table of contents, not a seed

**Bad opener (from a real doc):**
```
> **Related Doc:** [data-flow-understaning.md](../data-flow-understaning.md)

## 1. Overview
This document describes the low-level design of the Gmail data pipeline...
```

**The same document with a context seed:**
```
Enterprise Brain is an AI system that reads an organisation's communication tools — Gmail,
Jira, GChat — and distills them into a real-time project health picture for leadership.
This document describes one piece of that machine: how raw emails are transformed into
structured intelligence. By the end, you will understand exactly what happens to an email
between the moment it lands in someone's inbox and the moment it influences what a CXO sees
on their dashboard. One neighbour appears here — the RT Agent — which you can treat as a
black box that receives project IDs and updates an org-level snapshot; its internals are not
needed to follow this document.
```

---

## Narrative Before Diagram

Tell the story in prose before showing the diagram. The reader must know what they are about to see before they see it.

**Wrong:**
```markdown
## Pipeline Flow

[sequence diagram with 8 participants]

The Gmail DSA collects emails, enriches them...
```

**Right:**
```markdown
## Pipeline Flow

The pipeline runs in three steps. First, the Gmail Data Source Agent collects all emails
across the org and deduplicates them by message ID. Second, each email is individually
enriched — the LLM extracts a summary and per-insight bullets, each with sentiment, type,
and role. Third, the DSA notifies the RT Agent with the project IDs of newly written data,
and the RT Agent takes it from there.

[sequence diagram that confirms what was just described]
```

---

## Open Questions Are First-Class

Unresolved decisions are documented explicitly. They are not hidden in comments or deferred silently.

Every document with open decisions has a clearly named unresolved-decisions section at the end, before navigation. `Open Questions` is acceptable, but not required. Each item:
- Numbered
- States the question clearly
- States the options being considered (if known)
- States why it is blocked or deferred
- States which other document or decision it is blocked on

Open questions are resolved by updating them in place — the question is replaced with the answer and moved to the relevant section. Do not delete old questions; replace them with the resolved decision.

**Format:**

```markdown
## Open Questions

1. **Schema for the snapshot table** — The snapshot needs a column for "latest signals per
   project" but the shape (flat JSONB vs. separate rows) is undecided. Options: (a) JSONB —
   fast reads, schema-free; (b) separate table — queryable, FK-safe. Blocked on whether the
   distribution engine queries the snapshot directly or always joins through source tables.
   Unblocked by ADR-003.

2. **Hashtag taxonomy** — Whether per-item hashtags are a fixed enum or LLM-generated free
   strings needs to be decided. A fixed taxonomy makes downstream pattern detection
   deterministic. Blocked on a review of existing tags from the last 100 sync cycles to
   assess whether a closed vocabulary is feasible.
```

A question that is later answered is resolved in place: the question text is replaced with the resolution and the item is moved to the relevant design section. The numbering stays stable for any cross-references.

---

## Contextual Inline Links

Do not duplicate Vyasa's site navigation with footer link blocks. Instead, link to other documents at the natural moment in the prose when the reader's curiosity about that document arises.

**Right:**
> The bullets written here are the primary input for the RT Agent. For how the RT Agent
> merges signals across sources into a unified project view, see the
> [RT Agent LLD](../lld/rt-agent/index.md).

**Wrong:**
```
---
**Up:** [LLD Index](../index.md)
**Goes deeper into:** [RT Agent](../lld/rt-agent/index.md)
```

The difference: the right version appears because the narrative led there. The reader follows it because their question just formed. The wrong version is a signpost at the end of a road — by the time you see it, you've already stopped reading.

---

## Context Seed Variation

A reader going through multiple documents in sequence will encounter the seed of every document they open. If every seed opens with the same system description, the reader is annoyed by document #4.

**Rule: downstream documents compress the system-level context to one clause.**

- Document 1 (root index): Full 3–5 sentence seed. This is the canonical system description.
- Document 2+ (HLD, LLD, ops): The system is one subordinate clause. The seed's main statement is about this specific document.

**Root seed (full):**
> Enterprise Brain is an AI system that reads an organisation's communication tools — Gmail,
> Jira, GChat — and distills them into a real-time project health picture for leadership.
> [continues for 3–5 sentences]

**LLD component seed (compressed):**
> Enterprise Brain reads an organisation's communication tools and distills them into a
> real-time project health picture for leadership. This document covers the Gmail Ingestion
> component — the part that reads raw emails, runs LLM enrichment, and writes structured
> intelligence to the database. By the end, you will understand exactly what happens to an
> email between the moment it arrives and the moment its bullets are queryable by the RT Agent.

The first sentence is one clause summarising the system. The second sentence announces this specific document. The third tells the reader what they gain. The seed is still self-contained — a reader who opens this document cold can follow it. But it does not repeat the full origin story for readers who have already read it once.

---

## The "Why" Section Pattern

For tables that enumerate fields, decisions, or steps — always follow with a justification section that explains each entry. The heading should sound natural in the document's voice, not copied from this reference. This pattern prevents the reader from wondering "but why not X?"

**Format:**

```markdown
## Why These Choices — Nothing Missing?

| Field / Choice | Why it cannot be omitted or simplified |
|---|---|
| `summary` (item-level) | Provides a coarse-grained search surface and a human-readable digest.
Without it, the record has no LLM intelligence — it is only a header index. |
| `role` (per-signal) | The distribution layer routes signals to the right users. Without `role`,
every signal reaches everyone — targeted signals become noise. |
| `sentiment_value` + `sentiment_score` | Sentiment varies within a single source record —
one bullet can be positive while another is negative. Per-signal sentiment preserves fidelity. |
| `embeddings` at both levels | Item-level embeddings support broad semantic queries;
signal-level embeddings support precise retrieval. Without both, search depth is limited
to one granularity. |
```

Every row answers: *what breaks if this is removed?* A table that cannot answer that question for every row is incomplete.

---

## Plain Language

Write so a motivated 12-year-old could follow it. This is not about dumbing down — it is about removing the fog that makes readers re-read sentences. The fog is almost always one of three things:

**1. Nominalization — hiding verbs inside nouns**

Every time you write a noun that contains a hidden verb, the sentence loses energy and gains length.

| Foggy | Clear |
|---|---|
| "AI-powered case structuring" | "AI structures your case" |
| "intelligent moderation" | "AI flags off-topic posts" |
| "participant management" | "control who joins" |
| "decision quality improvement" | "decisions get better" |

Test: if you can find a verb inside the noun (structure, moderate, manage, improve), rewrite using the verb.

**2. Hollow adjectives — modifiers that do not discriminate**

"Advanced", "intelligent", "sophisticated", "enhanced", "AI-powered" — these say nothing unless the sentence also says *how*. If the adjective applies equally to everything, it applies to nothing.

Cut the adjective or replace it with the specific claim:
- "intelligent moderation" → "moderation that detects off-topic posts and flags them"
- "advanced participant management" → "invite contributors by expertise, not by name"

**3. Long sentences doing too many jobs**

One sentence, one idea. If a sentence lists 4 features to achieve 1 goal, split it: state the goal first, then the features.

---

## Callouts

Use Vyasa callouts for information that would interrupt the narrative but is important enough to surface:

```markdown
> [!note]
> The LLM never sees raw email content after enrichment. Only the derived intelligence is stored.

> [!warning]
> The `eb.org_project_snapshot` schema is TBD pending resolution of Open Question 6.

> [!tip]
> When debugging enrichment failures, check `eb.emails.enriched_at` — a missing value means the enrichment step never completed for that email.
```

Use Obsidian-style `> [!note]` syntax only. `///` callouts are no longer supported.

---

## Collapsibles for Deep Detail

Use `<details>` when technical detail is necessary but would interrupt the reading flow for most readers:

```markdown
<details>
<summary>Why IVFFlat over HNSW for the embedding index</summary>

IVFFlat was chosen over HNSW because the dataset size is currently unknown and IVFFlat
allows the `lists` parameter to be tuned after data volume is established, whereas HNSW's
`ef_construction` must be set at index creation time...

</details>
```
