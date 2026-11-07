import importlib.util
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/sprocket"
SCRIPT = ROOT / "skills/aeo/scripts/aeo_audit.py"
SPEC = importlib.util.spec_from_file_location("sprocket_audit", SCRIPT)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)
EXPECTED = {
    "feature": "fictional-sprocket",
    "items": 12,
    "batch_size": 4,
    "batches": 3,
    "network_calls": 0,
}


class SprocketExampleTests(unittest.TestCase):
    def document_command(self, name):
        text = (EXAMPLE / name).read_text()
        block = re.search(r"```bash\n([^\n]+)\n```", text)
        self.assertIsNotNone(block)
        command = shlex.split(block[1])
        self.assertEqual(command[:2], ["python3", "examples/sprocket/sprocket_demo.py"])
        return [sys.executable, str(EXAMPLE / "sprocket_demo.py"), *command[2:]]

    def run_demo(self, *args):
        return subprocess.run([sys.executable, str(EXAMPLE / "sprocket_demo.py"), *args],
                              cwd=ROOT, capture_output=True, text=True)

    def test_static_heading_defect_is_fixed(self):
        before = audit.audit(str(EXAMPLE / "before.md"))
        after = audit.audit(str(EXAMPLE / "after.md"))
        self.assertTrue(any(f["issue"] == "No title detected" for f in before["findings"]))
        self.assertEqual(after["findings"], [])
        self.assertNotIn("score", after)

    def test_before_command_fails_and_after_command_matches_documented_output(self):
        before = subprocess.run(self.document_command("before.md"), cwd=ROOT,
                                capture_output=True, text=True)
        after = subprocess.run(self.document_command("after.md"), cwd=ROOT,
                               capture_output=True, text=True)
        self.assertEqual(before.returncode, 2)
        self.assertEqual(before.stdout, "")
        self.assertEqual(after.returncode, 0, after.stderr)
        self.assertEqual(json.loads(after.stdout), EXPECTED)
        text = (EXAMPLE / "after.md").read_text()
        documented = json.loads(re.search(r"```json\n(.+?)\n```", text, re.S)[1])
        self.assertEqual(documented, EXPECTED)

    def test_inclusive_boundaries_and_rounding(self):
        for items, batch_size, batches in ((1, 1, 1), (1000, 32, 32), (13, 4, 4)):
            with self.subTest(items=items, batch_size=batch_size):
                result = self.run_demo("--items", str(items), "--batch-size", str(batch_size))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["batches"], batches)

    def test_invalid_values_and_missing_flags_are_explicit_errors(self):
        cases = [
            ("--items", "0", "--batch-size", "4"),
            ("--items", "1001", "--batch-size", "4"),
            ("--items", "12", "--batch-size", "0"),
            ("--items", "12", "--batch-size", "33"),
            ("--items", "twelve", "--batch-size", "4"),
            ("--items", "12"),
            ("--items", "12", "--batch-size", "4", "--mode", "turbo"),
        ]
        for args in cases:
            with self.subTest(args=args):
                result = self.run_demo(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)

    def test_reference_links_resolve_and_before_defects_are_intentional(self):
        for filename in ("after.md", "fixture-spec.md", "README.md", "walkthrough.md", "expected-review.md"):
            text = (EXAMPLE / filename).read_text()
            for target in re.findall(r"\]\(([^)]+)\)", text):
                self.assertTrue((EXAMPLE / target).exists(), (filename, target))
        self.assertFalse((EXAMPLE / "assets/missing-sprocket.png").exists())
        self.assertFalse((EXAMPLE / "missing-reference.md").exists())

    def test_diagram_has_accessible_identity_and_text(self):
        svg = ET.parse(EXAMPLE / "assets/batching.svg").getroot()
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        self.assertEqual(svg.attrib["role"], "img")
        self.assertTrue(svg.find("svg:title", namespace).text)
        self.assertIn("Twelve imaginary items", svg.find("svg:desc", namespace).text)
        self.assertIn("textual explanation", (EXAMPLE / "after.md").read_text())

    def test_fiction_and_unavailable_video_are_not_misrepresented(self):
        for filename in ("before.md", "after.md", "fixture-spec.md", "README.md", "walkthrough.md"):
            text = (EXAMPLE / filename).read_text().lower()
            self.assertRegex(text, r"(not (a real |an )azure cosmos db feature|does not exist)")
        after = (EXAMPLE / "after.md").read_text()
        self.assertIn("No video recording exists", after)
        self.assertIn("not a transcript", after)
        self.assertNotIn("<iframe", after)

    def test_reference_assessment_has_complete_criteria_and_correct_totals(self):
        text = (EXAMPLE / "expected-review.md").read_text()
        rows = re.findall(r"^\| ([A-E][1-4]) \| (pass|fail) \| (pass|fail) \|", text, re.M)
        self.assertEqual(len(rows), 20)
        self.assertEqual(len({row[0] for row in rows}), 20)
        self.assertEqual(sum(before == "pass" for _, before, _ in rows) * 5, 15)
        self.assertEqual(sum(after == "pass" for _, _, after in rows) * 5, 100)
        self.assertIn("not a claim that an unspecified agent", text)

    def test_scored_reference_report_has_apply_all_and_valid_source_snapshots(self):
        text = (EXAMPLE / "expected-review.md").read_text()
        for filename in ("before.md", "after.md"):
            digest = hashlib.sha256((EXAMPLE / filename).read_bytes()).hexdigest()
            self.assertIn(digest, text)
        self.assertIn("SP-ALL", text)
        self.assertIn("apply all proposed local recommendations", text)
        self.assertIn("exact bytes", text)
        self.assertIn("new `examples/sprocket/improved.md`", text)


if __name__ == "__main__":
    unittest.main()
