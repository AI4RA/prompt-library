#!/usr/bin/env python3
"""
Generate platform wrappers from canonical component sources.

Canonical sources (hand-authored):
  components/<name>/prompt.md       — frontmatter + body
  components/<name>/schema.json     — output contract (optional)
  components/<name>/README.md
  components/<name>/CHANGELOG.md
  components/<name>/evals/

Generated artifacts (do not hand-edit):
  .claude-plugin/marketplace.json
  components/<name>/.claude-plugin/plugin.json
  components/<name>/skills/<name>/SKILL.md

Running this script is idempotent. CI runs it and fails if
`git diff --exit-code` shows generated files are stale.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPONENTS_DIR = REPO_ROOT / "components"
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)

REQUIRED_FIELDS = ("name", "version", "description")

MARKETPLACE_OWNER = {
    "name": "AI4RA",
    "url": "https://github.com/AI4RA",
}


class GenError(Exception):
    pass


def parse_prompt(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise GenError(f"{path.relative_to(REPO_ROOT)}: missing YAML frontmatter block")
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        raise GenError(f"{path.relative_to(REPO_ROOT)}: invalid YAML frontmatter: {e}")
    if not isinstance(fm, dict):
        raise GenError(f"{path.relative_to(REPO_ROOT)}: frontmatter must be a mapping")
    for field in REQUIRED_FIELDS:
        if not fm.get(field):
            raise GenError(
                f"{path.relative_to(REPO_ROOT)}: frontmatter missing required field "
                f"'{field}'"
            )
    body = m.group(2).lstrip("\n")
    return fm, body


def write_if_changed(path: Path, content: str) -> bool:
    """Write file only if content differs. Returns True when write happened."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text() == content:
        return False
    path.write_text(content)
    return True


def render_skill(fm: dict, body: str) -> str:
    """Render SKILL.md: minimal frontmatter (name/version/description) + prompt body."""
    lines = [
        "---",
        f"name: {fm['name']}",
        f"version: {fm['version']}",
        f"description: {fm['description']}",
        "---",
        "",
    ]
    return "\n".join(lines) + body.rstrip() + "\n"


def render_plugin_json(fm: dict) -> str:
    data = {
        "name": fm["name"],
        "version": fm["version"],
        "description": fm["description"],
        "author": MARKETPLACE_OWNER,
    }
    category = fm.get("category")
    if category:
        data["category"] = category
    tags = fm.get("tags")
    if tags:
        data["keywords"] = list(tags)
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def render_marketplace_json(entries: list[dict]) -> str:
    data = {
        "name": "prompt-library",
        "owner": MARKETPLACE_OWNER,
        "metadata": {
            "description": (
                "AI4RA research-administration prompt library — skills and agents "
                "derived from canonical prompts."
            ),
        },
        "plugins": entries,
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def scan_components() -> list[tuple[Path, dict, str]]:
    if not COMPONENTS_DIR.is_dir():
        raise GenError(f"components/ directory missing at {COMPONENTS_DIR}")
    results = []
    for c in sorted(p for p in COMPONENTS_DIR.iterdir() if p.is_dir()):
        prompt = c / "prompt.md"
        if not prompt.is_file():
            raise GenError(f"{c.relative_to(REPO_ROOT)}: missing prompt.md")
        fm, body = parse_prompt(prompt)
        if fm["name"] != c.name:
            raise GenError(
                f"{prompt.relative_to(REPO_ROOT)}: frontmatter name '{fm['name']}' "
                f"does not match directory name '{c.name}'"
            )
        results.append((c, fm, body))
    return results


def main() -> int:
    try:
        components = scan_components()
    except GenError as e:
        print(f"::error::{e}", file=sys.stderr)
        return 1

    changed: list[Path] = []
    marketplace_entries: list[dict] = []

    for component_dir, fm, body in components:
        slug = fm["name"]

        skill_path = component_dir / "skills" / slug / "SKILL.md"
        if write_if_changed(skill_path, render_skill(fm, body)):
            changed.append(skill_path)

        plugin_path = component_dir / ".claude-plugin" / "plugin.json"
        if write_if_changed(plugin_path, render_plugin_json(fm)):
            changed.append(plugin_path)

        entry = {
            "name": slug,
            "source": f"./components/{slug}",
            "description": fm["description"],
            "version": fm["version"],
        }
        if fm.get("category"):
            entry["category"] = fm["category"]
        marketplace_entries.append(entry)

    if write_if_changed(MARKETPLACE_PATH, render_marketplace_json(marketplace_entries)):
        changed.append(MARKETPLACE_PATH)

    if changed:
        print("Wrote:")
        for p in changed:
            print(f"  {p.relative_to(REPO_ROOT)}")
    else:
        print("All wrappers already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
