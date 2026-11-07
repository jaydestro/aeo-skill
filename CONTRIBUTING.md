# Contributing

Ideas, bugs, missing content types, rule improvements, and compatibility reports
are welcome. [Open an issue](https://github.com/jaydestro/aeo-skill/issues/new)
to describe the problem, or [open a pull request](https://github.com/jaydestro/aeo-skill/compare)
with a focused change. Include the agent/CLI version, reproduction, expected
behavior, evidence, and relevant rule ID. Do not submit secrets, private source
content, personal data, or proprietary material.

## Testing and adding rules

The default suite is standard-library Python, offline, and runs on Python 3.10+:

```bash
python3 -m unittest discover -s tests -v
```

CI runs it on pushes and pull requests. It covers parser/discovery behavior,
read-only reports, profile propagation, snapshots, escaping, installer safety,
complete packaging, manifests, rule coverage, and the controlled Sprocket
fixture. It does **not** automatically judge prose quality or prove every
agent follows natural-language rules.

When adding or changing a rule:

1. Assign a stable `AEO-RNNN` ID and document it with the behavior, scope, evidence, failure/unknown handling, and
   approval boundary in the relevant skill/reference. Keep it host-neutral.
2. Add or update a stable entry in `tests/rules.json`. Cite a real automated
   test where code can exercise the rule, and/or a concrete scenario in
   `tests/agent-scenarios.md` for agent-only behavior. Do not claim a
   helper-level test enforces the host agent's permissions.
3. Write a failing regression first where practical, with both allowed and
   disallowed/boundary behavior. Use local fixtures or mocked fetches, not live
   network access in the default suite. A source-text keyword assertion alone
   is not a behavioral test.
4. Run the full offline suite. Rule-catalog tests reject duplicate IDs, missing
   test methods, missing scenarios, unregistered rule IDs in skill documentation,
   and undocumented coverage. Keep concrete
   fixture defects and snapshots consistent.
5. For prompt/permission/domain behavior, run the named agent scenario and
   record the actual agent/model/version, tools, mode, prompt, source hashes,
   report, observed edits, and pass/fail/unknown evidence in your PR. Unrun or
   inaccessible scenarios remain **not evaluated**, not passed.

Optional real-manager checks require npx, and APM or uv, with permitted network
access. They use temporary projects/home directories, do not install into your
actual agent profile, and must be explicitly enabled:

```bash
AEO_CLI_SMOKE=1 python3 -m unittest discover -s tests -p test_cli_integration.py -v
```

On PowerShell, set `$env:AEO_CLI_SMOKE="1"` first. The default suite skips these
checks. These test CLI discovery/copies, not authenticated provider reasoning.
Review third-party installer behavior and its documented telemetry controls.

## Assessment and compatibility changes

Keep the twenty rubric IDs and evidence-backed pass/fail/unknown semantics.
Changing criterion meaning, weight, profile, subject, tasks, or evidence scope
requires a fresh baseline; explain migrations instead of reporting artificial
before/after gains. Preserve general-purpose defaults and technical checks when
relevant, existing report filenames, approved-apply scope, and live URL report-only
boundaries. Verify provider/package-manager formats against current primary
sources and record unavailable evidence.

Keep one canonical skill under `skills/aeo`. Plugins/extensions are packaging,
not duplicated instruction sets or hidden permission grants. Include the MIT
license in skill copies; root and bundled license must match.

## Original work and license

Contributions are submitted under this repository's [MIT license](LICENSE).
Author original code, instructions, examples, and rubrics. Do not copy
third-party skills or proprietary content. External skills are validation-only
comparators; cite authoritative factual documentation separately. Do not claim
guaranteed rankings, citations, conversion uplift, expert certification, or
test results that were not observed.

## External score comparisons

An external URL-scoring service can supply a separate before/after benchmark,
not a replacement for the editorial rubric. Use public URLs only, keep the
same provider/rubric and scope, save timestamps and raw results, and re-fetch
actual published changes. Do not report local suggestions as externally measured
improvements or enable third-party requests/paid jobs without explicit scope.

[AI Crawler Health Check](https://github.com/sstklen/aeo-crawler-check)
documents a public URL-to-AEO-score endpoint at
`https://aeo.washinmura.jp/api/v1/crawl-check`. Its published scoring emphasizes
crawlers, sitemaps, `llms.txt`, and schema; those assumptions differ from this
skill's evidence-backed content rubric. The published point breakdown also
sums to 95 although its total row says 100. Treat it as a candidate heuristic
benchmark, not an endorsed content-quality validator. Live verification failed
DNS on 2026-11-07; no working integration or observed external score is claimed.
