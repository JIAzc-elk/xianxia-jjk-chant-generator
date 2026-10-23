"""Exercise actual isolated installs, duplicate installs, and conflict preservation."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/install.py"
spec = importlib.util.spec_from_file_location("installer", SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def run_install(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            capture_output=True, text=True, encoding="utf-8",
            env=dict(os.environ, PYTHONUTF8="1"),
        )

    def test_all_user_targets_and_repeated_install(self):
        with tempfile.TemporaryDirectory(prefix="chant-user-") as temp:
            result = self.run_install("--tool", "all", "--home", temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            for directory in installer.USER_DIRS.values():
                target = Path(temp) / directory / installer.NAME
                self.assertTrue(installer.same_tree(installer.SOURCE, target))
            again = self.run_install("--tool", "all", "--home", temp)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(again.stdout.count("UNCHANGED"), 3)

    def test_all_project_targets_with_unicode_and_spaces(self):
        with tempfile.TemporaryDirectory(prefix="chant-project-") as temp:
            project = Path(temp) / "修仙 写作项目"
            project.mkdir()
            result = self.run_install("--tool", "all", "--scope", "project", "--project", project)
            self.assertEqual(result.returncode, 0, result.stderr)
            for directory in installer.PROJECT_DIRS.values():
                self.assertTrue(installer.same_tree(installer.SOURCE, project / directory / installer.NAME))

    def test_conflict_preserves_local_file_and_prevents_partial_install(self):
        with tempfile.TemporaryDirectory(prefix="chant-conflict-") as temp:
            target = Path(temp) / installer.USER_DIRS["claude"] / installer.NAME
            target.mkdir(parents=True)
            local_file = target / "SKILL.md"
            local_file.write_text("author local edits", encoding="utf-8")
            result = self.run_install("--tool", "all", "--home", temp)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(local_file.read_text(encoding="utf-8"), "author local edits")
            self.assertFalse((Path(temp) / installer.USER_DIRS["codex"]).exists())
            self.assertFalse((Path(temp) / installer.USER_DIRS["opencode"]).exists())

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory(prefix="chant-dry-") as temp:
            result = self.run_install("--tool", "all", "--home", temp, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_project_scope_requires_explicit_existing_project(self):
        result = self.run_install("--tool", "codex", "--scope", "project")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
