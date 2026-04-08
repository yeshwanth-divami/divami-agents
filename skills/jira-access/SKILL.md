````skill
---
name: jira-access
description: Use when the user asks about Jira tickets, sprints, backlogs, or issues for this project. Covers querying, filtering, fetching, and summarising Jira data for the DEB project at https://divami.atlassian.net. Invoke when the user says things like "show me open tickets", "what's in the backlog", "find ticket DEB-xxx", "who's working on X", "list blocked items", or any question about Jira issues.
---

# Jira Access Skill

## Overview

This skill lets you query and work with live Jira data for the **AI Enterprise Brain** project.

| Config            | Value                                     |
|-------------------|-------------------------------------------|
| Jira Server       | `https://divami.atlassian.net`            |
| Project Key       | `DEB`                                     |
| Auth Email        | `$JIRA_EMAIL`                             |
| Auth Token        | `$JIRA_TOKEN`                             |
| Python Interpreter | `/Users/yeshwanth/Code/Divami/ai-enterprise-brain/backend/.venv/bin/python` |

Credentials (`JIRA_SERVER`, `JIRA_EMAIL`, `JIRA_TOKEN`) are stored in **two places** — the project root `.env` file (`/Users/yeshwanth/Code/Divami/ai-enterprise-brain/.env`) and `~/.zshrc`. When running terminal scripts, always `source ~/.zshrc` first or load from the root `.env` explicitly.

---

## Connecting to Jira

Use the `jira` Python library (already a dependency in this repo).

```python
import os
from jira import JIRA

client = JIRA(
    server=os.environ["JIRA_SERVER"],          # https://divami.atlassian.net
    basic_auth=(os.environ["JIRA_EMAIL"], os.environ["JIRA_TOKEN"]),
)
```

Cache the client with `lru_cache` to avoid creating multiple connections per session.

---

## Common Operations

### 1. Fetch a Single Ticket

```python
issue = client.issue("DEB-123")
print(issue.fields.summary)
print(issue.fields.status.name)
print(issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned")
print(issue.fields.description)

# Fetch sub-tasks
for subtask in issue.fields.subtasks:
    print(f"Sub-task: [{subtask.key}] {subtask.fields.summary}")

# Fetch Acceptance Criteria (Commonly in description or a custom field)
# If not in description, check custom fields:
# print(issue.fields.customfield_XXXXX)
```

### 2. Search with JQL

```python
issues = client.search_issues(
    'project = DEB AND status = "In Progress" ORDER BY updated DESC',
    maxResults=20,
)
for i in issues:
    print(f"[{i.key}] {i.fields.summary} — {i.fields.status.name}")
```

### 3. Full-Text Keyword Search

```python
issues = client.search_issues(
    'project = DEB AND text ~ "authentication" ORDER BY updated DESC',
    maxResults=20,
)
```

### 4. Filter by Status / Priority / Assignee

```python
# All open high-priority tickets
issues = client.search_issues(
    'project = DEB AND status != Done AND priority = High ORDER BY created DESC',
    maxResults=30,
)

# Tickets assigned to a specific person
issues = client.search_issues(
    'project = DEB AND assignee = "yeshwanth@divami.com" AND status != Done',
    maxResults=50,
)
```

### 5. Sprint / Backlog Queries

```python
# Current sprint tickets
issues = client.search_issues(
    'project = DEB AND sprint in openSprints() ORDER BY rank ASC',
    maxResults=50,
)

# Backlog (not in any sprint, not done)
issues = client.search_issues(
    'project = DEB AND sprint is EMPTY AND status != Done ORDER BY created ASC',
    maxResults=50,
)

# Blocked tickets (has blocker links)
issues = client.search_issues(
    'project = DEB AND issueFunction in linkedIssuesOf("project = DEB", "is blocked by")',
    maxResults=20,
)
```

### 6. Recently Updated Tickets

```python
issues = client.search_issues(
    'project = DEB AND updated >= -7d ORDER BY updated DESC',
    maxResults=30,
)
```

---

## Useful JQL Patterns for DEB

| Intent | JQL |
|--------|-----|
| All open tickets | `project = DEB AND status != Done ORDER BY updated DESC` |
| Current sprint | `project = DEB AND sprint in openSprints()` |
| Unassigned tickets | `project = DEB AND assignee is EMPTY AND status != Done` |
| My tickets | `project = DEB AND assignee = currentUser()` |
| Created this week | `project = DEB AND created >= startOfWeek()` |
| Bugs only | `project = DEB AND issuetype = Bug AND status != Done` |
| High/Critical blockers | `project = DEB AND priority in (High, Critical) AND status != Done` |
| Done this sprint | `project = DEB AND sprint in openSprints() AND status = Done` |

---

## Formatting Issue Output

Use this helper (consistent with the existing agent pattern):

```python
def fmt_issue_full(issue) -> str:
    f = issue.fields
    assignee = getattr(f.assignee, 'displayName', 'Unassigned')
    subtasks = [f"- [{st.key}] {st.fields.summary} ({st.fields.status.name})" for st in f.subtasks]
    
    output = [
        f"[{issue.key}] {f.summary}",
        f"Status: {f.status.name} | Priority: {f.priority.name if f.priority else 'None'}",
        f"Type: {f.issuetype.name} | Assignee: {assignee}",
        f"Created: {f.created[:10]} | Updated: {f.updated[:10]}",
        f"Description:\n{f.description or 'No description provided.'}"
    ]
    
    if subtasks:
        output.append("\nSub-tasks:")
        output.extend(subtasks)
        
    return "\n".join(output)

def fmt_issue_compact(issue) -> str:
    f = issue.fields
    return (
        f"[{issue.key}] {f.status.name} | "
        f"{f.priority.name if f.priority else 'None'} | {f.summary}\n"
        f"Type: {f.issuetype.name} | "
        f"Assignee: {getattr(f.assignee, 'displayName', 'Unassigned')} | "
        f"Reporter: {getattr(f.reporter, 'displayName', 'Unknown')}\n"
        f"Created: {f.created[:10]} | Updated: {f.updated[:10]}\n"
        f"Labels: {', '.join(f.labels) if f.labels else 'none'}"
    )
```

---

## Error Handling

Always wrap Jira calls in try/except:

```python
from jira import JIRAError

try:
    issue = client.issue("DEB-999")
except JIRAError as e:
    print(f"Jira error {e.status_code}: {e.text}")
```

Common errors:
- `404` — ticket key doesn't exist
- `400` — malformed JQL (check quotes and field names)
- `401` — token expired or wrong email/token pair (re-check `~/.zshrc`)

---

## Running a Quick Ad-Hoc Query (Terminal)

Since the env vars are in `.zshrc`, you can run one-off scripts directly:

```bash
# From repo root
source ~/.zshrc
python -c "
import os
from jira import JIRA
c = JIRA(server=os.environ['JIRA_SERVER'], basic_auth=(os.environ['JIRA_EMAIL'], os.environ['JIRA_TOKEN']))
issues = c.search_issues('project = DEB AND status != Done ORDER BY updated DESC', maxResults=10)
for i in issues:
    print(f'[{i.key}] {i.fields.status.name} | {i.fields.summary}')
"
```

---

## Notes

- **Project key is `DEB`** — always scope queries with `project = DEB` unless intentionally searching across all projects.
- **Board ID is `2494`** — useful for any board-specific API calls via the REST API directly if needed.
- **Max results cap** — the Jira library defaults to 50 per page; use pagination (`.search_issues(..., startAt=50)`) for larger result sets.
- **Field access** — use `getattr(f.assignee, 'displayName', 'Unassigned')` style to avoid AttributeError on None fields.

---

## Known Sprint IDs

| Sprint Name   | ID   | State  |
|---------------|------|--------|
| DEB Sprint 1  | 6085 | future |
| DEB Sprint 2  | 6518 | future |

To discover sprint IDs for new sprints, use the agile REST API:

```python
import os, requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth(os.environ["JIRA_EMAIL"], os.environ["JIRA_TOKEN"])
resp = requests.get(
    f"{os.environ['JIRA_SERVER']}/rest/agile/1.0/board/2494/sprint",
    auth=auth,
    params={"state": "active,future"},
)
for s in resp.json()["values"]:
    print(s["id"], s["name"], s["state"])
```

Then query by sprint ID:
```python
issues = client.search_issues(
    'project = DEB AND sprint = 6085 ORDER BY rank ASC',
    maxResults=100,
)
```
````
