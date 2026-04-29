#!/usr/bin/env python3
"""
Build Vandalizer workflow exports from authored manifest.yaml files.

Every manifest.yaml under workflows/<wf-slug>/ is compiled into a sibling
<wf-slug>.vandalizer.json that can be uploaded directly into Vandalizer.
The generated JSON carries an x_ai4ra provenance block (workflow source
path, workflow version, pinned component versions, and prompt content
hashes) so a downloaded export can be traced back to this repository.

Use `--check` to verify checked-in JSON files match a fresh build.
Use `--workflow <path>` to restrict to a single manifest.yaml.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_DIR = REPO_ROOT / "components"
WORKFLOWS_DIR = REPO_ROOT / "workflows"
TEMPLATES_DIR = REPO_ROOT / "templates"

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

DEFAULT_TASK_KIND = "Prompt"
ALLOWED_TASK_KINDS = {"Prompt", "Extraction"}


class BuildError(Exception):
    def __init__(self, manifest_path: Path, message: str):
        self.manifest_path = manifest_path
        self.message = message
        rel = manifest_path.relative_to(REPO_ROOT) if manifest_path.is_absolute() else manifest_path
        super().__init__(f"{rel}: {message}")


def split_frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    data = yaml.safe_load(match.group(1)) or {}
    return data, match.group(2)


def slice_prompt_body(prompt_md: str, from_section: str) -> str:
    """Return everything after the first line equal to from_section."""
    target = from_section.strip()
    lines = prompt_md.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() == target:
            tail = "\n".join(lines[idx + 1 :])
            return tail.strip()
    raise ValueError(f"from_section {from_section!r} not found in prompt body")


def discover_manifests() -> list[Path]:
    if not WORKFLOWS_DIR.is_dir():
        return []
    paths = sorted(WORKFLOWS_DIR.glob("*/manifest.yaml"))
    return [p for p in paths if TEMPLATES_DIR not in p.parents]


def load_component_version(slug: str) -> str | None:
    prompt_path = COMPONENTS_DIR / slug / "prompt.md"
    if not prompt_path.is_file():
        return None
    frontmatter, _ = split_frontmatter(prompt_path.read_text(encoding="utf-8"))
    version = frontmatter.get("version")
    return version if isinstance(version, str) else None


def load_component_prompt_body(slug: str) -> str:
    prompt_path = COMPONENTS_DIR / slug / "prompt.md"
    _, body = split_frontmatter(prompt_path.read_text(encoding="utf-8"))
    return body


def resolve_task_prompt(
    task: dict,
    manifest_path: Path,
    declared_slugs: set[str],
) -> tuple[str, str | None, str | None]:
    """
    Return (prompt_body, source_slug_or_None, prompt_sha256_or_None).

    source_slug is None for prompt_inline tasks. prompt_sha256 is only
    returned for prompt_ref tasks so the provenance block can record
    the hash of the embedded body.
    """
    has_ref = "prompt_ref" in task
    has_inline = "prompt_inline" in task
    task_name = task.get("name", "<unnamed>")

    if has_ref and has_inline:
        raise BuildError(manifest_path, f"task {task_name!r} sets both prompt_ref and prompt_inline")
    if not has_ref and not has_inline:
        raise BuildError(manifest_path, f"task {task_name!r} sets neither prompt_ref nor prompt_inline")

    if has_inline:
        body = str(task["prompt_inline"]).strip()
        return body, None, None

    ref = task["prompt_ref"] or {}
    slug = ref.get("component")
    from_section = ref.get("from_section")
    if not slug or not from_section:
        raise BuildError(manifest_path, f"task {task_name!r} prompt_ref missing component or from_section")
    if slug not in declared_slugs:
        raise BuildError(
            manifest_path,
            f"task {task_name!r} prompt_ref component {slug!r} is not listed in manifest.components",
        )
    if not (COMPONENTS_DIR / slug / "prompt.md").is_file():
        raise BuildError(manifest_path, f"task {task_name!r} references unknown component {slug!r}")

    try:
        body = slice_prompt_body(load_component_prompt_body(slug), from_section)
    except ValueError as exc:
        raise BuildError(
            manifest_path,
            f"task {task_name!r}: {exc} (components/{slug}/prompt.md)",
        ) from None

    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return body, slug, sha


def build_embedded_search_set(task: dict, manifest_path: Path) -> dict:
    """
    Compile the manifest's `searchset:` block into the Vandalizer
    `_embedded_search_set` payload that the importer reconstructs into a
    SearchSet plus SearchSetItems on the target Vandalizer instance.
    """
    task_name = task.get("name", "<unnamed>")
    searchset = task.get("searchset")
    if not isinstance(searchset, dict):
        raise BuildError(
            manifest_path,
            f"task {task_name!r} kind: Extraction requires a searchset block",
        )
    items = searchset.get("items")
    if not isinstance(items, list) or not items:
        raise BuildError(
            manifest_path,
            f"task {task_name!r} searchset.items must be a non-empty list",
        )

    title = searchset.get("title")
    if not isinstance(title, str) or not title.strip():
        raise BuildError(
            manifest_path,
            f"task {task_name!r} searchset.title must be a non-empty string",
        )

    built_items: list[dict] = []
    seen_titles: set[str] = set()
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise BuildError(
                manifest_path,
                f"task {task_name!r} searchset.items[{idx}] must be a mapping",
            )
        item_title = item.get("title")
        searchphrase = item.get("searchphrase")
        if not isinstance(item_title, str) or not item_title.strip():
            raise BuildError(
                manifest_path,
                f"task {task_name!r} searchset.items[{idx}] missing title",
            )
        if not isinstance(searchphrase, str) or not searchphrase.strip():
            raise BuildError(
                manifest_path,
                f"task {task_name!r} searchset.items[{idx}] missing searchphrase",
            )
        if item_title in seen_titles:
            raise BuildError(
                manifest_path,
                f"task {task_name!r} searchset has duplicate item title {item_title!r}",
            )
        seen_titles.add(item_title)
        enum_values = item.get("enum_values")
        if enum_values is not None and not isinstance(enum_values, list):
            raise BuildError(
                manifest_path,
                f"task {task_name!r} searchset.items[{idx}] enum_values must be a list or null",
            )
        built_items.append({
            "searchphrase": searchphrase,
            "searchtype": "extraction",
            "title": item_title,
            "is_optional": bool(item.get("is_optional", False)),
            "enum_values": enum_values,
        })

    return {
        "title": title,
        "extraction_config": searchset.get("extraction_config", {}) or {},
        "domain": searchset.get("domain"),
        "cross_field_rules": searchset.get("cross_field_rules"),
        "items": built_items,
    }


def validate_manifest(manifest: dict, manifest_path: Path) -> None:
    required = [
        "name",
        "description",
        "workflow_version",
        "vandalizer_schema_version",
        "status",
        "updated",
        "components",
        "steps",
        "evals",
    ]
    for field in required:
        if field not in manifest:
            raise BuildError(manifest_path, f"missing required field {field!r}")

    if not SEMVER_RE.match(str(manifest["workflow_version"])):
        raise BuildError(
            manifest_path,
            f"workflow_version must be MAJOR.MINOR.PATCH, got {manifest['workflow_version']!r}",
        )
    if manifest["vandalizer_schema_version"] != 2:
        raise BuildError(
            manifest_path,
            f"vandalizer_schema_version must be 2, got {manifest['vandalizer_schema_version']!r}",
        )

    components = manifest.get("components") or []
    if not isinstance(components, list) or not components:
        raise BuildError(manifest_path, "components must be a non-empty list")

    for component in components:
        slug = component.get("slug")
        pinned = component.get("pinned_version")
        if not slug or not pinned:
            raise BuildError(manifest_path, f"component entry missing slug or pinned_version: {component!r}")
        if not (COMPONENTS_DIR / slug).is_dir():
            raise BuildError(manifest_path, f"component {slug!r} does not exist under components/")
        current = load_component_version(slug)
        if current is None:
            raise BuildError(manifest_path, f"component {slug!r} has no version in its prompt.md frontmatter")
        if pinned != current and "pinned_version_sha" not in component:
            raise BuildError(
                manifest_path,
                f"component {slug!r} pinned_version {pinned!r} does not match current prompt.md version "
                f"{current!r}; bump the manifest or set pinned_version_sha to record an intentional lag",
            )

    steps = manifest.get("steps") or []
    if not isinstance(steps, list) or not steps:
        raise BuildError(manifest_path, "steps must be a non-empty list")

    output_steps = [s for s in steps if s.get("is_output")]
    if len(output_steps) > 1:
        raise BuildError(manifest_path, "at most one step may set is_output: true")

    for step in steps:
        for task in step.get("tasks", []) or []:
            kind = task.get("kind", DEFAULT_TASK_KIND)
            if kind not in ALLOWED_TASK_KINDS:
                raise BuildError(
                    manifest_path,
                    f"task {task.get('name', '<unnamed>')!r} has unknown kind {kind!r}; "
                    f"allowed: {sorted(ALLOWED_TASK_KINDS)}",
                )

    validation_plan = manifest.get("validation_plan", [])
    if not isinstance(validation_plan, list):
        raise BuildError(manifest_path, "validation_plan must be a list when present")

    evals = manifest.get("evals") or {}
    has_inherit = "inherits_from" in evals
    has_local = bool(evals.get("workflow_local"))
    if has_inherit and has_local:
        raise BuildError(manifest_path, "evals sets both inherits_from and workflow_local; pick one")
    if not has_inherit and not has_local:
        raise BuildError(manifest_path, "evals must set one of inherits_from or workflow_local")
    if has_inherit:
        target = REPO_ROOT / evals["inherits_from"]
        if not target.is_dir():
            raise BuildError(manifest_path, f"evals.inherits_from {evals['inherits_from']!r} does not exist")
    if has_local and not (manifest_path.parent / "evals" / "cases").is_dir():
        raise BuildError(manifest_path, "evals.workflow_local is true but evals/cases/ is missing")


def build_workflow(manifest_path: Path) -> tuple[dict, Path]:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise BuildError(manifest_path, "manifest root must be a mapping")
    validate_manifest(manifest, manifest_path)

    declared_slugs = {c["slug"] for c in manifest["components"]}

    provenance: dict[str, dict] = {}
    for component in manifest["components"]:
        entry: dict = {"slug": component["slug"], "version": component["pinned_version"]}
        if "pinned_version_sha" in component:
            entry["pinned_version_sha"] = component["pinned_version_sha"]
        provenance[component["slug"]] = entry

    built_steps: list[dict] = []
    for step in manifest["steps"]:
        built_tasks: list[dict] = []
        for task in step.get("tasks", []):
            kind = task.get("kind", DEFAULT_TASK_KIND)
            body, source_slug, sha = resolve_task_prompt(task, manifest_path, declared_slugs)
            if source_slug and sha:
                provenance[source_slug]["prompt_sha256"] = sha
            task_data: dict = {
                "name": task["name"],
                "prompt": body,
                "input_source": task.get("input_source", "step_input"),
            }
            if kind == "Extraction":
                task_data["_embedded_search_set"] = build_embedded_search_set(task, manifest_path)
            built_tasks.append({"name": kind, "data": task_data})
        built_steps.append({
            "name": step["name"],
            "data": {},
            "is_output": bool(step.get("is_output", False)),
            "tasks": built_tasks,
        })

    validation_plan = manifest.get("validation_plan", []) or []

    description = manifest["description"]
    if isinstance(description, str):
        description = description.strip()

    exported_at = f"{manifest['updated']}T00:00:00+00:00"
    export = {
        "vandalizer_export": True,
        "schema_version": int(manifest["vandalizer_schema_version"]),
        "export_type": "workflow",
        "exported_at": exported_at,
        "exported_by": manifest.get("owner") or "ai4ra-prompt-library-build",
        "items": [{
            "name": manifest["name"],
            "description": description,
            "steps": built_steps,
            "input_config": {},
            "output_config": {},
            "resource_config": {},
            "validation_plan": validation_plan,
            "validation_inputs": [],
            "x_ai4ra": {
                "workflow_source": manifest_path.relative_to(REPO_ROOT).as_posix(),
                "workflow_version": manifest["workflow_version"],
                "status": manifest["status"],
                "components": [provenance[slug] for slug in sorted(provenance)],
            },
        }],
    }

    workflow_slug = manifest_path.parent.name
    output_path = manifest_path.parent / f"{workflow_slug}.vandalizer.json"
    return export, output_path


def render(export: dict) -> str:
    return json.dumps(export, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify checked-in files match a fresh build")
    ap.add_argument("--workflow", type=Path, help="build a single manifest.yaml path")
    args = ap.parse_args()

    if args.workflow:
        manifests = [args.workflow.resolve()]
    else:
        manifests = discover_manifests()

    errors: list[str] = []
    drift: list[Path] = []
    written = 0

    for manifest_path in manifests:
        try:
            export, output_path = build_workflow(manifest_path)
        except BuildError as exc:
            errors.append(str(exc))
            continue
        except Exception as exc:  # noqa: BLE001
            rel = manifest_path.relative_to(REPO_ROOT) if manifest_path.is_absolute() else manifest_path
            errors.append(f"{rel}: {type(exc).__name__}: {exc}")
            continue

        rendered = render(export)
        if args.check:
            existing = output_path.read_text(encoding="utf-8") if output_path.is_file() else ""
            if existing != rendered:
                drift.append(output_path)
        else:
            existing = output_path.read_text(encoding="utf-8") if output_path.is_file() else None
            if existing != rendered:
                output_path.write_text(rendered, encoding="utf-8")
                written += 1

    if errors:
        print("Build errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    if args.check:
        if drift:
            print("Vandalizer workflow exports are stale:", file=sys.stderr)
            for path in drift:
                print(f"  - {path.relative_to(REPO_ROOT)}", file=sys.stderr)
            print("Run `python3 scripts/build_vandalizer_workflows.py` and commit.", file=sys.stderr)
            return 1
        print(f"All {len(manifests)} workflow export(s) up to date.")
        return 0

    print(f"Built {written} workflow export(s) (of {len(manifests)} manifest(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
