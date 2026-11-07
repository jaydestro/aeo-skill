# Content Readiness Skill

An [Agent Skill](https://agentskills.io) for reviewing and improving **content
for humans and agents**: articles, blogs, marketing copy, education, policies,
descriptions, help, docs, READMEs, and other communication. General-purpose by
default, with an optional technical profile for code, APIs, and implementation.
It reviews embedded media and code when present alongside prose. AEO/GEO supports
discovery and citation but does not override correctness, clarity, or usability.
The repository and skill name remain `aeo-skill` / `aeo` for compatibility.

## What it does

- **Reviews** local repository sources or live URLs with evidence-backed scores
- **Scans recursively** across article subdirectories, root/nested READMEs,
  and other repository documentation with explicit coverage and exclusions
- **Produces Markdown reports** with stable recommendations that an agent can
  later apply by report filename or selected IDs
- **Adapts** content to its audience, purpose, domain, style, and surface constraints
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
supports evidence-backed before/after content assessments. It measures editorial
readiness, not predicted AI visibility.
See [the content/media playbook](skills/aeo/references/technical-review.md)
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

### One-line installs

Run skill/package installs from your target project. Pick **one** route rather
than installing duplicate copies through several managers.

| Route | Command |
|---|---|
| Interactive skill/agent selection | `npx skills add jaydestro/aeo-skill --skill aeo` |
| Every agent supported by the skills CLI, without prompts | `npx skills add jaydestro/aeo-skill --all` |
| APM, portable skill across its supported standard targets | `apm install jaydestro/aeo-skill/skills/aeo --target all` |
| APM without a persistent CLI install (requires uv) | `uvx --from apm-cli apm install jaydestro/aeo-skill/skills/aeo --target all` |
| GitHub Copilot CLI plugin | `copilot plugin install jaydestro/aeo-skill` |
| Claude Code plugin (current CLI) | `claude plugin install aeo --marketplace jaydestro/aeo-skill` |
| Gemini CLI extension | `gemini extensions install https://github.com/jaydestro/aeo-skill` |

`npx skills` requires Node.js 22.20+ according to its current documentation;
APM's Python distribution requires Python 3.10+. Provider commands require that
provider's CLI and supported version. Add `-g` to skill/APM installs for user
scope where supported. `--all`/`--target all` cover each manager's documented
agent set, not every possible product or experimental integration.

For a specific agent:

| Agent | One-line skill install |
|---|---|
| Claude Code | `npx skills add jaydestro/aeo-skill --skill aeo -a claude-code` |
| Codex | `npx skills add jaydestro/aeo-skill --skill aeo -a codex` |
| GitHub Copilot | `npx skills add jaydestro/aeo-skill --skill aeo -a github-copilot` |
| Cursor | `npx skills add jaydestro/aeo-skill --skill aeo -a cursor` |
| Gemini CLI | `npx skills add jaydestro/aeo-skill --skill aeo -a gemini-cli` |
| Windsurf | `npx skills add jaydestro/aeo-skill --skill aeo -a windsurf` |
| OpenCode | `npx skills add jaydestro/aeo-skill --skill aeo -a opencode` |
| Cline | `npx skills add jaydestro/aeo-skill --skill aeo -a cline` |
| Roo Code | `npx skills add jaydestro/aeo-skill --skill aeo -a roo` |
| Continue | `npx skills add jaydestro/aeo-skill --skill aeo -a continue` |
| Kiro CLI | `npx skills add jaydestro/aeo-skill --skill aeo -a kiro-cli` |
| Amp | `npx skills add jaydestro/aeo-skill --skill aeo -a amp` |

The current Claude CLI can add the marketplace during the one-line install.
For older versions or interactive use, add it in the session and then select
`aeo` using `/plugin`:

```text
/plugin marketplace add jaydestro/aeo-skill
```

The next interactive command is `/plugin install aeo@aeo-skill`. The skill-only
`npx` route above needs no marketplace registration.

These are install commands, **not approval to change reviewed content**.
External managers can write their own configuration, dependency manifests, and
lockfiles. Review their prompts/policies and avoid force or policy-bypass flags.
`npx skills` documents telemetry/security-audit requests; use its documented
`DO_NOT_TRACK=1` setting if desired. Installation does not provision browsing.
See [packages and primary sources](skills/aeo/references/distribution.md).

### Local installer and manual loading

Use one unchanged skill across coding agents. From this cloned repository:

```bash
# Install into a target project for all supported profiles
python3 scripts/install_skill.py --agent all --root /path/to/project

# Or select an agent and scope
python3 scripts/install_skill.py --agent copilot --root /path/to/project
python3 scripts/install_skill.py --agent claude --scope user
python3 scripts/install_skill.py --agent codex --scope user
```

Native profiles cover **Copilot, Claude Code, Codex, Gemini CLI, OpenCode,
Cline, and Roo Code**. **Cursor, Windsurf, Continue, Amazon Q, Kiro, Aider,
and other agents** have explicit-loading profiles using `.agents/skills/aeo`;
these do not claim unverified native discovery paths. The same review, product
context, rubric, report, and approved-apply workflow is used everywhere.

See [coding-agent compatibility](skills/aeo/references/agent-compatibility.md)
for exact paths, official sources, host/version limits, and smoke checks. Reload
the host and verify discovery; if needed, explicitly ask it to read the installed
`SKILL.md` and its references. No installation is necessary when you can load
`skills/aeo/SKILL.md` directly from this checkout.

The Python 3.10+ installer includes all resources and the license, never
overwrites conflicting installs, and leaves host rules and permissions untouched.
Native host sessions are not automatically activated or end-to-end certified.
Agents without permitted file/context access cannot use the skill; unavailable
web/media tools remain explicit unknowns. The static helper is optional.

## Use

### General-purpose or technical review

> Use the AEO skill to review `articles/` and `landing-page.md` with the general
> profile. Preserve the intended voice; inspect media and factual claims.
> Save one scored report to `content-review.md`. Do not edit source content.

```bash
python3 skills/aeo/scripts/aeo_audit.py articles/ --profile general --report content-review.md
python3 skills/aeo/scripts/aeo_audit.py docs/ --profile technical --product "Azure Cosmos DB" --report cosmos-review.md
```

The [general core and technical overlay](skills/aeo/references/profiles.md)
share the same rubric. Code checks still apply whenever code is present.
Narrative, marketing, educational, and policy content do not acquire irrelevant
API requirements. Preserve fiction/opinion boundaries and use qualified review
for high-impact claims. Fix profile, subject, product, tasks, and evidence scope
for before/after comparisons; changing them requires a new baseline.

### Set the primary product

Supply a product as review context in your agent prompt:

> Use the AEO skill to scan this repository with primary product
> "Azure Cosmos DB". Review its technical copy, examples, and media; save one
> scored Markdown report. Do not edit source files.

Or pass the flag to the static helper:

```bash
python3 skills/aeo/scripts/aeo_audit.py docs/ README.md \
  --profile technical --product "Azure Cosmos DB" --report cosmos-review.md --json
```

The product is recorded in JSON and Markdown and guides the agent's terminology,
API/version, capability, and source checks. It does not filter files or prove
feature support. If omitted, it remains unspecified. Keep it fixed for
before/after comparisons and applying a report.

The skill and examples are independently authored. Third-party skills are
validation references only; their code, wording, templates, and scoring rules
are not copied, installed, or executed. Primary factual sources remain cited.

### Local repository review and updates

Pass a repository root, directories, or files, including relevant READMEs,
descriptions, docs, example sources, and assets. The default local
**review-first** workflow is **scan -> score -> propose -> approve
-> update -> verify -> re-score**.
The agent first reviews content without changing repository content, presents
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

**Scan, report scan, score scan, and read-only review are one workflow.** Every skill scan produces
one consolidated Markdown report containing
all requested articles' scores/evidence, code/media coverage, supported improvements
with exact changes, and apply-all/selected-ID prompts. The default report-file
name is `content-review.md` (a new numbered name if already present).
Specify another destination or request inline-only output when preferred.
This authorizes the report artifact only, not article changes.
No second scoring/reporting request is necessary. A named report is ready for
an apply-all prompt once its concrete local proposals are reviewed.

This also works for **one document without editing it**:

> Use the AEO skill to review `README.md` in report-only mode. Save its scores,
> evidence, and all supported recommendations to `readme-review.md`.
> Do not change `README.md` or other source content.

If no report path is given, the normal `content-review.md` default applies.
An explicit inline-only/no-file instruction returns Markdown in the response.
No approval to edit is required to produce this read-only scored report.

> Use the AEO skill to scan this repository recursively, including all article
> folders, root/nested READMEs, and other repo docs. Review code and embedded
> media. Save scores, evidence, concrete recommendations, and an apply prompt
> to `reports/technical-review.md`. Do not change the source content.

Then:

> Apply the proposed local recommendations from `reports/technical-review.md`
> to this repository. Recheck source snapshots, validate, re-score, and update
> the report with results. Do not commit or push.

To execute the entire validated recommendation set, say:

> Apply all proposed local recommendations from `content-review.md`.
> Validate and re-score the changes and update the same report. Do not commit or push.

Or approve selected IDs:

> Apply only AEO-0002 and AEO-0007 from `reports/technical-review.md` to `docs/`.

The agent follows [the report/apply workflow](skills/aeo/references/report-workflow.md)
and [Markdown report template](skills/aeo/templates/review-report.md). Reports
include per-source scores/criterion evidence, code/media coverage, stable IDs,
exact changes, dependencies, and original source snapshots. Applying checks
current files first and skips stale, blocked, or out-of-scope items rather than
blindly patching. The saved prompt/report itself is not authorization.
Older `technical-copy-review v1` reports and explicitly named report files
remain usable; preserve their original assessment context.
For large repositories, the report includes a per-article assessment and combined
recommendation index, with explicit pending/unreviewed coverage. Applying all
respects dependencies and skips stale, blocked, or unreviewed recommendations.

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
permissions: authorized local changes do not permit live-site changes. Live
reviews use the same consolidated Markdown report default; explicitly request
inline-only output when no report artifact is wanted.
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

### Content, code, and media scoring

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

This helper is not the complete content or media review. The agent uses
suitable tools for the other surfaces and shared repo-documentation standards.
HTML/Markdown/MDX only for this helper: binaries and API contracts need native validators.
The Markdown parser does not render MDX components or transclusions. The Python
robots parser is best-effort and does not implement every provider's precedence
or REP extension. Verify rules with provider tooling before deployment.
Network failures are explicit unknowns/errors, not successful checks. Exit code
1 means an input could not be audited; findings alone do not fail the command.
Clean static findings do not establish accurate answers, indexing, or citations.

Run the offline suite with `python3 -m unittest discover -s tests -v`.
See [testing and adding rules](CONTRIBUTING.md#testing-and-adding-rules) for
regressions, rule coverage, opt-in CLI integrations, and agent conformance checks.

## Try the skill on an intentionally bad document

[The fictional Cosmos DB Sprocket exercise](examples/sprocket/README.md) includes
a flawed Learn-style article, a local source-of-truth spec and offline simulator,
a reference rewrite, code/media defects, and a criterion-by-criterion assessment.
Sprocket is not a real Azure feature and these are not Microsoft Learn documents.

Use the provided scan/report and apply prompts, then compare your agent's actual
results against the fixture's tasks and reproducible checks. The reference
rewrite demonstrates concrete improvements; it does not guarantee that every
agent will produce them or prove AI-search visibility.

## License

**MIT**, including the [bundled skill](skills/aeo/LICENSE). See [LICENSE](LICENSE).

## Contribute

Suggest improvements or report bugs by [opening an issue](https://github.com/jaydestro/aeo-skill/issues/new).
Contribute tested changes through a [pull request](https://github.com/jaydestro/aeo-skill/compare).
See [CONTRIBUTING.md](CONTRIBUTING.md) for rule tests, source verification,
original-authorship requirements, and compatibility checks.
