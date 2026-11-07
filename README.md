# AEO Agent Skill

An [Agent Skill](https://agentskills.io) that teaches AI coding agents (GitHub Copilot, Claude Code, etc.) to do **Answer Engine Optimization (AEO)** — making web content easy for AI answer engines like ChatGPT, Copilot, Perplexity, Gemini, and Google AI Overviews to retrieve, extract, and cite.

## What it does

- **Audits** HTML, Markdown, and MDX with static observations and explicit unknowns
- **Adapts** blogs, tutorials, API references, support, and other content to actual user tasks
- **Validates** appropriate schema, delivery, version context, and factual attribution
- **Reviews** search versus training policies and optional agent-facing Markdown/`llms.txt`

See [research and adaptation](skills/aeo/references/research.md) for primary
sources, evidence limits, content-type playbooks, publishing, and evaluation.
No technique guarantees an AI citation. The original speculative numeric score,
word-count/heading quotas, mandatory schema, and training-access penalties are
removed. Missing `llms.txt` is not a defect.

## Layout

```
skills/aeo/
├── SKILL.md                 # Skill entry point (frontmatter + instructions)
├── scripts/aeo_audit.py     # Static audit (Python 3.10+, no dependencies)
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

The intended workflow is **scan -> propose -> approve -> update -> verify**.
The agent first reviews docs without changing repository content, presents
source-backed suggestions with stable IDs and concrete edits, and waits for
explicit approval. It then applies only the approved changes.

For example:

> Use the AEO skill to scan `docs/` for content-readiness improvements. Do not
> modify files. Propose prioritized changes with IDs, evidence, concrete diffs,
> and validation plans. Wait for my approval.

Then:

> Approve DOC-01 and DOC-03. Apply only those changes and validate them.
> Do not commit or push.

Or explicitly authorize delivery:

> Approve all proposed changes. Apply and validate them, then open a pull request.

Approving edits does not implicitly approve commits, pushes, publishing, or
access/crawler-policy changes. Additional findings remain proposals until
approved. The skill is behavioral guidance, not a tool-permission boundary;
use read-only sessions or host permission controls for technical enforcement.

Or run the audit directly:

```bash
python3 skills/aeo/scripts/aeo_audit.py https://example.com --json
python3 skills/aeo/scripts/aeo_audit.py docs/guide.md --json
```

Audit one file/URL per invocation; inventory the requested corpus with the
agent. HTML/Markdown/MDX only: binaries and API contracts need native validators.
The Markdown parser does not render MDX components or transclusions. The Python
robots parser is best-effort and does not implement every provider's precedence
or REP extension. Verify rules with provider tooling before deployment.
Network failures are explicit unknowns/errors, not successful checks. Exit code
1 means an input could not be audited; findings alone do not fail the command.
Clean static findings do not establish accurate answers, indexing, or citations.

Run regression checks with `python3 -m unittest discover -s tests -v`.

## License

MIT
