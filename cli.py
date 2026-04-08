import argparse
import getpass
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

def cmd_unpack(_args) -> None:
    zip_path = Path(__file__).parent / "skills.zip"
    if not zip_path.exists():
        print("Error: skills.zip not found in package.", file=sys.stderr)
        sys.exit(1)
    password = getpass.getpass("Password: ")
    UNPACK_DEST.mkdir(parents=True, exist_ok=True)
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.extractall(path=UNPACK_DEST, pwd=password.encode())
        print(f"Skills unpacked to {UNPACK_DEST}")
    except (RuntimeError, pyzipper.BadZipFile):
        print("Error: wrong password or corrupt zip.", file=sys.stderr)
        sys.exit(1)


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


def cmd_update_toml(args) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    reg = _registry(args)
    rc_path = manager.dump_rc(cwd, reg)
    print(f"Written: {rc_path}")


def cmd_tui(args) -> None:
    from .tui import SkillsApp
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    reg = _registry(args)
    SkillsApp(cwd=cwd, registry=reg).run()


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(prog="divami-skills")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    sub.add_parser("unpack", help=f"Unpack built-in skills to {UNPACK_DEST}")

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

    p_update = sub.add_parser("update-toml", help=f"Write current linked state to {manager.RC_FILENAME}")
    _add_common(p_update)

    args = parser.parse_args()

    dispatch = {
        "unpack":      cmd_unpack,
        "link":        cmd_link,
        "unlink":      cmd_unlink,
        "list":        cmd_list,
        "sync":        cmd_sync,
        "init":        cmd_init,
        "update-toml": cmd_update_toml,
        "tui":         cmd_tui,
    }

    if args.command in dispatch:
        dispatch[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)
