# Ops Handbook

This project is operationally simple: it is a Python package that ships a CLI, a Textual TUI, and a packaged archive of skills. There is no long-running service to deploy. The main operations work are building the encrypted skill archive, publishing a release, validating that dependencies are present, and diagnosing path or packaging failures on a workstation. This handbook covers those runtime and release procedures.

## Runtime Footprint

Divami Agents runs entirely on the local filesystem. A command reads registered skill sets, then creates or removes filesystem entries in assistant-owned skill directories.

```mermaid
flowchart LR
    A["skills/<skill>/...<br/>authoring source"] --> B["scripts/pack.py<br/>build encrypted zip"]
    B --> C["GitHub release<br/>skills.zip asset"]
    C --> D["divami-skills unpack<br/>download + extract"]
    D --> E["~/agents/skill-sets/<set><br/>registered source"]
    E --> F["divami-skills link or sync<br/>install selected skills"]
    F --> G["assistant skill folders<br/>global or repo-local"]
```

The shipping asset is `src/divami_skills/skills.zip`. The code that consumes it lives in `src/divami_skills/cli.py`. The working source for that archive is the repo's top-level `skills/` directory.

## Environment Requirements

The package metadata declares these runtime dependencies:

| Dependency | Source | Purpose |
|---|---|---|
| `pyzipper` | `pyproject.toml` | AES zip extraction and creation. |
| `textual` | `pyproject.toml` | Terminal UI runtime. |
| `tomli` | `pyproject.toml` | TOML parsing on Python<br/>< 3.11. |

The build system is `setuptools`. The Makefile assumes `uv` is available for environment management and publishing.

## Local Setup

From the repo root:

```bash
uv venv .venv --clear
uv pip install --python .venv pyzipper textual build twine tomli
```

This mirrors the `venv` target in [Makefile](/Users/yeshwanth/Code/Divami/divami-agents/Makefile). It is the fastest way to get the packaging toolchain into a clean environment.

## Building the Encrypted Skill Archive

The archive build is a local packaging step, not part of ordinary end-user usage.

Required input:

| Input | Type | Default | Why it matters |
|---|---|---|---|
| `DIVAMI_AGENTS_PASSWORD` | env var | none | Used as the AES<br/>zip password during pack. |

Run:

```bash
DIVAMI_AGENTS_PASSWORD="..." .venv/bin/python scripts/pack.py
```

Or through Make:

```bash
make pack
```

What happens:

1. `scripts/pack.py` walks every file under `skills/`
2. It writes them into `src/divami_skills/skills.zip`
3. The zip uses LZMA compression and WinZip AES encryption

The script exits immediately if `DIVAMI_AGENTS_PASSWORD` is missing. That is intentional because an unencrypted archive would break the distribution contract.

## Publishing a Release

The `publish` target in [Makefile](/Users/yeshwanth/Code/Divami/divami-agents/Makefile) performs the release sequence. It is the source of truth for the intended publish order.

Run:

```bash
make publish
```

Optional variable:

| Name | Type | Default | Meaning |
|---|---|---|---|
| `BUMP` | `patch|minor|major` | `patch` | Version bump applied<br/>before wheel build and<br/>release creation. |

The publish target:

1. Builds the encrypted archive through `pack`
2. Bumps the version in `pyproject.toml`
3. Rebuilds `dist/`
4. Uploads the wheel with Twine to the `divami` repository target
5. Creates a GitHub release in `yeshwanth-divami/divami-skills-dist`
6. Attaches `src/divami_skills/skills.zip` as the `skills.zip` asset

## Operational Checks

There is no dedicated test suite in the root project today, so operational verification is mainly command-level.

Recommended checks after packaging or installation changes:

```bash
python -c "from divami_skills import cli, manager; print('import ok')"
python - <<'PY'
from divami_skills import manager
print(manager.SKILL_SETS_DIR)
print(manager.GLOBAL_LLM_DEFAULTS)
print(manager.LOCAL_LLM_RELPATHS)
PY
divami-skills list
```

These checks confirm importability, resolved path contracts, and basic skill-set discovery.

## Failure Modes Worth Knowing

### `Error: DIVAMI_AGENTS_PASSWORD is required.`

Cause: the password env var is missing for `unpack` or `pack`.

Fix: export the variable in the same shell session that runs the command.

### `wrong DIVAMI_AGENTS_PASSWORD or corrupt zip`

Cause: decryption failed during unpack.

Fix: verify the password first. If the password is correct, re-download and try again.

### `No skill-sets found in ~/agents/skill-sets`

Cause: no skill set has been unpacked or registered yet, or discovery depends on an extra root that was not passed.

Fix: run `divami-skills unpack` or use `--roots` with `list`, `link`, `init`, or `sync`.

### TUI starts but actions do not appear to work

Cause: the selected assistant path is not the one you intended, often because the view is showing global targets when you expected repo-local targets.

Fix: press `t` to switch view and confirm the status line includes the expected `cwd`.

## Boundaries

The root project's operational scope ends at packaging and local filesystem installation. It does not provision the target assistants themselves, validate that an assistant actively loaded a skill after installation, or synchronize across machines. If you need those guarantees, they belong in a higher-level workstation setup process, not in this package.
