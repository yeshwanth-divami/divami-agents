---
name: code-refactoring
description: Refactor code by finding the canonical existing implementation, choosing the smallest safe seam, and extracting or redirecting behavior instead of rewriting solved logic from scratch.
---

# Code Refactoring

## Table of Contents

- [Read This First](#read-this-first)
- [Workflow](#workflow)
- [Step 1: Find the Real Slop Source](#step-1-find-the-real-slop-source)
- [Step 2: Identify the Canonical Implementation](#step-2-identify-the-canonical-implementation)
- [Step 3: Choose the Smallest Safe Seam](#step-3-choose-the-smallest-safe-seam)
- [Mechanical Editing Moves](#mechanical-editing-moves)
- [Editing Context Matters](#editing-context-matters)
- [Step 4: Extract or Redirect, Do Not Rewrite](#step-4-extract-or-redirect-do-not-rewrite)
- [Step 5: Lock Behavior with Validation](#step-5-lock-behavior-with-validation)
- [Rules](#rules)
- [Output Expectations](#output-expectations)

## Read This First

Use this skill when the goal is to improve structure while preserving behavior.

This skill is for refactors where the main risk is wasting effort by rewriting code that already exists somewhere else in the repo. The default move is to find the best existing implementation, extract it cleanly, and redirect callers with the smallest possible change set.

The workflow is collaborative when there is more than one plausible canonical source or more than one safe seam. In those cases, present 2-4 options with tradeoffs and let the user choose the direction.

## Default stance

- Prefer extraction over rewrite.
- Prefer reusing an existing good pattern over inventing a new one.
- Treat duplicated behavior as a design signal.
- Keep refactors incremental and reviewable.
- Protect behavioral equivalence before optimizing aesthetics.
- Prefer mechanical edits over retyping.
- Prefer net code reduction when it does not cost features, quality, or maintainability.

## Negative code principle

The goal is not just cleaner code. The goal is less code, fewer branches, and fewer moving parts, but only when that reduction preserves or improves:

- feature coverage
- correctness
- readability
- maintainability
- validation confidence

Use "negative code" as a pressure toward deletion, convergence, and simplification. Do not use it to justify dense cleverness, hidden coupling, or under-explained shortcuts.

## Token-saving decision ladder

Use this order before generating fresh code:

1. Reuse exact existing code.
2. Move or extract existing code.
3. Redirect callers to existing code.
4. Parameterize a small variation on existing code.
5. Wrap existing code with a compatibility shim.
6. Generate new code only if no canonical implementation exists.

If steps 1-5 are viable, do not re-derive the implementation from scratch.
Prefer the option that removes more duplicated or unnecessary code, but reject it if it weakens feature support, testability, or future readability.

## Workflow

**COPY THIS CHECKLIST** and work through each step:

```text
Code Refactoring Workflow
- [ ] Step 1: Find the real slop source
- [ ] Step 2: Identify the canonical implementation
- [ ] Step 3: Choose the smallest safe seam
- [ ] Step 4: Extract or redirect, do not rewrite
- [ ] Step 5: Lock behavior with validation
```

## Step 1: Find the real slop source

Look for:

- duplicate logic with drift
- upward imports and circular convenience dependencies
- god modules mixing unrelated concerns
- runtime side effects at import time
- route/view/build logic reimplementing the same policy
- noisy helper layers that hide simple behavior

Start by naming the slop precisely: duplication, coupling, boundary leak, oversized module, hidden side effect, or dead abstraction.

User choice point:

- If the slop source is ambiguous, present the top 2-3 interpretations and explain which one you would attack first.

## Step 2: Identify the canonical implementation

Before writing code, find the best existing version of the behavior.

- If two modules do the same thing, pick the one with fewer side effects and clearer inputs.
- If no implementation is clean, pick the one closest to production behavior and extract from there.
- If the repo already has a good shape elsewhere, adapt that shape instead of inventing a new API.
- If the code already exists but lives in the wrong place, prefer moving it over rewriting it.

See [references/refactor-playbook.md](references/refactor-playbook.md).

User choice point:

- If two implementations are both viable, explain which one is more canonical and why.
- If neither is clearly canonical, recommend a temporary owner and say what validation will confirm it.

## Step 3: Choose the smallest safe seam

Good first seams:

- pure helper extraction
- shared service extraction
- config/runtime boundary cleanup
- moving side-effectful startup code into entrypoints
- replacing duplicate traversal/path logic with one canonical function

Avoid starting with:

- full package reshuffles
- renaming everything at once
- speculative abstraction layers
- big-bang rewrites of giant modules

User choice point:

- If there are several seams, rank them by impact, safety, and churn before editing.
- Prefer the seam that collapses the most duplicate or unnecessary code per unit of risk.

## Mechanical editing moves

Prefer operations like these before writing new code:

- exact block extraction into a new module
- import rewrites to redirect callers
- function wrapping for compatibility during migration
- parameterizing small behavior differences
- deleting duplicate branches after convergence
- line-oriented search and replace for names, imports, and paths
- moving existing modules or files into clearer ownership boundaries

Useful command patterns:

- `rg` to find all canonical and duplicate implementations
- `sed` for simple line-based rewrites
- `awk` for structured extraction or report generation
- `perl -0pi` for multiline replacements when line tools are too weak
- `cp` and `mv` for promoting an existing implementation into shared ownership
- `apply_patch` for exact block moves, deletions, and shims

Prefer `apply_patch` when edits must be precise or reviewable. Prefer `sed` or `perl` when many near-identical changes are mechanical.

## Editing context matters

Distinguish between Codex-only tools and shell-native commands.

### Codex editing tools

- `apply_patch` is a Codex tool, not a terminal command.
- Use it for exact block edits, compatibility shims, deletions, and reviewable extractions.
- Prefer it when the change is surgical and should remain easy to inspect.

### Shell-native refactor commands

- `sed -i` for line-oriented import, symbol, and path rewrites
- `awk` for extracting or reporting repeated structures
- `perl -0pi -e` for multiline substitutions
- `cp`, `mv`, and `diff -u` for moving canonical code and comparing before/after
- `python -c` only when the text transform is structured enough that line tools are unsafe

If working directly in the user's shell, do not suggest `apply_patch` as a terminal command. Suggest shell-native commands instead.

## Step 4: Extract or redirect, do not rewrite

Preferred order:

1. Create the shared unit.
2. Redirect one caller.
3. Validate behavior.
4. Redirect the second caller.
5. Delete the duplicate.

When possible, preserve signatures at the call site first and improve API shape second.
If a caller can be updated with a search-and-replace plus import rewrite, do that instead of hand-retyping the body.

User choice point:

- If the refactor can be done by either extraction or parameterization, state the tradeoff and prefer the option with lower behavioral risk.

## Step 5: Lock behavior with validation

Use the cheapest validation that proves equivalence:

- existing tests
- snapshot comparisons
- compile/import checks
- before/after output diffs
- targeted manual smoke tests

If tests are weak, add narrow regression coverage around the extracted seam before bigger decomposition.
Negative code only counts as a win after the smaller implementation is validated against the same behavior expectations.

## Rules

- Do not rewrite 90% identical code if 10% extraction solves it.
- Do not move code across boundaries until the target boundary is named.
- Do not create a new abstraction unless at least two callers benefit now.
- Do not leave both old and new policy paths alive longer than necessary.
- Prefer boring names like `tree_service.py`, `assets.py`, `bootstrap.py`, `auth.py` over clever names.
- Treat text-editing commands as first-class refactoring tools, not as a last resort.
- If a transformation is mechanical, perform it mechanically.
- Use generation for missing logic, not for code that already exists elsewhere in the repo.
- Prefer deletion over extraction if the code is unnecessary.
- Prefer convergence over new abstractions if multiple paths can become one.
- Treat lines of code as carrying maintenance cost, but never trade away features, quality, or maintainability just to reduce line count.
- Reject "negative code" changes that make the code denser, less legible, or harder to validate.

## Output expectations

When using this skill:

1. State the slop source in one sentence.
2. Name the canonical implementation or target seam.
3. Propose 2-4 refactor options if the path is not obvious.
4. Execute the smallest high-leverage step first.
5. Tell the user how to validate before continuing into the next chunk.
6. If a decision was made, record why that option beat the alternatives.
