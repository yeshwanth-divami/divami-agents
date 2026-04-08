---
name: outline
description: Template for the pre-write doc plan presented to the user before the feasibility document is generated. Fill all placeholders before presenting.
type: template
---

# Outline: {{idea_slug}} Feasibility Analysis

**Idea:** {{idea_one_liner}}

**Scope confirmed:**
{{scope_summary — 3–6 bullet points drawn from probing answers. Each is one concrete fact about the system: modality, consumer, integrations, constraints, boundary.}}

---

## Sections I will write

1. **Context seed** — {{one sentence on the angle: what scene will be painted, what the cold reader will understand}}
2. **What the system must do** — {{one sentence on the scenario that will be traced: user journey from entry to output}}
3. **Where {{AI_capability}} adds value** — {{named AI tasks: e.g., "adaptive questioning, NLU, summarisation" or "anomaly detection, trend forecasting"}}
4. **Architecture** — {{one sentence on the layers: e.g., "voice front-end → orchestration → LLM → EHR write-back" or similar}}
5. **What is hard** — {{named challenges, comma-separated: e.g., "safety guardrails, urgency detection, EHR integration, HIPAA compliance"}}
6. **Feasibility verdict** — table with {{N}} dimensions: {{dimension names, comma-separated}}
7. **Why these outputs** — Why? table for {{output names, comma-separated}}
8. **Build order** — Spine: `{{spine_node_1}} → {{spine_node_2}} → {{spine_node_3}}`; Bulges: {{bulge features and their parent spine nodes}}
9. **Open questions** — {{N}} items: {{one-line description of each, semicolons}}

---

## Key angles

- {{Angle 1 — something non-obvious this doc will address, derived from probing answers}}
- {{Angle 2}}
- {{Angle 3 if needed}}

---

## Assumptions I'm making

{{List any dimensions that were not explicitly answered but where I will proceed with a reasonable default. Each assumption names the default and notes it is unconfirmed.}}

- {{e.g., "Assuming web/mobile text interface unless voice is confirmed"}}
- {{e.g., "Assuming FHIR R4 for EHR integration unless otherwise specified"}}

---

**Output file:** `{{kebab-case-idea}}-feasibility.md` in the current working directory.

Confirm to proceed, or steer any section before I write.
