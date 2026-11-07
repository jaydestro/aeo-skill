import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_manifests_share_name_version_and_license_without_execution_hooks(self):
        manifests = [ROOT / "plugin.json", ROOT / ".claude-plugin/plugin.json",
                     ROOT / "gemini-extension.json"]
        for path in manifests:
            data = json.loads(path.read_text())
            self.assertEqual(data["name"], "aeo")
            self.assertEqual(data["version"], "0.1.0")
            self.assertNotIn("hooks", data)
            self.assertNotIn("mcpServers", data)
            self.assertNotIn("excludeTools", data)
        allowed = {"$schema", "name", "version", "description", "author", "homepage",
                   "repository", "license", "keywords", "extensions"}
        plugin = json.loads((ROOT / "plugin.json").read_text())
        self.assertLessEqual(plugin.keys(), allowed)
        self.assertEqual(plugin["$schema"],
                         "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertRegex(plugin["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertEqual(plugin["license"], "MIT")
        self.assertTrue((ROOT / "skills/aeo/SKILL.md").is_file())

    def test_marketplaces_resolve_to_the_canonical_plugin(self):
        for relative in (".claude-plugin/marketplace.json", ".github/plugin/marketplace.json"):
            data = json.loads((ROOT / relative).read_text())
            self.assertEqual(data["name"], "aeo-skill")
            self.assertEqual(len(data["plugins"]), 1)
            plugin = data["plugins"][0]
            self.assertEqual(plugin["name"], "aeo")
            self.assertEqual(plugin["source"], "./")
            self.assertEqual(plugin["version"], "0.1.0")
            self.assertTrue((ROOT / plugin["source"] / "skills/aeo/SKILL.md").exists())

    def test_bundled_mit_license_is_complete_and_identical(self):
        self.assertEqual((ROOT / "LICENSE").read_bytes(),
                         (ROOT / "skills/aeo/LICENSE").read_bytes())

    def test_all_bundled_documentation_links_resolve_inside_skill(self):
        skill = ROOT / "skills/aeo"
        for path in skill.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if target.startswith(("https://", "http://", "#")):
                    continue
                resolved = (path.parent / target.split("#")[0]).resolve()
                self.assertTrue(resolved.is_relative_to(skill), (path, target))
                self.assertTrue(resolved.exists(), (path, target))

    def test_rubric_and_template_retain_all_twenty_criteria(self):
        rubric = (ROOT / "skills/aeo/references/rubric.md").read_text()
        template = (ROOT / "skills/aeo/templates/review-report.md").read_text()
        expected = {f"{letter}{number}" for letter in "ABCDE" for number in range(1, 5)}
        self.assertEqual(set(re.findall(r"\| ([A-E][1-4]) \|", rubric)), expected)
        self.assertEqual(set(re.findall(r"\| ([A-E][1-4]) \|", template)), expected)
        self.assertIn("Rubric: content-readiness v2", template)
        self.assertIn("Review profile:", template)
        self.assertIn("Subject/domain", template)


if __name__ == "__main__":
    unittest.main()
