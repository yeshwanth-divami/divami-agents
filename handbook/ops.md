Divami Agents is operationally light: it is a local Python package with a CLI, a Textual TUI, and a packaged zip of skills built from this repo. There is no service to deploy and no background worker to monitor, so most operational work is workstation setup, packaging, and release hygiene. This handbook covers the commands that matter when you need to bootstrap a machine or publish updated package content. By the end, you should know which Make targets are real, which artifacts are produced, and how to check the install path quickly.

# Ops Handbook

## Workstation Setup

The simplest bootstrap path from this repo is:

```bash
make setup-tui
```

In the current [Makefile](/Users/yeshwanth/Code/Divami/divami-agents/Makefile), that target installs `uv` through Homebrew if it is missing, installs the package globally with `uv tool install --reinstall .`, registers the local `skills/` directory with `divami-agents unpack`, and launches `divami-agents tui`.

If you only need a local packaging environment, use:

```bash
make venv
```

That creates `.venv` and installs the repo's packaging dependencies there. The runtime package metadata itself lives in [pyproject.toml](/Users/yeshwanth/Code/Divami/divami-agents/pyproject.toml).

## Packaging And Release

The package ships skill content from the top-level `skills/` directory into `src/divami_skills/skills.zip`. In the current implementation, [scripts/pack.py](/Users/yeshwanth/Code/Divami/divami-agents/scripts/pack.py) creates a normal zip with `zipfile`; it does not encrypt the archive and it does not require a password environment variable.

Build the zip with:

```bash
make pack
```

Publish with:

```bash
make publish
```

`publish` runs `pack`, bumps the version with `uv version --bump`, rebuilds `dist/`, uploads the wheel with Twine, and creates a GitHub release asset from `src/divami_skills/skills.zip`.

## Fast Operational Checks

Use `divami-agents list --cwd /path/to/repo` to verify skill-set discovery and target resolution together. Use `python3 scripts/update-readme.py` after README-source edits so the generated root README stays in sync with `scripts/readme-preamble.md`. If packaging changed, confirm that `src/divami_skills/skills.zip` was recreated before you publish.

## When Something Fails

If `list` shows no skill sets, inspect `~/agents/skillsets/` and rerun `divami-agents unpack` from a repo that contains `skills/`. If local installs land in the wrong repo, rerun the command with the correct `--cwd`. If `make publish` fails after version bump or wheel build, inspect the exact step in `Makefile` rather than assuming the zip step was the problem.
