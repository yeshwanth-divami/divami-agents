---
name: retrospect-and-update-skill
description: Retrospect on a failed or wasteful thread, extract the corrected execution pattern, and patch the responsible skill instructions so the same mistake is less likely to recur.
---

# Retrospect And Update Skill

Use this skill after a thread has already revealed failure modes. Treat the current chat as the primary artifact.

## Workflow

1. Reconstruct the failure chain from the chat: note each wrong assumption, the action it triggered, and the retry or wasted work that followed.
2. Extract the corrected pattern that eventually worked: commands, decision rules, stop conditions, ordering, and validation steps.
3. Map each failure to the skill or skills that should have prevented it. Prefer the smallest responsible set of skills.
4. Patch those skills directly. Tighten trigger text in frontmatter if invocation was wrong; tighten body instructions if execution was wrong.
5. Preserve progressive disclosure. Put core decision rules in `SKILL.md`; move bulky detail to `references/` only if needed.
6. Validate every changed skill with `quick_validate.py`. If a skill has scripts, run the smallest representative check that proves the fix is real.

## What To Capture

- False belief: what Codex assumed that turned out to be wrong.
- Harm: what retry, wrong tool use, or wasted step followed from that belief.
- Correct pattern: the exact rule or sequence that worked later.
- Skill gap: what the current skill omitted, overstated, or left ambiguous.
- Patch: the concrete wording or resource change needed to prevent recurrence.

## Editing Rules

- Fix instructions, not symptoms. Do not add vague warnings like "be careful."
- **Scripts belong in files.** If the fix involves code the skill must execute, write it as a real script in `scripts/` with proper CLI I/O — not as a fenced code block in markdown. Markdown code blocks get rewritten from scratch every invocation; a `scripts/` file gets reused as-is.
- Prefer imperative rules with observable triggers: "Read X before Y", "Use tool A for B", "Stop if C".
- Remove stale or misleading guidance when replacing it.
- Do not broaden a skill unless the chat proves the broader trigger is needed.
- If no existing skill is responsible, create a narrow new skill only when the pattern is reusable.
- **Abstract until project-blind.** A rule passes if it would prevent the same failure in a completely different domain or stack. If the rule mentions a framework, language, or component, raise the abstraction. Keep narrowing until only the principle remains.
- **Update the skill that governs the failure, not the skill that was active during it.** If the failure was that feedback was too session-specific, that's a retrospect skill failure — patch here, not in the skill being retrospected.

## Output

Report the retrospective in three parts: false assumptions, corrected patterns, and skills updated. Include file paths changed and any validation run. If the chat is too incomplete to justify edits, say that explicitly and stop instead of inventing guidance.
