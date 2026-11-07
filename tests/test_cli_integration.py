import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENABLED = os.environ.get("AEO_CLI_SMOKE") == "1"


@unittest.skipUnless(ENABLED, "Opt-in CLI checks require AEO_CLI_SMOKE=1 and permitted network access")
class CLIIntegrationTests(unittest.TestCase):
    def test_npx_copies_complete_skill_for_codex(self):
        if not shutil.which("npx"):
            self.skipTest("npx is not installed")
        with tempfile.TemporaryDirectory() as project, tempfile.TemporaryDirectory() as cache:
            env = dict(os.environ, npm_config_cache=cache, DO_NOT_TRACK="1", DISABLE_TELEMETRY="1")
            result = subprocess.run(
                ["npx", "--yes", "skills", "add", str(ROOT), "--skill", "aeo",
                 "--agent", "codex", "--yes", "--copy"], cwd=project, env=env,
                capture_output=True, text=True, timeout=300,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = Path(project) / ".agents/skills/aeo"
            self.assertEqual((installed / "SKILL.md").read_bytes(),
                             (ROOT / "skills/aeo/SKILL.md").read_bytes())
            self.assertEqual((installed / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
            self.assertTrue((installed / "references/profiles.md").is_file())

    def test_apm_installs_bare_skill_for_codex(self):
        command = ["apm"] if shutil.which("apm") else (
            ["uvx", "--from", "apm-cli", "apm"] if shutil.which("uvx") else None)
        if command is None:
            self.skipTest("APM and uvx are unavailable")
        with tempfile.TemporaryDirectory() as project:
            env = dict(os.environ, HOME=project)
            if os.name == "nt":
                env["USERPROFILE"] = project
            result = subprocess.run(
                [*command, "install", str(ROOT / "skills/aeo"), "--target", "codex"],
                cwd=project, env=env, capture_output=True, text=True, timeout=300,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = Path(project) / ".agents/skills/aeo"
            self.assertEqual((installed / "SKILL.md").read_bytes(),
                             (ROOT / "skills/aeo/SKILL.md").read_bytes())
            self.assertTrue((installed / "references/profiles.md").is_file())

    def test_copilot_discovers_plugin_without_persistent_install(self):
        if not shutil.which("copilot"):
            self.skipTest("Copilot CLI is unavailable")
        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ, HOME=home)
            if os.name == "nt":
                env["USERPROFILE"] = home
            result = subprocess.run(
                ["copilot", "--plugin-dir", str(ROOT), "plugin", "list", "--json"],
                env=env, capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            plugins = json.loads(result.stdout)
            self.assertTrue(any(p["name"] == "aeo" and p["source"] == "external" for p in plugins))

    def test_claude_validates_plugin_metadata(self):
        if not shutil.which("npx"):
            self.skipTest("npx is unavailable for the isolated Claude CLI validator")
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as cache:
            env = {key: value for key, value in os.environ.items()
                   if key in {"PATH", "LANG", "NODE_EXTRA_CA_CERTS", "NODE_OPTIONS",
                              "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTPS_PROXY",
                              "HTTP_PROXY", "ALL_PROXY", "NO_PROXY", "SYSTEMROOT"}}
            env.update(HOME=home, npm_config_cache=cache, DO_NOT_TRACK="1",
                       CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1")
            if os.name == "nt":
                env["USERPROFILE"] = home
            result = subprocess.run(
                ["npx", "--yes", "--package", "@anthropic-ai/claude-code",
                 "claude", "plugin", "validate", str(ROOT)], cwd=home, env=env,
                capture_output=True, text=True, timeout=300,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
