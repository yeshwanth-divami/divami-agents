# Refactor Playbook

## Heuristics

- Duplicate logic across runtime and build paths usually wants a shared service.
- Import-time logging, config mutation, or browser opening usually belongs in bootstrap code.
- A config module should not import from a higher-level web or rendering module.
- If one file mixes parsing, routing, auth, caching, and rendering, split by responsibility, not by line count.
- Fewer lines are usually better only when they also reduce concepts, branches, and maintenance burden.

## Canonical extraction patterns

### Shared policy extraction

- Move inclusion, traversal, filtering, and path policy into one pure module.
- Keep rendering-specific code in callers.
- Feed the shared module plain values, not framework objects.

### Mechanical reuse first

- Copy the exact implementation only as a temporary extraction step, then converge callers onto one owner.
- Prefer moving the canonical implementation and updating imports over recreating it from scratch.
- If only names or paths differ, use text transforms instead of manual rewriting.
- If only one branch differs, extract the common body and parameterize the delta.

### Negative code with guardrails

- Prefer deleting dead paths, duplicate branches, and obsolete wrappers before adding new structure.
- Measure success by net complexity reduction, not just raw line count.
- A shorter implementation is worse if it hides policy, compresses readability, or makes validation harder.
- The best refactor often deletes one implementation, keeps one canonical implementation, and adds little or no new code.

### Runtime boundary cleanup

- Keep `main.py` or entrypoints responsible for process wiring.
- Keep content modules import-safe.
- Move side effects behind explicit functions.

### Duplication reduction

- Extract common code only after confirming the behaviors are intended to stay aligned.
- If two implementations differ for a reason, make the variation explicit with parameters.
- If they differ accidentally, unify now.

## Anti-patterns

- Creating a `utils.py` sink.
- Splitting a god file into many vague helper files.
- Building a service layer that only forwards arguments.
- Renaming aggressively before behavior is centralized.
- Leaving the old duplicate in place “temporarily” without a deletion checkpoint.
- Manually retyping code that already exists elsewhere in the repo.
- Generating a fresh abstraction before checking whether a mechanical move solves it.
- Chasing lower LOC by introducing clever one-liners, implicit behavior, or unreadable indirection.
- Keeping all features but weakening maintainability just to make the diff smaller.

## Good first modules

- `assets.py`
- `tree_service.py`
- `metadata.py`
- `bootstrap.py`
- `auth.py`
- `navigation.py`

## Mechanical tool guide

- Use `rg` to find all copies, callers, and import sites before editing.
- Use `sed` for line-oriented import and symbol rewrites.
- Use `awk` when you need to report or extract structured text from repeated patterns.
- Use `perl -0pi` for multiline transforms across a file.
- Use `cp` or `mv` when an existing file is the canonical implementation and ownership should change.
- Use `apply_patch` for exact block extraction, compatibility wrappers, and cleanup.

### Tool boundary

- `apply_patch` is available inside Codex, not as a shell binary.
- In a normal terminal session, reach for `sed`, `awk`, `perl`, `cp`, `mv`, `diff`, and occasional `python -c` instead.
- Do not waste time trying to run Codex tool names from `zsh`.

## Refactor sequence heuristic

1. Find the canonical implementation.
2. Move or extract it.
3. Redirect one caller mechanically.
4. Validate.
5. Redirect remaining callers mechanically.
6. Delete the duplicate.

## Validation ladder

1. Import/compile check
2. Narrow unit or snapshot test
3. Caller-level smoke test
4. Full app test only if the seam touches startup or routing
