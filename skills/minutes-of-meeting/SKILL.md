---
name: minutes-of-meeting
description: Turn meeting transcripts or Google Docs into durable MOM artifacts by extracting acts, decisions, and todos, checking for financial sensitivity, previewing structure, and then writing the final markdown summary.
---

# Meeting to MOM

## Read This First

This skill turns meeting transcript files into a durable Markdown MOM.

Input: one or more transcript files **or** a Google Doc URL. Output: `<basename>-mom.md` saved alongside the transcript in `docs/conversations/` under the current working directory.

### Google Doc Input

If the user provides a Google Doc URL instead of a local file:

1. Run the dedicated downloader script to save the transcript under `docs/conversations/` in the current working directory:
   ```bash
   python3 scripts/download_meeting_transcript.py '<gdoc-url>' docs/conversations/YYYYMMDD-<slug>.txt
   ```
   Create the directory first if it does not exist (`mkdir -p docs/conversations`).
2. Prefer the URL's explicit transcript tab when present. Otherwise, the script must resolve the tab named `Transcript`, not the notes tab.
3. The downloader prepends an alias map such as `YR = Yeshwanth Reddy Yerraguntla` and only rewrites leading `Speaker Name:` prefixes to aliases. Never replace names inside spoken text.
4. Proceed with Step 1 using the saved `.txt` as the canonical transcript source.
5. The MOM's frontmatter must reference both the local `.txt` file and the original Google Doc URL.

### Workflow Rules

- One stage, one job: first define the transcript set, then extract, then write.
- Keep context narrow: only load the transcript files being processed plus the rubric sections needed for the current stage.
- Treat the written MOM as the durable artifact and avoid mixing raw extraction notes into the final file.

## Workflow

```text
Meeting to MOM Workflow
- [ ] Step 1: Select transcript files
- [ ] Step 2: Extract meeting structure and key moments
- [ ] Step 2.3: Financial sensitivity scan and disclosure
- [ ] Step 2.5: Preview act/todo shape for user review
- [ ] Step 3: Write the MOM artifact after preview confirmation
```

## Step 1: Select transcript files

Contract:

- Inputs: user-provided transcript paths
- Process: decide which files belong to the same meeting and in what order
- Outputs: ordered transcript set and output filename plan
- Stop Conditions: unclear file grouping or missing transcript source

Use the transcript file(s) the user provides. If multiple files belong to one meeting, process them together in chronological order.

See [resources/transcript-processing.md](resources/transcript-processing.md).

## Step 2: Extract meeting structure and key moments

Contract:

- Inputs: ordered transcript set and the transcript rubric
- Process: identify acts with start/end time ranges, decisions, tensions, quotes, timestamps, and action items
- Outputs: a reviewable internal outline for the MOM
- Stop Conditions: the meeting flow is still too vague to narrate or action items lack enough evidence

Use [resources/transcript-processing.md](resources/transcript-processing.md) to extract the narrative spine before writing prose. Keep the extraction focused on the current meeting only.
Before writing, explicitly extract:

- each act's approximate start and end timestamp
- key decisions
- why each decision was made
- rejected alternatives or anti-patterns
- deadline/pressure signals
- exact owner/date evidence for todos

## Step 2.3: Financial sensitivity scan and disclosure

Contract:

- Inputs: extracted meeting outline and raw transcript
- Process: scan for financially sensitive content; disclose to user; optionally redact before proceeding
- Outputs: clean transcript and outline, or explicit user decision to keep the content
- Stop Conditions: do not proceed to Step 2.5 until the user has seen the disclosure and responded

Financially sensitive signals to look for:

- Specific monetary values: prices, project quotes, budgets, revenue figures
- Rates and percentages tied to payments: billing rates, penalty clauses, discount terms
- Compensation, salary, or contractor fee discussion
- Procurement terms, contract values, or SLA financial penalties

**If any signals are found**, list them to the user with timestamps and a one-line description of the context. Then ask:

> "This transcript contains financially sensitive information. Do you want me to remove it from both the transcript and the MOM before proceeding? (yes / no / show me first)"

- On **yes**: redact the identified sections from the downloaded transcript file, then continue to Step 2.5 with a clean outline.
- On **no**: proceed with content intact.
- On **show me first**: display the flagged excerpts verbatim, then re-ask.

If no financially sensitive content is found, state that clearly and proceed to Step 2.5 without interruption.

## Step 2.5: Preview act/todo shape for user review

Contract:

- Inputs: transcript-derived outline from Step 2
- Process: give the user a ballpark structure before drafting the full MOM
- Outputs: estimated act count, one-line synopsis per act, estimated todo count, and one-line todo list
- Stop Conditions: do not write the MOM file yet; wait for confirmation or corrections

The preview must include:

- `Estimated acts: N`
- one line per act, in order, with a short synopsis
- `Estimated todos: M`
- one line per todo candidate, with owner when known

Treat this as a checkpoint. If the user corrects the act count, merges/splits acts, or challenges the todo count, update the outline first and only then proceed to writing.

## Step 3: Write the MOM artifact

Contract:

- Inputs: transcript set, corrected preview, extracted meeting structure, and naming rules
- Process: write the Markdown MOM in final form next to the transcript source
- Outputs: completed `*-mom.md` artifact
- Stop Conditions: missing source context, no `## Participants` section before Act I, no `## Todos` section, weak attribution/timestamps, or no preview confirmation

Create a Markdown MOM in the same folder as the transcript.

- Single transcript: use the same basename with `-mom.md`
- Multiple transcripts for one meeting: use `YYYYMMDD-mom.md`

The MOM must follow the narrative meeting-summary rubric in [resources/transcript-processing.md](resources/transcript-processing.md), including quotes, timestamps, a substantial narrative, and a final todo section.
Do not invent owners or deadlines. If transcript evidence is missing, leave the item out or mark it clearly as unresolved in prose instead of fabricating a todo.

## Validation

When forward-testing this skill, score outputs using [resources/evaluation-rubric.json](resources/evaluation-rubric.json). A score of 3 or more across the four criteria indicates adequate performance.
