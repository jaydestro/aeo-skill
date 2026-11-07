#!/usr/bin/env python3
"""Install the unchanged AEO skill for native discovery or explicit loading."""

import argparse
import json
from pathlib import Path
import sys
import tempfile


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE = REPOSITORY / "skills" / "aeo"
NATIVE_PATHS = {
    "copilot": (".github/skills", ".copilot/skills"),
    "claude": (".claude/skills", ".claude/skills"),
    "codex": (".agents/skills", ".agents/skills"),
    "gemini": (".gemini/skills", ".gemini/skills"),
    "opencode": (".opencode/skills", ".config/opencode/skills"),
    "cline": (".cline/skills", ".cline/skills"),
    "roo": (".roo/skills", ".roo/skills"),
}
MANUAL_AGENTS = ("cursor", "windsurf", "continue", "amazon-q", "kiro", "aider", "generic")


def payload(directory):
    files = {}
    for path in directory.rglob("*"):
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        if path.is_symlink():
            raise ValueError(f"Refusing symlink in skill directory: {path}")
        if path.is_file():
            files[path.relative_to(directory)] = path.read_bytes()
    return files


def install(agents, scope, root):
    root = Path(root).expanduser().resolve()
    if SOURCE.is_symlink() or not (SOURCE / "SKILL.md").is_file():
        raise ValueError(f"Source skill entry point missing or symlinked: {SOURCE}")
    expected = payload(SOURCE)
    expected[Path("LICENSE")] = (REPOSITORY / "LICENSE").read_bytes()
    plans = {}
    results = []
    for agent in agents:
        paths = NATIVE_PATHS.get(agent, (".agents/skills", ".agents/skills"))
        destination = root / paths[1 if scope == "user" else 0] / "aeo"
        if destination.is_symlink() or not destination.resolve().is_relative_to(root):
            raise ValueError(f"Refusing symlink or destination outside installation root: {destination}")
        if destination.is_relative_to(SOURCE) or SOURCE.is_relative_to(destination):
            raise ValueError(f"Installation destination overlaps the source skill: {destination}")
        if destination not in plans:
            if destination.exists():
                if not destination.is_dir() or payload(destination) != expected:
                    raise ValueError(f"Existing installation differs; nothing overwritten: {destination}")
                plans[destination] = "unchanged"
            else:
                plans[destination] = "installed"
        results.append({
            "agent": agent,
            "destination": str(destination),
            "status": plans[destination],
            "activation": "native" if agent in NATIVE_PATHS else "manual",
            "prompt": f"Read {destination / 'SKILL.md'} and its referenced resources. "
                      "Use the AEO workflow to review the requested sources in report-only mode. "
                      "Save one scored Markdown report; do not edit source content.",
        })
    # Preflight every destination before writing any installation.
    for destination, status in plans.items():
        if status == "unchanged":
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".aeo-install-", dir=destination.parent) as staging:
            packaged = Path(staging) / "aeo"
            packaged.mkdir()
            for relative, content in expected.items():
                target = packaged / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            if destination.exists() or destination.is_symlink():
                raise ValueError(f"Destination appeared during installation; refusing replacement: {destination}")
            packaged.rename(destination)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", action="append",
                        choices=["all", *NATIVE_PATHS, *MANUAL_AGENTS],
                        help="Repeat to install for multiple agents; default: generic")
    parser.add_argument("--scope", choices=["project", "user"], default="project")
    parser.add_argument("--root", type=Path,
                        help="Project root or alternate home directory; default: cwd or user home")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    agents = args.agent or ["generic"]
    if "all" in agents:
        agents = [*NATIVE_PATHS, *MANUAL_AGENTS]
    agents = list(dict.fromkeys(agents))
    root = args.root if args.root is not None else (Path.home() if args.scope == "user" else Path.cwd())
    try:
        results = install(agents, args.scope, root)
    except (OSError, ValueError) as error:
        print(f"Installation failed: {error}. If an I/O failure interrupted a multi-agent "
              "installation, inspect destinations before retrying; existing files are not overwritten.",
              file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"installations": results}, indent=2))
    else:
        for result in results:
            print(f"{result['agent']}: {result['status']} {result['destination']} "
                  f"({result['activation']} loading)")
        print("\nReload/restart the agent and verify discovery. If unavailable, use this prompt:")
        print(results[0]["prompt"])
        print("Manual profiles do not claim native auto-discovery. Host permissions remain unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
