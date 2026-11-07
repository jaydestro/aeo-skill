# Technical Copy Readiness Skill

An [Agent Skill](https://agentskills.io) for reviewing and improving **technical
copy for humans and agents**: blogs, docs, READMEs, API/CLI references, package/
product/tool descriptions, help/errors, onboarding, and other technical surfaces.
It reviews code examples and embedded media alongside prose. AEO/GEO supports
discovery and citation but does not override correctness, clarity, or usability.
The repository and skill name remain `aeo-skill` / `aeo` for compatibility.

## What it does

- **Reviews** local repository sources or live URLs with evidence-backed scores
- **Scans recursively** across article subdirectories, root/nested READMEs,
  and other repository documentation with explicit coverage and exclusions
- **Produces Markdown reports** with stable recommendations that an agent can
  later apply by report filename or selected IDs
- **Adapts** technical copy to its audience, purpose, style, and surface constraints
- **Inspects** code blocks, configuration examples, videos, images, diagrams,
  tables, downloads, and embedded components; reports unavailable inspection
- **Validates** appropriate schema, delivery, version context, and factual attribution
- **Reviews** search versus training policies and optional agent-facing Markdown/`llms.txt`
- **Researches** uncertain or stale claims using available web tools and primary sources

See [research and adaptation](skills/aeo/references/research.md) for primary
sources, evidence limits, content-type playbooks, publishing, and evaluation.
No technique guarantees an AI citation. The original speculative numeric score,
word-count/heading quotas, mandatory schema, and training-access penalties are
removed. Missing `llms.txt` is not a defect.

A separate [content-readiness rubric](skills/aeo/references/rubric.md) now
supports evidence-backed before/after technical-copy assessments. It measures editorial
readiness, not predicted AI visibility.
See [the technical review playbook](skills/aeo/references/technical-review.md)
for code/media checklists, source permissions, and report structure.

## Repository documentation standards

[Shared standards](skills/aeo/references/repository-standards.md) apply to every
authorized repository document, including root/nested READMEs, `.github` guides,
articles, package docs, contributing/setup/reference/support content, and
localized/versioned variants. Review purpose, supported facts, human/agent
readability, correct examples, embedded media, source identity, and maintained
links/consistency. Requirements are adapted to the document's purpose, not
applied as universal schema, keyword, word-count, or public-indexing obligations.

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

### Local repository review and updates

Pass a repository root, directories, or files, including relevant READMEs,
descriptions, docs, example sources, and assets. The default local
**review-first** workflow is **scan -> score -> propose -> approve
-> update -> verify -> re-score**.
The agent first reviews technical content without changing repository content, presents
source-backed suggestions with stable IDs and concrete edits, and waits for
explicit approval. It then applies only the approved changes.
Article folders and nested READMEs are discovered recursively with no arbitrary
depth or file-count limit. Large scans use bounded batches and report exactly
which files/subtrees remain pending instead of calling a sample a full review.

For example:

> Use the AEO skill to scan `docs/` for content-readiness improvements. Do not
> modify files. Review prose, code blocks, images, videos, and other embeds.
> Report scores, prioritized changes with IDs, evidence, concrete diffs, and
> validation plans. Wait for my approval.

Then:

> Approve DOC-01 and DOC-03. Apply only those changes and validate them.
> Do not commit or push.

Or explicitly authorize delivery:

> Approve all proposed changes. Apply and validate them, then open a pull request.

Approving edits does not implicitly approve commits, pushes, publishing, or
access/crawler-policy changes. In review-first mode, additional findings remain
proposals until approved. The skill is behavioral guidance, not a tool-permission boundary;
use read-only sessions or host permission controls for technical enforcement.

### Save a Markdown report and apply it later

> Use the AEO skill to scan this repository recursively, including all article
> folders, root/nested READMEs, and other repo docs. Review code and embedded
> media. Save scores, evidence, concrete recommendations, and an apply prompt
> to `reports/technical-review.md`. Do not change the source content.

Then:

> Apply the proposed local recommendations from `reports/technical-review.md`
> to this repository. Recheck source snapshots, validate, re-score, and update
> the report with results. Do not commit or push.

Or approve selected IDs:

> Apply only AEO-0002 and AEO-0007 from `reports/technical-review.md` to `docs/`.

The agent follows [the report/apply workflow](skills/aeo/references/report-workflow.md)
and [Markdown report template](skills/aeo/templates/review-report.md). Reports
include per-source scores/criterion evidence, code/media coverage, stable IDs,
exact changes, dependencies, and original source snapshots. Applying checks
current files first and skips stale, blocked, or out-of-scope items rather than
blindly patching. The saved prompt/report itself is not authorization.

`Apply ... from <report.md>` is a prompt for the agent, not a shell command.
The audit helper does not execute report recommendations. Draft `needs-review`
suggestions require completion and approval before implementation. Live URL
findings still require separately authorized and verified local source mappings.

### Live URLs: reports and scores only

> Use the AEO skill to review https://example.com/docs and
> https://example.com/blog/tutorial. Return a report with current scores,
> code/media inspection coverage, and concrete suggestions. Do not edit anything.

Live URL inputs are always **report-only**, even if auto-apply or autopilot is
active. Inspect permitted rendered content, examples, and available media;
report what could not be accessed or evaluated. Do not change a website, CMS,
remote repository, or local checkout as part of a URL-only review. A later local
update needs explicitly authorized sources and verified URL-to-source mapping.

Local inputs can also be explicitly report-only. Mixed inputs keep separate
permissions: authorized local changes do not permit live-site changes. Reports
appear in the response unless a report-file destination is explicitly requested.
Uninspectable pages are not scored. Current scores are not hypothetical after
scores; compare only actual updated content against a matching baseline.

### Auto-apply (explicit opt-in, local sources only)

Authorize automatic in-scope content improvements when you do not want per-edit
approval:

> Use the AEO skill in auto-apply mode on `docs/`. Scan and score the pages,
> apply evidence-backed content improvements without asking me to approve each
> edit, validate them, and report before/after scores. Do not commit or push.

Autopilot/YOLO tool confirmations alone do not select this mode. An explicit
request to automatically improve a specified scope does. Uncertain or
out-of-scope changes stay proposals while independent authorized work continues.
Auto-apply does not implicitly authorize changes to authentication/crawler
policies, deployment, dependency installation, or external mutations. Commits,
pushes, or PR creation require explicit delivery instructions.

### Web verification and agent capabilities

In every mode, uncertain, conflicting, or time-sensitive claims trigger
authoritative source research when the host agent has permitted browsing tools.
The agent should search, inspect the relevant primary-source passage, and report
its URL and version/date context before changing facts or awarding evidence-based
rubric points. Failed or unavailable browsing stays an explicit unknown; the
agent continues work that does not depend on that evidence.

The skill does not supply web tools or bypass network restrictions. It also
does not authorize sending private content to search services. A host agent
needs web search/fetch or browsing capabilities to perform live verification.

This can remain a reusable **skill**. A dedicated agent is an optional wrapper
for preconfigured tools, permissions, and a specialized role; it can load this
same skill rather than duplicate its guidance. Tool availability is determined
by the host, not by calling the workflow an agent.

### Technical copy, code, and media scoring

The **content-readiness v2** rubric has five dimensions, each worth 20 points:
purpose/answer coverage, factual support/trust, structure/extraction,
precision/task usefulness, and identity/maintenance. Each dimension has four
evidence-backed pass/fail/unknown criteria.

With all 20 criteria assessed, the total is 0-100. Unknowns produce an incomplete
range rather than a guessed score. Compare the same page, tasks, rubric, and
criteria before and after actual edits; include changed criterion evidence,
regressions, and separate delivery/correctness blockers. No schema, word count,
or crawler trick automatically earns points. A high score cannot guarantee
indexing or citations.

Code correctness/context, image meaning, video transcripts/captions, and other
embedded elements contribute evidence to relevant criteria; merely having an
embed does not earn points. Unknown required inspection keeps those criteria
unknown. Short descriptions/help copy use surface-appropriate criteria, not
artificial article structure. Establish a v2 baseline rather than comparing it
directly against earlier v1 scores.

The agent performs this semantic assessment; the static audit script does not
compute it. Ask for a rubric assessment explicitly, or let the scan workflow
include it by default.

### Static audit

Or run the audit directly:

```bash
python3 skills/aeo/scripts/aeo_audit.py https://example.com --json
python3 skills/aeo/scripts/aeo_audit.py docs/guide.md --json
python3 skills/aeo/scripts/aeo_audit.py docs/ blog/ README.md --json
python3 skills/aeo/scripts/aeo_audit.py . --exclude 'dist' --exclude 'build' \
  --report technical-review.md
```

The static helper accepts multiple files/URLs and recursively scans directories.
It deduplicates overlapping inputs, skips symlinks and `.git`, `node_modules`,
`.venv`, `venv`, and `__pycache__` directories, and lists exclusions/errors.
`--exclude` is repeatable and matches a basename or a path relative to each
input directory; it does not filter explicitly supplied files. It does not
implicitly follow gitignore or implement host content-exclusion policies.
Use only authorized inputs.

`--report` writes a new Markdown **static scaffold**; the parent directory must
exist and existing files are never overwritten. The scaffold includes source
hashes, findings, coverage, and manual-review placeholders, but not guessed
rubric scores. The agent completes the semantic assessment and exact proposals.
The report destination is excluded from directory discovery.

Single-file/URL JSON retains the individual report object; directory or
multi-input JSON contains `reports`, `errors`, and `skipped` lists. Errors do not
prevent independent inputs from being reviewed; exit code 1 reports incomplete
input processing or a report-write failure. An empty supported corpus is an error.

This helper is not the complete technical-copy or media review. The agent uses
suitable tools for the other surfaces and shared repo-documentation standards.
HTML/Markdown/MDX only for this helper: binaries and API contracts need native validators.
The Markdown parser does not render MDX components or transclusions. The Python
robots parser is best-effort and does not implement every provider's precedence
or REP extension. Verify rules with provider tooling before deployment.
Network failures are explicit unknowns/errors, not successful checks. Exit code
1 means an input could not be audited; findings alone do not fail the command.
Clean static findings do not establish accurate answers, indexing, or citations.

Run regression checks with `python3 -m unittest discover -s tests -v`.

## License

MIT
