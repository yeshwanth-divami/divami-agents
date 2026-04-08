# Ops Handbook

Daksh runs as a Claude Code skill with no server, no database, and no daemon — the [manifest](../docs/glossary#manifest) is a JSON file in git, and the scripts are plain Python. This handbook covers what a maintainer or infra owner needs to set up, verify, and recover Daksh on a new machine or after something breaks.

## System Requirements

Daksh has two operating modes with different dependencies:

| Mode | What you need |
|------|---------------|
| Core pipeline only | Python 3.11+, Claude Code, `uv` |
| Jira sync enabled | All of the above + `jira` Python package + three env vars |

The `jira` package is the only runtime dependency beyond the standard library. Everything else — manifest reads, preflight checks, list-tasks, approve, change, tend — runs on stdlib alone.

## Python Environment Setup

Daksh expects a `uv`-managed virtual environment. From the project root:

```bash
uv venv
source .venv/bin/activate     # or .venv\Scripts\activate on Windows
uv pip install jira
```

Verify:

```bash
python -c "import jira; print('ok')"
```

If you see `ModuleNotFoundError`, the venv is not activated or `jira` did not install into it.

> [!note] Daksh does not use system Python
> Always activate the project venv before running any `python scripts/...` command. Running with the wrong interpreter is the most common cause of `ModuleNotFoundError` on a fresh machine.

## Jira Credentials

Three environment variables are required for any `jira-sync.py` operation. Set them in your shell profile or a `.env` loader — never in the manifest, never in a file committed to git.

```bash
export JIRA_SERVER="https://your-org.atlassian.net"
export JIRA_EMAIL="you@example.com"
export JIRA_TOKEN="your-api-token"
```

`JIRA_SERVER` must use HTTPS. The script rejects plain HTTP.

To generate a token: Jira → Profile → Security → API tokens → Create.

Verify connectivity before any push or pull:

```bash
python scripts/jira-sync.py status
```

A successful status prints project key, board ID, last sync timestamp, and open time blocks. A failed status prints the first env var that is missing or the HTTP error from Jira.

## Running Tests

Daksh has two test layers. Run them from the project root.

**Unit tests only** (no filesystem, no network, no Jira):

```bash
python -m pytest tests/test_preflight.py tests/test_jira_sync.py -v
```

**Integration tests** (hit the real manifest and spawn real subprocesses):

```bash
python -m pytest -m integration -v
```

> [!warning] Integration tests use the real manifest
> `tests/test_preflight_integration.py` runs against `docs/.daksh/manifest.json`. If that file is stale — missing an approval, hash drifted — the integration test will fail. This is intentional. The test is the self-hosting gate. Do not skip it; diagnose the failure.

Full suite:

```bash
python -m pytest -v
```

## Adding a Team Member to the Roster

When someone joins a project mid-flight, the PTL edits `docs/.daksh/manifest.json` directly and adds an entry to `team_roster`:

```json
{ "name": "Priya Sharma", "role": "Engineer", "email": "priya@divami.com" }
```

Valid roles: `PTL`, `TL`, `Engineer`, `Client`, `Stakeholder`.

After editing, run `/daksh tend` to verify the manifest is internally consistent.

## Adding a Name Mapping for Task Lookup

If an engineer's display name in `tasks.md` differs from what they type in Slack or Jira, add a mapping to `manifest.jira.user_map`:

```json
"user_map": {
  "priya": "Priya Sharma",
  "ps": "Priya Sharma"
}
```

Keys are case-insensitive. Values must match the exact `Assigned to:` string in `tasks.md`. A mismatch produces empty results without an error — the first thing to check when someone says "my tasks are missing."

## Recovering from a Stale Manifest

A stale manifest means a document changed after it was approved. The symptom is `/daksh tend` reporting hash drift.

To recover:

1. Run `/daksh tend` — it prints exactly which file drifted and what the current hash is
2. Decide: was the change intentional?
   - **Yes** → re-run `/daksh approve [stage] [MODULE]` to record the new hash
   - **No** → revert the file to the approved version and re-run tend to confirm
3. Never manually patch `doc_hash` in the manifest — the approve command writes the correct hash atomically

## Recovering from a Broken Pipeline Init

If `/daksh init` was run but something failed mid-way:

1. Check whether `docs/.daksh/manifest.json` exists and is valid JSON
2. If it exists but is malformed, compare against `templates/manifest-template.json` and repair manually
3. If it does not exist, re-run `/daksh init` — it is safe to re-run on an empty project directory

> [!warning] Do not re-run init on an active project
> Re-running init on a project that already has stage approvals will overwrite the manifest. Back it up first.

## Common Operational Failures

| Symptom | Most likely cause | Fix |
|---------|-----------------|-----|
| `ModuleNotFoundError: jira` | Wrong Python interpreter | Activate venv: `source .venv/bin/activate` |
| `JIRA_SERVER not set` | Missing env var | Export the three Jira env vars in your shell |
| `HTTP 401` from Jira | Expired or wrong token | Regenerate API token in Jira → Security |
| `HTTP 404` on board operations | Wrong `board_id` in manifest | Verify board ID in your Jira project settings |
| Integration test failing | Manifest hash drift | Run `/daksh tend`; re-approve the drifted stage |
| `list-tasks.py` returns nothing | Name not in `user_map` or exact name mismatch | Check `manifest.jira.user_map` and `Assigned to:` field in `tasks.md` |
| `jira-sync.py push` creates duplicates | `ticket_map` already populated but `--force` not passed | Use `push --force --module M` to overwrite, or clear `ticket_map` entries manually |

## Changelog

- 2026-03-29: Initial ops handbook — environment setup, Jira credentials, test execution, roster management, stale manifest recovery, and failure table.
