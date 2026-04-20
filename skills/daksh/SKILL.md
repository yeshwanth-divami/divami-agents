---
name: daksh
description: Run the Daksh product-delivery pipeline through explicit stage and command contexts, from onboarding and strategy docs through implementation, approvals, Jira sync, and handbook updates.
---

# Daksh

A numbered, stage-by-stage product development methodology. Each stage has a `CONTEXT.md` that defines a persona, clarifying questions, and the document structure to produce.

## On Startup

1. If the input matches a **command** (init, approve, preflight, tend, jira,
   `impl start TASK-[MODULE]-NNN`, `impl done TASK-[MODULE]-NNN`),
   load the corresponding `commands/*/CONTEXT.md`. Commands do not require
   a manifest to exist (init creates it; others check and fail gracefully).
2. Otherwise, identify the **stage** from input signals and load the
   corresponding `stages/*/CONTEXT.md`.
3. For any stage invocation, read `docs/.daksh/manifest.json` first.
   If it does not exist, stop: "No Daksh pipeline found. Run `/daksh init` first."
4. Read `manifest.rules` to determine weight class behavior (approvals
   required, combined stages, open questions policy).

## Routing

### Commands

| Input signal | Load |
|---|---|
| init / initialize / set up pipeline | `commands/init/CONTEXT.md` |
| approve [stage] [module] | `commands/approve/CONTEXT.md` |
| preflight [stage] [module] | `commands/preflight/CONTEXT.md` |
| change / cr [MODULE] | `commands/change/CONTEXT.md` |
| tend / health check / audit | `commands/tend/CONTEXT.md` |
| jira [push\|pull\|sync\|status] | `commands/jira/CONTEXT.md` |
| handbook [section] | `commands/handbook/CONTEXT.md` |

### Stages

| Command | Input signal | Load |
|---|---|---|
| `onboard` | client onboarding / new project | `stages/00-client-onboarding/CONTEXT.md` |
| `vision` | vision / what are we building | `stages/10-vision/CONTEXT.md` |
| `brd` | business requirements / BRD | `stages/20-business/CONTEXT.md` |
| `roadmap` | roadmap / build sequence | `stages/30-roadmap/CONTEXT.md` |
| `prd` | module PRD / product spec | `stages/40a-prd/CONTEXT.md` |
| `trd` | module TRD / technical spec | `stages/40b-trd/CONTEXT.md` |
| `tasks` | module tasks / task breakdown | `stages/40c-tasks/CONTEXT.md` |
| `impl start TASK-ID` | start a task — git branch + time block | `commands/impl/CONTEXT.md` |
| `impl done TASK-ID` | complete a task — ACs + PR + Jira | `commands/impl/CONTEXT.md` |
| `impl` | implementation stage context | `stages/50-implementation/CONTEXT.md` |

## ⛔ Git Commit / Push Rule — Non-Negotiable

**Never run `git commit`, `git push`, or any destructive git operation
(`git reset`, `git rebase`, `git merge`, `git branch -d`, etc.) unless one
of the following is true:**

1. **Explicit ask** — the user's message directly requests a commit or push
   (e.g. "commit this", "push to origin", "git commit -m …").
2. **Implicit Daksh command** — the Daksh workflow being executed has a commit
   or push step built into its `CONTEXT.md` (e.g. `impl start`, `impl done`,
   `approve`). In that case, only the specific git operations listed in that
   command's context are permitted.

Outside these two conditions, **no git write operations may be performed**,
even if they "clean up" something, "fix" a manifest, or "complete" a task.
File edits are fine; committing them is not.

Violating this rule is a critical workflow failure. The user owns the git
history. The LLM does not commit on their behalf unless invited.

## Command Execution Rule

When the user invokes a concrete command such as `/daksh impl start TASK-[MODULE]-NNN`,
execute the command workflow in its command `CONTEXT.md` before doing the task's
implementation work. Do not reinterpret `impl start` as a generic request to work on
the task. For `impl start`, local edits begin only after preflight, branch setup,
Jira transition, and time-block start have all succeeded or the command context says
to stop.

### Supplementary

| Input signal | Also load |
|---|---|
| python code | `references/python-guidelines.md` |
| typescript / JS code | `references/typescript-guidelines.md` |

## Stages

| # | Command | Stage | Context | Output |
|---|---------|-------|---------|--------|
| 00 | `onboard` | Client Onboarding | `stages/00-client-onboarding/CONTEXT.md` | `docs/client-context.md` |
| 10 | `vision` | Vision | `stages/10-vision/CONTEXT.md` | `docs/vision.md` |
| 20 | `brd` | Business Requirements | `stages/20-business/CONTEXT.md` | `docs/business-requirements.md` |
| 30 | `roadmap` | Roadmap | `stages/30-roadmap/CONTEXT.md` | `docs/implementation-roadmap.md` + Jira epics/sprints/stories |
| 40a | `prd` | Module PRD | `stages/40a-prd/CONTEXT.md` | `docs/implementation/[MODULE]/prd.md` |
| 40b | `trd` | Module TRD | `stages/40b-trd/CONTEXT.md` | `docs/implementation/[MODULE]/trd.md` |
| 40c | `tasks` | Module Tasks | `stages/40c-tasks/CONTEXT.md` | `docs/implementation/[MODULE]/tasks.md` |
| 50 | `impl` | Implementation | `stages/50-implementation/CONTEXT.md` | Feature branches + code + change records |
| 60 | `handbook` | Handbook | `stages/60-handbook/CONTEXT.md` | `handbook/*.md` |

## Commands

| Command | Context | Purpose |
|---------|---------|---------|
| init | `commands/init/CONTEXT.md` | Create manifest, set weight class, scaffold dirs |
| approve | `commands/approve/CONTEXT.md` | Structured approval with doc hash + roster validation |
| preflight | `commands/preflight/CONTEXT.md` | Pre-stage validation: skills, gates, context budget |
| change | `commands/change/CONTEXT.md` | Raise a change record when implementation reality diverges from spec |
| tend | `commands/tend/CONTEXT.md` | Health audit: orphans, contract drift, stale docs |
| jira | `commands/jira/CONTEXT.md` | Bidirectional Jira sync: push, pull, sync, status |
| handbook | `commands/handbook/CONTEXT.md` | Patch or rebuild a handbook section |
| impl | `commands/impl/CONTEXT.md` | Task lifecycle: branch, ACs, PR, Jira transition |

## References

| Need | Read |
|---|---|
| Manifest schema | `references/manifest-schema.md` |
| Manifest template | `templates/manifest-template.json` |
| Python env + copilot rules | `references/python-guidelines.md` |
| TypeScript/JS conventions | `references/typescript-guidelines.md` |

## Handbook Rule

When writing or patching `handbook/*.md`, prefer topic-oriented `##` sections
over generic buckets. For LLM-operated systems such as Vyasa skills, document a
script or module in terms of purpose, invariants, boundaries, downstream
dependencies, and safe extension points before describing any manual command.

## Vyasa Rendering Rule

When a Daksh document includes a process flow, dependency chain, stage sequence,
 or any arrow-based structure, render it as a Mermaid diagram instead of ASCII
 art or plaintext arrows. Use prose before the diagram, and use Mermaid labels
 that follow Vyasa rules such as literal `<br/>` for multiline node text.

## The Zen of Daksh

> Docs are read by deaf ears and blind eyes.
> Give context at every junction.

> The document you wrote yesterday is already lying to someone.

> Structure without narrative is a skeleton without a body.

> Every enumeration deserves a "why these and nothing else."

> The baton carries no conversation. Write as if you won't be there.

> A polished wrong document is more dangerous than a rough right one.

> If you can't explain why, don't explain what.

> The decision is the artifact. The document is its trace.

> Unvalidated assumptions dressed as decisions are kindling.

> Write for the junior reading this cold at 11pm.
> If they can follow it, the senior will too.
