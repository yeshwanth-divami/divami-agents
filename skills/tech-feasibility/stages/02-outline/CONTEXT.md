# Stage 2 — Outline

> Synthesise probing answers into a compact doc plan and present it for human confirmation before writing begins.

---

## Inputs

| Type | Path | Purpose |
|---|---|---|
| Layer 3 | `references/doc-structure.md` | The required sections and what each must contain |
| Layer 4 | `templates/outline.md` | The outline template with placeholders to fill |
| Layer 4 | Conversation history from Stage 1 | The confirmed scope — answers to all five dimensions |

*Do not load doc-narrator-rules.md at this stage. That is for Stage 3.*

---

## Process

Read the probing answers from the conversation and the doc-structure reference. Fill every placeholder in the outline template. Every section listed in the outline must correspond to a section in doc-structure.md. Do not invent new sections; do not omit required ones unless the scope explicitly makes a section irrelevant (e.g., no AI — then "Where AI adds value" becomes something else).

Name the specific challenges that will appear in "What is hard" — derive these from the probing answers, not from imagination. If a dimension answer implied a hard constraint (e.g., voice-only → no typing → different latency budget), name it in the outline.

State all assumptions explicitly — any dimension not fully answered where a default will be used.

Write the filled outline to `tech-feasibility-analyses/<codename>/outline.md` immediately — do not print it in chat. Then tell the user the file path and end with: "Review `tech-feasibility-analyses/<codename>/outline.md` — confirm to proceed, or steer any section before I write."

### Constraints

- Do not write any part of the feasibility doc in this stage. The outline is a plan, not a draft.
- Do not add sections that are not in doc-structure.md unless the idea clearly requires one (name why).
- Every challenge named in "What is hard" must be derivable from a probing answer or a well-known constraint of the domain. Do not invent challenges.
- State assumptions clearly — do not silently default.

---

## Outputs

| Content | Format | What it contains |
|---|---|---|
| `tech-feasibility-analyses/<codename>/outline.md` | Markdown (doc-narrator) | Written immediately before asking for confirmation; updated in-place if user steers a section |

The file follows the intermediate file format: frontmatter with `skill: tech-feasibility`, `codename`, `stage: outline`, `status: needs-review`; a context seed; prose narrative of what the probing established and what the outline commits to; the confirmed outline in the Output section; and any open scope decisions in Open Questions.

**Never print the outline in chat.** Write the file, state the path, ask for confirmation.

---

## Human Review Gate

**The user must confirm before Stage 3 begins.**

**Verify the outline contains:**
- Confirmed scope bullets matching what was actually said in probing (not inferred)
- Named challenges (not "various technical challenges")
- Named outputs in the Why? table row

**If the user steers a section:** Edit `outline.md` in-place. Tell the user what changed and which line. Do not reprint the outline in chat. Do not proceed to Stage 3 until the user explicitly confirms.
