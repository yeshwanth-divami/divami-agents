#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_PATH = Path("docs/.daksh/manifest.json")

STAGE_MAP = {
    "onboard": {"default": "00", "small": "00+10"},
    "vision": {"default": "10", "small": "00+10"},
    "brd": {"default": "20", "small": "20"},
    "roadmap": {"default": "30", "small": "30"},
    "prd": {"default": "40a:{}", "small": "40a+40b:{}"},
    "trd": {"default": "40b:{}", "small": "40a+40b:{}"},
    "tasks": {"default": "40c:{}", "small": "40c:{}"},
    "impl": {"default": "50:{}", "small": "50:{}"},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_key(stage: str, module: str | None, weight_class: str) -> str:
    mapping = STAGE_MAP.get(stage)
    if not mapping:
        sys.exit(f"ERROR: Unknown stage '{stage}'.")
    template = mapping.get(weight_class, mapping["default"])
    if "{}" in template:
        if not module:
            sys.exit(f"ERROR: Stage '{stage}' requires a MODULE argument.")
        return template.format(module.upper())
    return template


def prior_stage_key(key: str) -> str | None:
    prefix, _, module = key.partition(":")
    chain = ["00+10", "20", "30", "40a+40b", "40c", "50"]
    current = prefix.split("+")[-1]
    if current not in chain or current == "00+10":
        return None
    prior = chain[chain.index(current) - 1]
    return f"{prior}:{module}" if module else prior


def module_from_key(key: str) -> str | None:
    _, _, module = key.partition(":")
    return module or None


def task_file_for_module(module: str) -> Path:
    return Path(f"docs/implementation/{module}/tasks.md")


def iter_task_dependencies(tasks_path: Path) -> list[tuple[str, list[str]]]:
    entries: list[tuple[str, list[str]]] = []
    current_task: str | None = None
    for line in tasks_path.read_text().splitlines():
        heading = re.match(r"^####\s+(TASK-[A-Z0-9-]+):", line)
        if heading:
            current_task = heading.group(1)
            continue
        depends = re.match(r"^- \*\*Depends on:\*\*\s*(.+)$", line)
        if current_task and depends:
            raw = depends.group(1).strip()
            if raw.lower() == "none":
                entries.append((current_task, []))
            else:
                deps = [part.strip() for part in raw.split(",") if part.strip()]
                entries.append((current_task, deps))
            current_task = None
    return entries


def git_working_tree_clean() -> bool:
    completed = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    return completed.returncode == 0 and not completed.stdout.strip()


def result(level: str, message: str, hard: bool = False) -> dict:
    return {"level": level, "message": message, "hard": hard}


def iter_output_paths(output: str | list[str] | None) -> list[Path]:
    if not output:
        return []
    return [Path(p) for p in (output if isinstance(output, list) else [output])]


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        sys.exit("ERROR: No Daksh pipeline found. Run /daksh init first.")
    try:
        return json.loads(MANIFEST_PATH.read_text())
    except json.JSONDecodeError as exc:
        sys.exit(f"ERROR: Invalid manifest JSON: {exc}")


def base_checks(manifest: dict, key: str) -> list[dict]:
    checks = [result("PASS", "Manifest exists")]
    stages = manifest.get("stages", {})
    if key not in stages:
        return checks + [result("FAIL", f"Stage {key} not registered in manifest", True)]
    checks.append(result("PASS", f"Stage {key} registered in manifest"))
    prior_key = prior_stage_key(key)
    if not prior_key:
        return checks
    prior = stages.get(prior_key)
    if not prior:
        return checks + [result("FAIL", f"Prior stage {prior_key} not registered in manifest", True)]
    required = manifest.get("rules", {}).get("approvals_per_gate", 1)
    approvals = len(prior.get("approvals", []))
    approved = approvals >= required
    checks.append(result("PASS" if approved else "WARN",
                         f"Prior stage {prior_key} approved: {approvals}/{required}",
                         False))
    hard_hash = key.startswith("50:")
    for path in iter_output_paths(prior.get("output")):
        exists = path.exists()
        checks.append(result("PASS" if exists else ("FAIL" if hard_hash else "WARN"),
                             f"{path} exists on disk", hard_hash and not exists))
        expected = (prior.get("doc_hash") or {}).get(str(path))
        if exists and expected:
            matches = sha256(path) == expected
            level = "PASS" if matches else ("FAIL" if hard_hash else "WARN")
            checks.append(result(level, f"{path} hash matches manifest", hard_hash and not matches))
    return checks


def pending_approval_checks(manifest: dict, module: str) -> list[dict]:
    """Fail if any module planning stage is pending_approval.

    Checks the authoritative source (stage status in manifest) first.
    Then cross-references change_records for a helpful diagnostic message,
    but the block decision is based on stage state, not CR metadata.
    """
    checks: list[dict] = []
    stages = manifest.get("stages", {})
    change_records = manifest.get("change_records", {})

    # Build a reverse index: doc_path -> CR-ID for open CRs (diagnostic only)
    cr_by_doc: dict[str, str] = {}
    for cr_id, cr in change_records.items():
        if cr.get("status") != "OPEN":
            continue
        for doc in cr.get("touched_docs", []):
            cr_by_doc[doc] = cr_id

    # Check each planning stage for this module by its authoritative status
    found_pending = False
    for stage_prefix in ("40a", "40b", "40c", "40a+40b"):
        stage_key = f"{stage_prefix}:{module}"
        stage_data = stages.get(stage_key)
        if not stage_data:
            continue
        if stage_data.get("status") != "pending_approval":
            continue
        found_pending = True
        # Try to identify the CR responsible for diagnostic clarity
        output = stage_data.get("output")
        output_paths = output if isinstance(output, list) else [output] if output else []
        cr_hint = None
        for p in output_paths:
            if p in cr_by_doc:
                cr_hint = cr_by_doc[p]
                break
        msg = f"Stage {stage_key} is pending_approval"
        if cr_hint:
            msg += f" (via {cr_hint}). Run `/daksh approve {cr_hint}` first"
        checks.append(result("WARN", msg, False))

    if not found_pending:
        checks.append(result("PASS", f"No pending_approval stages for {module}"))

    return checks


def impl_checks(manifest: dict, key: str, task_id: str | None = None) -> list[dict]:
    is_clean = git_working_tree_clean()
    checks = [result("PASS" if is_clean else "FAIL", "Git working tree clean", not is_clean)]
    module = module_from_key(key)
    if not module:
        return checks

    # Check for pending_approval docs from open CRs
    checks.extend(pending_approval_checks(manifest, module))
    traceability = manifest.get("traceability")
    if not isinstance(traceability, dict):
        return checks + [result("FAIL", "Manifest traceability map missing", True)]

    all_deps = iter_task_dependencies(task_file_for_module(module))

    if task_id:
        # Task-scoped: only check dependencies for the specified task
        task_deps = [(tid, deps) for tid, deps in all_deps if tid == task_id]
        if not task_deps:
            checks.append(result("FAIL",
                                 f"{task_id} not found in tasks.md — cannot verify dependencies",
                                 True))
    else:
        # Fallback: module-wide (no task specified — warn about reduced precision)
        task_deps = all_deps
        if task_deps:
            checks.append(result("WARN",
                                 "No TASK-ID provided — checking all module dependencies "
                                 "(pass --task TASK-ID for precise checks)"))

    for tid, dependencies in task_deps:
        if not dependencies:
            continue
        for dependency in dependencies:
            trace = traceability.get(dependency, "")
            if isinstance(trace, dict):
                done = str(trace.get("status", "")).lower() == "done"
            else:
                done = str(trace).lower() == "done"
            message = (
                f"{tid} dependency {dependency} done"
                if done else f"{tid} dependency {dependency} not done"
            )
            checks.append(result("PASS" if done else "FAIL", message, not done))
    return checks


def write_risk_entries(manifest: dict, stage_key: str, checks: list[dict]) -> None:
    """Append a risk register entry for each WARN check, deduplicating by message."""
    warns = [c for c in checks if c["level"] == "WARN"]
    if not warns:
        return
    register = manifest.setdefault("risk_register", [])
    existing_msgs = {e["reason"] for e in register}
    now = datetime.now(timezone.utc).isoformat()
    seq = len(register) + 1
    for w in warns:
        if w["message"] in existing_msgs:
            continue
        register.append({
            "risk_id": f"RISK-{seq:03d}",
            "stage": stage_key,
            "reason": w["message"],
            "detected_at": now,
            "status": "open",
            "acknowledged_by": None,
            "acknowledged_at": None,
        })
        existing_msgs.add(w["message"])
        seq += 1
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))


def print_table(stage: str, module: str | None, checks: list[dict],
                manifest: dict | None = None, key: str = "") -> int:
    label = f"{stage} {module.upper()}" if module else stage
    hard_failures = sum(1 for c in checks if c["hard"] and c["level"] == "FAIL")
    warnings = sum(1 for c in checks if c["level"] == "WARN")
    print(f"Preflight: {label}".rstrip())
    print("─" * 49)
    for check in checks:
        print(f"[{check['level']}] {check['message']}")
    print("─" * 49)
    if hard_failures:
        verdict = "BLOCKED"
    elif warnings:
        verdict = "WARN"
    else:
        verdict = "PASS"
    print(f"Result: {verdict} — {hard_failures} hard failure(s), {warnings} warning(s)")
    if warnings and manifest is not None:
        write_risk_entries(manifest, key, checks)
        print("  ↳ Risk entries written to manifest.risk_register — run `/daksh risk-profile` to review")
    return 1 if hard_failures else 0


def run_checks(manifest: dict, key: str, task_id: str | None = None) -> list[dict]:
    checks = base_checks(manifest, key)
    if key.startswith("50:"):
        checks.extend(impl_checks(manifest, key, task_id))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage")
    parser.add_argument("module", nargs="?", default=None)
    parser.add_argument("--task", default=None,
                        help="TASK-ID to scope dependency checks (impl stage only)")
    args = parser.parse_args()
    manifest = load_manifest()
    key = resolve_key(args.stage, args.module, manifest.get("weight_class", "medium"))
    return print_table(args.stage, args.module,
                       run_checks(manifest, key, args.task),
                       manifest=manifest, key=key)


if __name__ == "__main__":
    raise SystemExit(main())
