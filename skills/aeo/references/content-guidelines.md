# AEO Content Guidelines

## Answer-first structure

- **Question headings**: phrase H2/H3s as the questions users actually ask ("How long does X take?").
- **Direct answer first**: the first paragraph under a heading answers it in 40–60 words. Detail follows.
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

- Short sentences (≤ 25 words average); plain language.
- Define acronyms on first use.
- Use specific numbers, dates, and named entities instead of vague claims.
- Keep one canonical answer per question across the site — avoid contradicting pages.

## Trust (E-E-A-T)

- Named author with bio/credentials; `author` in JSON-LD.
- Visible "Published" and "Updated" dates; keep content fresh.
- Cite primary sources with outbound links.
- Organization info: about page, contact, `Organization` schema with `sameAs` profiles.

## Page hygiene

- Exactly one `<h1>`; logical heading hierarchy.
- Server-rendered main content (many AI crawlers don't execute JavaScript).
- Descriptive `<title>` and `<meta name="description">`; `rel="canonical"`.
- Fast, accessible HTML; meaningful `alt` text on images.
