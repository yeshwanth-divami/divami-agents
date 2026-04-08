import argparse
import getpass
import os
import sys
from pathlib import Path

import pyzipper

from . import manager

SKILLSET_NAME = "divami-skills"
UNPACK_DEST = manager.SKILL_SETS_DIR / SKILLSET_NAME


# ── Shared helpers ────────────────────────────────────────────────────────────

def _parse_roots(raw: list[str] | None) -> list[Path]:
    """Accept both  -r /a /b  and  -r /a,/b  (or mixed)."""
    paths: list[Path] = []
    for item in (raw or []):
        for part in item.split(","):
            p = Path(part.strip()).expanduser().resolve()
            if not p.exists():
                print(f"Warning: --roots path does not exist: {p}", file=sys.stderr)
            paths.append(p)
    return paths


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--cwd", metavar="DIR",
        help="Treat this directory as the repo root (default: $CWD)",
    )
    p.add_argument(
        "-r", "--roots", metavar="PATH", nargs="+", action="append",
        help=(
            "Extra skill roots to include. Each root must contain a skills/ "
            "subfolder (or be one). The folder's basename becomes the skill-set "
            "name. Repeatable or comma-separated: -r /a /b  or  -r /a,/b"
        ),
    )


def _registry(args) -> manager.Registry:
    raw = [item for group in (args.roots or []) for item in group]
    return manager.build_registry(_parse_roots(raw))


# ── Commands ──────────────────────────────────────────────────────────────────

GITHUB_REPO = "yeshwanth-divami/divami-skills-dist"


def _resolve_skills_folder(skills_folder: str | None) -> Path:
    if skills_folder:
        root = Path(skills_folder).expanduser().resolve()
        if root.name == "skills":
            return root
        return root / "skills"
    return UNPACK_DEST


def _unpack_skillset_name(skills_folder: str | None, skillset_name: str | None) -> str:
    if skillset_name:
        return skillset_name
    if skills_folder:
        return _resolve_skills_folder(skills_folder).parent.name
    return SKILLSET_NAME


def _extract_zip(tmp_path: Path, dest: Path, password: str | None = None) -> None:
    with pyzipper.AESZipFile(tmp_path) as zf:
        pwd = password.encode() if password else None
        zf.extractall(path=dest, pwd=pwd)


def _register_local_skillset(source_dir: Path, skillset_name: str) -> None:
    target = manager.SKILL_SETS_DIR / skillset_name
    manager.SKILL_SETS_DIR.mkdir(parents=True, exist_ok=True)

    if target.is_symlink():
        if target.resolve() == source_dir.resolve():
            print(f"Skill-set already registered: {skillset_name} -> {source_dir}")
            return
        print(
            f"Error: skill-set '{skillset_name}' already points to {target.resolve()}",
            file=sys.stderr,
        )
        sys.exit(1)

    if target.exists():
        print(
            f"Error: skill-set target already exists and is not a symlink: {target}",
            file=sys.stderr,
        )
        sys.exit(1)

    if not source_dir.is_dir():
        print(f"Error: skills folder not found: {source_dir}", file=sys.stderr)
        sys.exit(1)

    target.symlink_to(source_dir, target_is_directory=True)
    print(
        f"Registered local skill-set from {source_dir} "
        f"at {target}/ as a softlink"
    )


def cmd_unpack(args) -> None:
    import tempfile
    import urllib.request
    from importlib.metadata import version

    skillset_name = _unpack_skillset_name(args.skills_folder, args.skillset_name)
    if args.skills_folder:
        source_dir = _resolve_skills_folder(args.skills_folder)
        _register_local_skillset(source_dir, skillset_name)
        return

    v = version("divami-agents")
    url = f"https://github.com/{GITHUB_REPO}/releases/download/v{v}/skills.zip"
    dest = UNPACK_DEST
    print(f"Downloading built-in skills from GitHub release v{v} ...")
    try:
        with urllib.request.urlopen(url) as resp, tempfile.NamedTemporaryFile(
            suffix=".zip", delete=False
        ) as tmp:
            tmp.write(resp.read())
            tmp_path = Path(tmp.name)
    except Exception as e:
        print(f"Error: download failed: {e}", file=sys.stderr)
        sys.exit(1)

    dest.mkdir(parents=True, exist_ok=True)
    try:
        try:
            _extract_zip(tmp_path, dest)
        except RuntimeError:
            password = os.environ.get("SKILLS_PASSWORD")
            if not password:
                print("Downloaded archive is encrypted; password required.")
                password = getpass.getpass("Password: ")
            _extract_zip(tmp_path, dest, password)
        print(f"Skills unpacked to {dest}")
    except (RuntimeError, pyzipper.BadZipFile):
        print("Error: wrong password or corrupt zip.", file=sys.stderr)
        sys.exit(1)
    finally:
        tmp_path.unlink(missing_ok=True)


def cmd_link(args) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    reg = _registry(args)
    llms = manager.load_all_llms(local_base=cwd)
    if args.llm not in llms:
        print(f"Unknown LLM '{args.llm}'. Known: {', '.join(llms)}", file=sys.stderr)
        sys.exit(1)
    llm_path = llms[args.llm]
    if manager.link_status(llm_path, args.skillset, reg) == "full":
        print(f"Already fully linked: {args.skillset} → {args.llm}")
        return
    manager.link(llm_path, args.skillset, reg)
    n = len(manager._skills_in(args.skillset, reg))
    print(f"Linked {n} skills from {args.skillset} → {llm_path}")


def cmd_unlink(args) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    reg = _registry(args)
    llms = manager.load_all_llms(local_base=cwd)
    if args.llm not in llms:
        print(f"Unknown LLM '{args.llm}'. Known: {', '.join(llms)}", file=sys.stderr)
        sys.exit(1)
    llm_path = llms[args.llm]
    manager.unlink(llm_path, args.skillset, reg)
    print(f"Unlinked {args.skillset} from {args.llm}")


def cmd_list(args) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    reg = _registry(args)
    llms = manager.load_all_llms(local_base=cwd)
    skillsets = manager.discover_skill_sets(reg)
    if not skillsets:
        print(f"No skill-sets found in {manager.SKILL_SETS_DIR}")
        return
    col_w = 14
    STATUS_ICON = {"full": "✓", "partial": "~", "none": "·"}
    header = f"{'Skill Set':<30}" + "".join(
        f"{manager.display_name(n):<{col_w}}" for n in llms
    )
    print(header)
    print("-" * len(header))
    for ss in skillsets:
        row = f"{ss:<30}" + "".join(
            f"{STATUS_ICON[manager.link_status(p, ss, reg)]:<{col_w}}"
            for p in llms.values()
        )
        print(row)


def cmd_sync(args) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    reg = _registry(args)
    rc_path = cwd / manager.RC_FILENAME
    if not rc_path.exists():
        print(f"No {manager.RC_FILENAME} found in {cwd}", file=sys.stderr)
        print("  Run `divami-skills init` to create one.")
        sys.exit(1)
    results = manager.sync(cwd, reg)
    if not results:
        print("Nothing to sync (no entries in RC file).")
        return
    total_linked = total_already = total_missing = 0
    for r in results:
        print(f"\n[{r.llm}  ←  {r.skillset}]")
        for s in r.linked:         print(f"  ✓  {s}  (linked)")
        for s in r.already_linked: print(f"  ·  {s}  (already linked)")
        for s in r.missing_from_set: print(f"  ✗  {s}  (not found in skill-set)")
        total_linked  += len(r.linked)
        total_already += len(r.already_linked)
        total_missing += len(r.missing_from_set)
    print(f"\nSummary: {total_linked} linked, {total_already} already linked, "
          f"{total_missing} missing from skill-sets")


def cmd_init(args) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    reg = _registry(args)
    rc_path = cwd / manager.RC_FILENAME
    if rc_path.exists() and not args.force:
        print(f"{rc_path} already exists. Use --force to overwrite.")
        sys.exit(1)
    llm_keys = list(manager.load_all_llms(local_base=cwd).keys())
    skillsets = manager.discover_skill_sets(reg)
    path = manager.write_rc_template(cwd, llm_keys, skillsets, reg)
    print(f"Created {path}")
    print("Edit it to specify which skills each LLM needs, then run `divami-skills sync`.")


def cmd_tui(args) -> None:
    from .tui import SkillsApp
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    reg = _registry(args)
    SkillsApp(cwd=cwd, registry=reg).run()


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(prog="divami-skills")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    p_unpack = sub.add_parser("unpack", help=f"Unpack built-in skills to {UNPACK_DEST}")
    p_unpack.add_argument(
        "--skills-folder",
        metavar="DIR",
        help=(
            "Use a local skill-set source instead of downloading from GitHub. "
            "If the path is a repo root, the command uses <path>/skills; if "
            "the path already ends with skills, it uses that directory directly."
        ),
    )
    p_unpack.add_argument(
        "--skillset-name",
        metavar="NAME",
        help=(
            "Name to register under ~/agents/skill-sets when --skills-folder "
            "is set. Defaults to the parent folder name of the resolved skills "
            "directory."
        ),
    )

    p_tui = sub.add_parser("tui", help="Interactive TUI to manage skill-set links")
    _add_common(p_tui)

    p_list = sub.add_parser("list", help="List skill-sets and their LLM links")
    _add_common(p_list)

    p_link = sub.add_parser("link", help="Link all skills in a skill-set to an LLM")
    p_link.add_argument("skillset")
    p_link.add_argument("llm", help="e.g. claude, claude-local, copilot-local …")
    _add_common(p_link)

    p_unlink = sub.add_parser("unlink", help="Remove skill-set links from an LLM")
    p_unlink.add_argument("skillset")
    p_unlink.add_argument("llm")
    _add_common(p_unlink)

    p_sync = sub.add_parser("sync", help=f"Apply {manager.RC_FILENAME} in the repo")
    _add_common(p_sync)

    p_init = sub.add_parser("init", help=f"Create a starter {manager.RC_FILENAME}")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing file")
    _add_common(p_init)

    args = parser.parse_args()

    dispatch = {
        "unpack": cmd_unpack,
        "link":   cmd_link,
        "unlink": cmd_unlink,
        "list":   cmd_list,
        "sync":   cmd_sync,
        "init":   cmd_init,
        "tui":    cmd_tui,
    }

    if args.command in dispatch:
        dispatch[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)
