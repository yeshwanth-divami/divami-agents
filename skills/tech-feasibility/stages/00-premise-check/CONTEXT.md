# Stage 0 — Premise Check

> Extract and assess the assumptions baked into the raw idea before any scope probing begins.

---

## Inputs

| Type | Path | Purpose |
|---|---|---|
| Layer 3 | `references/premise-check-guide.md` | Assumption types, assessment criteria, verdict rules, reframe format |
| Layer 4 | `templates/premise-check.md` | Output table template with placeholders |
| Layer 4 | User's idea text (from conversation) | The raw idea being assessed |

*Do not load probing-guide.md, doc-structure.md, or any write-phase references at this stage.*

---

## Process

Read the idea and the premise-check guide. Extract all assumptions — domain, technical, and competitive. Include both explicit claims and implicit ones (things the idea takes for granted without stating).

Assess each assumption as solid, questionable, or false using the criteria in the guide. Write one honest reason per row. Do not hedge false assumptions.

Apply the verdict rules from the guide:
- All solid → state briefly, proceed to Phase 1 immediately without waiting for user input
- Any questionable or false → present the table, state the verdict, offer the three options, wait

If a reframe is warranted, write it using the format in the guide: what to build instead, what it preserves, what broken premise it sidesteps.

### Constraints

- Do not soften false assumptions. "This is false because X" is required. "May need revisiting" is not acceptable.
- Do not flag implementation unknowns as false premises — those belong in Phase 1 probing.
- Do not generate scope questions in this stage. Phase 0 is premise-only.
- Do not write any part of the feasibility doc. This stage produces a premise table and verdict, nothing else.
- The reframe must be a concrete, narrower idea — not a vague "consider scoping this down."

---

## Outputs

| Content | Format | What it contains |
|---|---|---|
| Premise check (presented in chat) | Filled `templates/premise-check.md` | Assumption table, verdict, optional reframe, three options |
| `tech-feasibility-analyses/<codename>/premise.md` | Markdown (doc-narrator) | Written when user proceeds (Option 1 or 2) or all assumptions solid |

The `tech-feasibility-analyses/<codename>/premise.md` file follows the intermediate file format: frontmatter with `skill: tech-feasibility`, `codename`, `stage: premise`, `status: complete`; a context seed; prose narrative of what the premise check found; the assumption table in the Output section; and any unresolved assumptions in Open Questions.

Write this file **after** the user's choice is made (or immediately if all assumptions are solid). Do not write it if the user stops (Option 3).

When writing `premise.md`, also create the Vyasa ordering files if they don't exist:
- `tech-feasibility-analyses/<codename>/.vyasa` — always write alongside `premise.md`
- `tech-feasibility-analyses/.vyasa` — write only if it does not already exist

See SKILL.md § Stage Folders for the exact TOML content of both files.

---

## Human Review Gate

**If all assumptions are solid:** No gate. Write `tech-feasibility-analyses/<codename>/premise.md`. Proceed to Phase 1.

**If any assumptions are questionable or false:** Wait for explicit user choice:
- Option 1 (reframe) → re-run Phase 0 on the reframed idea; write `tech-feasibility-analyses/<codename>/premise.md` after reframe accepted
- Option 2 (proceed anyway) → write `tech-feasibility-analyses/<codename>/premise.md` with shaky assumptions in Open Questions; move to Phase 1
- Option 3 (stop) → end the session; do not write any file

**A non-response or "yeah let's continue" counts as Option 2.** Do not re-present the premise check unless the user asks.
