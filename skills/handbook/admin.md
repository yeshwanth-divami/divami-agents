# Admin Handbook

This guide covers the Jira-side configuration Daksh needs in order to sync task state safely. The important rule is that admin setup is one-time and explicit: the scripts do not discover project settings for you, and they do not store secrets in the manifest.

## Jira Configuration Contract
`docs/.daksh/manifest.json` owns the non-secret Jira settings. `manifest.jira.project_key` is the Jira project key string, `manifest.jira.board_id` is the numeric board id used for sprint operations, `manifest.jira.done_statuses` is the list of workflow states that Daksh should treat as done, and `manifest.jira.user_map` stores optional display-name mappings for task lookup flows.

Set those values before the first real `push`. If `project_key` or `board_id` is missing, `scripts/jira-sync.py` exits with a clear error instead of guessing. That is deliberate: a wrong board id is like mailing invoices to the right company but the wrong department.

## Credentials And Safety
Secrets live only in environment variables: `JIRA_SERVER`, `JIRA_EMAIL`, and `JIRA_TOKEN`. `JIRA_SERVER` must be `https://...`; the script rejects plain HTTP. No token, email, or session secret is written into the manifest, handbook, or task documents.

The safest admin validation flow is `python scripts/jira-sync.py push --dry-run --module JIRA --force` followed by `python scripts/jira-sync.py status`. Dry-run proves the manifest and task parsing are sane without creating or editing tickets, and `status` reports whether Daksh already has a populated `ticket_map`, the last sync timestamp, and whether open time blocks exist locally.

## Name Mapping And Task Lookup
When a human asks for "my tasks", Daksh can resolve a friendly name through `manifest.jira.user_map`. That mapping is not an identity system; it is just a convenience alias from an entered name to the exact `Assigned to` string used in module `tasks.md`. If the task docs are rewritten with a different display name, update the map or the lookup will quietly miss tasks.

## Failure Modes Worth Checking First
If push fails immediately, check the three env vars and the two manifest config keys before looking anywhere else. If pull appears to work but done tasks do not disappear from `list-tasks.py --open`, inspect `manifest.traceability` and `manifest.jira.done_statuses`; those two fields define the local truth Daksh filters on.

## Changelog
- 2026-03-29: Replaced the placeholder admin skeleton with the actual Jira configuration, credential, and lookup rules used by Daksh.
