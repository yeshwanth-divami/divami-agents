"""Core logic: discover skill-sets and manage per-skill symlinks into LLM dirs."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

SKILL_SETS_DIR = Path.home() / "agents" / "skill-sets"
CONFIG_PATH = Path.home() / ".config" / "divami-skills" / "llms.json"
RC_FILENAME = ".divami-skills.toml"

# ── LLM path definitions ──────────────────────────────────────────────────────

GLOBAL_LLM_DEFAULTS: dict[str, str] = {
    "claude":  str(Path.home() / ".claude"  / "skills"),
    "codex":   str(Path.home() / ".codex"   / "skills"),
    "gemini":  str(Path.home() / ".gemini"  / "skills"),
    "copilot": str(Path.home() / ".copilot" / "skills"),
}

LOCAL_LLM_RELPATHS: dict[str, str] = {
    "claude":  ".claude/skills",
    "codex":   ".agents/skills",
    "gemini":  ".gemini/skills",
    "copilot": ".github/skills",
}

_LOCAL_SUFFIX = "-local"

LinkStatus = Literal["full", "partial", "none"]

# ── Registry ──────────────────────────────────────────────────────────────────
# Maps skillset_name -> the directory that directly contains individual skill dirs.
# Standard:  "divami-skills" -> ~/agents/skill-sets/divami-skills/
# Extra root "/repo":      "repo"       -> /repo/skills/   (or /repo/ if no skills/ subdir)

Registry = dict[str, Path]


def build_registry(extra_roots: list[Path] | None = None) -> Registry:
    """Build the full skill-set registry from SKILL_SETS_DIR + any extra roots."""
    reg: Registry = {}

    if SKILL_SETS_DIR.exists():
        for d in SKILL_SETS_DIR.iterdir():
            if d.is_dir() and not d.name.startswith("."):
                reg[d.name] = d

    for root in (extra_roots or []):
        root = root.resolve()
        # A root can either be:
        #   /some/repo  → look for /some/repo/skills/ first
        #   /some/repo/skills  → already the skills dir
        candidate = root / "skills"
        skills_dir = candidate if candidate.is_dir() else root
        if skills_dir.is_dir():
            reg[root.name] = skills_dir

    return reg


# ── LLM helpers ───────────────────────────────────────────────────────────────

def load_global_llms() -> dict[str, Path]:
    if CONFIG_PATH.exists():
        data = json.loads(CONFIG_PATH.read_text())
    else:
        data = GLOBAL_LLM_DEFAULTS
    return {name: Path(path) for name, path in data.items()}


def get_local_llms(base: Path) -> dict[str, Path]:
    return {f"{name}{_LOCAL_SUFFIX}": base / relpath
            for name, relpath in LOCAL_LLM_RELPATHS.items()}


def load_all_llms(local_base: Path | None = None) -> dict[str, Path]:
    """Return LLMs in paired order: claude, claude-local, codex, codex-local, …"""
    global_llms = load_global_llms()
    local_llms = get_local_llms(local_base) if local_base is not None else {}
    result: dict[str, Path] = {}
    for name, path in global_llms.items():
        result[name] = path
        local_key = f"{name}{_LOCAL_SUFFIX}"
        if local_key in local_llms:
            result[local_key] = local_llms[local_key]
    return result


def is_local(llm_name: str) -> bool:
    return llm_name.endswith(_LOCAL_SUFFIX)


def display_name(llm_name: str) -> str:
    if is_local(llm_name):
        base = llm_name[: -len(_LOCAL_SUFFIX)].capitalize()
        return f"·{base}"
    return llm_name.capitalize()


def save_global_llms(llms: dict[str, Path]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({k: str(v) for k, v in llms.items()}, indent=2))


# ── Skill-set / skill discovery ───────────────────────────────────────────────

def discover_skill_sets(registry: Registry | None = None) -> list[str]:
    if registry is not None:
        return sorted(registry.keys())
    if not SKILL_SETS_DIR.exists():
        return []
    return sorted(d.name for d in SKILL_SETS_DIR.iterdir()
                  if d.is_dir() and not d.name.startswith("."))


def _skills_in(skillset: str, registry: Registry | None = None) -> list[Path]:
    """Non-hidden skill dirs inside a skill-set, sorted."""
    if registry is not None:
        d = registry.get(skillset)
    else:
        d = SKILL_SETS_DIR / skillset
    if d is None or not d.exists():
        return []
    return sorted(
        [s for s in d.iterdir() if s.is_dir() and not s.name.startswith(".")],
        key=lambda p: p.name,
    )


# ── Skillset-level link ops ───────────────────────────────────────────────────

def link_status(llm_path: Path, skillset: str,
                registry: Registry | None = None) -> LinkStatus:
    skills = _skills_in(skillset, registry)
    if not skills:
        return "none"
    linked = sum(1 for s in skills if (llm_path / s.name).is_symlink())
    if linked == 0:
        return "none"
    return "full" if linked == len(skills) else "partial"


def link(llm_path: Path, skillset: str, registry: Registry | None = None) -> None:
    llm_path.mkdir(parents=True, exist_ok=True)
    for skill in _skills_in(skillset, registry):
        target = llm_path / skill.name
        if not target.exists() and not target.is_symlink():
            target.symlink_to(skill)


def unlink(llm_path: Path, skillset: str, registry: Registry | None = None) -> None:
    for skill in _skills_in(skillset, registry):
        target = llm_path / skill.name
        if target.is_symlink():
            target.unlink()


# ── Individual-skill link ops ─────────────────────────────────────────────────

def skill_is_linked(llm_path: Path, skill_name: str) -> bool:
    return (llm_path / skill_name).is_symlink()


def link_skill(llm_path: Path, skillset: str, skill_name: str,
               registry: Registry | None = None) -> None:
    llm_path.mkdir(parents=True, exist_ok=True)
    if registry is not None:
        skill = registry[skillset] / skill_name
    else:
        skill = SKILL_SETS_DIR / skillset / skill_name
    target = llm_path / skill_name
    if not target.exists() and not target.is_symlink():
        target.symlink_to(skill)


def unlink_skill(llm_path: Path, skill_name: str) -> None:
    target = llm_path / skill_name
    if target.is_symlink():
        target.unlink()


# ── RC file (.divami-skills.toml) ────────────────────────────────────────────────

@dataclass
class SkillSyncResult:
    llm: str
    skillset: str
    linked: list[str] = field(default_factory=list)
    already_linked: list[str] = field(default_factory=list)
    missing_from_set: list[str] = field(default_factory=list)


def read_rc(cwd: Path) -> dict[str, dict[str, list[str]]]:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redef]
    rc = cwd / RC_FILENAME
    if not rc.exists():
        return {}
    with rc.open("rb") as f:
        data = tomllib.load(f)
    result: dict[str, dict[str, list[str]]] = {}
    for llm_key, mapping in data.items():
        if isinstance(mapping, dict):
            result[llm_key] = {ss: list(skills) for ss, skills in mapping.items()}
    return result


def sync(cwd: Path, registry: Registry | None = None) -> list[SkillSyncResult]:
    rc = read_rc(cwd)
    if not rc:
        return []
    all_llms = load_all_llms(local_base=cwd)
    results: list[SkillSyncResult] = []
    for llm_key, skillsets in rc.items():
        llm_path = all_llms.get(llm_key)
        if llm_path is None:
            continue
        for skillset, wanted in skillsets.items():
            available = {s.name for s in _skills_in(skillset, registry)}
            res = SkillSyncResult(llm=llm_key, skillset=skillset)
            for skill_name in wanted:
                if skill_name not in available:
                    res.missing_from_set.append(skill_name)
                elif skill_is_linked(llm_path, skill_name):
                    res.already_linked.append(skill_name)
                else:
                    link_skill(llm_path, skillset, skill_name, registry)
                    res.linked.append(skill_name)
            results.append(res)
    return results


def write_rc_template(cwd: Path, llm_keys: list[str], skillsets: list[str],
                      registry: Registry | None = None) -> Path:
    all_llms = load_all_llms(local_base=cwd)
    lines = ["# .divami-skills.toml — run `divami-skills sync` to apply\n"]
    for llm_key in llm_keys:
        llm_path = all_llms.get(llm_key)
        if llm_path is None:
            continue
        lines.append(f"[{llm_key}]")
        for ss in skillsets:
            linked = [s.name for s in _skills_in(ss, registry)
                      if skill_is_linked(llm_path, s.name)]
            skills_str = ", ".join(f'"{s}"' for s in linked)
            lines.append(f'"{ss}" = [{skills_str}]')
        lines.append("")
    rc = cwd / RC_FILENAME
    rc.write_text("\n".join(lines))
    return rc
