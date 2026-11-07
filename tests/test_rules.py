import importlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RuleCoverageTests(unittest.TestCase):
    def test_every_rule_has_unique_id_real_tests_or_a_concrete_agent_scenario(self):
        catalog = json.loads((ROOT / "tests/rules.json").read_text())
        self.assertEqual(catalog["version"], 1)
        self.assertTrue(catalog["rules"])
        scenarios = (ROOT / "tests/agent-scenarios.md").read_text()
        ids = []
        for rule in catalog["rules"]:
            self.assertRegex(rule["id"], r"^AEO-R[0-9]{3}$")
            ids.append(rule["id"])
            self.assertTrue(rule["behavior"].strip())
            tests = rule.get("automated_tests", [])
            scenario = rule.get("agent_scenario")
            self.assertTrue(tests or scenario, rule["id"])
            if tests:
                self.assertTrue(rule["automated_scope"].strip(), rule["id"])
            for test in tests:
                module_name, class_name, method_name = test.rsplit(".", 2)
                cls = getattr(importlib.import_module(module_name), class_name)
                self.assertTrue(issubclass(cls, unittest.TestCase), test)
                self.assertTrue(method_name.startswith("test_"), test)
                self.assertTrue(callable(getattr(cls, method_name)), test)
            if scenario:
                self.assertRegex(scenario, r"^[a-z]+(?:-[a-z]+)*$")
                self.assertIn(f"## {scenario}\n", scenarios, rule["id"])
                section = scenarios.split(f"## {scenario}\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(rule["id"], section)
                self.assertIn("Acceptance:", section)
        self.assertEqual(len(ids), len(set(ids)))
        documents = [*(ROOT / "skills/aeo").rglob("*.md"), ROOT / "tests/agent-scenarios.md"]
        documented = set()
        for path in documents:
            documented.update(re.findall(r"\bAEO-R[0-9]{3}\b", path.read_text()))
        self.assertEqual(documented, set(ids), "Every documented rule ID must be registered and covered")


if __name__ == "__main__":
    unittest.main()
