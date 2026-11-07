# Structured Data for AEO

Use JSON-LD in a `<script type="application/ld+json">` block. Schema must describe content that is **visible on the page**.

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
- Validate with https://validator.schema.org/ and Google's Rich Results Test.
- See `../templates/` for ready-to-fill examples.
