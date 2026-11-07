# Technical Copy Guidelines

Scope: technical blogs, docs, READMEs, descriptions, references, and other
human- or agent-facing technical communication. Follow existing voice,
terminology, localization, and surface constraints. AEO is a secondary
application; factual correctness and human usability take priority.

Read [technical-review.md](technical-review.md) for source permissions and
required code/media inspection. Review code blocks, videos, images, diagrams,
tables, downloads, and embedded components with the surrounding copy.

## Answer-first structure

- **Descriptive headings**: use questions when useful, not a required percentage.
- **Direct answer first**: address the task early; there is no universal word limit.
- **Inverted pyramid**: conclusion → supporting facts → nuance/edge cases.
- **Self-contained passages**: each section must make sense if quoted alone. Repeat the subject instead of "it"/"this".

## Extractable formats

| Content type | Best format |
|---|---|
| Process | Numbered steps (`<ol>`), one action per step |
| Comparison | Table with clear column headers |
| Definitions | "**X** is a … that …" sentence |
| Options / features | Bulleted list with bolded lead-ins |
| Specs / numbers | Table or definition list with units |

## Clarity

- Clear sentences and plain language; preserve necessary technical precision.
- Define acronyms on first use.
- Use specific numbers, dates, and named entities instead of vague claims.
- Keep one canonical answer per question across the site — avoid contradicting pages.

## Trust (E-E-A-T)

- Appropriate accountable author/publisher; not mandatory personal bylines on every reference.
- Visible "Published" and "Updated" dates; keep content fresh.
- Cite primary sources with outbound links.
- Organization info: about page, contact, `Organization` schema with `sameAs` profiles.

## Page hygiene

- A clear main heading and logical hierarchy; editorial practice, not an AI ranking quota.
- Textual main content accessible to the intended consumer. Google can render JavaScript; other agents vary.
- Descriptive `<title>` and `<meta name="description">`; `rel="canonical"`.
- Fast, accessible HTML; meaningful image alt text (decorative images may use `alt=""`).

These are editorial recommendations, not confirmed ranking factors. Preserve
versions, prerequisites, warnings, units, and exceptions in independently
retrieved passages. Original evidence and tested examples matter more than
formulaic formatting. See [research.md](research.md) for sources and playbooks.

For short technical descriptions/help/error copy, prioritize purpose, precise
capabilities, limitations, and useful next actions; do not require article-style
headings. Preserve identifiers, translation keys, placeholders, escapes,
character limits, and valid markup. Label pseudocode versus runnable examples,
and distinguish inspected assets from unavailable recordings or images.
