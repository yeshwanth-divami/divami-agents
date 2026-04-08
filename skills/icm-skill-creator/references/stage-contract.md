---
name: stage-contract
description: How to write a stage contract — the CONTEXT.md file that defines a single stage's inputs, process, and outputs.
type: reference
---

# Stage Contracts

A stage contract is a `CONTEXT.md` file that answers three questions for the agent executing that stage:

1. **What do I load?** (Inputs)
2. **What do I do?** (Process)
3. **What do I write?** (Outputs)

It simultaneously functions as instructions and as pipeline documentation for humans.

---

## Anatomy

```markdown
# Stage N — <Name>

## Inputs

| Type | Path | Purpose |
|---|---|---|
| Layer 3 | references/<file>.md | <what constraint it provides> |
| Layer 4 | <path/to/artifact> | <what content it contains> |

## Process

<One paragraph. The single transformation this stage performs.
State what changes. State what must NOT change.>

### Constraints
- <Hard rule 1>
- <Hard rule 2>

## Outputs

| File | Format | Content |
|---|---|---|
| `<stage-folder>/<codename>.md` | Markdown (doc-narrator) | <what it contains> |

**Resumption artifact:** `<stage-folder>/<codename>.md` — written before yielding control.
Its `stage` and `status` frontmatter are the source of truth for resumption. No registry needed.
Write it following `references/intermediate-file-format.md`.

## Human Review Gate

<What the human should verify before the next stage runs.
What a bad output looks like. What to fix if it's wrong.
If the human edits the file, they must set `status: needs-review` — the skill will stop
and prompt for resolution before continuing.>
```

---

## Rules for Writing Stage Contracts

**Inputs section:**
- List only what this stage actually reads. Omit everything else.
- Distinguish Layer 3 (references/) from Layer 4 (working artifacts).
- Never list the same file in two stage contracts unless it truly is read by both.

**Process section:**
- One transformation per stage. If you need "and then", it's two stages.
- Name the transformation verb: extract, summarize, classify, structure, validate, generate.
- State invariants explicitly — what must NOT be modified.

**Outputs section:**
- One file per output slot. If a stage produces two files that serve different purposes, consider splitting the stage.
- Outputs of stage N become Layer 4 inputs of stage N+1.
- Every output file must follow `references/intermediate-file-format.md` — doc-narrator conventions with context seed, prose narrative, structured output, and open questions.
- The output file is also the completion marker. Its path must be declared explicitly. Never let the agent decide the path at runtime.

**Human Review Gate:**
- Every stage has one. Even if it's just "verify the output looks reasonable."
- Describe failure modes concretely, not abstractly.
- If the human edits the output file, they set `status: needs-review`. The skill must check this field and stop before the next stage if it is set.

---

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Stage reads 8 reference files | Split into sub-stages or merge references into one |
| Process section has "step 1... step 2... step 3..." | Each step is a stage |
| No human review gate | Add one — the whole point of ICM is human control |
| Output file is "whatever the agent decides" | Name it. Path it. Format it. |
