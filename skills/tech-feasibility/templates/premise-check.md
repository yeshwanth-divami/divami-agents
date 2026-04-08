---
name: premise-check
description: Template for the Phase 0 premise check output. Fill all placeholders. Presented to the user before any scope probing begins.
type: template
---

# Template: Premise Check Output

Fill every placeholder. Present in chat — no file is written at this stage.

---

```
## Premise Check — {{idea_slug}}

Before we scope this out, here are the assumptions baked into the idea and whether they hold.

| Assumption | Status | Why |
|---|---|---|
| {{assumption_1}} | {{Solid / Questionable / False}} | {{one-line reason}} |
| {{assumption_2}} | {{Solid / Questionable / False}} | {{one-line reason}} |
| {{assumption_3}} | {{Solid / Questionable / False}} | {{one-line reason}} |
[...add rows as needed — include all assumptions extracted, not just the problematic ones...]

---

**Verdict:** {{one or two sentences. Plain language. If something is broken, say what and why.
If all solid, say "Premises look sound — moving to scope questions." and stop here.}}

{{IF any false or 2+ questionable — include the following block:}}

**Reframe option:** Instead of {{original idea phrasing}}, consider: {{narrower idea that sidesteps the broken premise}}. This preserves {{the useful core}} without requiring {{the broken premise}}.

---

How do you want to proceed?
1. **Reframe** — use the suggested reframe above (or propose your own)
2. **Proceed anyway** — continue with the original idea; shaky assumptions will be documented as risks
3. **Stop** — the idea needs more thinking before we go further
```
