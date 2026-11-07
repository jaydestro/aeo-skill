# General-purpose review and domain profiles

## Shared core

The default `general` profile reviews any human- or agent-facing content using
the same twenty content-readiness v2 criteria. Establish purpose, audience,
subject, voice, locale, channel, and evidence requirements first. The optional
`technical` profile adds domain checks without changing the weights or IDs.
The flag records context; it does not filter files, score text automatically,
or authorize edits. Mixed collections may have documented per-source context.

All profiles review factual support, useful specificity, organization,
faithful extraction, terminology, necessary conditions, source identity,
maintenance, accessibility, and any meaningful media. Keep every criterion
pass/fail/unknown with evidence. Explain legitimate non-applicability without
adding irrelevant content; uncertain applicability stays unknown.

## Adapt general review to the actual content

| Content | Useful review evidence | Avoid |
|---|---|---|
| Articles, blogs, journalism | Clear thesis, accurate quotes, source provenance, fair context, dates/units, factual versus opinion boundaries | Invented quotes, false balance, unsupported certainty |
| Product/service and marketing copy | Supported benefits, audience fit, clear offer, eligibility, pricing/terms and substantiated comparisons | Fabricated testimonials, scarcity, guarantees, or conversion promises |
| Education and explainers | Appropriate prerequisite knowledge, correct definitions, supported explanations/examples, learning goals and accessible media | Oversimplification that changes meaning; invented curriculum credentials |
| Policies and operational guidance | Responsible owner, effective scope/date, applicable rules, exceptions, usable next actions and authoritative references | Silently changing policy, rights, obligations, or access controls as a copy edit |
| Help, descriptions, and short UI copy | Purpose, clear action, necessary conditions, appropriate tone, preserved placeholders/localization/limits | Forced article headings, FAQs, bylines, or unnecessary background |
| Narrative and creative work | Intended audience, coherent context, preserved voice/meaning, accessible presentation and clearly framed fiction/opinion | Treating fictional plot as a factual error; forcing every passage into an answer |

Domain context is not a new ranking formula. No subject needs universal keywords,
word counts, schema, citations on every sentence, or public indexing. Cite facts
when provenance is material, not as decoration. Use permitted web research for
uncertain public facts, without sending private content to public services.

For medical, legal, financial, or other high-impact content, identify the
applicable jurisdiction/date and qualification limits. Flag unsupported claims,
but do not invent expert approval or turn editorial improvements into
personalized professional advice. Defer changes needing qualified review.

## Technical overlay

Select `technical` explicitly for implementation-heavy blogs, documentation,
READMEs, API/CLI references, tool descriptions, and code-based tutorials. Check
actual supported behavior, versions, interfaces, identifiers, prerequisites,
dependencies, flags, configuration, output, failure paths, and side effects.
Use [the content/media playbook](technical-review.md) for code inspection and
safe validation. The overlay never authorizes implementation changes merely to
make a content claim true.

Code and technical media must still be checked when present under `general`;
the profile cannot suppress a relevant correctness or safety finding.
Conversely, a technical collection can contain editorial or policy pages that
legitimately need no runnable example.

## Stable assessment and application

Record profile, subject, optional product, tasks, and evidence scope in the
report. Keep them fixed for before/after comparisons and applying proposals.
Changing profile or domain interpretation requires a new baseline even if the
same rubric IDs are used. Existing v2 technical fixture assessments remain
valid in their original technical context; do not claim cross-profile deltas.
For legacy reports without a profile, retain clearly established original
context; if ambiguous, disclose it and establish a baseline before comparing.
