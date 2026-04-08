"""
Integration tests for scripts/preflight.py.

These tests run the REAL script against the REAL Daksh manifest (docs/.daksh/manifest.json).
No mocking. If a test fails here, there is a genuine issue in the manifest or the script —
fix the root cause, do not skip or mock your way past it.

Must be run from the Daksh project root:
    python -m pytest tests/test_preflight_integration.py -v

Kept in a separate file so unit tests (test_preflight.py) can be run in isolation:
    python -m pytest tests/test_preflight.py
"""

import subprocess
import sys
from pathlib import Path

import pytest

# Absolute path to the script so cwd changes in individual tests don't break resolution.
_SCRIPT = str(Path(__file__).parent.parent / "scripts" / "preflight.py")
_PROJECT_ROOT = str(Path(__file__).parent.parent)

# Approved stages to verify. Each entry is (stage_arg, module_or_None).
# Selected because each has at least 1 approval recorded in the manifest.
APPROVED_STAGES = [
    ("brd", None),
    ("roadmap", None),
    ("tasks", "PREFLIGHT"),
]


def run_preflight(*args: str) -> subprocess.CompletedProcess:
    """Invoke preflight.py as a subprocess from the project root."""
    return subprocess.run(
        [sys.executable, _SCRIPT, *args],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=_PROJECT_ROOT,
    )


@pytest.mark.integration
@pytest.mark.parametrize("stage,module", APPROVED_STAGES)
def test_preflight_exits_0_for_approved_stage(stage: str, module: str | None) -> None:
    """Preflight must exit 0 for every stage that has been approved."""
    cmd = [stage] if module is None else [stage, module]
    result = run_preflight(*cmd)
    assert result.returncode == 0, (
        f"preflight.py {' '.join(cmd)} exited {result.returncode}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


@pytest.mark.integration
@pytest.mark.parametrize("stage,module", APPROVED_STAGES)
def test_preflight_no_fail_lines_for_approved_stage(stage: str, module: str | None) -> None:
    """Preflight output must contain no [FAIL] lines for approved stages."""
    cmd = [stage] if module is None else [stage, module]
    result = run_preflight(*cmd)
    fail_lines = [line for line in result.stdout.splitlines() if line.startswith("[FAIL]")]
    assert not fail_lines, (
        f"preflight.py {' '.join(cmd)} produced FAIL lines:\n"
        + "\n".join(fail_lines)
    )


@pytest.mark.integration
def test_preflight_result_line_present() -> None:
    """Output must always end with a Result line (format contract)."""
    result = run_preflight("brd")
    result_lines = [l for l in result.stdout.splitlines() if l.startswith("Result:")]
    assert len(result_lines) == 1, (
        f"Expected exactly 1 Result: line, got {len(result_lines)}\n{result.stdout}"
    )


@pytest.mark.integration
def test_preflight_missing_manifest_exits_1(tmp_path: pytest.TempPathFactory) -> None:
    """Invoking the script where no manifest exists must exit 1 immediately."""
    result = subprocess.run(
        [sys.executable, _SCRIPT, "brd"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(tmp_path),  # no manifest.json here — script must detect and exit 1
    )
    assert result.returncode == 1
    assert "No Daksh pipeline found" in result.stdout + result.stderr
