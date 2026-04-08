# Transcript Processing

This resource supports transcript selection, extraction, and MOM creation.

## Stage Contracts

### Stage 1: Transcript Selection
- Inputs: candidate transcript files
- Process: group files into meetings, order them, and infer the output basename
- Outputs: one ordered transcript set per meeting
- Stop Conditions: grouping remains ambiguous or chronology cannot be established

### Stage 2: Meeting Extraction
- Inputs: ordered transcript set and this rubric
- Process: identify acts with start/end ranges, key quotes, timestamps, decisions, blockers, and todos
- Outputs: a concise meeting outline that can drive the MOM
- Stop Conditions: the outline is still summary-slop rather than a reconstructable meeting narrative

### Stage 3: MOM Writing
- Inputs: transcript-derived outline and naming rules
- Process: write the final Markdown artifact with narrative sections and todo cards
- Outputs: final MOM file next to the source transcript
- Stop Conditions: source attribution is weak, timestamps are missing, or todos are not independently actionable

## Context Discipline

Only load the transcript files for the active meeting and this rubric. Do not mix notes from other meetings into the same active context, and do not keep stale extraction scratch text once the final MOM is written.

## Handoff Standard

The final MOM should let a later agent understand what happened without reopening the full transcript unless they want verbatim detail.

## Why Transcript Grouping Matters

### WHY This Matters

Meeting recordings are often split across files or captured with noisy formatting. Grouping the right files first avoids fragmented MOM notes and duplicate action items.

### WHAT to Do

- Treat files from the same date and topic as one meeting unless the content clearly diverges.
- Normalize alias filenames before grouping, for example `YYYYMMDD.txt`, `Mar 3, 2026.txt`, and `Mar 3, 2026-2.txt`.
- Preserve chronology when combining multiple transcript files.
- Infer the meeting date from the filename first, then from transcript content.
- Record the chosen grouping and ordering before you start narrative extraction.

## Why MOM Structure Matters

### WHY This Matters

The MOM is both the human summary and the source artifact for sprint updates. If it is vague, downstream sprint updates will drift. If it loses speaker attribution, timestamps, emotional context, or the real shape of the conversation, it becomes much less useful for revisiting the actual meeting.

### WHAT to Do

Go through the transcript file carefully and preserve the actual flow of the meeting.

Before writing the final MOM, build a minimal outline with:
- meeting context
- act breaks or phase changes with approximate start and end timestamps
- key decisions and unresolved tensions
- key reasoning for each important decision
- rejected alternatives, anti-patterns, or "do not do this" guidance
- deadline pressure, blockers, or interpersonal friction when present
- quoted moments worth preserving
- todo candidates with owner and deadline evidence

The MOM should follow this rubric:

- Read the transcript fully before summarizing.
- Default to a heavier write-up, not a gist. The output should feel like a durable meeting artifact that someone can rely on later without reopening the transcript.
- Preserve who said what with actual quotes where they materially help.
- When the transcript identifies a speaker, the attribution line must use that actual speaker name. Do not use generic labels such as `Meeting notes`, `Transcript`, `AI summary`, or `System` unless the source truly lacks speaker identity.
- **All quoted speech must appear on its own line using Markdown blockquote syntax — never embedded inline within a prose sentence.** Format:
  ```
  > *"quote text"*
  > — Speaker _(~HH:MM:SS)_
  ```
- Include timestamps so a reader can jump back to specific moments.
- Capture the drama: audio issues, frustration, deadline pressure, disagreement, or urgency when present.
- Structure the write-up as a narrative with acts rather than generic bullet summaries.
- Every act header must include an approximate time range using the first and last meaningful timestamps in that section, for example `## Act II - AI first vs user first (~00:12 - ~00:28)`.
- Use as many acts as the meeting naturally requires. Three acts are a common default, not a limit.
- Expand important turns in the conversation: competing proposals, unresolved questions, ownership changes, and moments where the room's energy shifts.
- Preserve operationally important specifics when they shape future work: named tools, libraries, architectural options, concrete numbers, bounded prototype definitions, and explicit constraints.
- Do not sanitize disagreement. If the room contains pushback, frustration, correction, urgency, or deadline pressure, preserve it in the narrative with attribution.
- Preserve the "why", not just the "what". Important decisions should carry rationale and, when present, the alternative that was rejected.
- End with a **## Todos** section containing one `<todo>` card per action item. **Do not use a Markdown table.** Styling is provided globally by `docs/custom.css` — no inline `<style>` block is needed in the MOM file.

Recommended structure:

- Title and meeting context
- `## Act I - opening context and setup (~start - ~end)`
- Additional acts as needed for major discussion phases, pivots, or debates
- Final act: decisions, tensions, unresolved items, and close
- `## Todos` section — one `<todo>` card per action item

Within each act:

- weave the summary as prose
- keep the time range in the act heading, not buried in the prose
- use short quoted excerpts when useful, always as standalone `> ` blockquotes — never inline within a sentence
- blockquote format: `> *"quote text"*` on one line, then `> — Speaker _(~timestamp)_` on the next
- timestamps go on the attribution line of the blockquote, not in prose
- prefer enough detail that a reader can reconstruct what changed during the meeting, not just the final conclusions

### Todo Card Format

Each action item must be its own line:

- [ ] Task description text here | author: Owner Name | deadline: YYYY-MM-DD

- One line per action item — do not group multiple items in one card
- Only create a todo line when the transcript supports the task with reasonably clear owner evidence. Do not fabricate generic owners such as `Team`, `Platform team`, or `Next review` unless the meeting actually says that.

Naming rules:

- Single transcript: `<original-name>-mom.md`
- Multi-file meeting: `YYYYMMDD-mom.md`

Write the MOM into the same folder as the source transcript.
