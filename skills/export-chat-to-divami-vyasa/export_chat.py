#!/usr/bin/env python3
"""Export a Claude Code session to markdown and push to aws-ai."""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"
REMOTE_HOST = "aws-ai"
REMOTE_BASE = "/home/{user}/projects/chats/{user}"
VYASA_BASE = "https://vyasa.divami.com/posts/chats/{user}"


def list_sessions(project_slug: str | None = None):
    sessions = []
    for jsonl in sorted(CLAUDE_PROJECTS.rglob("*.jsonl")):
        if project_slug and project_slug not in jsonl.parent.name:
            continue
        entries = []
        with open(jsonl) as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        title = next((e.get("title", "") for e in entries if e.get("type") == "ai-title"), "")
        msgs = [e for e in entries if e["type"] in ("user", "assistant")]
        if not msgs:
            continue
        ts = msgs[0].get("timestamp", "")
        sessions.append({"path": jsonl, "title": title, "ts": ts, "count": len(msgs)})
    return sorted(sessions, key=lambda x: x["ts"], reverse=True)


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "tool_use":
                    name = block.get("name", "tool")
                    inp = block.get("input", {})
                    inp_str = json.dumps(inp, indent=2) if inp else ""
                    parts.append(f"```tool:{name}\n{inp_str}\n```")
                # tool_result blocks always stripped to avoid leaking file contents
        return "\n\n".join(p for p in parts if p.strip())
    return str(content)


def to_markdown(jsonl_path: Path) -> str:
    entries = []
    with open(jsonl_path) as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    title = next((e.get("title", "") for e in entries if e.get("type") == "ai-title"), "")
    session_id = entries[0].get("sessionId", jsonl_path.stem) if entries else jsonl_path.stem
    project = jsonl_path.parent.name.lstrip("-").replace("-", "/")

    lines = []
    lines.append(f"# {title or 'Claude Code Session'}")
    lines.append(f"\n**Session:** `{session_id}`  ")
    lines.append(f"**Project:** `{project}`  ")
    lines.append(f"**Exported:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ")
    lines.append("\n---\n")

    msgs = [e for e in entries if e["type"] in ("user", "assistant")]
    for msg in msgs:
        role = msg["type"]
        content = msg.get("message", {}).get("content", "")
        text = extract_text(content).strip()
        if not text:
            continue
        ts = msg.get("timestamp", "")
        ts_fmt = ""
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                ts_fmt = f" _{dt.strftime('%H:%M')}_"
            except ValueError:
                pass

        if role == "user":
            lines.append(f"## User{ts_fmt}\n\n{text}\n")
        else:
            lines.append(f"## Assistant{ts_fmt}\n\n{text}\n")
        lines.append("---\n")

    return "\n".join(lines)


def push_to_remote(local_path: Path, username: str) -> str:
    remote_path = REMOTE_BASE.format(user=username)
    dest = f"{REMOTE_HOST}:{remote_path}/"
    print(f"Pushing {local_path.name} -> {dest}")
    result = subprocess.run(
        ["scp", str(local_path), dest],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"scp failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    url = f"{VYASA_BASE.format(user=username)}/{local_path.name}"
    print(f"Done.\nAvailable at: {url}")
    return url


def pick_session(sessions: list) -> dict:
    if len(sessions) == 1:
        return sessions[0]
    print("\nAvailable sessions (most recent first):\n")
    for i, s in enumerate(sessions[:20]):
        ts = s["ts"][:10] if s["ts"] else "?"
        title = (s["title"] or "untitled")[:60]
        print(f"  [{i}] {ts}  {title}  ({s['count']} msgs)")
    print()
    idx = input("Pick session [0]: ").strip() or "0"
    return sessions[int(idx)]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Export Claude Code session to markdown + push to aws-ai")
    parser.add_argument("--project", "-p", help="Filter by project slug (partial match)")
    parser.add_argument("--session", "-s", help="Session UUID (skip interactive pick)")
    parser.add_argument("--list", "-l", action="store_true", help="List sessions and exit")
    parser.add_argument("--user", "-u", help="Vyasa username (prompted if not provided)")
    parser.add_argument("--no-push", action="store_true", help="Write markdown locally, skip scp")
    parser.add_argument("--out", "-o", help="Output file path (default: auto-named in /tmp)")
    args = parser.parse_args()

    sessions = list_sessions(args.project)
    if not sessions:
        print("No sessions found.", file=sys.stderr)
        sys.exit(1)

    if args.list:
        for s in sessions[:30]:
            ts = s["ts"][:10] if s["ts"] else "?"
            print(f"{ts}  {s['path'].stem}  {s['title'] or 'untitled'}")
        return

    if args.session:
        matched = [s for s in sessions if args.session in str(s["path"])]
        if not matched:
            print(f"Session '{args.session}' not found.", file=sys.stderr)
            sys.exit(1)
        session = matched[0]
    else:
        session = pick_session(sessions)

    md = to_markdown(session["path"])

    raw = (session["title"] or session["path"].stem)[:80]
    words = re.split(r"[\s\-_]+", raw)
    slug = "-".join(w.lower() for w in words if w)[:60]
    date = (session["ts"] or "")[:10] or datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-{slug}.md"

    username = re.sub(r"[\s_]+", "-", args.user).lower() if args.user else None
    if not args.no_push and not username:
        default_user = os.environ.get("USER", "")
        prompt = f"Vyasa username [{default_user}]: " if default_user else "Vyasa username: "
        entered = input(prompt).strip()
        username = re.sub(r"[\s_]+", "-", (entered or default_user)).lower()
        if not username:
            print("Username required.", file=sys.stderr)
            sys.exit(1)
        confirm = input(f"Push to ~/projects/chats/{username}/ on aws-ai? [Y/n]: ").strip().lower()
        if confirm == "n":
            print("Aborted.")
            sys.exit(0)

    out_path = Path(args.out) if args.out else Path("/tmp") / filename
    out_path.write_text(md, encoding="utf-8")
    print(f"Written: {out_path}")

    if not args.no_push:
        push_to_remote(out_path, username)


if __name__ == "__main__":
    main()
