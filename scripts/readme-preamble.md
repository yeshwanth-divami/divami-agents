# Divami Agents

Divami Agents is a Python package and skill workspace for installing reusable agent skills into the folders that Claude, Codex, Gemini, and Copilot already watch. The repo carries three things together: the shipping CLI and TUI under `src/divami_skills/`, the source skill library under `skills/`, and supporting docs for the people who use, operate, and extend the tool. If you are opening this repo cold, the important model is simple: skill sets are discovered from disk, then linked into assistant-specific global or repo-local folders. By the end of this README, you should know which handbook to open next and where the shipped skills live.

Choose the handbook that matches the job in front of you:

- [handbook/end-user.md](handbook/end-user.md) is the quickest path if you want to open the TUI and install skills.
- [handbook/ops.md](handbook/ops.md) covers workstation setup, packaging, and release operations.
- [handbook/developer.md](handbook/developer.md) explains how the CLI, manager layer, and TUI fit together.
- [handbook/admin.md](handbook/admin.md) covers path overrides, skill-set registration, and repo-local policy files.

One repo detail matters before you go deeper: the runtime installs from skill sets on disk, and this repository's packaged source of truth is the top-level [`skills/`](skills) directory. The parallel [`agents/`](agents) tree exists in the repo, but the current packaging and install path described in the handbooks runs through `skills/`, `scripts/pack.py`, and `src/divami_skills/`.

Following are the skills currently included in the repo and their purposes.