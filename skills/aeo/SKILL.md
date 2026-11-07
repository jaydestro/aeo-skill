---
name: aeo
description: Answer Engine Optimization (AEO) for web content. Use when asked to audit, write, or restructure pages so they are discovered, understood, and cited by AI answer engines (ChatGPT, Copilot, Perplexity, Gemini, Google AI Overviews), or when working with FAQ/HowTo schema, llms.txt, AI crawler robots.txt rules, or "answer-first" content.
---

# Answer Engine Optimization (AEO)

AEO makes content easy for AI answer engines to **retrieve**, **extract**, and **cite**. Classic SEO wins a ranked link; AEO wins the quoted answer.

## When to use

- Auditing a URL or local HTML file for AI-answer readiness
- Rewriting content into answer-first, quotable structure
- Adding or fixing structured data (JSON-LD: `FAQPage`, `HowTo`, `Article`, `Organization`, `Product`)
- Creating `llms.txt` or reviewing `robots.txt` for AI crawlers

## Workflow

1. **Audit** – run the audit script (Python 3.8+, stdlib only) and read its findings:
   ```bash
   python3 scripts/aeo_audit.py <url-or-file.html> [--json]
   ```
   It checks crawlability (robots.txt AI bots, `llms.txt`), structure (single H1, question-style headings, answer-first paragraphs, lists/tables), structured data (JSON-LD types), and trust signals (author, dates, canonical, meta description). Paths are relative to this skill's directory.
2. **Identify target questions** – list the 5–15 real questions a user would ask an assistant that this page should answer. Prefer conversational, long-tail phrasing ("How do I…", "What is the difference between…").
3. **Restructure content** using [references/content-guidelines.md](references/content-guidelines.md):
   - Put a 40–60 word direct answer immediately under each question heading.
   - One idea per section; self-contained passages that make sense when quoted alone.
   - Use lists, steps, and comparison tables for extractable facts.
4. **Add structured data** using [templates/](templates/) and [references/structured-data.md](references/structured-data.md). JSON-LD must match visible on-page content.
5. **Fix crawlability** per [references/crawlers.md](references/crawlers.md): allow desired AI crawlers, add `llms.txt` (see [templates/llms.txt](templates/llms.txt)).
6. **Re-run the audit** and report the before/after score and remaining issues.

## Output format

When reporting an audit, give:
- Overall score (0–100) and a one-line verdict
- A prioritized table: `Priority | Issue | Fix`
- Concrete rewritten snippets (headings, answer paragraphs, JSON-LD) — not generic advice

## Rules

- Never fabricate facts, statistics, authors, dates, or reviews to "boost" authority.
- Never add schema for content that isn't visible on the page.
- Don't keyword-stuff; write for a human reader first — answer engines reward clarity.
- Respect the site owner's crawler choices; recommend, don't silently change, `robots.txt` policy.
