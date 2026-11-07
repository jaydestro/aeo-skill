#!/usr/bin/env python3
"""Static HTML/Markdown readiness checks, not an AI visibility score (Python 3.10+)."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

UA = "aeo-audit/2.0"
SEARCH_BOTS = ("Googlebot", "Bingbot", "OAI-SearchBot", "Claude-SearchBot", "PerplexityBot")
SUPPORTED = {".html", ".htm", ".md", ".markdown", ".mdx"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta = {}
        self.canonical = ""
        self.headings = []
        self.jsonld = []
        self.missing_alt = 0
        self._capture = None
        self._buffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            self.meta[key] = a.get("content") or ""
        if tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.canonical = a.get("href") or ""
        if tag == "img" and "alt" not in a:
            self.missing_alt += 1
        if tag in ("title", "h1", "h2", "h3", "h4", "h5", "h6"):
            self._capture = tag
            self._buffer = []
        if tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._capture = "script"
            self._buffer = []

    def handle_data(self, data):
        if self._capture:
            self._buffer.append(data)

    def handle_endtag(self, tag):
        if tag != self._capture:
            return
        text = "".join(self._buffer).strip()
        if tag == "script":
            self.jsonld.append(text)
        elif tag == "title":
            self.title = text
        else:
            self.headings.append((tag, text))
        self._capture = None
        self._buffer = []


def markdown_headings(text):
    """ATX/setext headings outside frontmatter and fenced code; not an MDX renderer."""
    lines = text.splitlines()
    headings = []
    frontmatter = bool(lines and lines[0].strip() == "---")
    fence = None
    previous = ""
    for i, line in enumerate(lines):
        if frontmatter:
            if i and line.strip() == "---":
                frontmatter = False
            continue
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            previous = ""
            continue
        if fence:
            continue
        match = re.match(r"^\s{0,3}(#{1,6})\s+(.+)", line)
        if match:
            headings.append((f"h{len(match[1])}", re.sub(r"\s+#+\s*$", "", match[2])))
        elif previous.strip() and re.fullmatch(r"\s{0,3}(=+|-+)\s*", line):
            headings.append(("h1" if line.strip().startswith("=") else "h2", previous.strip()))
        previous = line
    return headings


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as response:
        text = response.read().decode(response.headers.get_content_charset() or "utf-8", "replace")
        return text, response.geturl(), response.headers


def jsonld_types(blocks):
    types = set()
    errors = 0

    def walk(node):
        if isinstance(node, dict):
            value = node.get("@type", [])
            if isinstance(value, str):
                types.add(value)
            elif isinstance(value, list):
                types.update(v for v in value if isinstance(v, str))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for block in blocks:
        try:
            walk(json.loads(block))
        except json.JSONDecodeError:
            errors += 1
    return sorted(types), errors


def audit(target):
    is_url = urlparse(target).scheme in ("http", "https")
    headers = {}
    final_url = target
    if is_url:
        text, final_url, headers = fetch(target)
        media = headers.get_content_type()
        if media not in ("text/html", "application/xhtml+xml", "text/markdown", "text/plain"):
            raise ValueError(f"Unsupported response type: {media}; use a native format validator")
        markdown = media in ("text/markdown", "text/plain")
    else:
        path = Path(target)
        if path.suffix.lower() not in SUPPORTED:
            raise ValueError("Expected HTML, Markdown, or MDX; use native tools for other formats")
        text = path.read_text(encoding="utf-8")
        markdown = path.suffix.lower() in (".md", ".markdown", ".mdx")
    p = PageParser()
    if markdown:
        p.headings = markdown_headings(text)
        p.title = next((value for tag, value in p.headings if tag == "h1"), "")
    else:
        p.feed(text)
    findings = []

    def issue(priority, message, fix, evidence="editorial"):
        findings.append({"priority": priority, "issue": message, "fix": fix, "evidence": evidence})

    if not p.title:
        issue("Medium", "No title detected", "Check the published page title or Markdown main heading.")
    if not p.headings:
        issue("Medium", "No headings detected", "Provide useful descriptive structure where appropriate.")
    if p.missing_alt:
        issue("Low", f"{p.missing_alt} image(s) lack an alt attribute",
              "Describe meaningful images; use empty alt for decorative images.")
    if not markdown and not p.meta.get("description"):
        issue("Low", "No meta description detected", "Consider an accurate page summary.")
    types, invalid = jsonld_types(p.jsonld)
    if invalid:
        issue("High", f"{invalid} invalid JSON-LD block(s)", "Fix JSON syntax and validate visible-content agreement.")
    directives = " ".join(value for key, value in p.meta.items()
                          if key == "robots" or key in tuple(b.lower() for b in SEARCH_BOTS))
    directives += " " + headers.get("X-Robots-Tag", "")
    if re.search(r"\b(noindex|nosnippet|none)\b|max-snippet\s*:\s*0\b", directives, re.I):
        issue("High", "Index/snippet restrictions detected",
              "Review intended audience and provider scope; preserve intentional restrictions.", "documented")
    crawl = {}
    if is_url:
        parsed = urlparse(final_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        try:
            robots, _, _ = fetch(base + "/robots.txt")
            parser = RobotFileParser()
            parser.parse(robots.splitlines())
            crawl["blocked_search_bots"] = [bot for bot in SEARCH_BOTS if not parser.can_fetch(bot, final_url)]
            crawl["robots_status"] = "fetched; standard-library best-effort evaluation"
            if crawl["blocked_search_bots"]:
                issue("High", "Search crawler restrictions detected for the target path",
                      "Verify provider-specific robots precedence and intended policy.", "documented")
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            crawl["robots_status"] = f"unknown: {exc}"
        try:
            llms, _, _ = fetch(base + "/llms.txt")
            crawl["llms_txt"] = "candidate found" if llms.lstrip().startswith("#") else "not recognized"
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            crawl["llms_txt"] = f"not verified: {exc}"
    return {
        "target": target,
        "final_url": final_url if is_url else None,
        "format": "markdown" if markdown else "html",
        "title": p.title,
        "canonical": p.canonical,
        "headings": p.headings,
        "jsonld_types": types,
        "crawl": crawl,
        "findings": findings,
        "manual_checks": [
            "Factual accuracy, original evidence, appropriate ownership and actual update/version context",
            "Rendered MDX/JS/CSS content, links, examples, schema semantics and export fidelity",
            "Actual bot/WAF access, provider-specific robots precedence, index and snippet eligibility",
            "Fixed-query retrieval, source/version-correct citations, task success and abstention",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="HTTP(S) URL or local HTML/Markdown/MDX file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = audit(args.target)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        if args.json:
            print(json.dumps({"target": args.target, "error": str(exc)}))
        else:
            print(f"Audit failed: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Static readiness observations: {args.target} (not a visibility score)")
        for finding in result["findings"]:
            print(f"{finding['priority']} | {finding['issue']} | {finding['fix']}")
        if result["crawl"]:
            print(json.dumps(result["crawl"], indent=2))
        print("Manual checks required: " + "; ".join(result["manual_checks"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
