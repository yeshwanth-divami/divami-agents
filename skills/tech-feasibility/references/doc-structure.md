---
name: doc-structure
description: The required sections of a tech feasibility document, what each must contain, and what a stub looks like vs. a complete section.
type: reference
---

# Feasibility Document Structure

Every feasibility analysis has these sections, in this order. Sections are not optional — a missing section is a gap in the analysis, not a stylistic choice.

---

## 1. Context Seed (no heading — appears before everything)

3–5 sentences. No heading. No TOC. Appears before any section marker.

Must answer:
- What world does this idea live in? (one sentence on the domain/problem space)
- What is this document about? (the specific system being assessed)
- What will the reader understand by the end?

**Stub:** "This document analyses the feasibility of X." — This says nothing a reader couldn't infer from the title.
**Good:** Paints the problem the system solves, names the specific approach being assessed, and tells the reader what they will know at the end.

---

## 2. What the System Must Do

Prose. No bullets. 2–4 paragraphs.

Describes the system's job in plain language: who uses it, when, and what it produces. Sets the scene before any technical content. The reader should understand the full scope of the system — including its explicit limits — before seeing any architecture.

**Must include:**
- The user's journey from entry to exit
- What the system produces (outputs, not features)
- What the system explicitly does not do (boundary)

**Stub:** A list of features or requirements. That is a PRD, not a scenario.
**Good:** A narrative that traces what happens from the user's first action to the final output.

---

## 3. Where the LLM / AI Adds Value

Prose. 3–5 paragraphs or a short prose + named subsections.

Explains specifically why this system benefits from LLM or AI — what the AI does that a rule-based or traditional system cannot. This section justifies the "why AI?" question.

**Must include:**
- The specific capability gap that AI closes (e.g., adaptive branching, NLU, summarisation)
- Named AI tasks the system will perform (e.g., "next-question generation", "intent classification", "transcript summarisation")
- Why each task is appropriate for an LLM (reliable in this context) vs. risky (hallucination-prone)

**Stub:** "AI enables dynamic responses." — This is a marketing phrase, not an analysis.
**Good:** Names each AI task, explains why a rule-based approach fails for it, and flags which tasks are reliable vs. which need guardrails.

---

## 4. Architecture

Prose walk-through of the system's layers, then a Mermaid diagram that confirms what was just described.

**Must include:**
- Every major component named and its job described in one sentence
- The data flow: what enters each component and what leaves
- A Mermaid sequence or component diagram placed after the prose, not before

**Stub:** A diagram with no prose before it, or a bullet list of components.
**Good:** 3–4 paragraphs tracing the system's layers, followed by a diagram the reader can verify against what they just read.

---

## 5. What Is Hard

The core feasibility content. This is where the analysis earns its keep.

One subsection per significant challenge. Each subsection:
- Names the challenge as a heading
- Explains why it is hard (not just what it is)
- Names the options for addressing it
- States which option is recommended and why

Use `<details>` collapsibles for implementation trade-off depth that would interrupt the main read.

Use `> [!warning]` callouts for challenges that are non-negotiable safety or compliance issues.

**Must include at minimum:**
- The hardest technical challenge specific to this system
- Any safety, compliance, or liability concern (if domain-relevant)
- Integration complexity (if the system touches external systems)

**Stub:** "There are some challenges." or a single paragraph naming everything without depth.
**Good:** Each challenge gets its own heading and enough prose that an engineer understands what they are signing up for.

---

## 6. Feasibility Verdict

A table. One row per dimension. Three columns: Dimension, Assessment, and Time Horizon.

Standard dimensions (add/remove based on what was probed):
- Core AI/LLM task
- Output quality / reliability
- Safety / guardrails
- Integration with external systems
- Regulatory compliance
- User experience / accessibility

Each assessment is a plain-English verdict: **Straightforward**, **Feasible with caveats**, **Technically feasible / operationally hard**, **Risky — needs mitigation**, or **Unknown — depends on X**.

**Time Horizon labels** — use exactly these three, with these precise definitions:

| Label | Meaning |
|---|---|
| **Now** | Operational pilot within 6–8 weeks of install using off-the-shelf models; no custom training required |
| **6 months** | Architecture exists but depends on a local calibration dataset that can only be collected by running the system first — real sessions, real outcomes, real site geometry. That data cannot be purchased or substituted; it takes a full project cycle to accumulate. |
| **Futuristic** | Research-grade problem. No commodity model covers it today. No timeline is possible without first proving the capability exists at the required accuracy in a lab setting. Do not include in any delivery commitment. |

When a capability has a "6 months" label, add a one-sentence **Time horizon rationale** immediately below its description explaining the *specific* technical reason: what dataset is missing, what threshold cannot be set until real events are observed, or what upstream dependency must stabilise first.

Follow the verdict table with 2–3 sentences of overall verdict prose: what the timeline looks like at a high level, what is the long pole, whether the idea is sound.

---

## 7. Why These Outputs — Nothing Missing?

A Why? table. One row per system output.

Columns: Output | Why it cannot be dropped

Each row answers: what breaks if this output is removed? A table that cannot answer that question for every row is incomplete.

---

## 8. Build Order — Critical Path and Dependency Graph

The implementation sequence. Answers: what do we build first, what can run in parallel, and what is the long pole?

The strategy is **spine first, then bulge out.** The spine is the longest unbroken dependency chain — the sequence whose delay delays everything else. Bulge nodes are features that depend on exactly one spine node and can be built in parallel with the rest of the spine once that node is live.

**Depth required depends on `output_purpose`:**

| Purpose | Required depth |
|---|---|
| Client evaluation | Spine statement (prose) + `flowchart LR`. No Gantt. |
| Internal architecture review | Full: spine statement, flowchart, Gantt, parallelism rules |
| Implementation planning | Full, and spine rationale must justify each ordering decision, not just name the sequence |

**Must include (all purposes):**

- An explicit statement of the spine: a left-to-right chain naming each node and why it precedes the next
- Named bulge nodes and which spine node unblocks each
- A Mermaid `flowchart LR` diagram: spine flows left-to-right, bulge nodes branch downward from their parent spine node. Style spine nodes distinctly (e.g., coloured fills).

**Full depth only (architecture review + implementation planning):**

- A Mermaid `gantt` diagram showing which tracks run in parallel and when

**Stub:** A numbered list of features in vague priority order. That is a backlog, not a build sequence.
**Good:** Names the spine explicitly, explains *why* each node is on the spine (not just that it is), and names each bulge's unblocking condition. The diagram confirms the prose.

**Example spine statement format:**
> The spine for this system is: `Infra → [Component A] → [Component B] → [Component C]`. Everything else is a bulge. [Feature X] is a bulge off [Component A] — it needs inference routing but not the knowledge layer. Building [Feature X] before [Component B] is complete is not only possible, it is the right call.

**Parallelism rules to include:**
- Which nodes can never be parallelised with their upstream spine node (and why)
- Which sprint tracks can run simultaneously (and which engineers own each)

---

## 9. Open Questions

Numbered list. Every unresolved decision that would materially change the architecture, timeline, or scope.

Each item:
- States the question clearly
- Names the options under consideration
- States what unblocks it (a decision, a review, a vendor answer)

Do not omit open questions to make the doc look more complete. An unresolved decision documented is better than one discovered in sprint 3.
