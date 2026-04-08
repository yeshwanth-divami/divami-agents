---
description: "Patch or rebuild a handbook section. Runs automatically after approve impl; call directly to fix tend flags."
---

# Command: /daksh handbook

## Syntax

```
/daksh handbook [section]
```

`section`: optional — `end-user` · `admin` · `ops` · `developer`

- With section: patch that file only.
- Without section: patch all sections that tend flagged as missing or drifted.

## Steps

1. Read `docs/.daksh/manifest.json` to identify completed modules.
2. For each target section, collect inputs:
   - All `docs/implementation/[MODULE]/tasks.md` — filter tasks by audience signals (mapping below)
   - Relevant `trd.md` and `prd.md` sections for those tasks
   - Existing `handbook/[section].md` if present — patch it, do not overwrite unrelated content
3. Write or update `handbook/[section].md` using topic-oriented `##` sections from `stages/60-handbook/CONTEXT.md`.
4. Commit: `docs(manual): update [section] — [TASK-IDs that triggered this]`

For `end-user`, synthesize by journey, not by task cluster. Merge related task
signals into one role-based flow so the reader sees the next command, success
state, and blocked-state recovery in one place.

## Audience signal mapping

| Task signals (anywhere in summary or description) | Section |
|---|---|
| ui, ux, screen, frontend, form, dashboard, view, component, user flow | `end-user.md` |
| config, setting, env, permission, access control, role, flag, toggle | `admin.md` |
| deploy, docker, infra, ci, cd, migration, install, rollback, monitor, log | `ops.md` |
| scaffold, api, test, refactor, architecture, integration, sync, extend, cli | `developer.md` |

A task can match multiple sections — patch all that apply.

## Rules

- **Patch mode** (file exists): add or update only the topic sections relevant to the tasks being processed. Do not touch unrelated sections.
- **Write mode** (file absent): create a minimal audience-specific skeleton with topic sections that fit the implemented behavior; do not stub generic headings just to satisfy a template.
- Quality bar is defined in `stages/60-handbook/CONTEXT.md` — apply it on every write.
- Do not run this command if no module has reached stage 50. Manual content without implemented behaviour is fiction.
- For LLM-operated systems, document why a script or file exists, what contract it enforces, and what depends on it before describing any human-invoked command.
- Do not let task-to-section mapping fragment a single user workflow across
  multiple pages. If the reader's question is "what do I do next?", answer it
  before adding conceptual deep links.
