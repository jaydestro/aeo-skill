# AI Crawlers, robots.txt, and llms.txt

## Common AI user agents

| User agent | Operator | Purpose |
|---|---|---|
| `GPTBot` | OpenAI | Training |
| `OAI-SearchBot` | OpenAI | ChatGPT search results |
| `ChatGPT-User` | OpenAI | User-initiated fetches |
| `ClaudeBot` / `Claude-User` / `Claude-SearchBot` | Anthropic | Training / user fetch / search |
| `PerplexityBot` / `Perplexity-User` | Perplexity | Search index / user fetch |
| `Google-Extended` | Google | Gemini training/grounding control token |
| `Bingbot` | Microsoft | Bing index (powers Copilot answers) |
| `Applebot-Extended` | Apple | Apple Intelligence training control |
| `CCBot` | Common Crawl | Open dataset used by many models |

User agents change — verify against each operator's current docs before recommending rules.
Primary-source links and review limitations are in [research.md](research.md).

## Recommendations

- To be **cited** in AI answers, allow the *search* / *user* agents (e.g., `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Bingbot`) even if you block training bots.
- Crawl denial affects content access but does not guarantee URL removal; blocked
  URLs may still be discovered as bare links. Google Search AI controls use
  Googlebot, not Google-Extended.
- Make sure key content is in server-rendered HTML.
- Search, training, and user retrieval are separate. Do not penalize GPTBot or
  ClaudeBot training opt-outs. OpenAI says user-fetch robots rules may not apply;
  Perplexity says its user fetcher generally ignores them; Anthropic documents
  controls for Claude-User. Robots is not authentication.
- Check target-path rules, HTTP status/redirects, auth/WAF challenges, verified
  bot identity, meta robots and X-Robots-Tag, noindex, snippet limits, canonical
  conflicts, indexed status, internal links, and sitemap freshness.
- Never relax access or crawler policies without owner approval. An unavailable
  robots response is unknown, not evidence that all bots are allowed.

## llms.txt

A Markdown file at `/llms.txt` (proposal: https://llmstxt.org) giving LLMs a curated map of the site: H1 site name, a `>` summary blockquote, then H2 sections of links with one-line descriptions. Optionally provide `/llms-full.txt` with full content. See `../templates/llms.txt`.

Optional navigation for supporting agents, not an AI-search requirement. Google
states it does not affect Search visibility. Publisher adoption is not proof
that their search crawlers consume it. Generate links from maintained sources
and verify versions, content equivalence, and access controls.
