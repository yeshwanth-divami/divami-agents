Divami Agents is a small Python package that discovers skill sets on disk and materializes filesystem links into assistant-owned folders. It does not define a new skill runtime; it only helps assistants find the skill directories they already know how to load. This handbook is for the engineer changing the package, not the person using the TUI. By the end, you should understand where discovery happens, where linking happens, and which repository paths actually ship.

# Developer Handbook

## The Runtime Spine

Most of the runtime lives in four files:

| Path | Responsibility | Why it matters |
|---|---|---|
| [src/divami_skills/cli.py](/Users/yeshwanth/Code/Divami/divami-agents/src/divami_skills/cli.py) | Argument parsing and command dispatch | Keeps the shell surface thin. |
| [src/divami_skills/manager.py](/Users/yeshwanth/Code/Divami/divami-agents/src/divami_skills/manager.py) | Discovery, link, unlink, relay, and sync rules | Holds the real install contract. |
| [src/divami_skills/tui.py](/Users/yeshwanth/Code/Divami/divami-agents/src/divami_skills/tui.py) | Textual matrix UI over manager calls | Reuses manager behavior instead of duplicating it. |
| [scripts/pack.py](/Users/yeshwanth/Code/Divami/divami-agents/scripts/pack.py) | Builds `src/divami_skills/skills.zip` from `skills/` | Defines what packaged content ships. |

The shipping source of truth is the top-level `skills/` directory. The repo also has an `agents/` tree, but the current package and pack script do not consume it.

## Command Flow

The CLI currently exposes `unpack`, `list`, `link`, `unlink`, `sync`, `init`, and `tui`, plus the separate `divami-web-ui` entry point from [pyproject.toml](/Users/yeshwanth/Code/Divami/divami-agents/pyproject.toml). `cli.py` parses flags, builds a registry from `~/agents/skillsets` plus any `--roots`, resolves assistant destinations, and then hands the actual filesystem work to `manager.py`.

One non-obvious detail matters when reading the code: `unpack` is a local registration command in the current implementation. It resolves a `skills/` folder and creates a symlink in `~/agents/skillsets`; it does not fetch a release asset or ask for a password.

## Discovery and Install Rules

`build_registry()` merges the default machine-wide skill-set directory with any extra roots passed by the caller. `load_all_llms()` combines global assistant targets with repo-local targets like `.agents/skills` and `.claude/skills`. Link operations then iterate the chosen skill set and either create direct global symlinks or local relay symlinks under `<repo>/agents/<skill>`.

That relay is the main invariant worth protecting. Repo-local consumer folders do not point straight at the original skill source; they point at a relay inside the repo so multiple local assistant targets can share one stable source and prune it safely when the last consumer disappears.

## What To Verify After Changes

If you touch discovery, verify `divami-agents list --cwd /path/to/repo`. If you touch relay logic, verify both `codex-local` and `claude-local` installs against the same repo and confirm the shared relay under `<repo>/agents/`. If you touch the TUI, confirm that the symbols in `tui.py` still match the real manager status behavior instead of only the display legend.

## Updating Skills

Most skill folders in this repo are softlinks, so a skill update usually means editing the source and then opening a pull request. That is the normal path for `retrospect-and-update-skill` work: update the skill content, let the linked folders reflect it, and ship the change through a PR instead of hand-copying changes into every assistant folder.

## Current Unknowns

1. The repo carries both `skills/` and `agents/`, but only `skills/` is packaged today. If `agents/` is meant to become a runtime source, that contract should move from convention into code.
2. The web UI exists as `divami-web-ui`, but the root docs still treat the Textual UI as the primary interface. Any expansion there should document when a user should prefer one surface over the other.
