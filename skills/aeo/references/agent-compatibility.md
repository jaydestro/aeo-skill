# Coding-agent compatibility

## One workflow, different hosts (AEO-R007)

The same `SKILL.md`, rubric, scripts, references, and report template work through
native Agent Skills discovery or explicit instruction loading. No vendor-specific
tool names, slash commands, models, or MCP servers are required. Follow host
instructions and permissions first. Installing a skill does not activate it,
grant tool access, authorize edits, or select auto-apply.
The default profile is general-purpose; `technical` is optional. See
[distribution.md](distribution.md) for one-line package-manager installs,
provider plugin/extension manifests, and their verified source documentation.

Resolve links and bundled scripts relative to the installed `SKILL.md`, **not**
the workspace or this repository's original layout. Keep the target repository
as the working directory when auditing it. For example, invoke Python with the
absolute installed `scripts/aeo_audit.py` path and workspace-relative inputs;
report paths remain relative to the workspace.

## Installation profiles

Run `python3 scripts/install_skill.py --agent <profile> --root <project>` from
the cloned skill repository. Repeat `--agent` for several hosts or use `all`.
`--scope user` defaults the root to your home directory. The table paths below
are relative to the project root or home directory, respectively.

| Profile | Project directory | User directory | Loading |
|---|---|---|---|
| `copilot` | `.github/skills/aeo` | `.copilot/skills/aeo` | Native; surface-dependent |
| `claude` | `.claude/skills/aeo` | `.claude/skills/aeo` | Native; path corroborated by interoperability docs |
| `codex` | `.agents/skills/aeo` | `.agents/skills/aeo` | Native |
| `gemini` | `.gemini/skills/aeo` | `.gemini/skills/aeo` | Native; activation consent may be required |
| `opencode` | `.opencode/skills/aeo` | `.config/opencode/skills/aeo` | Native; honor skill permissions |
| `cline` | `.cline/skills/aeo` | `.cline/skills/aeo` | Native; skill must be enabled |
| `roo` | `.roo/skills/aeo` | `.roo/skills/aeo` | Native; mode/permission restrictions may apply |
| `cursor`, `windsurf`, `continue`, `amazon-q`, `kiro`, `aider`, `generic` | `.agents/skills/aeo` | `.agents/skills/aeo` | Explicit manual loading; native paths not asserted |

Manual profiles are a portable staging location, **not** a claim those products
lack native skills. Native discovery varies with versions and configuration.
Where a host provides its own skill import or directory setting, point it at
this complete installed folder after checking current primary documentation.
For an unlisted agent, use `generic` and the same explicit-loading prompt.

The installer copies the complete skill plus its MIT license, excludes Python
caches, and never changes existing instruction/configuration files or host
permissions. Identical installs are unchanged; conflicting content is rejected,
including when one target in an `all` installation conflicts. It does not
overwrite older skills: compare or back up that specific folder yourself before
replacing it. Unexpected I/O failures are explicit and may leave earlier
destinations installed. No dependency or agent installation is performed.

## Explicit loading and capability negotiation

For any agent with permitted file/context access, use:

> Read `.agents/skills/aeo/SKILL.md` and its referenced resources. Use that
> workflow to scan `docs/` and `README.md` with primary product "Azure Cosmos DB"
> in report-only mode. Inspect code and media, verify uncertain public facts,
> and save scores, evidence, concrete recommendations, and an apply-all prompt
> to `content-review.md`. Do not edit source content.

Substitute the actual installed path, or use `skills/aeo/SKILL.md` directly in
this checkout without installing. User installs need the absolute home path.
If file/context loading is unavailable, attach the entry point and needed
references using the host's supported attachment mechanism. Do not claim a
full assessment without the rubric/report instructions and source evidence.

At activation, establish:

| Capability | With permitted tools | Without usable tools |
|---|---|---|
| Local files | Discover/read authorized files and assets | Request accessible sources; report inaccessible coverage |
| Shell/Python 3.10+ | Optional static helper and safe validators | Review manually; never invent command/test results |
| Web search/fetch/browser | Verify uncertain public facts; inspect live URLs | Mark dependent claims/pages unknown and defer factual changes |
| Image/video/rendering | Inspect meaning, captions, transcripts, rendered output | Report inspection limits; retain unknown criteria where required |
| File writes | Save the report; edit only with workflow authorization | Return inline Markdown; do not claim files were written |

Use equivalent host tools, not a required tool name. Activate native skills
through the host's supported mechanism; otherwise load files explicitly. A
read-only/plan session can produce the report without source writes. If the
default report artifact cannot be written, disclose that and return inline
Markdown. Apply requests still need the authorized local paths, readable report,
current snapshots, and permitted edit tools. Shell access does not authorize
running untrusted code blocks or installing dependencies.

## Verification and evidence limits

After installation, reload/restart the host if needed and confirm it can load
`aeo`. Use a single-file report-only review of the fictional Sprocket `before.md`
with `fixture-spec.md` as local evidence. Confirm the report identifies fiction,
invalid flags/limits/output, and inaccessible media without editing the article.
Then explicitly approve a concrete local proposal and check that only its
authorized files change. Apply-by-report and primary-product behavior are the
same in every host. Do not treat a high fixture score as proof of agent quality.

Installer tests verify complete copies, paths, non-overwrites, and packaging;
they do not constitute authenticated end-to-end runs in each vendor product.
Keep native discovery and actual workflow conformance separate in any test report.

Primary documentation inspected on 2026-11-07:

- [Agent Skills specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx):
  format, metadata limits, and bundled resources.
- [GitHub Copilot](https://docs.github.com/en/copilot/concepts/customizations/agent-skills):
  project/personal paths and surface limitations.
- [Codex official root discovery](https://github.com/openai/codex/blob/main/codex-rs/ext/skills/src/host_roots.rs):
  project/user `.agents/skills`; legacy user path is deprecated.
- [Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md):
  project/user paths, consent, and discovery.
- [OpenCode](https://github.com/anomalyco/opencode/blob/dev/packages/web/src/content/docs/skills.mdx):
  project/user paths, Claude-compatible paths, and permissions.
- [Cline](https://github.com/cline/cline/blob/main/docs/customization/skills.mdx):
  project/user paths and activation.
- [Roo Code](https://github.com/RooCodeInc/Roo-Code/blob/main/apps/docs/docs/features/skills.mdx):
  project/user paths and mode restrictions.

Direct Claude Code, Cursor, Windsurf, Kiro, Continue, and specification-site
requests failed DNS during this update. Official GitHub sources were used where
available; manual profiles avoid guessing unverified host discovery behavior.
The [standard's client list](https://github.com/agentskills/agentskills/blob/main/docs/snippets/clients.jsx)
links additional vendor documentation but is not proof of installation paths.
Recheck the installed host's current documentation before relying on auto-discovery.
