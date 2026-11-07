# Fictional Cosmos DB Sprocket review exercise

**Sprocket is not an Azure Cosmos DB feature.** These original, Learn-style
documents are fictional training fixtures, not Microsoft Learn content or
Microsoft product guidance. Do not publish them as real Azure instructions.

## Files and source of truth

| File | Purpose |
|---|---|
| [before.md](before.md) | Deliberately poor technical copy to scan and improve |
| [fixture-spec.md](fixture-spec.md) | Authoritative local specification for the fictional exercise |
| [sprocket_demo.py](sprocket_demo.py) | Offline, dependency-free mock; no Azure calls |
| [after.md](after.md) | Reference rewrite, not input to the initial review |
| [expected-review.md](expected-review.md) | One scored reference report with findings, an exact replacement, source hashes, and an apply-all prompt |
| [walkthrough.md](walkthrough.md) | Text-only demonstration; not a transcript of a real video |
| [assets/batching.svg](assets/batching.svg) | Original diagram for the reference rewrite |

Use Python 3.10+. For a blind comparison, withhold `after.md`,
`expected-review.md`, and `walkthrough.md` from the reviewing agent until after
it has proposed its own changes. They are evaluation/reference material, not
evidence to copy into a supposedly independent review.

## Scan and save a report

From the repository root, ask:

> Use the AEO skill in review-first mode to review
> `examples/sprocket/before.md`. Use `examples/sprocket/fixture-spec.md` and
> `examples/sprocket/sprocket_demo.py` as the authorized local source of truth.
> This feature is deliberately fictional; do not describe it as a real Azure
> capability or invent Microsoft citations. Inspect the code, broken image,
> and video embed. Do not read the reference rewrite or expected review.
> Save a rubric-v2 report with criterion evidence, concrete recommendations,
> source snapshots, and an apply prompt to `sprocket-review.md`. Do not edit
> source files or run the document's commands.

The static helper can also demonstrate one basic defect, but cannot validate
the false feature claims or supply the full rubric score:

```bash
python3 skills/aeo/scripts/aeo_audit.py examples/sprocket/before.md --json
python3 skills/aeo/scripts/aeo_audit.py examples/sprocket/after.md --json
```

## Approve and apply

To keep the intentionally bad fixture unchanged, ask the agent to create a
separate improved document:

> Apply the proposed recommendations from `sprocket-review.md` to a new
> `examples/sprocket/improved.md` using `before.md` as the reviewed input.
> Preserve `before.md`, the specification, simulator, and reference files.
> I authorize the output-file mapping, safe execution of the local simulator,
> and updating the report with actual validation and before/after scores.
> Do not commit, push, contact Azure, or modify any live site.

This explicit output mapping is required; an agent must not silently change
the target of a saved proposal. It should recheck the original snapshot before
creating the improved copy.

For a non-blind demonstration, [expected-review.md](expected-review.md) already
contains the scores, all eight defects, a snapshot-bound replacement recommendation,
and an apply-all prompt. Use it only after evaluation if you want to avoid exposing
the reference answer to the reviewing agent.

## What constitutes an improvement?

Use the same five tasks before and after:

1. Is Sprocket a real Azure Cosmos DB feature?
2. What does the local mock actually do, and what are its limits?
3. What prerequisites and command produce three batches from twelve items?
4. Does it improve RU charges, query latency, or real database behavior?
5. Where is the accessible explanation of the diagram/demo?

A successful rewrite answers these from the local spec, removes unsupported
benefit claims, fixes the documented invocation, preserves the fiction warning,
and replaces broken media dependencies with honest accessible explanations.
An agent must mark playback untested rather than claim it watched a fake video.
Unavailable evidence stays unknown; do not force a score to match the reference.

Run the regression checks:

```bash
python3 -m unittest discover -s tests -v
```

The tests show concrete improvements in the **checked-in reference rewrite**:
a detected heading defect is resolved, its documented command produces the exact
specified JSON, the bad command fails, and the replacement asset links resolve.
They do not prove a particular agent loaded the skill, validate every possible
rewrite, or establish AI-search visibility. To evaluate your agent, review its
actual report, changes, task answers, and evidence against
[expected-review.md](expected-review.md) after it finishes.
