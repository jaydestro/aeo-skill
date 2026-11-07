# AEO research and adaptation

Reviewed 2026-11-07. This is a broad prioritized synthesis, not an exhaustive
internet census. Direct provider-page fetches failed DNS in the research
environment; the statements below were verified through indexed primary-source
excerpts. Reopen current sources before deploying policy changes.
This ledger is a starting point, not a substitute for live verification of
uncertain or time-sensitive claims. Follow the source-verification workflow in
`../SKILL.md`; report unavailable access rather than assuming this review is current.

## Evidence mapped to implementation

| Primary source | Finding | Skill adaptation |
|---|---|---|
| [Google AI features](https://developers.google.com/search/docs/appearance/ai-features) | Ordinary SEO applies; indexing and snippet eligibility matter; no special AI schema required | Check delivery, links, index state, preview restrictions; do not promise inclusion |
| [Google AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Useful original content and technical fundamentals, not artificial chunking or AI-text-file hacks | Prioritize expertise and tasks; no universal word count, heading ratio, or chunk size |
| [Google documentation updates](https://developers.google.com/search/updates/) | llms.txt does not affect Google visibility; FAQ rich results deprecated May 2026 | Make llms.txt optional; supersede older government/health-only FAQ advice |
| [OpenAI crawlers](https://developers.openai.com/api/docs/bots) | OAI-SearchBot, GPTBot, and ChatGPT-User have independent purposes | Preserve training opt-outs; ChatGPT-User is not search control and robots may not apply |
| [Anthropic crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) | Separate search, training, user agents | Include Claude-SearchBot; Anthropic documents robots controls for Claude-User |
| [Perplexity crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers) | PerplexityBot is search, not foundation training; user fetches generally ignore robots | Check target-path search access and verified delivery; distinguish user fetches |
| [Google robots guidance](https://developers.google.com/search/docs/crawling-indexing/robots/intro) | Crawl denial is not guaranteed removal or authentication | Check index/serving controls separately and preserve privacy boundaries |
| [Google FAQ/HowTo changes](https://developers.google.com/search/blog/2023/08/howto-faq-changes) | HowTo rich results deprecated September 2023 | Schema vocabulary does not imply a Google feature or AI citation |
| [Bing AI Performance](https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview/) | Citation/page/grounding-query observations; IndexNow supports update discovery | Measure actual citations and fresh delivery; counts are not ranking or all-engine coverage |
| [Bing Topics Portfolio beta](https://blogs.bing.com/webmaster/2026/10/introducing-topics-portfolio-beta-in-ai-performance/) | Thematic coverage where data/UI available | Use to prioritize missing tasks, not as a mandatory tool |
| [llms.txt proposal](https://llmstxt.org/) | Evolving curated agent-navigation format | Maintain optional linked Markdown; publisher adoption does not prove search consumption |
| [Cloudflare Markdown for Agents](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/) | Optional `Accept: text/markdown` delivery | Test conversion fidelity and cache variation; not a universal requirement |
| [Diataxis](https://diataxis.fr/) | Tutorials, how-to, reference, explanation serve different needs | Preserve content-specific structure, not a universal FAQ layout |
| [GEO research](https://arxiv.org/abs/2311.09735) | Benchmark-specific visibility experiments | Test real evidence/clarity; do not predict production uplift from reported percentages |

Provider statements are **documented** within their scope; writing/structure
guidance is **editorial**. llms.txt interoperability and GEO interventions are
**experimental**. Unavailable engine measurements are **unknown**, not successes.
Recheck sources when provider features or policies change; indexes can lag.

## Content-type playbooks

These source-backed playbooks cover selected surfaces; use
[profiles.md](profiles.md) for the general core, including marketing,
educational, policy, and narrative content, and the optional technical overlay. Apply
[technical-review.md](technical-review.md) to prose, descriptions, code examples,
and embedded assets. Live URLs produce reports/scores only; local source updates
follow the skill's approval and auto-apply scope rules.

| Surface | Optimize for | Verify |
|---|---|---|
| Blog/editorial | Thesis, original analysis, primary evidence, methodology, accountable authorship, real dates, caveats | Claims, citations, and excerpts preserve scope; retain useful narrative |
| Tutorial | Learning goal, tested version/prerequisites, steps, expected output, checkpoints, cleanup | Run from a supported clean setup |
| How-to/runbook | Outcome, permissions, commands/configuration, verification, failure/rollback paths | Task success and safe handling of errors/destructive steps |
| Concept docs | Definitions, relationships, rationale, worked examples, trade-offs | Conceptual answers do not invent capabilities |
| API/CLI reference | Stable operation identity/version, types/defaults, auth, examples, errors, pagination/limits | Native OpenAPI/schema validation and implementation/example tests |
| FAQ/support | Actual questions/error strings, diagnostics, affected versions, resolution/escalation | Retrieve by symptom/code and test the fix |
| Product/pricing | Entity, actual capability, price/currency/billing units, availability, effective date | Source-of-truth facts and honest comparison criteria |
| README/internal KB | Scope, source/owner, setup/task links, access classification, version | Authorized retrieval; private content need not be search indexed |
| Release notes | Exact version/date, migrations, deprecations, compatibility | Historical and current claims remain distinct |
| PDFs/media | Searchable text, transcript/diagram descriptions, provenance, accessible canonical copy | Intended consumer's text extraction/order; not the HTML audit |
| JSON/YAML/other exports | Stable IDs, descriptive fields, types/units/version, source identity | Native validators and intended consumers, not prose linting |

## Site-wide and agent publishing

Link overview -> tutorial/how-to -> reference -> troubleshooting with descriptive
links and stable anchors. Avoid orphan pages and near-duplicate query variants.
Keep sitemaps, canonical/version/language policies consistent. Do not collapse
meaningfully different historical references into latest-only canonical copies.

Generate HTML, clean Markdown, API schemas, and optional llms.txt from one
maintained source. Preserve warnings, links, code languages, version and source
identity. Raw MDX may omit component/tab/transclusion content; inspect the
rendered/exported result. For negotiated Markdown use correct Content-Type and
cache variation (normally `Vary: Accept`), retain authentication, and verify
equivalence. Never create hidden agent-only claims or instructions.

An llms-full.txt dump is optional; bounded topic documents often suit retrieval
better. Keep source URLs and version boundaries. No bot request, token reduction,
or successful file fetch proves correct answers or citations.

## Evaluation and measurement

Create a fixed representative question/task set before edits. Include negative
and wrong-version cases. Record expected facts, source URL/anchor, required
caveats, prohibited claims, corpus revision, engine/model/configuration, exact
query, locale, timestamp, fresh context, answer and citation evidence.

Compare repeated runs when nondeterministic. Report retrieval success, supported
answer accuracy, correct citations, runnable task success, and correct abstention
with denominators and failures. Do not fabricate unavailable results or infer
causality from an uncontrolled before/after observation.

Use current Search Console reports (Google's AI-feature guide describes Web
performance data) and Bing AI Performance where available. Confirm UI features
instead of inventing filters. Separate citation, brand mention, referral, and
conversion. Bot logs show delivery, not citations; referrers miss some usage.
Record external query conditions, recrawl delays, personalization, and engine
changes. Static checks are never a proxy for these outcomes.

The [content-readiness rubric](rubric.md) provides a separate, transparent local
editorial assessment for before/after scans. Its weights are project-defined,
not validated ranking factors. Keep unknowns, delivery blockers, and empirical
retrieval/citation outcomes separate from the rubric score.
