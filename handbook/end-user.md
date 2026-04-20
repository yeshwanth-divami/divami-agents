# End-User Handbook

Divami Agents is a terminal UI for browsing and installing reusable AI skills into the folders that different coding assistants already watch. In this repo a "skill set" is a collection of skill folders; the TUI lets you install or remove them into any supported assistant with a single keypress. This handbook is for the person who wants to use the TUI, not maintain it.

## Who This File Is For

Use this file if your question is "what do I run next?" and you are trying to get skills into Claude, Codex, Gemini, or Copilot. You do not need to understand how the package works internally. You only need to know which skill set you want and which assistant should receive it.

For installation prerequisites and environment setup, see [ops.md](ops.md).

## Opening the TUI

From the repo root:

```bash
make setup-tui
```

This is the recommended first-time path. It installs `uv` if it is missing, sets up the environment, unpacks the built-in skill archive, and opens the TUI.

On subsequent runs, `divami-agents` is available globally — no venv activation needed:

```bash
divami-agents tui
```

Pass `--cwd` if you want the TUI to also show repo-local assistant targets for a specific project:

```bash
divami-agents tui --cwd /path/to/repo
```

## What You See

The TUI opens a matrix. Each row is a skill set or an individual skill within a set. Each column is an assistant target. The status symbol in each cell tells you what is currently installed there.

| Symbol | Meaning |
|---|---|
| `●` | Installed locally in this repo for this LLM. |
| `◎` | Installed globally and available to all repos for this LLM. |
| `○` | Partially installed from this skill-set for this LLM. |
| `·` | Not installed in this repo for this LLM. |

| Assistant column | Global path | Repo-local path |
|---|---|---|
| `claude` / `claude-local` | `~/.claude/skills` | `./.claude/skills` |
| `codex` / `codex-local` | `~/.codex/skills` | `./.agents/skills` |
| `gemini` / `gemini-local` | `~/.gemini/skills` | `./.gemini/skills` |
| `copilot` / `copilot-local` | `~/.copilot/skills` | `./.github/skills` |

Press `t` to toggle between global and repo-local views.

During `unpack`, skill sets are registered under `~/agents/skillsets/<repo-name>` by default, as a symlink to that repo's `skills/` folder.

Skill sets are shown collapsed by default. Press `Enter` or `Space` on a skill-set row to expand it and see individual skills.

## Installing and Removing Skills

Navigate to the cell you want to change and press `Enter` or `Space`:

- If the cell is empty, the skill or skill set is installed into that assistant.
- If the cell is already installed, it is removed.

The TUI installs by symlink. There is no copy-mode toggle in the current UI.

After an install or removal, the matrix refreshes automatically. Press `r` to force a manual refresh if the display looks stale.

## Key Bindings

| Key | Action |
|---|---|
| `Enter` / `Space` | Install or remove the selected cell. |
| `t` | Toggle between global and repo-local assistant views. |
| `r` | Refresh the matrix from disk. |
| `q` | Quit. |

## If You Get Blocked

**The matrix is empty or shows no skill sets.** The skill archive has not been unpacked yet. Quit the TUI and run `make setup-tui` from the repo root, then reopen.

**An install does nothing or shows an error.** If you are on the repo-local view, make sure you opened the TUI with `--cwd /path/to/repo` pointing at the correct repo. Without `--cwd`, the local columns resolve to the directory the command was run from.

**The TUI opens but the assistant column you expect is missing.** The column names come from the runtime configuration. Global names are `claude`, `codex`, `gemini`, `copilot`. Repo-local names are the same with a `-local` suffix and only appear when `--cwd` is set.
