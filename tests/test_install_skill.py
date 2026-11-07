import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "install_skill.py"
spec = importlib.util.spec_from_file_location("install_skill", SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallSkillTests(unittest.TestCase):
    def run_installer(self, root, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *arguments, "--json"],
            capture_output=True, text=True,
        )

    def test_all_project_profiles_copy_complete_unchanged_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_installer(directory, "--agent", "all")
            self.assertEqual(result.returncode, 0, result.stderr)
            installations = json.loads(result.stdout)["installations"]
            self.assertEqual({item["agent"] for item in installations},
                             {*installer.NATIVE_PATHS, *installer.MANUAL_AGENTS})
            expected = installer.payload(installer.SOURCE)
            expected[Path("LICENSE")] = (installer.REPOSITORY / "LICENSE").read_bytes()
            for item in installations:
                destination = Path(item["destination"])
                self.assertEqual(installer.payload(destination), expected)
                self.assertEqual(item["activation"],
                                 "native" if item["agent"] in installer.NATIVE_PATHS else "manual")
                self.assertIn(str(destination / "SKILL.md"), item["prompt"])
                self.assertIn("report-only", item["prompt"])
                self.assertEqual(destination,
                                 Path(directory) / installer.NATIVE_PATHS.get(
                                     item["agent"], (".agents/skills", ".agents/skills"))[0] / "aeo")

    def test_user_profiles_use_home_relative_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_installer(directory, "--agent", "all", "--scope", "user")
            self.assertEqual(result.returncode, 0, result.stderr)
            for item in json.loads(result.stdout)["installations"]:
                paths = installer.NATIVE_PATHS.get(item["agent"], (".agents/skills", ".agents/skills"))
                self.assertEqual(Path(item["destination"]), Path(directory) / paths[1] / "aeo")

    def test_identical_install_is_idempotent_and_ignores_runtime_caches(self):
        with tempfile.TemporaryDirectory() as directory:
            first = self.run_installer(directory)
            self.assertEqual(first.returncode, 0, first.stderr)
            destination = Path(directory) / ".agents/skills/aeo"
            before = (destination / "SKILL.md").stat().st_mtime_ns
            cache = destination / "scripts/__pycache__"
            cache.mkdir()
            (cache / "aeo_audit.pyc").write_bytes(b"runtime cache")
            second = self.run_installer(directory)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(json.loads(second.stdout)["installations"][0]["status"], "unchanged")
            self.assertEqual((destination / "SKILL.md").stat().st_mtime_ns, before)
            self.assertEqual((cache / "aeo_audit.pyc").read_bytes(), b"runtime cache")

    def test_conflict_preflights_all_targets_and_preserves_existing_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / ".roo/skills/aeo/SKILL.md"
            source.parent.mkdir(parents=True)
            source.write_text("Existing custom skill")
            rules = root / "AGENTS.md"
            rules.write_text("Existing project rules")
            result = self.run_installer(root, "--agent", "all")
            self.assertEqual(result.returncode, 1)
            self.assertIn("nothing overwritten", result.stderr)
            self.assertEqual(source.read_text(), "Existing custom skill")
            self.assertEqual(rules.read_text(), "Existing project rules")
            self.assertFalse((root / ".github").exists())
            self.assertFalse((root / ".agents").exists())

    def test_symlink_destination_and_parent_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            (root / ".agents").symlink_to(outside, target_is_directory=True)
            result = self.run_installer(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("outside installation root", result.stderr)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_differing_file_and_extra_resource_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(self.run_installer(root).returncode, 0)
            extra = root / ".agents/skills/aeo/custom.md"
            extra.write_text("User customization")
            result = self.run_installer(root)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(extra.read_text(), "User customization")

    def test_installed_helper_runs_outside_original_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.run_installer(root, "--agent", "codex")
            self.assertEqual(result.returncode, 0, result.stderr)
            article = root / "README.md"
            article.write_text("# Technical example\n\nThis is a local review.\n")
            report = root / "review.md"
            script = root / ".agents/skills/aeo/scripts/aeo_audit.py"
            run = subprocess.run(
                [sys.executable, str(script), "README.md", "--product", "Example Product",
                 "--report", "review.md", "--json"], cwd=root, capture_output=True, text=True,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["primary_product"], "Example Product")
            self.assertIn("Primary product: Example Product", report.read_text())
            self.assertEqual(article.read_text(), "# Technical example\n\nThis is a local review.\n")

    def test_portable_frontmatter_matches_specification_limits(self):
        text = (installer.SOURCE / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        fields = dict(line.split(": ", 1) for line in text.split("---", 2)[1].strip().splitlines())
        self.assertEqual(fields["name"], installer.SOURCE.name)
        self.assertLessEqual(len(fields["description"]), 1024)
        self.assertLessEqual(len(fields["compatibility"]), 500)
        self.assertEqual(fields["license"], "MIT")
        self.assertNotIn("allowed-tools", fields)


if __name__ == "__main__":
    unittest.main()
