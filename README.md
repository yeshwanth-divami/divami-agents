# Divami Agents

Divami Agents is a [Python package](https://github.com/yeshwanth-divami/divami-agents) and skill workspace for installing reusable agent skills into the folders that Claude, Codex, Gemini, and Copilot already watch. The repo carries three things together: the shipping CLI and TUI under `src/divami_skills/`, the source skill library under `skills/`, and supporting docs for the people who use, operate, and extend the tool. If you are opening this repo cold, the important model is simple: skill sets are discovered from disk, then linked into assistant-specific global or repo-local folders. By the end of this README, you should know which handbook to open next and where the shipped skills live.

Choose the handbook that matches the job in front of you:

- [handbook/end-user.md](handbook/end-user.md) is the quickest path if you want to open the TUI and install skills.
- [handbook/ops.md](handbook/ops.md) covers workstation setup, packaging, and release operations.
- [handbook/developer.md](handbook/developer.md) explains how the CLI, manager layer, and TUI fit together.
- [handbook/admin.md](handbook/admin.md) covers path overrides, skill-set registration, and repo-local policy files.

One repo detail matters before you go deeper: the runtime installs from skill sets on disk, and this repository's packaged source of truth is the top-level [`skills/`](skills) directory. The parallel [`agents/`](agents) tree exists in the repo, but the current packaging and install path described in the handbooks runs through `skills/`, `scripts/pack.py`, and `src/divami_skills/`.

Following are the skills currently included in the repo and their purposes.

| Skill | Description |
| --- | --- |
| [cleanup-and-refactor](skills/cleanup-and-refactor/SKILL.md) | Clean up already-working feature code after exploratory implementation by removing dead paths, tightening local structure, running one focused verification pass, and reporting what is safe to commit. |
| [code-refactoring](skills/code-refactoring/SKILL.md) | Refactor code by finding the canonical existing implementation, choosing the smallest safe seam, and extracting or redirecting behavior instead of rewriting solved logic from scratch. |
| [code-review](skills/code-review/SKILL.md) | Perform a severity-rated code review across security, correctness, performance, and maintainability, with concrete file-level findings and optional cross-validation for high-risk changes. |
| [convo-with-me](skills/convo-with-me/SKILL.md) | Collaboration rules for working with Me. Always invoke this skill at the start of every conversation with me to apply my preferred working style. |
| [daksh](skills/daksh/SKILL.md) | Run the Daksh product-delivery pipeline through explicit stage and command contexts, from onboarding and strategy docs through implementation, approvals, Jira sync, and handbook updates. |
| [divami-system-design](skills/divami-system-design/SKILL.md) |  |
| [doc-narrator](skills/doc-narrator/SKILL.md) | Write or review technical docs for cold readers by seeding context first, leading with prose before diagrams, surfacing open questions, and formatting the result for Vyasa. |
| [find-skills](skills/find-skills/SKILL.md) | Find relevant third-party skills, vet them for quality, and present or install the best-fit options when a user needs a capability that may already exist in the skills ecosystem. |
| [gws-chat](skills/gws-chat/SKILL.md) | Reference the Google Chat `gws` surface for inspecting schema, browsing resources, and calling raw Chat API methods for spaces, messages, memberships, and media. |
| [gws-chat-send](skills/gws-chat-send/SKILL.md) | Send a plain-text Google Chat message to a specific space with the `gws` helper command and explicit write-safety confirmation. |
| [gws-classroom](skills/gws-classroom/SKILL.md) | Reference the Google Classroom `gws` surface for exploring courses, rosters, invitations, coursework, and other raw API methods through schema-driven commands. |
| [gws-docs](skills/gws-docs/SKILL.md) | Reference the Google Docs `gws` surface for discovering document methods, inspecting schemas, and using raw Docs API calls alongside the append helper. |
| [gws-docs-write](skills/gws-docs-write/SKILL.md) | Append plain text to the end of a Google Doc with the `gws` helper command, with clear guidance on when to switch to raw `batchUpdate` calls for richer edits. |
| [gws-gmail](skills/gws-gmail/SKILL.md) | Reference the Gmail `gws` surface for discovering mail resources and helper commands, then build the right raw or helper invocation for sending, reading, labels, threads, drafts, and watch flows. |
| [gws-gmail-read](skills/gws-gmail-read/SKILL.md) | Read Gmail messages through the raw `gws gmail users messages get` API path, including header extraction, multipart body decoding, and the missing `+read` helper caveat. |
| [gws-gmail-triage](skills/gws-gmail-triage/SKILL.md) | Summarize unread or query-filtered Gmail inbox messages with the `gws gmail +triage` helper, including sender, subject, date, and optional labels. |
| [gws-gmail-watch](skills/gws-gmail-watch/SKILL.md) | Watch Gmail for new messages through Pub/Sub-backed `gws gmail +watch`, with options for polling, filtering, one-shot pulls, cleanup, and JSON output capture. |
| [gws-meet](skills/gws-meet/SKILL.md) | Reference the Google Meet `gws` surface for inspecting conference records, spaces, participants, recordings, transcripts, and other raw Meet API methods. |
| [gws-shared](skills/gws-shared/SKILL.md) | Shared operating rules for all `gws` skills, covering authentication, global flags, shell safety, JSON parsing quirks, and write-operation caution. |
| [icm-skill-creator](skills/icm-skill-creator/SKILL.md) | Design and scaffold a new ICM-style skill workspace by interviewing the user, confirming the staged architecture, and generating the layered files, templates, and routing needed for resumable workflows. |
| [jira-access](skills/jira-access/SKILL.md) | Query and summarize live Jira data for the DEB project, including ticket lookups, backlog and sprint views, assignee filters, blocked work, and reusable JQL patterns. |
| [lit-parse](skills/lit-parse/SKILL.md) | Parse PDFs, Office docs, and images into readable text files with the local `lit` CLI, including batch conversion patterns and filename normalization guidance. |
| [minutes-of-meeting](skills/minutes-of-meeting/SKILL.md) | Turn meeting transcripts or Google Docs into durable MOM artifacts by extracting acts, decisions, and todos, checking for financial sensitivity, previewing structure, and then writing the final markdown summary. |
| [retrospect-and-update-skill](skills/retrospect-and-update-skill/SKILL.md) | Retrospect on a failed or wasteful thread, extract the corrected execution pattern, and patch the responsible skill instructions so the same mistake is less likely to recur. |
| [tech-feasibility](skills/tech-feasibility/SKILL.md) | Turn a raw tech idea into a staged feasibility workspace by checking premises, probing scope in batches, confirming an outline, writing the analysis, and optionally generating a scoped Excel deliverable. |
| [use-cases](skills/use-cases/SKILL.md) | Excavate evidence from a finished project repo and turn it into a staged, publishable use-case narrative through extraction, story drafting, and final polish. |
