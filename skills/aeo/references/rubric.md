# Content-readiness rubric v2

This is a **local editorial assessment**, not an industry-standard AEO score,
search-engine ranking model, or predictor of citations. It operationalizes the
skill's [content guidance](content-guidelines.md) and
[source-backed playbooks](research.md). The weights are transparent design
choices, not scientifically validated ranking factors.

Use it per article, page, or identified copy unit during the initial
scan and after actual updates. A
static HTML/Markdown parser cannot score these semantic criteria by itself.
The agent must inspect content and evidence, identifying what it could not
verify. Do not award points merely because a heading, link, schema field, date,
or byline exists.

Version 2 makes technical-copy and code/media evidence requirements explicit
and adapts criteria to short descriptions as well as articles. Keep the same
five dimensions, twenty IDs, and point scale, but establish a v2 baseline;
do not report a direct delta against a v1 assessment.
The general profile uses these same criteria without changing the point scale.
Use [profiles.md](profiles.md) for domain-appropriate evidence and the optional
technical overlay. Existing v2 technical assessments retain their original context.

Record which claims, passages, examples, and companion pages were inspected.
Passing a criterion based on that evidence does not certify all possible claims
or tasks. Keep the assessed set fixed for comparison and disclose sampling;
unavailable evidence needed to judge a criterion makes it unknown.
For uncertain or stale external facts, follow the skill's source-verification
workflow and use permitted web tools before awarding points. Record source URLs
and version/access dates; search-snippet presence alone is not a pass.

## Set the assessment context first

Record page/file identity, source revision, assessment time, review profile, subject, content type,
primary product (or unspecified), intended audience/consumer, supported version/language, and representative
questions/tasks. Select tasks based on the page's actual purpose, including an
unsupported question or relevant boundary case. Keep this context and the
criterion interpretations unchanged for before/after comparison.

Adapt the evidence, not the point scale: a blog needs supported insight, a
tutorial needs correct steps/results, an API reference needs a correct contract,
and an internal KB needs authorized source provenance. Narrative articles do
not need API parameters; API references do not need personal bylines or FAQs.
Educational, editorial, marketing, policy, narrative, and short-description
content use their own purpose and evidence, without forced technical requirements.
Distinguish factual claims from clearly framed fiction and opinion.
Short descriptions, README sections, help/error copy, and tool
descriptions use their own purpose and surface constraints; they do not need
an article introduction or artificial headings. Identify the assessed unit and
its surrounding context instead of mixing it with unrelated content.

Inventory and review code blocks, images/diagrams, embedded videos, tables, and
other meaningful elements with [technical-review.md](technical-review.md).
Use their evidence for B1/B4 (accuracy/consistency), C3/C4 (format and faithful
delivery), D1-D4 (precision, prerequisites, caveats, examples), and E2/E3
(version/link context). A missing asset is a failure when confirmed; inability
to inspect necessary evidence is unknown. Presence alone earns no points.
If no such elements exist and none are needed, explain applicability without
adding irrelevant media. Distinguish static inspection from actual execution
or playback; claims that need those checks remain unknown if unverified.

## Twenty criteria, five points each

Mark every criterion **pass**, **fail**, or **unknown**. Pass earns five points;
fail earns zero. Attach a file/section/quote, source URL, or verification result
to every judgment, including failures. Unknown is not a failure or a pass.

| Dimension | ID | Criterion |
|---|---|---|
| Purpose and answer coverage | A1 | Title/introduction or short-copy wording/context clearly identify the topic, audience, and purpose |
| Purpose and answer coverage | A2 | The main question, thesis, task, capability, or recovery action is addressed directly and appropriately for the surface |
| Purpose and answer coverage | A3 | The preselected representative questions/tasks are sufficiently covered |
| Purpose and answer coverage | A4 | The page contributes useful specifics, examples, or original insight beyond generic claims |
| Factual support and trust | B1 | Material factual claims or instructions checked against authoritative evidence are supported |
| Factual support and trust | B2 | Claims/measurements needing provenance have traceable relevant sources or documented first-hand methods |
| Factual support and trust | B3 | The responsible author, publisher, team, or authoritative source is identifiable and authentic |
| Factual support and trust | B4 | Facts, examples, and conclusions agree internally and with relevant authoritative companion sources |
| Structure and extraction | C1 | Organization suits the surface and makes the relevant information easy to locate; headings/sections where useful, precise wording for short copy |
| Structure and extraction | C2 | Retrieved key passages preserve subject, conditions, and qualifications without misleading missing context |
| Structure and extraction | C3 | The format suits the information: steps, code, tables, prose, or media equivalents as appropriate |
| Structure and extraction | C4 | The assessed representation exposes the important text, examples, and warnings faithfully |
| Precision and task usefulness | D1 | Terminology, entities, identifiers, units, or parameters are unambiguous where relevant |
| Precision and task usefulness | D2 | Necessary prerequisites, assumptions, applicability, or environment are explicit |
| Precision and task usefulness | D3 | Limitations, exceptions, failure paths, or counterarguments needed for a correct answer are preserved |
| Precision and task usefulness | D4 | Examples, comparisons, explanations, or instructions enable the stated purpose and have been checked appropriately |
| Identity and maintenance | E1 | The authoritative page/source identity is clear enough to attribute the answer |
| Identity and maintenance | E2 | Relevant version/time context is accurate and clear; evergreen content is not assigned invented dates |
| Identity and maintenance | E3 | Relevant companion/source links or references are usable and resolve to the intended material |
| Identity and maintenance | E4 | The page agrees with maintained representations/related content, or clearly labels intentional version/history differences |

When a criterion refers to information that the page legitimately does not
need, explain why the page satisfies that criterion without it. For example,
an evergreen definition can pass E2 because it has no time-sensitive claims;
it does not need a fabricated publication date. If you cannot determine
applicability or inspect necessary evidence, mark unknown. Do not silently drop
criteria, change weights, or force irrelevant content into the page.

## Calculation and reporting

Each dimension contains four criteria and scores 0-20. A complete assessment
scores `5 * number_of_passes` out of 100, with no letter-grade or visibility
threshold. State that this measures inspected content readiness.

If any criterion is unknown, **do not publish a single complete /100 score**.
Report a range: `earned points` to `earned points + 5 * unknown count`, plus
known/unknown criterion counts. For a dimension with unknowns, report its range
instead of a falsely precise number. This prevents untested pages from looking
equivalent to fully inspected ones.

Example: 12 passes, 6 fails, 2 unknowns means **60-70/100, incomplete
(18/20 assessed)**, not 60/100 or a score normalized over the known checks.
After all 20 criteria are assessed, 17 passes means **85/100**. Do not claim
a precise +25 delta between that incomplete baseline and the completed result;
report which criteria became known and their outcomes.

For complete comparisons, report `after - before` in points and list changed
criterion IDs/evidence. Example: 12 passes before and 17 after means
**60 -> 85 (+25)**. A changed question set, rubric, source scope, or interpretation
requires a new baseline, not a directly comparable delta.
Changing the primary product also changes assessment context and requires a
new baseline. A product flag never validates the existence of a feature.
Changing the profile or subject interpretation likewise requires a new baseline.

Live URL inputs are report-only: score observed content, not an imagined rewrite.
Re-score only after fetching actual updated content. If a source cannot be
inspected at all, report "not scored" and the reason rather than a vacuous
0-100 range. List blocked URLs alongside reviewed URLs in corpus coverage.

Do not conceal regressions or count proposed snippets as completed changes.
For corpus reports, show per-page assessments and coverage. Average only a
disclosed fixed set of fully assessed pages; keep incomplete/excluded pages
visible and never describe a sample average as a full-site score.

## Separate blockers and empirical outcomes

Always report these separately, even if the content score is high:

- Intended-consumer delivery: fetched/rendered usable content, or blocked/unknown.
  Public search access differs from authorized internal retrieval.
- Policy/eligibility: intentional or accidental robots/index/snippet restrictions;
  do not relax them merely to improve the score.
- Material factual contradictions, unsafe instructions, and fabricated evidence.
  A high aggregate score does not excuse these; do not label the page ready
  while an unresolved material correctness problem remains.
- Existing docs/build/link/example validation results and unavailable checks.
- Actual retrieval accuracy, version-correct citation, task success, and
  abstention results, when measured.

Missing FAQ schema, `llms.txt`, question-heading ratios, fixed word counts,
or permission for model training never deduct points by themselves.

## Report skeleton

```text
Source: local repository | live URL
Mode: report-only | review-first | auto-apply (local only)
Page/copy unit, source revision or final URL/fetch date:
Profile, subject, content type, audience, relevant date/version, target tasks:
Rubric: content-readiness v2

Dimension | Before (0-20 or range) | After (0-20 or range) | Changed IDs/evidence
Purpose and answer coverage |
Factual support and trust |
Structure and extraction |
Precision and task usefulness |
Identity and maintenance |

Total: complete /100 or incomplete range; after only if actually reassessed
Coverage: assessed /20; unknown IDs and reasons
Delta: only for comparable complete assessments
Blockers and validation:
Code/media inventory and inspected/unavailable evidence:
Proposals/applied changes: stable IDs, concrete edits, supporting evidence
Approval request (local review-first), completed updates (auto-apply), or final report (report-only)
```
