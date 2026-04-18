#!/usr/bin/env python3
"""
Lint components in the AI4RA prompt library.

Checks:
  1. Each components/<slug>/ has README.md and CHANGELOG.md.
  2. Each manifestation file (prompt.md, skill/SKILL.md, agent/AGENT.md) has
     YAML frontmatter with required fields: name, version, category, domain, status.
  3. version matches semver (MAJOR.MINOR.PATCH).
  4. category / domain / status are declared in taxonomy.md.
  5. All manifestation files in one component share the same version (lockstep).

Exits 0 on success, 1 on any error. Errors are printed in GitHub-Actions-friendly
form (::error file=...::message) so they surface on the PR diff.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPONENTS_DIR = REPO_ROOT / "components"
TAXONOMY_PATH = REPO_ROOT / "taxonomy.md"

MANIFESTATION_FILES = ["prompt.md", "skill/SKILL.md", "agent/AGENT.md", "system.md"]

# Fields required on every manifestation file.
COMMON_REQUIRED = ["name", "version"]

# Extra fields required per manifestation type. The canonical prompt carries the
# task-level taxonomy; platform-specific files carry the fields their platform needs.
EXTRA_REQUIRED_BY_FILE = {
    "prompt.md": ["category", "domain", "status"],
    "skill/SKILL.md": ["description"],
    "agent/AGENT.md": ["description", "tools"],
    "system.md": ["category", "domain", "status"],
}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)

errors: list[str] = []


def error(file: Path, message: str) -> None:
    rel = file.relative_to(REPO_ROOT) if file.is_absolute() else file
    errors.append(f"::error file={rel}::{message}")


def load_taxonomy(path: Path) -> dict[str, set[str]]:
    """Parse taxonomy.md for valid values under each ## section.

    Expected format per section:
      ## Section Name
      - `value` — description
    """
    text = path.read_text()
    sections: dict[str, set[str]] = {}
    current: str | None = None
    bullet_re = re.compile(r"^-\s+`([^`]+)`")
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = set()
        elif current:
            m = bullet_re.match(line)
            if m:
                sections[current].add(m.group(1))
    return sections


def parse_frontmatter(file: Path) -> dict | None:
    text = file.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        error(file, "Missing YAML frontmatter (file must begin with '---' block).")
        return None
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        error(file, f"Invalid YAML frontmatter: {e}")
        return None
    if not isinstance(data, dict):
        error(file, "Frontmatter must be a YAML mapping.")
        return None
    return data


def check_manifestation(
    file: Path, rel_key: str, taxonomy: dict[str, set[str]]
) -> str | None:
    """Validate a single manifestation file. Returns its version or None."""
    fm = parse_frontmatter(file)
    if fm is None:
        return None

    required = COMMON_REQUIRED + EXTRA_REQUIRED_BY_FILE.get(rel_key, [])
    for field in required:
        if field not in fm:
            error(file, f"Missing required frontmatter field: '{field}'.")
        elif fm[field] in (None, "", []):
            error(file, f"Frontmatter field '{field}' is empty.")

    version = fm.get("version")
    if version and not isinstance(version, str):
        error(file, f"version must be a string in quotes (got {type(version).__name__}).")
        version = None
    elif version and not SEMVER_RE.match(version):
        error(file, f"version '{version}' is not semver (expected MAJOR.MINOR.PATCH).")

    for field, taxonomy_key in [
        ("category", "categories"),
        ("domain", "domains"),
        ("status", "status"),
    ]:
        value = fm.get(field)
        if value and taxonomy_key in taxonomy and value not in taxonomy[taxonomy_key]:
            valid = ", ".join(sorted(taxonomy[taxonomy_key]))
            error(
                file,
                f"{field} '{value}' is not in taxonomy.md. Valid values: {valid}.",
            )

    return version if isinstance(version, str) and SEMVER_RE.match(version) else None


def check_component(component_dir: Path, taxonomy: dict[str, set[str]]) -> None:
    slug = component_dir.name

    for required in ["README.md", "CHANGELOG.md"]:
        if not (component_dir / required).is_file():
            error(component_dir / required, f"Component '{slug}' is missing {required}.")

    manifestations_found: list[tuple[Path, str | None]] = []
    for rel in MANIFESTATION_FILES:
        f = component_dir / rel
        if f.is_file():
            manifestations_found.append((f, check_manifestation(f, rel, taxonomy)))

    if not manifestations_found:
        error(
            component_dir,
            f"Component '{slug}' has no manifestation files "
            f"(expected at least one of: {', '.join(MANIFESTATION_FILES)}).",
        )
        return

    versions = {v for _, v in manifestations_found if v is not None}
    if len(versions) > 1:
        listing = ", ".join(
            f"{f.relative_to(REPO_ROOT)}={v}" for f, v in manifestations_found if v
        )
        error(
            component_dir,
            f"Component '{slug}' has inconsistent versions across manifestations "
            f"(lockstep versioning required): {listing}.",
        )


def main() -> int:
    if not COMPONENTS_DIR.is_dir():
        print(f"No components/ directory at {COMPONENTS_DIR}", file=sys.stderr)
        return 1

    if not TAXONOMY_PATH.is_file():
        print(f"No taxonomy.md at {TAXONOMY_PATH}", file=sys.stderr)
        return 1

    taxonomy = load_taxonomy(TAXONOMY_PATH)
    for required_section in ("categories", "domains", "status"):
        if required_section not in taxonomy:
            error(
                TAXONOMY_PATH,
                f"taxonomy.md missing '## {required_section.title()}' section.",
            )

    component_dirs = sorted(p for p in COMPONENTS_DIR.iterdir() if p.is_dir())
    if not component_dirs:
        print("No components found under components/ — nothing to lint.")
        return 0

    for component_dir in component_dirs:
        check_component(component_dir, taxonomy)

    if errors:
        for e in errors:
            print(e)
        print(f"\nLint failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Linted {len(component_dirs)} component(s). OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
