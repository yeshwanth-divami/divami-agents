---
name: workspace-scaffold
description: Base template for the SKILL.md of any new ICM-compliant skill. Fill in all {{placeholders}} before writing the file.
type: template
---

# Template: SKILL.md for a new ICM skill

Replace all `{{placeholders}}` with values from the interview. Do not leave any placeholders unfilled in the output file.

---

```markdown
---
name: {{skill_name}}
description: {{one_sentence_description}}. {{trigger_conditions}}. {{output_description}}.
argument-hint: "{{argument_hint}}"
allowed-tools: {{tools_list}}
---

# {{Skill Display Name}}

{{One paragraph: what this skill does, who it's for, and the core transformation it performs.}}

---

## Core Principle

> {{The single most important constraint or philosophy for this skill — 1–2 sentences.}}

---

## The Zen of {{Skill Display Name}}

```
{{5–10 lines. Write these LAST, after the entire skill is designed.
Each line is one belief the skill holds — short, declarative, opinionated.
No filler. No "be good". Every line should make someone nod or argue.
Derive them from the skill's actual constraints and tradeoffs, not platitudes.}}
```

---

## On Startup

{{What to read first. Usually: "Read `references/{{primary_reference}}.md` before doing anything else."}}

---

## Workflow

{{Numbered phases. Each phase is one human-reviewable step.
Use the interview answers to determine how many phases and what each does.
Do not include more phases than the skill genuinely needs.}}

### Phase 1 — {{Phase Name}}

{{What the agent does in this phase. What it reads. What it produces or asks.}}

### Phase 2 — {{Phase Name}}

{{...}}

---

## Output Rules

- {{Rule 1 specific to this skill's outputs}}
- {{Rule 2}}
- {{Rule 3}}

---

## Reference Files

| Need | Read |
|---|---|
{{| {{what you need}} | `references/{{filename}}.md` |}}
{{| {{what you need}} | `templates/{{filename}}.md` |}}

---

## Routing

| Input signal | Load |
|---|---|
{{| {{signal description}} | `references/{{file}}.md` |}}
{{| {{signal description}} | `templates/{{file}}.md` |}}
```
