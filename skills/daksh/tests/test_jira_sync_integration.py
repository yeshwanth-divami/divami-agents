import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPT = str(Path(__file__).parent.parent / "scripts" / "jira-sync.py")
_PROJECT_ROOT = str(Path(__file__).parent.parent)


@pytest.mark.integration
def test_jira_push_dry_run_against_real_manifest() -> None:
    result = subprocess.run(
        [sys.executable, _SCRIPT, "push", "--dry-run", "--module", "JIRA", "--force"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=_PROJECT_ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Creating Sprint: Sprint 2" in result.stdout
    assert "Creating Sprint: Sprint 3" in result.stdout
    assert "Push complete:" in result.stdout
