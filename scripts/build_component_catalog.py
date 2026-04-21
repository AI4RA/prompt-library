#!/usr/bin/env python3
"""
Build the machine-readable component catalog for AI4RA/prompt-library.

The checked-in `component_catalog.json` is generated from:
  - discovered component manifests under `components/`
  - curated triad metadata in `component_catalog_overrides.yaml`

Use `--check` to verify the checked-in JSON is up to date.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_DIR = REPO_ROOT / "components"
OVERRIDES_PATH = REPO_ROOT / "component_catalog_overrides.yaml"
OUTPUT_PATH = REPO_ROOT / "component_catalog.json"

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    data = yaml.safe_load(match.group(1)) or {}
    return data, match.group(2)


def parse_semver(value: str | None) -> tuple[int, int, int] | None:
    if not isinstance(value, str) or not SEMVER_RE.match(value):
        return None
    major, minor, patch = value.split(".")
    return int(major), int(minor), int(patch)


@dataclass
class Component:
    slug: str
    path: Path
    prompt_frontmatter: dict
    prompt_body: str
    readme: str
    manifestation_frontmatters: dict[str, dict]
    has_schema: bool
    eval_case_count: int
    eval_report_count: int
    last_fully_evaluated_version: str | None

    @property
    def name(self) -> str:
        return str(self.prompt_frontmatter.get("name", self.slug))

    @property
    def version(self) -> str:
        return str(self.prompt_frontmatter.get("version", ""))

    @property
    def category(self) -> str:
        return str(self.prompt_frontmatter.get("category", ""))

    @property
    def domain(self) -> str:
        return str(self.prompt_frontmatter.get("domain", ""))

    @property
    def status(self) -> str:
        return str(self.prompt_frontmatter.get("status", ""))

    @property
    def tags(self) -> list[str]:
        values = self.prompt_frontmatter.get("tags", []) or []
        return [str(value) for value in values]

    @property
    def audience(self) -> list[str]:
        values = self.prompt_frontmatter.get("audience", []) or []
        return [str(value) for value in values]

    @property
    def short_description(self) -> str:
        lines: list[str] = []
        in_body = False
        for raw in self.readme.splitlines():
            line = raw.strip()
            if line.startswith("#"):
                in_body = True
                continue
            if not in_body:
                continue
            if not line:
                if lines:
                    break
                continue
            lines.append(line)
            if len(" ".join(lines)) > 280:
                break
        return " ".join(lines).strip()


def load_component(path: Path) -> Component | None:
    prompt_path = path / "prompt.md"
    if not prompt_path.is_file():
        return None

    prompt_frontmatter, prompt_body = split_frontmatter(
        prompt_path.read_text(encoding="utf-8")
    )
    readme_path = path / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""

    manifestation_frontmatters: dict[str, dict] = {}
    for rel_path in ("prompt.md", "skill/SKILL.md", "agent/AGENT.md"):
        file_path = path / rel_path
        if file_path.is_file():
            frontmatter, _ = split_frontmatter(file_path.read_text(encoding="utf-8"))
            manifestation_frontmatters[rel_path] = frontmatter

    last_fully_evaluated_version = compute_last_fully_evaluated_version(path)
    eval_case_count = count_case_dirs(path / "evals" / "cases")
    eval_report_count = count_case_dirs(path / "evals" / "reports")

    return Component(
        slug=path.name,
        path=path,
        prompt_frontmatter=prompt_frontmatter,
        prompt_body=prompt_body,
        readme=readme,
        manifestation_frontmatters=manifestation_frontmatters,
        has_schema=(path / "schema.json").is_file(),
        eval_case_count=eval_case_count,
        eval_report_count=eval_report_count,
        last_fully_evaluated_version=last_fully_evaluated_version,
    )


def count_case_dirs(path: Path) -> int:
    if not path.is_dir():
        return 0
    return len([item for item in path.iterdir() if item.is_dir()])


def compute_last_fully_evaluated_version(component_dir: Path) -> str | None:
    cases_dir = component_dir / "evals" / "cases"
    if not cases_dir.is_dir():
        return None

    min_parsed: tuple[int, int, int] | None = None
    for case_dir in sorted(p for p in cases_dir.iterdir() if p.is_dir()):
        meta_path = case_dir / "metadata.yaml"
        if not meta_path.is_file():
            continue
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        validated = meta.get("validated_against_version")
        parsed = parse_semver(validated)
        if parsed is None:
            continue
        if min_parsed is None or parsed < min_parsed:
            min_parsed = parsed

    if min_parsed is None:
        return None
    return ".".join(str(part) for part in min_parsed)


def discover_components() -> list[Component]:
    components: list[Component] = []
    for path in sorted(COMPONENTS_DIR.iterdir()):
        if not path.is_dir():
            continue
        component = load_component(path)
        if component is not None:
            components.append(component)
    return components


def load_overrides() -> dict:
    if not OVERRIDES_PATH.is_file():
        raise FileNotFoundError(f"Missing overrides file: {OVERRIDES_PATH}")
    return yaml.safe_load(OVERRIDES_PATH.read_text(encoding="utf-8")) or {}


def manifestation_entries(component: Component) -> list[dict]:
    entries: list[dict] = []
    order = [
        ("prompt.md", "prompt", "canonical_prompt"),
        ("skill/SKILL.md", "skill", "claude_skill"),
        ("agent/AGENT.md", "agent", "agent_manifest"),
    ]
    for rel_path, manifestation_type, role in order:
        frontmatter = component.manifestation_frontmatters.get(rel_path)
        if frontmatter is None:
            continue
        entry = {
            "type": manifestation_type,
            "path": f"components/{component.slug}/{rel_path}",
            "version": str(frontmatter.get("version", component.version)),
            "role": role,
        }
        description = frontmatter.get("description")
        if description:
            entry["description"] = str(description)
        entries.append(entry)
    return entries


def output_contract(component: Component, overrides: dict) -> dict:
    output = dict(overrides["output_contract"])
    schema_path = f"components/{component.slug}/schema.json" if component.has_schema else None
    output.setdefault("schema_path", schema_path)
    if output.get("schema_path") and "schema_entrypoints" not in output:
        output["schema_entrypoints"] = ["#"]
    if not output.get("schema_path"):
        output["schema_entrypoints"] = []

    validation_surfaces: list[str] = []
    if output.get("schema_path"):
        if output.get("schema_entrypoints") and output["schema_entrypoints"] != ["#"]:
            validation_surfaces.append("json_schema_entrypoints")
        else:
            validation_surfaces.append("json_schema")
    if component.eval_case_count:
        validation_surfaces.append("golden_eval_cases")
    if component.eval_report_count:
        validation_surfaces.append("published_eval_reports")
    output["validation_surfaces"] = validation_surfaces
    return output


def build_component_entry(component: Component, overrides: dict) -> dict:
    current_version = component.version
    last_eval = component.last_fully_evaluated_version
    return {
        "component_id": f"prompt.{component.slug}",
        "slug": component.slug,
        "name": component.name,
        "summary": component.short_description,
        "version": current_version,
        "category": component.category,
        "domain": component.domain,
        "status": component.status,
        "tags": component.tags,
        "audience": component.audience,
        "paths": {
            "component_dir": f"components/{component.slug}",
            "readme": f"components/{component.slug}/README.md",
            "prompt": f"components/{component.slug}/prompt.md",
            "schema": f"components/{component.slug}/schema.json" if component.has_schema else None,
            "evals_dir": f"components/{component.slug}/evals",
            "eval_case_metadata_glob": f"components/{component.slug}/evals/cases/*/metadata.yaml",
            "eval_reports_dir": f"components/{component.slug}/evals/reports",
        },
        "manifestations": manifestation_entries(component),
        "contracts": {
            "output": output_contract(component, overrides),
        },
        "evaluation": {
            "case_count": component.eval_case_count,
            "report_count": component.eval_report_count,
            "last_fully_evaluated_version": last_eval,
            "current_version_is_fully_evaluated": (
                bool(last_eval) and last_eval == current_version
            ),
        },
        "related_components": overrides.get("related_components", []),
        "triad_integration": overrides["triad_integration"],
    }


def build_catalog() -> dict:
    overrides = load_overrides()
    components = discover_components()

    override_components = overrides.get("components", {})
    component_slugs = {component.slug for component in components}
    override_slugs = set(override_components)

    missing_overrides = sorted(component_slugs - override_slugs)
    extra_overrides = sorted(override_slugs - component_slugs)
    if missing_overrides:
        raise ValueError(
            "Missing component_catalog_overrides.yaml entries for: "
            + ", ".join(missing_overrides)
        )
    if extra_overrides:
        raise ValueError(
            "component_catalog_overrides.yaml contains unknown components: "
            + ", ".join(extra_overrides)
        )

    return {
        "catalog_version": overrides["catalog_version"],
        "generated_from": str(OVERRIDES_PATH.relative_to(REPO_ROOT)),
        "repo": {
            "name": "AI4RA Prompt Library",
            "slug": "AI4RA/prompt-library",
            "default_branch": "main",
            "machine_discovery_surface": str(OUTPUT_PATH.relative_to(REPO_ROOT)),
        },
        "triad": overrides["triad"],
        "shared_contracts": overrides["shared_contracts"],
        "components": [
            build_component_entry(component, override_components[component.slug])
            for component in components
        ],
    }


def normalize_value(value):
    if isinstance(value, dict):
        return {key: normalize_value(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [normalize_value(item) for item in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, str):
        return value.rstrip("\n")
    return value


def rendered_catalog(catalog: dict) -> str:
    normalized = normalize_value(catalog)
    return json.dumps(normalized, indent=2, sort_keys=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify component_catalog.json is up to date",
    )
    args = parser.parse_args()

    try:
        catalog = build_catalog()
    except Exception as exc:  # noqa: BLE001
        print(f"component catalog generation failed: {exc}", file=sys.stderr)
        return 1

    content = rendered_catalog(catalog)

    if args.check:
        existing = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.is_file() else None
        if existing != content:
            print(
                "component_catalog.json is out of date. Run "
                "`python3 scripts/build_component_catalog.py` and commit the result.",
                file=sys.stderr,
            )
            return 1
        print("component_catalog.json is up to date.")
        return 0

    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
