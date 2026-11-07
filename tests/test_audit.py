import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/aeo/scripts/aeo_audit.py"
SPEC = importlib.util.spec_from_file_location("aeo_audit", SCRIPT)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def local(self, text, suffix=".html"):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ("page" + suffix)
            path.write_text(text, encoding="utf-8")
            return audit.audit(str(path))

    def test_no_speculative_penalties(self):
        result = self.local('<title>API</title><meta name="description" content="Reference">'
                            '<h1>API</h1><h2>Parameters</h2><p>Short.</p>')
        self.assertEqual(result["findings"], [])
        self.assertNotIn("score", result)

    def test_decorative_alt(self):
        result = self.local('<title>Title</title><h1>Title</h1><img alt=""><img src="x">')
        self.assertTrue(any("1 image(s)" in f["issue"] for f in result["findings"]))

    def test_markdown_ignores_metadata_and_code(self):
        result = self.local('---\ntitle: Guide\n---\n# Guide\n\n```md\n# Not a heading\n```\n'
                            '## Setup\n\nUse the documented command.\n', ".md")
        self.assertEqual(result["headings"], [("h1", "Guide"), ("h2", "Setup")])
        self.assertEqual(result["findings"], [])

    def test_invalid_jsonld_and_directives(self):
        result = self.local('<title>X</title><h1>X</h1><meta name="robots" content="noindex">'
                            '<script type="application/ld+json">{bad}</script>')
        self.assertTrue(any("invalid JSON-LD" in f["issue"] for f in result["findings"]))
        self.assertTrue(any("restrictions" in f["issue"] for f in result["findings"]))

    def test_graph_types(self):
        types, errors = audit.jsonld_types(['{"@graph":[{"@type":["Article","TechArticle"]}]}'])
        self.assertEqual(types, ["Article", "TechArticle"])
        self.assertEqual(errors, 0)

    def test_path_rules_and_training_optout(self):
        from email.message import Message
        headers = Message()
        headers["Content-Type"] = "text/html"
        robots = "User-agent: GPTBot\nDisallow: /\n\nUser-agent: OAI-SearchBot\nDisallow: /docs/\n"
        with patch.object(audit, "fetch", side_effect=[
            ("<title>X</title><h1>X</h1>", "https://example.com/docs/a", headers),
            (robots, "https://example.com/robots.txt", headers),
            OSError("unavailable"),
        ]):
            result = audit.audit("https://example.com/docs/a")
        self.assertEqual(result["crawl"]["blocked_search_bots"], ["OAI-SearchBot"])
        self.assertNotIn("GPTBot", str(result["findings"]))
        self.assertIn("not verified", result["crawl"]["llms_txt"])

    def test_failed_policy_is_unknown(self):
        from email.message import Message
        headers = Message()
        headers["Content-Type"] = "text/html"
        with patch.object(audit, "fetch", side_effect=[
            ("<title>X</title>", "https://example.com", headers),
            OSError("network down"), OSError("network down"),
        ]):
            result = audit.audit("https://example.com")
        self.assertIn("unknown", result["crawl"]["robots_status"])
        self.assertNotIn("blocked_search_bots", result["crawl"])

    def test_missing_input_exit(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "/nonexistent/page.md", "--json"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("error", json.loads(result.stdout))


if __name__ == "__main__":
    unittest.main()
