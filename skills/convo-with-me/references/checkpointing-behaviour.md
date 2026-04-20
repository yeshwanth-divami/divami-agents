# Checkpointing Behaviour

## Trigger

| Command | Action |
|---|---|
| `!ckpt` | Write a checkpoint for the current thread. No confirmation needed. |
| `!ckpt load <keyword>` | Search front matter across `.claude/checkpoints/` for `<keyword>` and resume the matching thread. |

Also self-trigger a save if: the conversation is clearly getting large and multi-threaded, or Yeshwanth signals the convo might warrant a return visit.

---

## File Location

```
<project-root>/.claude/checkpoints/YYYYMMDDHHmm-<slug>.md
```

- `slug` = 2-4 word kebab-case label derived from the active thread (e.g. `daksh-api-design`, `checkpoint-system`)
- Timestamp-first so files sort chronologically by default. Run ./scripts/time-now.py to get the exact timestamp.
- One file per thread. Multiple `!ckpt` calls on the same thread overwrite the same file (update slug if thread shifted significantly).

---

## Format

```markdown
---
thread: <slug>
project: <basename of working directory>
summary: <one line — shown when surfacing multiple checkpoints>
---

## Goal
What we were trying to accomplish and why. 1-2 sentences.

## Context
- Key fact needed to avoid re-explaining (who is X, what constraint, what codebase rule)
- ...

## Decisions
- [what]: [why] — settled, do not re-propose

## Open
- [thread name]: [what's blocking or why tabled]

## Next
The agreed next step or mid-task position. Where to resume *from*.

## Resume
Written *to* the new LLM as a handoff note. 3-4 sentences.
"We were doing X. Yeshwanth wants Y next. Key thing to know: Z. Start by doing W."

---

## Working Set

### Files
- `path/to/file.py:42-87` — why this range matters

### Discoveries
- `ClassName.method()` at `path:line` — what it does and why it's relevant

### Dead Ends
- Tried X (e.g. grepped for `session_id`) — ruled out because Y (codebase uses `thread_id`)

### Artifacts
- Created `path/to/file.py` — what it does
- Modified `path/to/other.md` — what changed and why
```

---

## Two-Tier Philosophy

The checkpoint has two tiers:

- **Conversation state** (Goal → Resume): the *what* and *why* — restores intent and decisions
- **Working Set**: the *where* — restores expensive pointers so the new session doesn't re-explore

Together: bookmark + browser cache. Restores the tab, not just the URL.

Dead ends are load-bearing. Without them, the new LLM re-explores dismissed paths.

---

## Resuming

When Yeshwanth says something like "resume daksh discussion from yesterday":

1. Search checkpoints using the front-matter script:
   ```bash
   ./skills/convo-with-yeshwanth/scripts/read-md-front-matter.py \
     <project-root>/.claude/checkpoints/ --keyword <topic>
   ```
   This searches `thread`, `project`, and `summary` fields for the keyword.

2. If multiple matches, surface them as a short list:
   ```
   1. 202604141432-daksh-api-design.md — Designing REST endpoints for Daksh onboarding flow
   2. 202604141801-daksh-db-schema.md — Modelling the user/session tables for Daksh
   ```
3. He picks one (or it's obvious from context)
4. Read the file, prime from the `## Resume` section, then continue

Do not summarize the checkpoint back to him. Just enter the thread.
