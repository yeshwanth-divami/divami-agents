---
name: export-chat-to-divami-vyasa
description: Export a Claude Code session to a markdown file and push it to the Divami Vyasa server (aws-ai:/home/yeshwanth/projects/chats/yeshwanth). Use when the user says "export this chat", "push conversation", or "export session".
user-invocable: true
allowed-tools:
  - Bash
---

# export-chat-to-divami-vyasa

Exports the current (or selected) Claude Code session as a markdown file and SCPs it to the Divami Vyasa host (`aws-ai`).

Arguments: `$ARGUMENTS`

Script lives at the same directory as this SKILL.md: `export_chat.py`.

---

## SSH config required

`~/.ssh/config` must have:

```
Host aws-ai
  HostName ec2-13-233-157-246.ap-south-1.compute.amazonaws.com
  IdentityFile ~/Documents/certificates/yeshwanth
```

---

## Dispatch on arguments

Parse `$ARGUMENTS`. Run the script with the appropriate flags.

### No args — interactive

Confirm username first, then run:

```bash
cd /Users/yeshwanth/Code/Divami/divami-agents/skills/export-chat-to-divami-vyasa
/Users/yeshwanth/.venv/bin/python export_chat.py --user <username>
```

Presents numbered list of recent sessions. User picks one. Exports + pushes. Prints Vyasa URL on success.

### `--project <slug>` or `-p <slug>`

Filter sessions by project slug (partial match on project directory name).

Most common use — export the current project's session:

```bash
/Users/yeshwanth/.venv/bin/python export_chat.py --project <current-project-slug> --user <username>
```

To get the current project slug, derive it from `cwd`: replace `/` with `-` and strip leading `-`.

### `--list` or `-l`

List available sessions without exporting.

### `--no-push`

Write markdown locally to `/tmp/`, skip scp.

### `--session <uuid>` or `-s <uuid>`

Export a specific session by UUID.

### `--out <path>` or `-o <path>`

Override output file path.

---

## Default behaviour when user says "export this chat"

1. Identify current project directory from conversation context.
2. Derive project slug: last path component, e.g. `export-chats`.
3. Ask: **"Export as which Vyasa username?"** — wait for confirmation before running.
4. Run:
   ```bash
   cd /Users/yeshwanth/Code/Divami/divami-agents/skills/export-chat-to-divami-vyasa
   /Users/yeshwanth/.venv/bin/python export_chat.py --project <slug> --user <username>
   ```
5. If multiple sessions exist for that project, the script shows a list and prompts.
6. After push, report the Vyasa URL: `https://vyasa.divami.com/posts/chats/<username>/<slug>.md`

---

## Output format

Markdown file named `<date>-<title-slug>.md` containing:
- Session metadata header (session ID, project, export timestamp)
- Alternating `## User` / `## Assistant` sections with timestamps
- Tool calls rendered as fenced code blocks
