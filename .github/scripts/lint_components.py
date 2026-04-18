#!/usr/bin/env python3
"""
Lint components in the AI4RA prompt library.

Checks:
  1. Each components/<slug>/ has README.md and CHANGELOG.md.
  2. Each manifestation file (prompt.md, skill/SKILL.md, agent/AGENT.md) has
     YAML frontmatter with required fields.
  3. version matches semver (MAJOR.MINOR.PATCH).
  4. category / domain / status are declared in taxonomy.md.
  5. All manifestation files in one component share the same version (lockstep).
  6. Each eval case's metadata.yaml declares validated_against_version as
     semver. The component's "last fully evaluated version" is computed as the
     minimum across cases; if it trails the current version a WARNING is
     emitted (non-blocking).

Errors exit 1. Warnings don't affect exit status. Both use GitHub Actions
annotation format (::error or ::warning file=...::message).
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

COMMON_REQUIRED = ["name", "version"]
EXTRA_REQUIRED_BY_FILE = {
    "prompt.md": ["category", "domain", "status"],
    "skill/SKILL.md": ["description"],
    "agent/AGENT.md": ["description", "tools"],
    "system.md": ["category", "domain", "status"],
}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)

errors: list[str] = []
warnings: list[str] = []
status_lines: list[str] = []


def _rel(path: Path) -> Path:
    return path.relative_to(REPO_ROOT) if path.is_absolute() else path


def error(file: Path, message: str) -> None:
    errors.append(f"::error file={_rel(file)}::{message}")


def warning(file: Path, message: str) -> None:
    warnings.append(f"::warning file={_rel(file)}::{message}")


def parse_semver(s: str) -> tuple[int, int, int] | None:
    if not isinstance(s, str) or not SEMVER_RE.match(s):
        return None
    major, minor, patch = s.split(".")
    return int(major), int(minor), int(patch)


def load_taxonomy(path: Path) -> dict[str, set[str]]:
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


def check_eval_validation(
    component_dir: Path, component_version: str | None
) -> str | None:
    """Returns the component's last fully evaluated version, or None if no
    cases exist or none declare a valid validated_against_version."""
    cases_dir = component_dir / "evals" / "cases"
    if not cases_dir.is_dir():
        return None

    case_dirs = sorted(p for p in cases_dir.iterdir() if p.is_dir())
    if not case_dirs:
        return None

    min_parsed: tuple[int, int, int] | None = None
    min_case_name: str | None = None

    for case_dir in case_dirs:
        meta_path = case_dir / "metadata.yaml"
        if not meta_path.is_file():
            error(case_dir, f"Eval case '{case_dir.name}' is missing metadata.yaml.")
            continue
        try:
            meta = yaml.safe_load(meta_path.read_text())
        except yaml.YAMLError as e:
            error(meta_path, f"Invalid YAML: {e}")
            continue
        if not isinstance(meta, dict):
            error(meta_path, "metadata.yaml must be a YAML mapping.")
            continue

        v = meta.get("validated_against_version")
        if v in (None, ""):
            error(
                meta_path,
                "Missing required field 'validated_against_version' (semver string, "
                "e.g., '1.0.0'). Declares which component version this case's "
                "expected.* was validated against.",
            )
            continue
        parsed = parse_semver(v)
        if parsed is None:
            error(
                meta_path,
                f"validated_against_version '{v}' is not semver "
                f"(expected MAJOR.MINOR.PATCH).",
            )
            continue

        if min_parsed is None or parsed < min_parsed:
            min_parsed = parsed
            min_case_name = case_dir.name

    if min_parsed is None:
        return None

    min_version_str = ".".join(str(x) for x in min_parsed)
    component_parsed = parse_semver(component_version) if component_version else None

    if component_parsed is not None and component_parsed > min_parsed:
        warning(
            component_dir,
            f"Component '{component_dir.name}' is at version {component_version} but "
            f"last fully evaluated version is {min_version_str} (oldest case: "
            f"'{min_case_name}'). Re-run evals against the current version and update "
            f"validated_against_version in the relevant case metadata.yaml, or declare "
            f"the current version still valid by bumping validated_against_version.",
        )

    return min_version_str


def check_component(
    component_dir: Path, taxonomy: dict[str, set[str]]
) -> tuple[str | None, str | None]:
    """Returns (current_version, last_fully_evaluated_version)."""
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
        return None, None

    versions = {v for _, v in manifestations_found if v is not None}
    current_version: str | None = None
    if len(versions) > 1:
        listing = ", ".join(
            f"{f.relative_to(REPO_ROOT)}={v}" for f, v in manifestations_found if v
        )
        error(
            component_dir,
            f"Component '{slug}' has inconsistent versions across manifestations "
            f"(lockstep versioning required): {listing}.",
        )
    elif len(versions) == 1:
        current_version = next(iter(versions))

    last_evaluated = check_eval_validation(component_dir, current_version)
    return current_version, last_evaluated


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

    component_status: list[tuple[str, str | None, str | None]] = []
    for component_dir in component_dirs:
        current, last = check_component(component_dir, taxonomy)
        component_status.append((component_dir.name, current, last))

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    print()
    print(f"Linted {len(component_dirs)} component(s).")
    print("Evaluation status:")
    for slug, current, last in component_status:
        current_str = current or "?"
        last_str = last or "none"
        if current and last:
            flag = "current" if current == last else f"behind ({last} validated)"
        elif current and not last:
            flag = "no validated eval cases"
        else:
            flag = "version unknown"
        print(f"  {slug}: {current_str} — {flag}")

    if errors:
        print(f"\nLint failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    if warnings:
        print(f"\n{len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
