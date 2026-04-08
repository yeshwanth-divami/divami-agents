---
name: premise-check-guide
description: How to extract and assess the assumptions baked into a raw tech idea before any scope probing begins. Covers assumption types, assessment criteria, verdict rules, and how to offer a reframe.
type: reference
---

# Premise Check Guide

Before probing scope, check whether the idea stands on solid ground. Every tech idea carries assumptions — some stated, most not. A flawed premise makes the entire feasibility analysis misleading. Catch it here.

---

## What to Extract

Read the idea and identify assumptions in three categories:

### 1. Domain assumptions
Facts the idea takes for granted about the real-world domain it operates in.
- "Patients have a year of ICU data" — is that how ICUs work?
- "Doctors check dashboards between consultations" — do they actually?
- "Inventory data is available in a structured format" — is it?

### 2. Technical assumptions
Claims about what the technology (LLM, ML, AI) can do for this use case.
- "An LLM can detect patterns in time-series vitals" — is LLM the right tool, or is this a job for a specialised ML model?
- "The system can ask follow-up questions dynamically" — yes, this is LLM's core capability; solid.
- "AI can predict deterioration better than existing clinical scoring systems" — this is a research-grade claim, not a product assumption.

### 3. Market/competitive assumptions
Claims about whether a gap exists that this system fills.
- "No existing system does this" — is that true? Are there validated alternatives already deployed?
- "Medical staff will adopt this" — is there a known adoption barrier (e.g., alarm fatigue) that undermines the premise?

---

## How to Assess Each Assumption

Rate every assumption as one of three statuses:

| Status | Meaning |
|---|---|
| **Solid** | Verifiably true or widely accepted in the domain. No action needed. |
| **Questionable** | Plausible but uncertain — depends on context, deployment setting, or an unverified claim. Worth flagging; proceeding is possible with caveats. |
| **False** | Contradicted by known domain facts, existing systems, or the nature of the technology. Should not be silently accepted. |

One-line reason required for every row. Do not hedge — if it's false, say it's false.

---

## Verdict Rules

After filling the assumption table, apply this decision rule:

| Condition | Verdict |
|---|---|
| All solid | State this briefly. Move to Phase 1 immediately — no user confirmation needed. |
| One or more questionable, none false | Flag the questionable ones. Offer to proceed with caveats or reframe. Wait for user. |
| Any false | State the verdict plainly. Name what is broken. Offer reframe or stop. Wait for user. |

**Do not soften false assumptions.** "This assumption may need revisiting" is not the same as "this is false because X." Say the second one.

---

## How to Offer a Reframe

When the idea has false or multiple questionable assumptions, suggest a narrower version that removes the broken premise while preserving the useful core.

Format:
> **Reframe:** Instead of [original idea], consider: [narrower idea that sidesteps the false assumption]. This preserves [the useful part] without requiring [the broken premise].

Example:
> **Reframe:** Instead of building a new deterioration prediction model for ICU, consider building a triage assistant that consumes outputs from existing early warning score systems (NEWS2, SOFA) and uses an LLM to surface the highest-risk patients in plain language with a recommended action. This preserves the "AI helps staff prioritise" value without requiring a new clinical prediction model or FDA clearance.

---

## What Not to Flag

- Implementation unknowns that are normal for any early-stage idea (e.g., "which EHR vendor?" is a probing question, not a broken premise)
- Assumptions that are simply unspecified — probe those in Phase 1
- Opinions about product strategy or market fit — this is a technical feasibility check, not a business case review
