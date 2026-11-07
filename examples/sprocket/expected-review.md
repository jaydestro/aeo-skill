# Sprocket reference review and evaluation

**Fictional exercise, not Azure guidance.** This is a reference assessment of
`before.md` and the checked-in `after.md`, not a claim that an unspecified agent
performed the rewrite. It includes one reviewed, snapshot-bound replacement
proposal covering all eight findings, so it can also demonstrate apply-by-report.
For a blind agent evaluation, create a fresh report without reading this reference.

Report format: technical-copy-review v1
Report status: reviewed reference proposal
Assessment date: 2026-11-07
Rubric: content-readiness v2
Mode: local review-first; no approval is stored or implied
Repository: the checkout containing `examples/sprocket/`
Scope: one reviewed article; source/support files inspected for evidence
Coverage: before.md and reference after.md assessed; no pending articles in this fixture scope

| Source ID | Local path | Exact-byte SHA-256 | Reference score |
|---|---|---|---|
| SRC-SP-BEFORE | examples/sprocket/before.md | b6deab9c4e3fea9910dc2d3bba724011d3b7542a8e5249de930c81b1fb5cb9b1 | 15/100 |
| SRC-SP-AFTER | examples/sprocket/after.md | c9324d709f7a355b2e74e9eb70b12ff865138280c139737cd014b63dde8e22d4 | 100/100 |

These are observed reference documents, not a projected score for a future
agent rewrite. Actual applied output must be rechecked and reassessed.

## Defects a reviewer should identify

| ID | Defect in before.md | Concrete correction |
|---|---|---|
| SP-01 | No Markdown main heading; unclear audience, outcome, and purpose | Give the page a useful title and explain the offline exercise early |
| SP-02 | Guaranteed speedup, zero RU, index changes, and all-account support contradict the local spec | Remove those benefits and state the mock's non-cloud boundary |
| SP-03 | `--mode turbo` is unsupported and batch size 1000 is out of range | Use `--items 12 --batch-size 4`; preserve code language/formatting |
| SP-04 | No working-directory/Python prerequisites or exact expected output | Document Python 3.10+, repository root, exact JSON, and verification |
| SP-05 | Unlimited inputs conflict with both the spec and "one item only" | Document actual inclusive ranges and explicit argument errors |
| SP-06 | Broken screenshot, vague alt text, and image-only instructions | Use the original local diagram, meaningful alt text, and equivalent prose |
| SP-07 | Nonexistent video treated as proof; no accessible alternative | Admit no recording exists and provide a labeled text walkthrough |
| SP-08 | Missing reference link and unsupported "current forever" claim | Link local spec/implementation and identify fixture version 0.1 |

## Consolidated apply recommendation

| Recommendation ID | Source | Priority | Status | Dependencies |
|---|---|---|---|---|
| SP-ALL | SRC-SP-BEFORE | High | proposed | Verified reference candidate and existing fixture assets |

**Exact proposed change:** replace the complete contents of
`examples/sprocket/before.md` with the exact bytes of
`examples/sprocket/after.md`, after verifying both hashes in the source table.
This one coherent replacement implements SP-01 through SP-08 without overlapping
patches. The defect IDs above are evaluation findings, not separate approved edits.
The reference candidate is an original local file, not material fetched from a
website or a command to execute.

**Scope:** article copy and documented example only. Do not change the fixture
specification, simulator, diagram, walkthrough, or a live Azure resource. Keep
the intentionally bad source for repeated testing by explicitly authorizing
`examples/sprocket/improved.md` as the output mapping instead of overwriting it.

**Verification:** confirm the baseline/candidate hashes; inspect the resulting
fiction warning, source links, code, diagram/text alternative, and no-recording
statement. With user permission for the safe local simulator, run the documented
command and compare its exact JSON. Reassess the same five tasks and rubric.
Do not infer Azure behavior or claim video playback.

### Apply all from this report

Copy and send this user instruction; its presence in the report is not approval:

> Use the AEO skill to apply all proposed local recommendations from
> `examples/sprocket/expected-review.md`. I authorize mapping the reviewed
> `before.md` source to a new `examples/sprocket/improved.md`; preserve the bad
> fixture and reference files. Verify baseline/candidate hashes, use the exact
> reviewed replacement, validate with safe local simulator execution, and
> report actual before/after results. Do not commit, push, deploy, or contact Azure.

If either snapshot changed, treat SP-ALL as stale and report it instead of
blindly copying. The same report provides both scores and implementation details;
no separate score or report scan is required.

Keep the fiction warning in every rewritten document. Do not fabricate Microsoft
citations or claim to have watched a video. The broken image/reference links
are confirmed missing local files; the video is deliberately nonexistent by
the fixture specification. Do not confuse that controlled fact with having
successfully fetched or played a real recording.

## Reference rubric assessment

Context: developers learning to review this offline fixture, version 0.1, using
the five tasks in [README.md](README.md). Sources inspected are the local spec,
simulator, documents, SVG text/structure, and walkthrough. Execution evidence
comes from the repository tests, not from an Azure service.

This manual reference assessment uses content-readiness v2. Judgments on a
different rewrite need their own evidence; matching these numbers is not the
acceptance criterion.

| Criterion | Before | After | Evidence / rationale |
|---|---|---|---|
| A1 | fail | pass | Before has vague title/purpose; after identifies the local mock and developer exercise |
| A2 | fail | pass | Before opens with vague unsupported benefits; after explains the actual calculation early |
| A3 | fail | pass | Before cannot answer the fixed tasks correctly; after addresses behavior, command, boundaries, and media |
| A4 | fail | pass | Before specifics are misleading; after supplies useful verified inputs, arithmetic, output, and troubleshooting |
| B1 | fail | pass | Before contradicts fixture-spec.md; after agrees with the local contract and simulator |
| B2 | fail | pass | Before has no evidence for its benefits; after links spec/implementation and avoids benchmark claims |
| B3 | pass | pass | Both identify this repository's fictional exercise rather than impersonating Microsoft |
| B4 | fail | pass | Before conflicts internally and with ranges/behavior; after/spec/walkthrough agree |
| C1 | fail | pass | Vague "Things" sections versus task-specific headings and coherent sequence |
| C2 | fail | pass | Before passages imply unlimited cloud capability; after key passages retain the fictional/local scope |
| C3 | pass | pass | Both present the command in a Bash code block; correctness is assessed separately |
| C4 | fail | pass | Before relies on missing media; after important information is available in text with a local SVG |
| D1 | fail | pass | Vague "stuff"/capacity versus explicit item count, batch size, named arguments, and result fields |
| D2 | fail | pass | "Run from wherever" versus Python version, working directory, and no-credential prerequisites |
| D3 | fail | pass | "No limitations" versus ranges, failures, and explicit non-cloud/no-performance caveats |
| D4 | fail | pass | Before command returns an argument error; after documented command matches reproducible JSON |
| E1 | pass | pass | Both are identifiable local documents explicitly labeled fictional rather than official guidance |
| E2 | fail | pass | Before labels version 0.1 but falsely treats all versions as identical/current forever; after keeps accurate scoped version context |
| E3 | fail | pass | Before local image/reference paths are missing; after local links/assets resolve |
| E4 | fail | pass | Before contradicts the maintained spec; after, simulator, and walkthrough align |

| Dimension | Before /20 | Reference after /20 |
|---|---|---|
| Purpose and answer coverage | 0 | 20 |
| Factual support and trust | 5 | 20 |
| Structure and extraction | 5 | 20 |
| Precision and task usefulness | 0 | 20 |
| Identity and maintenance | 5 | 20 |
| Total | 15/100 | 100/100 |

The reference delta is +85 points for this inspected fictional fixture only.
It is not a predicted search uplift, universal quality certification, or proof
of external visibility. If your tools cannot inspect a required source/asset,
mark affected criteria unknown instead of copying these complete scores.

## Reproducible checks and limits of proof

The automated example tests verify:

- The static helper finds the missing main title before and no static findings
  in the reference rewrite. This is not the full semantic assessment.
- The bad command fails locally; the reference command returns exactly the
  specified three-batch JSON. Boundary inputs and invalid flags are checked.
- The reference rewrite's local asset/source links resolve, the SVG includes
  an accessible description, and the fictional labeling remains intact.

These checks validate the reference artifacts and concrete fixes. They do not
execute an AI agent or compute the manual rubric from prose. Evaluate an actual
agent separately using its source-backed report and answers:

| Task | Required supported answer |
|---|---|
| Real Cosmos DB feature? | No; this is a fictional local training mock, not an Azure capability |
| Behavior and limits? | Local batch-count arithmetic; items 1-1000, batch size 1-32 |
| Reproduce three batches? | Python 3.10+, repository root, documented command, exact JSON |
| Cloud performance/RU changes? | None established or performed; do not claim a speedup or pricing effect |
| Media explanation? | Original diagram plus text; authored walkthrough; no recording to watch |

An agent that prettifies the text but preserves the false claims or invalid
command fails this exercise, regardless of its claimed score.
