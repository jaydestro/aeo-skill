import importlib.util
import hashlib
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

    def test_hash_preserves_exact_file_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            content = b"# README\r\n\r\nText.\r\n"
            path.write_bytes(content)
            result = audit.audit(str(path))
            self.assertEqual(result["snapshot_sha256"], hashlib.sha256(content).hexdigest())

    def test_recursive_many_articles_and_nested_readmes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for number in range(120):
                folder = root / "articles" / f"topic-{number}" / "nested"
                folder.mkdir(parents=True)
                (folder / "article.md").write_text("# Article\n", encoding="utf-8")
                (folder / "README.md").write_text("# Component\n", encoding="utf-8")
            (root / ".github").mkdir()
            (root / ".github" / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8")
            targets, skipped, errors = audit.collect_targets([directory])
            self.assertEqual(len(targets), 241)
            self.assertEqual(skipped, [])
            self.assertEqual(errors, [])

    def test_exclusions_overlap_and_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            article = docs / "article.md"
            article.write_text("# Article\n", encoding="utf-8")
            for folder in (".git", "node_modules", "generated"):
                (root / folder).mkdir()
                (root / folder / "copy.md").write_text("# Excluded\n", encoding="utf-8")
            (root / "link.md").symlink_to(article)
            (root / "linked-docs").symlink_to(docs, target_is_directory=True)
            targets, skipped, errors = audit.collect_targets(
                [directory, str(docs), str(article)], excludes=["generated"])
            self.assertEqual(len(targets), 1)
            self.assertEqual(errors, [])
            self.assertTrue(any(item["reason"] == "symlink" for item in skipped))
            self.assertEqual(len(skipped), 5)

    def test_recursive_errors_do_not_drop_valid_articles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.md").write_text("# Good\n", encoding="utf-8")
            (root / "bad.md").write_bytes(b"\xff")
            result = subprocess.run([sys.executable, str(SCRIPT), directory, "--json"],
                                    capture_output=True, text=True)
            data = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(len(data["reports"]), 1)
            self.assertEqual(len(data["errors"]), 1)

    def test_empty_directory_is_error(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(SCRIPT), directory, "--json"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("No supported articles", json.loads(result.stdout)["errors"][0]["error"])

    def test_markdown_report_scaffold_and_destination_exclusion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("Missing main title\n", encoding="utf-8")
            report = root / "report.md"
            result = subprocess.run([sys.executable, str(SCRIPT), directory, "--report",
                                     str(report), "--json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(result.stdout)["reports"]), 1)
            text = report.read_text()
            self.assertIn("Not scored: semantic assessment pending", text)
            self.assertIn("AEO-0001", text)
            self.assertIn("Snapshot SHA-256", text)
            self.assertIn("needs-review", text)
            self.assertIn("prompt for a capable agent", text)
            targets, skipped, errors = audit.collect_targets([directory], report_path=report)
            self.assertEqual(len(targets), 1)
            self.assertEqual(errors, [])
            self.assertEqual(skipped[0]["reason"], "report destination")

    def test_report_never_overwrites_sources_or_existing_report(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "README.md"
            source.write_text("# Original\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                     "--report", str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(source.read_text(), "# Original\n")

    def test_report_escapes_untrusted_markdown(self):
        text = audit.markdown_cell("<script>bad</script> | [link](url)\n# Heading")
        self.assertNotIn("<script>", text)
        self.assertNotIn("\n", text)
        self.assertIn("\\|", text)

    def test_multiple_inputs_and_root_relative_exclusion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs" / "keep.md").write_text("# Keep\n", encoding="utf-8")
            (root / "docs" / "skip.md").write_text("# Skip\n", encoding="utf-8")
            (root / "README.md").write_text("# README\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), directory,
                                     str(root / "README.md"), "--exclude", "docs/skip.md", "--json"],
                                    capture_output=True, text=True)
            data = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(data["reports"]), 2)
            self.assertEqual(len(data["skipped"]), 1)

    def test_report_write_failure_is_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "README.md"
            source.write_text("# README\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--report",
                                     str(Path(directory) / "missing" / "report.md")],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Report write failed", result.stderr)

    def test_report_generation_does_not_modify_articles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "README.md"
            original = b"# Original\r\n\r\nKeep this code: `x = 1`.\r\n"
            source.write_bytes(original)
            result = subprocess.run([sys.executable, str(SCRIPT), directory, "--report",
                                     str(root / "report.md")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(source.read_bytes(), original)

    def test_single_document_still_gets_read_only_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "README.md"
            source.write_text("# Single document\n", encoding="utf-8")
            report = root / "readme-review.md"
            result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                     "--report", str(report), "--json"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["target"], str(source))
            text = report.read_text()
            self.assertIn("Inspected: 1", text)
            self.assertIn("report-only static scan", text)
            self.assertIn("Not scored: semantic assessment pending", text)
            self.assertEqual(source.read_text(), "# Single document\n")

    def test_walk_permission_error_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            def failed_walk(root, followlinks, onerror):
                onerror(PermissionError(13, "Permission denied", str(root)))
                return iter(())

            with patch.object(audit.os, "walk", side_effect=failed_walk):
                targets, skipped, errors = audit.collect_targets([directory])
            self.assertEqual(targets, [])
            self.assertEqual(skipped, [])
            self.assertTrue(any("Permission denied" in item["error"] for item in errors))


if __name__ == "__main__":
    unittest.main()
