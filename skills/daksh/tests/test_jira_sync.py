import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from scripts import jira_sync


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def manifest() -> dict:
    return {"modules": ["JIRA"], "jira": {"project_key": "AD", "board_id": 1094, "ticket_map": {}}}


class JiraSyncScaffoldTests(unittest.TestCase):
    def test_parse_tasks_md_reads_jira_tasks(self) -> None:
        tasks = jira_sync.parse_tasks_md("JIRA")
        self.assertEqual(tasks[0]["id"], "TASK-JIRA-001")
        self.assertEqual(tasks[0]["sprint"], "Sprint 2")
        self.assertEqual(tasks[0]["assignee"], "Yeshwanth")

    def test_save_manifest_writes_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.json"
            with patch.object(jira_sync._MODULE, "MANIFEST_PATH", manifest_path):
                jira_sync.save_manifest({"ok": True})
            self.assertEqual(json.loads(manifest_path.read_text()), {"ok": True})
            self.assertFalse(manifest_path.with_suffix(".tmp").exists())

    def test_validate_env_vars_exits_on_missing_token(self) -> None:
        with patch.dict("os.environ", {"JIRA_SERVER": "https://jira", "JIRA_EMAIL": "a@b.c"}, clear=True):
            with self.assertRaises(SystemExit) as ctx:
                jira_sync.validate_env_vars()
        self.assertEqual(str(ctx.exception), "ERROR: JIRA_TOKEN not set")

    def test_push_creates_missing_sprints_and_assigns_story(self) -> None:
        client = Mock()
        client.sprints.return_value = [SimpleNamespace(name="Sprint 2", id=10)]
        client.create_sprint.return_value = SimpleNamespace(id=11)
        client.create_issue.side_effect = [SimpleNamespace(key="AD-230"), SimpleNamespace(key="AD-236")]
        with patch.object(jira_sync._MODULE, "parse_tasks_md", return_value=[{"id": "TASK-JIRA-001", "summary": "One", "type": "Story", "points": 5, "description": "", "acceptance_criteria": [], "parent": None, "sprint": "Sprint 3"}]), patch.object(jira_sync._MODULE, "save_manifest"):
            jira_sync.push(client, manifest(), "JIRA", False, False)
        client.create_sprint.assert_called_once_with("Sprint 3", 1094)
        client.add_issues_to_sprint.assert_called_once_with(11, ["AD-236"])

    def test_pull_marks_done_task_and_updates_summary_table(self) -> None:
        client = Mock()
        client.issue.return_value = SimpleNamespace(fields=SimpleNamespace(status=SimpleNamespace(name="Done")))
        repo_manifest = manifest()
        repo_manifest["jira"]["ticket_map"]["TASK-JIRA-001"] = "AD-236"
        with tempfile.TemporaryDirectory() as tmpdir:
            impl_root = Path(tmpdir) / "docs/implementation"
            write(impl_root / "JIRA/tasks.md", "| ID | Summary |\n|---|---|\n| TASK-JIRA-001 | One |\n")
            with patch.object(jira_sync._MODULE, "IMPL_ROOT", impl_root), patch.object(jira_sync._MODULE, "save_manifest"):
                jira_sync.pull(client, repo_manifest, "JIRA", False)
            self.assertEqual(repo_manifest["traceability"]["TASK-JIRA-001"]["status"], "done")
            self.assertIn("Done", (impl_root / "JIRA/tasks.md").read_text())

    def test_time_block_start_auto_closes_open_block(self) -> None:
        repo_manifest = {"traceability": {"TASK-JIRA-001": {"status": "in_progress", "time_blocks": [{"start": "2026-03-29T00:00:00+00:00", "end": None, "jira_worklog_id": None}]}}}
        with patch.object(jira_sync._MODULE, "_submit_worklog") as submit, patch.object(jira_sync._MODULE, "load_manifest", return_value=repo_manifest), patch.object(jira_sync._MODULE, "save_manifest"):
            jira_sync.time_block_start(repo_manifest, "TASK-JIRA-001")
        self.assertIsNotNone(repo_manifest["traceability"]["TASK-JIRA-001"]["time_blocks"][0]["end"])
        self.assertIsNone(repo_manifest["traceability"]["TASK-JIRA-001"]["time_blocks"][-1]["end"])
        submit.assert_called_once()

    def test_time_block_stop_without_ticket_skips_worklog(self) -> None:
        repo_manifest = {"traceability": {"TASK-JIRA-001": {"status": "in_progress", "time_blocks": [{"start": "2026-03-29T00:00:00+00:00", "end": None, "jira_worklog_id": None}]}}}
        with patch.object(jira_sync._MODULE, "save_manifest"), patch("builtins.print") as mock_print:
            jira_sync.time_block_stop(repo_manifest, "TASK-JIRA-001")
        self.assertIsNotNone(repo_manifest["traceability"]["TASK-JIRA-001"]["time_blocks"][0]["end"])
        self.assertTrue(any("not in ticket_map" in str(call.args[0]) for call in mock_print.call_args_list))
