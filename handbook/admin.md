# Admin Handbook

Divami Agents has very little mutable configuration, which is good news for the person who owns setup. The tool does not run a server, does not store secrets in a database, and does not maintain a background daemon. Its administrative surface is limited to assistant path mapping, skill-set registration, repo-local RC files, and one password used for the packaged skill archive. This handbook covers those ownership points and the mistakes that usually break them.

## What You Actually Own

As the config owner, you are responsible for four contracts:

| Contract | Where it lives | Why it exists |
|---|---|---|
| Global assistant paths | `~/.config/divami-skills/llms.json` | Overrides the built-in<br/>destination folders for each<br/>assistant. |
| Registered skill sets | `~/agents/skillsets/` | Holds named sources that<br/>the CLI can discover and link. |
| Repo-local selection | `<repo>/.divami-skills.toml` | Declares which exact skills<br/>belong in a specific repo. |
| Archive password | `DIVAMI_AGENTS_PASSWORD` | Decrypts the packaged<br/>`skills.zip` download. |

The tool has sensible defaults for assistant paths. Only create `llms.json` when your environment differs from the code's built-in assumptions.

## Default Path Contract

The code defines four global assistant destinations and four repo-local destinations. These values are not discovered dynamically. If your environment uses different folders, you must override the global ones with `llms.json`.

### Global destinations

| Assistant key | Default path |
|---|---|
| `claude` | `~/.claude/skills` |
| `codex` | `~/.codex/skills` |
| `gemini` | `~/.gemini/skills` |
| `copilot` | `~/.copilot/skills` |

### Repo-local destinations

| Assistant key | Relative path under `--cwd` |
|---|---|
| `claude-local` | `.claude/skills` |
| `codex-local` | `.agents/skills` |
| `gemini-local` | `.gemini/skills` |
| `copilot-local` | `.github/skills` |

These repo-local mappings are hard-coded in the package. They are not user-configurable through a file today.

## Overriding Global Assistant Paths

The override file is `~/.config/divami-skills/llms.json`. It should be a JSON object whose keys match the global assistant names and whose values are absolute paths.

Example:

```json
{
  "claude": "/Users/yeshwanth/.claude/skills",
  "codex": "/Users/yeshwanth/.codex/skills",
  "gemini": "/Volumes/work/.gemini/skills",
  "copilot": "/Users/yeshwanth/.copilot/skills"
}
```

Why this shape and nothing else:

| Choice | Why it matters |
|---|---|
| Flat JSON object | The code loads one<br/>mapping and returns it<br/>as a `dict[str, Path]`. |
| Assistant name as key | The CLI resolves target<br/>names exactly from these<br/>keys. |
| Absolute path as value | Link and sync operations<br/>write directly to the returned<br/>path. Relative paths would<br/>be ambiguous. |

If the file does not exist, the defaults in code are used. If the file exists but omits one assistant, that assistant disappears from the global runtime map because the file replaces the defaults rather than merging into them.

## Registering Skill Sets Safely

The CLI discovers skill sets from `~/agents/skillsets` plus any roots passed with `--roots`. A registered skill set is simply a directory that contains one subdirectory per skill. The directory name becomes the skill-set name.

There are two ways to populate `~/agents/skillsets`:

1. Download and unpack the packaged release with `divami-skills unpack`
2. Register a local `skills/` directory with `divami-skills unpack --skills-folder ...`

For local registration, the command creates a symlink at `~/agents/skillsets/<repo-name>` pointing at the repo's `skills/` folder. It refuses to overwrite a non-symlink target. That is a deliberate safety check because a real directory at that location may contain manually managed content.

## Owning `.divami-skills.toml`

The repo-local RC file is not global state. It is a repo contract. Use it when a project wants a precise subset of skills rather than an entire skill set.

The file structure is:

```toml
[codex-local]
"divami-agents" = ["daksh", "doc-narrator"]

[claude-local]
"divami-agents" = ["daksh"]
```

The top-level table is the assistant target name. Inside it, each key is a skill-set name and each value is a list of exact skill folder names. `divami-skills sync` treats missing names as an error report, not as a fuzzy search.

## Password Handling

`DIVAMI_AGENTS_PASSWORD` is required in two places:

| Operation | Why the password is needed |
|---|---|
| `divami-skills unpack` without `--skills-folder` | Decrypts the downloaded release archive. |
| `python scripts/pack.py` | Encrypts the release archive before publish. |

The password is not stored in repo files. Keep it in your shell environment or secret manager. If unpack fails with "wrong password or corrupt zip", assume the password is wrong before assuming the archive is broken.

## Common Admin Failures

### A global assistant disappears from `list`

Most likely cause: `~/.config/divami-skills/llms.json` exists and does not include that assistant key.

Fix: add the missing key or remove the override file to fall back to built-in defaults.

### `unpack --skills-folder` refuses to register a skill set

Most likely cause: the destination under `~/agents/skillsets/<repo-name>` already exists as a real directory or points somewhere else.

Fix: inspect the target manually. Remove or rename it only if you are certain it is stale. The CLI exits rather than replacing it blindly.

### `sync` says a skill is missing from the set

Most likely cause: the skill name in `.divami-skills.toml` does not exactly match a folder name under the chosen skill set.

Fix: compare the RC file against the real directory names. The match is exact.

### Repo-local targets are written to the wrong place

Most likely cause: the command ran without `--cwd` or ran from an unexpected working directory.

Fix: pass `--cwd /absolute/path/to/repo` for any `*-local` action if there is any ambiguity about the current shell location.
