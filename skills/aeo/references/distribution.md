# Installers, plugins, and extensions

## One skill, shared packaging

All routes load the same `skills/aeo` entry point, profiles, references, rubric,
templates, and optional helper. This repository is a skills collection and
also contains provider manifests:

| File | Role |
|---|---|
| `plugin.json` | Agent Plugins 1.0 skill-only package; fixed root `skills/` layout |
| `.claude-plugin/plugin.json` | Claude Code plugin using that same `skills/` directory |
| `.claude-plugin/marketplace.json` | Claude marketplace with one root plugin |
| `.github/plugin/marketplace.json` | Copilot marketplace with one root plugin |
| `gemini-extension.json` | Gemini CLI extension; native discovery of bundled `skills/aeo` |

No hooks, background processes, MCP servers, network credentials, or automatic
edit actions are bundled. Plugin installation is separate from review/apply
authorization. Duplicate installs can cause precedence/version confusion; choose
one route and confirm the loaded skill.

## Package managers

`npx skills add jaydestro/aeo-skill --skill aeo` discovers the collection and
lets users select agents. `--all` installs all bundled skills to the manager's
supported agents without prompts. Specific aliases include `claude-code`,
`codex`, `github-copilot`, `cursor`, `gemini-cli`, `windsurf`, `opencode`,
`cline`, `roo`, `continue`, `kiro-cli`, and `amp`. Use `-g` for user scope,
`--copy` if symlinks are unsuitable, and `--list` to inspect discovery first.
These aliases belong to that CLI, not to the Python installer's profile names.

APM supports bare skills at repository subpaths:

```bash
apm install jaydestro/aeo-skill/skills/aeo --target all
uvx --from apm-cli apm install jaydestro/aeo-skill/skills/aeo --target all
```

This explicit skill route avoids confusing a portable skill install with
Agent Plugins 1.0 native plugin registration. Select one target with, for example,
`--target codex`, or comma-separated targets with `--target copilot,claude,codex`.
APM creates/updates its project manifest and lockfile and deploys for the selected
targets. Its `all` excludes some experimental/explicit-only integrations.
Do not add `--force`, `--no-policy`, or trust-bypass options to examples.

## Provider packages

Install the root plugin with `copilot plugin install jaydestro/aeo-skill`, or
register the marketplace with `copilot plugin marketplace add jaydestro/aeo-skill`
and then install `aeo@aeo-skill`. Local development can use the read-only
`copilot --plugin-dir /absolute/path/to/aeo-skill plugin list --json` to inspect
discovery without persisting an install.

For the current Claude Code CLI, use
`claude plugin install aeo --marketplace jaydestro/aeo-skill`.
The CLI's inspected help documents automatic marketplace registration for
this option. Older versions can use `/plugin marketplace add jaydestro/aeo-skill`
followed by `/plugin install aeo@aeo-skill` in the interactive session. The npx
skill install is another one-line alternative.

For Gemini CLI:

```bash
gemini extensions install https://github.com/jaydestro/aeo-skill
```

Restart the session after extension changes. Extension installation and native
skill activation may ask for consent; do not suppress it by default.

Codex's inspected source recognizes the Agent Plugins 1.0 root manifest, but
we do not invent a `codex plugin install` command or promise support in every
released version. Its documented skill install is the npx/APM/native path.
Other providers use the compatible skill route or explicit loading rather than
unverified plugin formats. No npm publication, extension-gallery listing, or
external marketplace approval is claimed by merely adding these manifests.

## Verified sources and limits

Primary source passages inspected on 2026-11-07:

- [skills CLI](https://github.com/vercel-labs/skills/blob/main/README.md) and
  [commands](https://github.com/vercel-labs/skills/blob/main/docs/commands.md):
  add, scope, all/agent selection, Node requirement, and telemetry.
- [skills agent adapters](https://github.com/vercel-labs/skills/blob/main/docs/agents.md):
  supported aliases/paths. This is the installer's documentation, not
  independent end-to-end certification of each host.
- [APM](https://github.com/microsoft/apm): bare-skill paths, package installation,
  pip distribution, and target support; inspect `apm install --help` for the
  installed version's targets and side effects.
- [Copilot authoring](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)
  and [CLI reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference):
  root schema, layout, marketplace, and install specifications.
- [Agent Plugins schema](https://github.com/agentplugins/agent-plugins-spec/blob/main/schemas/1.0.0/plugin.schema.json):
  allowed metadata and fixed skill layout.
- [Claude plugin structure](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)
  and [official marketplace](https://github.com/anthropics/claude-code/blob/main/.claude-plugin/marketplace.json):
  manifest/layout and distribution. Direct Claude documentation failed DNS.
  Current official npm CLI help verified `plugin install --marketplace` and
  marketplace registration syntax; older installed versions may differ.
- [Gemini extension reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md)
  and [authoring](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/writing-extensions.md):
  extension install command and automatic bundled-skill discovery.
- [Codex plugin recognition](https://github.com/openai/codex/blob/main/codex-rs/utils/plugins/src/plugin_namespace.rs):
  recognition of the canonical root schema; release/runtime limits still apply.

Validation covers actual installers where available, package layout, and
read-only Copilot plugin discovery. Authenticated semantic sessions in every
provider remain separate conformance evaluations; see the contribution guide
in the repository for the scenario protocol.
