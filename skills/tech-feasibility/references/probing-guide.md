---
name: probing-guide
description: The five core dimensions to probe for any tech idea, batching rules, follow-up strategy, and stop conditions.
type: reference
---

# Probing Guide

Before writing a feasibility analysis, you must understand the shape of the idea. Shape is defined by five dimensions. You probe these through iterative Q&A batches.

---

## The Five Core Dimensions

Every tech idea has unknowns in these areas. Probe all five.

### 1. Interaction Modality
How do users interact with the system? Text chat, voice, kiosk, mobile app, API-only, embedded widget? The modality determines latency budget, accessibility constraints, UI complexity, and which LLM capabilities are relevant.

**Why it matters:** A voice-driven system has no typing — turn-taking, response length, and latency all change. A kiosk has no take-home — session scope is bounded. Getting this wrong makes the architecture section meaningless.

### 2. Output Consumer
Who reads or uses the output, and when? Is it a human reading a summary, a downstream system ingesting structured data, or both? Is the consumer time-pressured (e.g., doctor walking in) or reviewing at leisure?

**Why it matters:** The consumer determines what the output must contain, how it must be formatted, and what "good enough" means. An output optimised for a doctor's five-minute pre-consultation review looks nothing like one optimised for an EHR API.

### 3. Integration Surface
What existing systems must this touch? What are their APIs, data formats, and access constraints? Integrations are almost always the long pole in the tent — not technically hard, but operationally slow.

**Why it matters:** A system that integrates with a modern REST API ships in weeks. One that integrates with a legacy HL7 v2 EHR ships in months, depending on procurement. The feasibility timeline is determined here.

### 4. Regulatory and Safety Constraints
What compliance, liability, or risk boundaries apply? Medical → HIPAA. Finance → SOC2/PCI. Children → COPPA. High-stakes output (medical, legal, financial) → hallucination risk becomes safety risk.

**Why it matters:** Constraints here are not features to implement — they are hard walls that narrow the solution space and inflate timeline. They must be named explicitly, not discovered in production.

### 5. Scope Boundary
What is explicitly out of scope? What does the system hand off to, and where does it stop? A system with no defined boundary expands to fill all available complexity.

**Why it matters:** The hardest parts of a feasibility analysis are often the things the idea does not mention. Naming the boundary prevents the doc from being a product roadmap disguised as a feasibility study.

### 6. Hardware & Deployment Constraints *(conditional)*

**Trigger:** Probe this dimension when the idea involves cameras, microphones, sensors, physical kiosks, edge inference, on-premises data processing, or any constraint that prevents cloud round-trips.

What hardware is assumed or available? Is inference on-premises (edge node), cloud, or hybrid? Are there data residency or air-gap requirements (GDPR, DPDPA, HIPAA) that prohibit data leaving the site? Are off-the-shelf models sufficient for the task, or does it require custom training — and if custom, does a labelled training dataset exist or must it be collected?

**Why it matters:** Hardware class determines inference latency, model size ceiling, and cost. Data residency constraints are architecture-determining, not a compliance footnote. The gap between "off-the-shelf model works" and "requires a custom-trained model with 6 months of data collection" is the single largest driver of timeline variance in ML feasibility. Getting this wrong produces a confident doc with a wrong timeline.

---

## Batching Rules

- Ask all questions for a round in a single message. Never drip one question at a time.
- Target ~5 questions per batch — enough to cover a dimension-round without overwhelming the user.
- Number questions within each batch so the user can answer selectively (e.g., "1. ..., 2. ..., 3. ...").
- Frame questions as open-ended, not yes/no. "What does the user see when..." not "Is the UI a chat interface?"
- If a dimension was partially answered but remains ambiguous, probe deeper in the next batch — do not re-ask the same question.

---

## Follow-Up Strategy

After the user answers the first batch:

1. Mark each dimension as: **resolved**, **partially resolved**, or **unresolved**.
2. Generate a second batch covering only unresolved and partially-resolved dimensions.
3. Do not re-ask resolved dimensions. Do not add new dimensions.
4. Make follow-up questions more specific — if modality was "voice", the follow-up is not "what is the modality?" but "is there a companion screen, or is the interface audio-only?"

---

## Stop Conditions

Stop probing when ALL of the following are true:

- Modality is known (at least one primary channel is named)
- Output consumer is named (human role + timing, or system + format)
- Integration surface is either named or explicitly acknowledged as TBD
- Regulatory/safety constraints are either named or confirmed absent
- Scope boundary is articulated (what the system does NOT do)
- If dimension 6 was triggered: hardware class is named, edge vs cloud is resolved, and training data availability is either confirmed or flagged as the long pole

**Exception:** The user may waive a dimension by saying "not relevant", "TBD", "doesn't matter for now", or equivalent. Treat an explicit waiver as resolved — do not probe further.

---

## What Not to Probe

- Implementation details the user has not raised (don't ask about database choice if they haven't mentioned data storage)
- Timeline or budget (out of scope for a feasibility analysis)
- Team size or org structure (not a technical feasibility concern)
- Hypothetical future requirements ("what if you later wanted to...")
