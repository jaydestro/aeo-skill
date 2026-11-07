#!/usr/bin/env python3
"""AEO (Answer Engine Optimization) audit for a URL or local HTML file.

Usage: python3 aeo_audit.py <url-or-file.html> [--json]
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; aeo-audit/1.0)"
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "PerplexityBot",
           "Google-Extended", "Bingbot", "CCBot"]
QUESTION_RE = re.compile(
    r"^(what|how|why|when|where|who|which|can|should|is|are|do|does|will)\b|\?$", re.I)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.headings: list[tuple[str, str]] = []
        self.blocks: list[tuple[str, str]] = []  # ordered (tag, text) for headings and paragraphs
        self.jsonld: list[str] = []
        self.counts = {"ul": 0, "ol": 0, "table": 0, "img": 0, "img_noalt": 0, "time": 0}
        self.lang = ""
        self._stack: list[str] = []
        self._buf: list[str] = []
        self._capture: str | None = None
        self._in_jsonld = False
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and "canonical" in a.get("rel", "").lower():
            self.canonical = a.get("href", "")
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._in_jsonld = True
            self._buf = []
        elif tag in ("h1", "h2", "h3", "p") and self._capture is None:
            self._capture = tag
            self._buf = []
        elif tag in self.counts and tag != "img":
            self.counts[tag] += 1
        if tag == "img":
            self.counts["img"] += 1
            if not a.get("alt", "").strip():
                self.counts["img_noalt"] += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_jsonld:
            self.jsonld.append("".join(self._buf))
            self._in_jsonld = False
        elif tag == self._capture:
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if text:
                self.blocks.append((tag, text))
                if tag != "p":
                    self.headings.append((tag, text))
            self._capture = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_jsonld or self._capture:
            self._buf.append(data)


def fetch(url: str, timeout: int = 15) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")
    except (urllib.error.URLError, ValueError, TimeoutError):
        return None


def jsonld_types(raw_blocks: list[str]) -> tuple[set[str], int]:
    types: set[str] = set()
    errors = 0

    def walk(node):
        if isinstance(node, dict):
            t = node.get("@type")
            if isinstance(t, str):
                types.add(t)
            elif isinstance(t, list):
                types.update(x for x in t if isinstance(x, str))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for raw in raw_blocks:
        try:
            walk(json.loads(raw))
        except json.JSONDecodeError:
            errors += 1
    return types, errors


def robots_blocks(robots: str, bot: str) -> bool:
    """True if robots.txt fully disallows `bot` (explicit group or wildcard)."""
    groups: list[tuple[list[str], list[str]]] = []
    agents: list[str] = []
    rules: list[str] = []
    for line in robots.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = (s.strip() for s in line.split(":", 1))
        k = k.lower()
        if k == "user-agent":
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(v.lower())
        elif k in ("disallow", "allow"):
            rules.append(f"{k}:{v}")
    if agents:
        groups.append((agents, rules))

    def blocked(rs):
        return "disallow:/" in rs and "allow:/" not in rs

    for ags, rs in groups:
        if bot.lower() in ags:
            return blocked(rs)
    for ags, rs in groups:
        if "*" in ags:
            return blocked(rs)
    return False


def audit(target: str) -> dict:
    is_url = urlparse(target).scheme in ("http", "https")
    html = fetch(target) if is_url else Path(target).read_text(encoding="utf-8", errors="replace")
    if html is None:
        raise SystemExit(f"Could not fetch {target}")

    p = PageParser()
    p.feed(html)
    findings: list[dict] = []
    score = 100

    def issue(priority: str, msg: str, fix: str, cost: int):
        nonlocal score
        score -= cost
        findings.append({"priority": priority, "issue": msg, "fix": fix})

    # Structure
    h1s = [t for tag, t in p.headings if tag == "h1"]
    if len(h1s) != 1:
        issue("High", f"Found {len(h1s)} <h1> elements", "Use exactly one descriptive <h1>.", 10)
    subs = [t for tag, t in p.headings if tag in ("h2", "h3")]
    q_heads = [t for t in subs if QUESTION_RE.search(t)]
    if not subs:
        issue("High", "No H2/H3 subheadings", "Break content into question-style H2/H3 sections.", 10)
    elif len(q_heads) / len(subs) < 0.3:
        issue("Medium", f"Only {len(q_heads)}/{len(subs)} subheadings are phrased as questions",
              "Rephrase key H2/H3s as the questions users ask.", 8)

    # Answer-first: paragraph right after each question heading should be 20-80 words
    weak = 0
    for i, (tag, text) in enumerate(p.blocks):
        if tag in ("h2", "h3") and QUESTION_RE.search(text):
            nxt = p.blocks[i + 1] if i + 1 < len(p.blocks) else None
            if not nxt or nxt[0] != "p" or not 20 <= len(nxt[1].split()) <= 80:
                weak += 1
    if weak:
        issue("Medium", f"{weak} question heading(s) lack a concise 20-80 word answer paragraph",
              "Add a direct 40-60 word answer immediately under each question heading.", min(15, 5 * weak))

    if p.counts["ul"] + p.counts["ol"] + p.counts["table"] == 0:
        issue("Low", "No lists or tables", "Use lists/steps/tables for extractable facts.", 5)
    if p.counts["img_noalt"]:
        issue("Low", f"{p.counts['img_noalt']} image(s) missing alt text", "Add descriptive alt text.", 3)

    # Metadata / trust
    if not p.title.strip():
        issue("High", "Missing <title>", "Add a descriptive title.", 8)
    if not p.meta.get("description"):
        issue("Medium", "Missing meta description", "Add a 120-160 char summary answering the main query.", 5)
    if not p.canonical:
        issue("Low", "Missing canonical link", 'Add <link rel="canonical">.', 3)
    if not p.lang:
        issue("Low", "Missing <html lang>", "Declare the page language.", 2)

    # Structured data
    types, bad = jsonld_types(p.jsonld)
    if bad:
        issue("High", f"{bad} JSON-LD block(s) fail to parse", "Fix JSON syntax in ld+json scripts.", 8)
    if not types:
        issue("High", "No JSON-LD structured data", "Add Article/FAQPage/HowTo/Organization JSON-LD.", 12)
    else:
        if q_heads and "FAQPage" not in types and "QAPage" not in types:
            issue("Medium", "Question headings present but no FAQPage schema",
                  "Add FAQPage JSON-LD mirroring the visible Q&A.", 5)
        has_author = bool(re.search(r'"author"\s*:', " ".join(p.jsonld))) or "author" in p.meta
        if not has_author:
            issue("Medium", "No author signal", "Add a visible byline and author in JSON-LD.", 5)
        if not re.search(r'"date(Modified|Published)"\s*:', " ".join(p.jsonld)) and not p.counts["time"]:
            issue("Low", "No published/modified date", "Add datePublished/dateModified.", 4)

    # Crawlability (URL only)
    crawl: dict = {}
    if is_url:
        base = f"{urlparse(target).scheme}://{urlparse(target).netloc}"
        robots = fetch(urljoin(base, "/robots.txt"))
        if robots is not None:
            blocked = [b for b in AI_BOTS if robots_blocks(robots, b)]
            crawl["blocked_bots"] = blocked
            if blocked:
                issue("High" if {"Bingbot", "OAI-SearchBot", "PerplexityBot"} & set(blocked) else "Medium",
                      f"robots.txt blocks: {', '.join(blocked)}",
                      "Allow search/answer bots you want to be cited by (see references/crawlers.md).",
                      min(15, 3 * len(blocked)))
        llms = fetch(urljoin(base, "/llms.txt"))
        crawl["llms_txt"] = bool(llms and llms.lstrip().startswith("#"))
        if not crawl["llms_txt"]:
            issue("Low", "No /llms.txt", "Add an llms.txt site map (see templates/llms.txt).", 4)

    order = {"High": 0, "Medium": 1, "Low": 2}
    findings.sort(key=lambda f: order[f["priority"]])
    return {
        "target": target,
        "score": max(0, score),
        "title": p.title.strip(),
        "jsonld_types": sorted(types),
        "headings": {"total_subheadings": len(subs), "question_style": len(q_heads)},
        "crawl": crawl,
        "findings": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("target", help="URL or local HTML file")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()
    r = audit(args.target)
    if args.json:
        print(json.dumps(r, indent=2))
        return 0
    s = r["score"]
    verdict = "Strong" if s >= 85 else "Needs work" if s >= 60 else "Poor"
    print(f"AEO score: {s}/100 ({verdict}) — {r['target']}")
    print(f"JSON-LD types: {', '.join(r['jsonld_types']) or 'none'}")
    h = r["headings"]
    print(f"Question-style subheadings: {h['question_style']}/{h['total_subheadings']}")
    if r["crawl"]:
        print(f"llms.txt: {'yes' if r['crawl'].get('llms_txt') else 'no'}; "
              f"blocked AI bots: {', '.join(r['crawl'].get('blocked_bots', [])) or 'none'}")
    if r["findings"]:
        print("\nPriority | Issue | Fix")
        for f in r["findings"]:
            print(f"{f['priority']} | {f['issue']} | {f['fix']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
