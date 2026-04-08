---
name: feasibility-doc
description: Skeleton of the feasibility analysis output document. All {{placeholders}} must be filled before writing. Structure is fixed; only content changes per run.
type: template
---

# Template: Feasibility Analysis Output

This is the shape of the document. Fill every placeholder. Do not leave `{{...}}` in the output. Do not add a TOC — Vyasa generates it.

---

```markdown
{{context_seed}}

[3–5 sentences. No heading. Paints the problem space, names the system,
tells the reader what they will understand by the end. See doc-narrator-rules.md.]

---

## {{section_what_system_does}}

[2–4 paragraphs. The user's journey from entry to exit. What the system
produces. What it explicitly does not do. No bullets. No feature lists.]

---

## {{section_where_ai_adds_value}}

[3–5 paragraphs or named subsections. Specific AI tasks named. Why each
is appropriate vs. risky. Why a rule-based approach fails here.]

---

## {{section_architecture}}

[3–4 paragraphs tracing the system's layers. Every component named and
its job stated in one sentence. Data flow described.
Then the Mermaid diagram.]

```mermaid
{{mermaid_diagram}}
```

---

## {{section_what_is_hard}}

[One subsection per major challenge. Each has: why it's hard, options,
recommendation. Use [!warning] for safety/compliance issues.
Use <details> for deep trade-off comparisons.]

### {{challenge_1}}

{{prose}}

### {{challenge_2}}

{{prose}}

[...additional challenges from probing answers...]

---

## Feasibility Verdict

| Dimension | Assessment | Time Horizon |
|---|---|---|
{{| {{dimension}} | {{verdict}} | Now / 6 months / Futuristic |}}

{{2–3 sentence overall verdict: timeline shape, long pole, whether the idea is sound.}}

---

## Why These {{Outputs / Choices}} — Nothing Missing?

| {{Output / Field}} | Why it cannot be dropped |
|---|---|
{{| {{item}} | {{what breaks if removed — max 8 words per visual line, use <br/> for wrapping}} |}}

---

## Build Order

[State the spine in one sentence first: "The spine is: A → B → C → D."
Explain why each node precedes the next — not just sequencing, but why
building in a different order would defer the riskiest problem.
Name each bulge node and the spine node that unblocks it.
Then the dependency graph diagram, then the Gantt.]

The spine for this system is:

`{{spine_node_1}} → {{spine_node_2}} → {{spine_node_3}} → ...`

{{spine_rationale — 2–3 sentences explaining why this chain and not another}}

{{bulge_description — one sentence per bulge: "[Feature X] is a bulge off [Spine Node Y] — it needs [Y's output] but not [Z], so it can run in parallel with the rest of the spine once [Y] is live."}}

```mermaid
flowchart LR
    {{spine_node_1}}["{{Phase/Sprint label}}: {{Component name}}<br/>{{one-line job}}"]
    {{spine_node_2}}["..."]
    {{bulge_node_1}}["{{Phase label}} bulge: {{Feature name}}<br/>{{one-line job}}"]

    {{spine_node_1}} --> {{spine_node_2}}
    {{spine_node_1}} --> {{bulge_node_1}}

    style {{spine_node_1}} fill:#E3F2FD,color:#0D47A1
    style {{bulge_node_1}} fill:#E8F5E9,color:#1B5E20
```

**Spine nodes** (delay here delays everything): {{spine node list}}

**Bulge nodes** (unblocked when parent spine node completes): {{bulge node list with parent}}

```mermaid
gantt
    title {{idea_slug}} — Spine + Bulge Build Plan
    dateFormat YYYY-MM-DD
    axisFormat Phase %W

    section Spine
    {{spine_phase_1}} :p1, {{start_date}}, {{duration}}
    {{spine_phase_2}} :p2, after p1, {{duration}}

    section Bulge (parallel)
    {{bulge_phase_1}} :b1, after {{parent_phase}}, {{duration}}
```

**Parallelism rules:**
- {{Which tracks can run simultaneously and why}}
- {{What can never be parallelised with its upstream spine node and why}}

---

## Open Questions

{{numbered_open_questions}}

[Each item: question stated clearly, options named, what unblocks it.
If none exist, omit this section entirely — do not write "None."]
```
