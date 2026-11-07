# Shared content-readiness standards for repository documentation

Apply these standards to **all authorized repository documentation**, including
root and nested READMEs, articles, blogs, descriptions, docs indexes,
setup/reference/troubleshooting pages, contributing guides, `.github` guidance,
release notes, and localized/versioned variants. Discover Markdown/MDX, HTML,
reStructuredText, AsciiDoc, text documents, and prose embedded in supported
configuration/source formats using appropriate tools.

The static helper is only an HTML/Markdown/MDX check; its unsupported-format
list is not permission to omit other docs from the agent's requested review.
Classify each document's audience and purpose before applying requirements.
Contributor/security/internal documents may have intentionally different
access and presentation needs from public product articles.

## Shared standards

| Standard | Required review evidence | Related rubric |
|---|---|---|
| Clear purpose and scope | Identify audience, subject, relevant product/date/version, and what the document helps them understand or do | A1-A3 |
| Useful, direct information | Explain capabilities/tasks early; use concrete details without keyword or word-count quotas | A2-A4 |
| Supported factual claims | Check applicable authoritative evidence, provenance, limitations, and consistency; implementation/tests for technical behavior | B1-B4 |
| Human and agent readability | Appropriate organization, unambiguous terminology, accessible text, self-contained context, and source identity | C1-C4, D1, E1 |
| Correct examples and necessary conditions | Check relevant explanations, assumptions, exceptions, and safety; commands/configuration/output when present | D1-D4 |
| Meaningful embedded content | Inspect images, code, videos, tables, diagrams, and downloads; check text equivalents and disclose unavailable inspection | B1, C3-C4, D4 |
| Maintained relationships | Resolve relevant links; keep root/nested READMEs, docs, APIs, exports, and historical/localized copies consistent | E2-E4 |

Use [technical-review.md](technical-review.md) for code/media and copy constraints,
[profiles.md](profiles.md) for general-purpose and technical context,
[rubric.md](rubric.md) for evidence-backed scoring, and
[report-workflow.md](report-workflow.md) for coverage and apply-by-report.

## README-specific review

Check a root README for project identity/purpose, accurate capabilities, supported
setup/prerequisites, a usable first example, expected outcome, limitations, and
links to deeper docs/support/contribution information where appropriate. Check
commands against actual manifests/configuration and preserve useful badges,
images, videos, and reference links without assuming they are correct.

Nested package/component READMEs should identify their own scope, relationship
to the parent project, supported interfaces, setup/use differences, and relevant
local docs. Do not copy root-level requirements blindly into every tiny component
README. Localized/versioned READMEs must preserve intentional differences and
clearly identify their version/language.

## Corpus consistency and exclusions

Recursively discover every in-scope documentation subtree, including `.github`
and nested READMEs. Record explicit exclusions, generated/vendor/dependency
directories, denied access, unsupported tools, and pending docs. No hidden
article-count or directory-depth cutoff; label partial scans accurately.

Compare shared product facts, commands, examples, version claims, links, and
terminology across the corpus. Prefer authoritative maintained sources over
duplicated claims; propose template/shared-source fixes when appropriate.
Do not delete or rewrite valid history to make every document say the same thing.

If existing repository style/contributor standards are present, follow them and
identify any conflict explicitly. This reference defines the review standard;
it does not authorize adding a policy file to the target repository. Proposing
or updating contributor/style rules is a separately scoped recommendation.

## No artificial AEO obligations

Not every README or internal guide needs schema, a meta description, public
indexing, a byline/date, question headings, or `llms.txt`. Preserve intentional
private/noindex/training policies. Presence of these signals is not evidence of
content correctness, retrieval quality, or a guaranteed citation.

Record criterion evidence and applicable context in the Markdown report.
Missing essential information is a supported finding; unavailable evidence is
unknown. Do not invent facts or add irrelevant boilerplate to increase a score.
