# Divami Agents

Divami Agents is a Python package and skill workspace for installing reusable agent skills into the folders that Claude, Codex, Gemini, and Copilot already watch. The repo carries three things together: the shipping CLI and TUI under `src/divami_skills/`, the source skill library under `skills/`, and supporting docs for the people who use, operate, and extend the tool. If you are opening this repo cold, the important model is simple: skill sets are discovered from disk, then linked into assistant-specific global or repo-local folders. By the end of this README, you should know which handbook to open next and where the shipped skills live.

Choose the handbook that matches the job in front of you:

- [handbook/end-user.md](handbook/end-user.md) is the quickest path if you want to open the TUI and install skills.
- [handbook/ops.md](handbook/ops.md) covers workstation setup, packaging, and release operations.
- [handbook/developer.md](handbook/developer.md) explains how the CLI, manager layer, and TUI fit together.
- [handbook/admin.md](handbook/admin.md) covers path overrides, skill-set registration, and repo-local policy files.

One repo detail matters before you go deeper: the runtime installs from skill sets on disk, and this repository's packaged source of truth is the top-level [`skills/`](skills) directory. The parallel [`agents/`](agents) tree exists in the repo, but the current packaging and install path described in the handbooks runs through `skills/`, `scripts/pack.py`, and `src/divami_skills/`.

| Skill | Description |
| --- | --- |
| [cleanup-and-refactor](skills/cleanup-and-refactor/SKILL.md) | Cleans up working feature code after iterative chat-driven development. Use when code now works but contains dead paths, duplicate logic, or refactor debt from back-and-forth implementation. Produces a narrowed cleanup plan, one verification pass, and a commit-ready summary. |
| [code-refactoring](skills/code-refactoring/SKILL.md) | Use when the user wants to refactor an existing codebase without rewriting large amounts of already-solved logic. Invoke when reducing slop, extracting shared modules, deduplicating behavior, tightening boundaries, reusing existing code patterns, or turning copy-paste candidates into canonical services. |
| [code-review](skills/code-review/SKILL.md) | Run a comprehensive code review |
| [daksh](skills/daksh/SKILL.md) | Structured product development lifecycle workflow using numbered AI chat modes. Use when building a new product or feature from scratch, onboarding a new client project, writing vision/business/roadmap documents, defining module PRDs and TRDs, breaking work into dev tasks, or implementing tasks with Git workflow. Invoke for any phase client onboarding → vision → business requirements → roadmap → module PRD → module TRD → module tasks → implementation. |
| [doc-narrator](skills/doc-narrator/SKILL.md) | Narrative writing skill for technical documentation. Writes context seeds, prose-first sections, open questions, inline links, and 'Why?' tables for any technical document. Output targets Vyasa. Use standalone when writing or reviewing any technical doc, or invoked by grove as its writing layer. |
| [find-skills](skills/find-skills/SKILL.md) | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill. |
| [gws-chat](skills/gws-chat/SKILL.md) | Google Chat: Manage Chat spaces and messages. |
| [gws-chat-send](skills/gws-chat-send/SKILL.md) | Google Chat: Send a message to a space. |
| [gws-classroom](skills/gws-classroom/SKILL.md) | Google Classroom: Manage classes, rosters, and coursework. |
| [gws-docs](skills/gws-docs/SKILL.md) | Read and write Google Docs. |
| [gws-docs-write](skills/gws-docs-write/SKILL.md) | Google Docs: Append text to a document. |
| [gws-gmail](skills/gws-gmail/SKILL.md) | Gmail: Send, read, and manage email. |
| [gws-gmail-read](skills/gws-gmail-read/SKILL.md) | Gmail: Read a message and extract its body or headers. |
| [gws-gmail-triage](skills/gws-gmail-triage/SKILL.md) | Gmail: Show unread inbox summary (sender, subject, date). |
| [gws-gmail-watch](skills/gws-gmail-watch/SKILL.md) | Gmail: Watch for new emails and stream them as NDJSON. |
| [gws-meet](skills/gws-meet/SKILL.md) | Manage Google Meet conferences. |
| [gws-shared](skills/gws-shared/SKILL.md) | gws CLI: Shared patterns for authentication, global flags, and output formatting. |
| [icm-skill-creator](skills/icm-skill-creator/SKILL.md) | Creates new Claude Code skills that strictly follow the Interpretable Context Methodology (ICM) — filesystem-based, progressively discloseable, staged workflows. Interviews the user (up to 5 questions), then scaffolds a complete ICM-compliant skill directory. Use when creating any new skill or restructuring an existing one to be ICM-compliant. |
| [jira-access](skills/jira-access/SKILL.md) |  |
| [lit-parse](skills/lit-parse/SKILL.md) | Convert documents (DOCX, PDF, XLSX, PPTX, images) to text/markdown files using the `lit` CLI tool. Use when the user wants to batch-convert or individually parse documents into readable text or markdown format. |
| [minutes-of-meeting](skills/minutes-of-meeting/SKILL.md) | Use when the user wants to process one or more meeting transcript files into minutes of meeting (MOM). Invoke when the user asks to summarize a meeting, create MOM notes, capture action items, write up a standup or sprint planning session, or document decisions from any conversation transcript. |
| [retrospect-and-update-skill](skills/retrospect-and-update-skill/SKILL.md) | Analyze the current chat after retries, false starts, or repeated corrections. Use when Codex needs to identify which false assumptions caused wasted work, extract the correct execution patterns discovered later in the thread, and update the implicated skill files so future runs start with the corrected workflow. |
| [tech-feasibility](skills/tech-feasibility/SKILL.md) | Given a tech idea (1–3 sentences), probes scope through iterative Q&A batches, presents a doc outline for confirmation, then writes a feasibility analysis following doc-narrator conventions. Invoke when the user describes a tech idea and wants to understand how to build it. |
| [use-cases](skills/use-cases/SKILL.md) | Excavate a use case from a finished project's artifacts (code, docs, transcripts) and produce a publishable narrative through gated stages. Invoke from within a project repo. |
