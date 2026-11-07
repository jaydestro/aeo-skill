# AEO Agent Skill

An [Agent Skill](https://agentskills.io) that teaches AI coding agents (GitHub Copilot, Claude Code, etc.) to do **Answer Engine Optimization (AEO)** — making web content easy for AI answer engines like ChatGPT, Copilot, Perplexity, Gemini, and Google AI Overviews to retrieve, extract, and cite.

## What it does

- **Audits** a URL or HTML file with a stdlib-only Python script (score + prioritized fixes)
- **Rewrites** content into answer-first, question-led, quotable sections
- **Generates** JSON-LD structured data (`FAQPage`, `HowTo`, `Article`, …)
- **Reviews** `robots.txt` AI-crawler rules and creates `llms.txt`

## Layout

```
skills/aeo/
├── SKILL.md                 # Skill entry point (frontmatter + instructions)
├── scripts/aeo_audit.py     # Audit tool (Python 3.8+, no dependencies)
├── references/              # Content, structured-data, and crawler guidance
└── templates/               # JSON-LD and llms.txt templates
```

## Install

Copy (or symlink) `skills/aeo` into your agent's skills directory, for example:

```bash
# GitHub Copilot (personal skills)
cp -r skills/aeo ~/.copilot/skills/aeo

# Project-level (Copilot / Claude Code)
cp -r skills/aeo .github/skills/aeo   # or .claude/skills/aeo
```

## Use

Ask your agent things like:

- "Run an AEO audit on https://example.com/pricing"
- "Rewrite this doc page so it gets cited in AI answers"
- "Add FAQ schema and an llms.txt for this site"

Or run the audit directly:

```bash
python3 skills/aeo/scripts/aeo_audit.py https://example.com --json
```

## License

MIT
