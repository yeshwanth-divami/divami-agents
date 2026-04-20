Divami Agents has a small admin surface: you control where assistant skill folders live, which skill sets are registered on a machine, and which repo-local subsets a project wants to sync. The tool does not run a server or keep background state, so most admin work is filesystem verification rather than service management. This handbook covers the ownership points that can actually break installs on a workstation. By the end, you should know which file to inspect first when a target, skill set, or repo policy looks wrong.

# Admin Handbook

## What You Own

| Contract | Where it lives | Why it matters |
|---|---|---|
| Global assistant paths | `~/.config/divami-skills/llms.json` | Overrides the built-in destinations for global installs. |
| Registered skill sets | `~/agents/skillsets/` | Gives the CLI and TUI named skill sources to discover. |
| Repo policy file | `<repo>/.divami-skills.toml` | Declares which skills a repo wants for each local target. |

The code-path behind these contracts lives in [manager.py](/Users/yeshwanth/Code/Divami/divami-agents/src/divami_skills/manager.py). If an install looks wrong, the failure is usually one of those three inputs rather than the TUI itself.

## Global Path Overrides

Global installs default to `~/.claude/skills`, `~/.codex/skills`, `~/.gemini/skills`, and `~/.copilot/skills`. Override them only when your workstation uses different locations.

```json
{
  "claude": "/Users/name/.claude/skills",
  "codex": "/Users/name/.codex/skills",
  "gemini": "/Users/name/.gemini/skills",
  "copilot": "/Users/name/.copilot/skills"
}
```

Why this shape: `load_global_llms()` reads one flat JSON object and replaces the defaults instead of merging with them. If you omit a key from `llms.json`, that assistant disappears from the global runtime map until the key is restored.

## Registering a Skill Set

`divami-agents unpack` does not download anything in the current code. It registers a local `skills/` directory by creating a symlink under `~/agents/skillsets/<name>`, and the TUI later discovers that symlink as one named skill set. If the destination already exists as a real directory, registration stops on purpose so the tool does not overwrite user-managed content.

Use `divami-agents unpack --skills-folder /path/to/repo/skills --skillset-name team-skills` when the default name or current directory is not what you want. For how that registration is later consumed during installs, see [developer.md](developer.md).

## Repo Policy Files

Repo-local sync reads `.divami-skills.toml` from the repo root and applies only the listed skill names for each local target. The filename matters: the runtime expects `.divami-skills.toml`, not `.divami-agents.toml`.

```toml
[codex-local]
"divami-agents" = ["daksh", "doc-narrator"]
```

The table name must match a resolved target such as `codex-local`, and each value must exactly match a skill folder inside the named skill set. `sync` treats missing names as an error report, not a fuzzy lookup.

## When Something Breaks

If a global assistant is missing, inspect `llms.json` first. If no skill sets appear, inspect `~/agents/skillsets/` next and confirm the symlink target still exists. If repo-local sync skips expected skills, inspect `.divami-skills.toml` and compare the skill names to the real folders under the registered skill set.
