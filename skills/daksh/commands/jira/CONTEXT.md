---
description: "Run Jira sync commands and show the script output verbatim."
---

# Command: /daksh jira

## Persona
Jira Bridge. Run the script, show output verbatim, and keep manifest-backed name mapping minimal and explicit.

## Steps — push
1. Verify `JIRA_SERVER`, `JIRA_EMAIL`, and `JIRA_TOKEN`.
2. Run `python scripts/jira-sync.py push [--module MODULE] [--dry-run] [--force]`.
3. Show output verbatim.
4. On exit 0: `Jira push complete. manifest.jira.ticket_map updated.`

## Steps — pull
1. Verify `JIRA_SERVER`, `JIRA_EMAIL`, and `JIRA_TOKEN`.
2. Run `python scripts/jira-sync.py pull [--module MODULE] [--dry-run]`.
3. Show output verbatim.
4. On exit 0: `Jira pull complete. tasks.md status columns updated.`

## Steps — status
1. Run `python scripts/jira-sync.py status`.
2. Show output verbatim.

## Steps — list-my-tasks --name NAME
1. Check `manifest.jira.user_map` for `NAME`.
2. If found, run `python scripts/list-tasks.py --name "mapped_name" [--sprint N] [--open]`.
3. If not found, scan `Assigned to` fields across `docs/implementation/*/tasks.md`, propose the closest match, confirm it, then write the mapping to `manifest.jira.user_map`.
4. Show output verbatim.
