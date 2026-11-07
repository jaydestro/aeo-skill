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

## Recommendations

- To be **cited** in AI answers, allow the *search* / *user* agents (e.g., `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Bingbot`) even if you block training bots.
- Blocking `Googlebot` or `Bingbot` removes you from those engines' AI answers too.
- Make sure key content is in server-rendered HTML.

## llms.txt

A Markdown file at `/llms.txt` (proposal: https://llmstxt.org) giving LLMs a curated map of the site: H1 site name, a `>` summary blockquote, then H2 sections of links with one-line descriptions. Optionally provide `/llms-full.txt` with full content. See `../templates/llms.txt`.
