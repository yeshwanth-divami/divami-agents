import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import preflight


def write(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return preflight.sha256(path)


def manifest_with_stage(tmp: Path) -> dict:
    client = tmp / "docs/client-context.md"
    vision = tmp / "docs/vision.md"
    client_hash = write(client, "client")
    vision_hash = write(vision, "vision")
    return {
        "rules": {"approvals_per_gate": 1},
        "stages": {
            "00+10": {
                "output": [str(client), str(vision)],
                "approvals": [{"by": "Y"}],
                "doc_hash": {str(client): client_hash, str(vision): vision_hash},
            },
            "20": {"output": str(tmp / "docs/business.md"), "approvals": []},
        },
    }


def manifest_with_impl_stage(tmp: Path, traceability: dict[str, str] | None = None) -> dict:
    manifest = manifest_with_stage(tmp)
    tasks = tmp / "docs/implementation/PREFLIGHT/tasks.md"
    tasks.parent.mkdir(parents=True, exist_ok=True)
    tasks.touch(exist_ok=True)
    manifest["stages"]["40c:PREFLIGHT"] = {
        "output": str(tasks),
        "approvals": [{"by": "Y"}],
        "doc_hash": {str(tasks): preflight.sha256(tasks)},
    }
    manifest["stages"]["50:PREFLIGHT"] = {"output": str(tmp / "changes"), "approvals": []}
    manifest["traceability"] = traceability or {}
    return manifest


class BaseChecksTests(unittest.TestCase):
    def test_base_checks_pass_for_brd(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            checks = preflight.base_checks(manifest_with_stage(Path(tmpdir)), "20")
        self.assertEqual([c["level"] for c in checks], ["PASS"] * 7)

    def test_stage_not_registered_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            checks = preflight.base_checks(manifest_with_stage(Path(tmpdir)), "30")
        self.assertEqual(checks[-1]["level"], "FAIL")
        self.assertTrue(checks[-1]["hard"])

    def test_prior_stage_not_approved_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest = manifest_with_stage(Path(tmpdir))
            manifest["stages"]["00+10"]["approvals"] = []
            checks = preflight.base_checks(manifest, "20")
        self.assertEqual(checks[2]["level"], "FAIL")
        self.assertTrue(checks[2]["hard"])

    def test_missing_prior_output_warns_for_doc_stage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest = manifest_with_stage(Path(tmpdir))
            Path(manifest["stages"]["00+10"]["output"][0]).unlink()
            checks = preflight.base_checks(manifest, "20")
        self.assertEqual(checks[3]["level"], "WARN")
        self.assertFalse(checks[3]["hard"])

    def test_hash_drift_warns_for_doc_stage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest = manifest_with_stage(Path(tmpdir))
            path = Path(manifest["stages"]["00+10"]["output"][0])
            path.write_text("changed")
            checks = preflight.base_checks(manifest, "20")
        self.assertEqual(checks[4]["level"], "WARN")
        self.assertFalse(checks[4]["hard"])

    def test_missing_prior_output_fails_for_impl_stage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            manifest = manifest_with_impl_stage(tmp)
            Path(manifest["stages"]["40c:PREFLIGHT"]["output"]).unlink()
            checks = preflight.base_checks(manifest, "50:PREFLIGHT")
        exists_check = next(c for c in checks if "exists on disk" in c["message"])
        self.assertEqual(exists_check["level"], "FAIL")
        self.assertTrue(exists_check["hard"])

    def test_hash_drift_fails_for_impl_stage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            manifest = manifest_with_impl_stage(tmp)
            Path(manifest["stages"]["40c:PREFLIGHT"]["output"]).write_text("tampered")
            checks = preflight.base_checks(manifest, "50:PREFLIGHT")
        hash_check = next(c for c in checks if "hash matches manifest" in c["message"])
        self.assertEqual(hash_check["level"], "FAIL")
        self.assertTrue(hash_check["hard"])

    def test_load_manifest_exits_when_manifest_missing(self) -> None:
        with patch.object(preflight, "MANIFEST_PATH", Path("/tmp/does-not-exist.json")):
            with self.assertRaises(SystemExit) as ctx:
                preflight.load_manifest()
        self.assertEqual(str(ctx.exception), "ERROR: No Daksh pipeline found. Run /daksh init first.")

    def test_main_prints_pass_result_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            manifest_path = tmp / "manifest.json"
            manifest_path.write_text(__import__("json").dumps(manifest_with_stage(tmp)))
            with patch.object(preflight, "MANIFEST_PATH", manifest_path):
                with patch("sys.argv", ["preflight.py", "brd"]):
                    with patch("builtins.print") as mock_print:
                        exit_code = preflight.main()
        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_print.call_args_list[-1].args[0], "Result: PASS — 0 hard failure(s)")

    def test_main_returns_exit_1_on_hard_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            manifest_path = tmp / "manifest.json"
            manifest_path.write_text(__import__("json").dumps(manifest_with_stage(tmp)))
            with patch.object(preflight, "MANIFEST_PATH", manifest_path):
                with patch("sys.argv", ["preflight.py", "roadmap"]):
                    with patch("builtins.print"):
                        exit_code = preflight.main()
        self.assertEqual(exit_code, 1)


class ImplChecksTests(unittest.TestCase):
    @patch.object(preflight, "git_working_tree_clean", return_value=True)
    def test_tasks_with_no_dependencies_skip_dependency_failures(self, _mock_git: patch) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            tasks = tmp / "docs/implementation/PREFLIGHT/tasks.md"
            write(tasks, "#### TASK-PREFLIGHT-001: Sample\n- **Depends on:** none\n")
            with patch.object(preflight, "task_file_for_module", return_value=tasks):
                checks = preflight.impl_checks(manifest_with_impl_stage(tmp), "50:PREFLIGHT")
        self.assertFalse(any(c["level"] == "FAIL" for c in checks))
        self.assertEqual(checks[0]["message"], "Git working tree clean")

    @patch.object(preflight, "git_working_tree_clean", return_value=False)
    def test_git_dirty_fails(self, _mock_git: patch) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            checks = preflight.impl_checks(manifest_with_impl_stage(Path(tmpdir)), "50:PREFLIGHT")
        self.assertEqual(checks[0]["level"], "FAIL")
        self.assertTrue(checks[0]["hard"])
        self.assertEqual(checks[0]["message"], "Git working tree clean")

    @patch.object(preflight, "git_working_tree_clean", return_value=True)
    def test_unresolved_dependency_fails(self, _mock_git: patch) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            tasks = tmp / "docs/implementation/PREFLIGHT/tasks.md"
            write(tasks, "#### TASK-PREFLIGHT-002: Sample\n- **Depends on:** TASK-PREFLIGHT-001\n")
            with patch.object(preflight, "task_file_for_module", return_value=tasks):
                checks = preflight.impl_checks(manifest_with_impl_stage(tmp), "50:PREFLIGHT")
        self.assertEqual(checks[-1]["message"], "TASK-PREFLIGHT-002 dependency TASK-PREFLIGHT-001 not done")
        self.assertEqual(checks[-1]["level"], "FAIL")

    @patch.object(preflight, "git_working_tree_clean", return_value=True)
    def test_resolved_dependency_passes(self, _mock_git: patch) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            tasks = tmp / "docs/implementation/PREFLIGHT/tasks.md"
            write(tasks, "#### TASK-PREFLIGHT-002: Sample\n- **Depends on:** TASK-PREFLIGHT-001\n")
            manifest = manifest_with_impl_stage(tmp, traceability={"TASK-PREFLIGHT-001": "Done"})
            with patch.object(preflight, "task_file_for_module", return_value=tasks):
                checks = preflight.impl_checks(manifest, "50:PREFLIGHT", task_id="TASK-PREFLIGHT-002")
        dep_check = next(c for c in checks if "dependency" in c["message"].lower())
        self.assertEqual(dep_check["level"], "PASS")

    @patch.object(preflight, "git_working_tree_clean", return_value=True)
    def test_impl_checks_not_used_for_doc_stage(self, _mock_git: patch) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest = manifest_with_stage(Path(tmpdir))
            checks = preflight.run_checks(manifest, "20")
            baseline = preflight.base_checks(manifest, "20")
        self.assertEqual(checks, baseline)


if __name__ == "__main__":
    unittest.main()
