# Structured Data for AEO

Use JSON-LD in a `<script type="application/ld+json">` block. Schema must describe content that is **visible on the page**.

Schema is optional and page-specific, not required for Google AI features.
Question headings do not automatically justify FAQPage; it describes a genuine
publisher-authored FAQ. QAPage serves a different community question/answer use.
Google FAQ rich results were deprecated in May 2026 (see its documentation
changelog); HowTo rich results were deprecated in September 2023. These
schema.org types remain vocabulary, not citation guarantees.

| Page type | Schema types |
|---|---|
| FAQ / Q&A section | `FAQPage` → `Question` → `acceptedAnswer` (`Answer`) |
| Tutorial / steps | `HowTo` with `HowToStep` items |
| Blog / docs | `Article` / `TechArticle` / `BlogPosting` with `author`, `datePublished`, `dateModified` |
| Company / site | `Organization` (+ `sameAs`), `WebSite` |
| Product | `Product` with `offers`, `aggregateRating` (only if real) |
| Navigation | `BreadcrumbList` |

## Tips

- One `@graph` array can hold multiple entities; link them with `@id`.
- Answer text in `FAQPage` should match the on-page answer verbatim or nearly so.
- Validate vocabulary with https://validator.schema.org/; Google's Rich Results
  Test only covers features it currently supports. JSON parsing is not semantic validation.
- See `../templates/` for ready-to-fill examples.
- Replace all placeholders with verified facts or omit unknown fields. Do not
  fabricate dates, authors, reviews, or durations. Generate schema in the HTML
  publishing layer rather than requiring it in every Markdown source.
