from __future__ import annotations

import os
import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest import mock

from divami_skills import cli
from divami_skills import manager


class LocalRelayTests(unittest.TestCase):
    def _source_registry(self, root: Path) -> tuple[manager.Registry, Path]:
        source = root / "home" / "agents" / "registry" / "abc-skillset"
        skill = source / "skills-xyz"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("test skill\n")
        return {"abc-skillset": source}, skill

    def test_local_link_creates_relay_symlink_to_skillset_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry, source_skill = self._source_registry(root)
            llm_path = root / "local" / ".agents" / "skills"

            manager.link_skill(llm_path, "abc-skillset", "skills-xyz", registry)

            relay = root / "local" / "agents" / "skills-xyz"
            consumer = llm_path / "skills-xyz"
            self.assertTrue(relay.is_symlink())
            self.assertEqual(relay.resolve(), source_skill.resolve())
            self.assertTrue(consumer.is_symlink())
            self.assertEqual(os.readlink(consumer), "../../agents/skills-xyz")

    def test_local_link_mode_repairs_existing_copied_relay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry, source_skill = self._source_registry(root)
            llm_path = root / "local" / ".agents" / "skills"

            manager.link_skill(llm_path, "abc-skillset", "skills-xyz", registry, copy=True)
            self.assertFalse((root / "local" / "agents" / "skills-xyz").is_symlink())

            manager.link_skill(llm_path, "abc-skillset", "skills-xyz", registry)

            relay = root / "local" / "agents" / "skills-xyz"
            self.assertTrue(relay.is_symlink())
            self.assertEqual(relay.resolve(), source_skill.resolve())

    def test_sync_repairs_existing_copied_relay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry, source_skill = self._source_registry(root)
            cwd = root / "local"
            llm_path = cwd / ".agents" / "skills"

            manager.link_skill(llm_path, "abc-skillset", "skills-xyz", registry, copy=True)
            (cwd / manager.RC_FILENAME).write_text(
                '[codex-local]\n"abc-skillset" = ["skills-xyz"]\n'
            )

            results = manager.sync(cwd, registry)

            relay = cwd / "agents" / "skills-xyz"
            self.assertTrue(relay.is_symlink())
            self.assertEqual(relay.resolve(), source_skill.resolve())
            self.assertEqual(results[0].linked, ["skills-xyz"])


class UnpackTests(unittest.TestCase):
    def test_unpack_registers_repo_skills_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "divami-agents"
            skills = repo / "skills"
            skills.mkdir(parents=True)
            (skills / "demo").mkdir()
            target_root = root / "home" / "agents" / "skillsets"
            with mock.patch.object(manager, "SKILL_SETS_DIR", target_root):
                cli.cmd_unpack(SimpleNamespace(skills_folder=str(repo), skillset_name=None))
            target = target_root / "divami-agents"
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), skills.resolve())

    def test_unpack_defaults_to_current_repo_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "divami-agents"
            skills = repo / "skills"
            skills.mkdir(parents=True)
            (skills / "demo").mkdir()
            target_root = root / "home" / "agents" / "skillsets"
            with mock.patch.object(manager, "SKILL_SETS_DIR", target_root), \
                 mock.patch.object(cli.Path, "cwd", return_value=repo):
                cli.cmd_unpack(SimpleNamespace(skills_folder=None, skillset_name=None))
            target = target_root / "divami-agents"
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), skills.resolve())

    def test_discover_ignores_legacy_skillsets_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            modern = root / "home" / "agents" / "skillsets"
            other = root / "home" / "agents" / "other-root"
            (modern / "modern-set").mkdir(parents=True)
            (other / "ignored-set").mkdir(parents=True)
            with mock.patch.object(manager, "SKILL_SETS_DIR", modern):
                self.assertEqual(manager.discover_skill_sets(), ["modern-set"])


if __name__ == "__main__":
    unittest.main()
