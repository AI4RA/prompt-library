#!/usr/bin/env python3
"""
Generate the AI4RA Prompt Library MkDocs site content from `components/`.

Reads each `components/<slug>/` directory, extracts frontmatter from
`prompt.md`, and writes:

- `docs/index.md`                  — landing page with a filterable component table
- `docs/components/index.md`       — alphabetical component index
- `docs/components/<slug>.md`      — per-component detail page
- `docs/browse/by-category.md`     — grouped by category
- `docs/browse/by-domain.md`       — grouped by domain
- `docs/browse/by-status.md`       — grouped by lifecycle status
- `docs/browse/by-tag.md`          — grouped by tag
- `docs/taxonomy.md`               — copy of the repo-root taxonomy

Idempotent: rerunning produces identical output given unchanged inputs.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "PyYAML not installed. Run: pip install -r requirements-docs.txt\n"
    )
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_DIR = REPO_ROOT / "components"
DOCS_DIR = REPO_ROOT / "docs"
CATALOG_PATH = REPO_ROOT / "component_catalog.json"
REPO_URL = "https://github.com/AI4RA/prompt-library"
BRANCH = "main"
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


# --- frontmatter + component model ----------------------------------------


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"frontmatter parse error: {e}")
    return data, m.group(2)


@dataclass
class EvalCase:
    slug: str
    path: Path
    metadata: dict = field(default_factory=dict)
    has_expected: bool = False
    has_input: bool = False


@dataclass
class EvalReport:
    run_id: str
    path: Path
    body: str
    title: str
    chart_files: list[Path] = field(default_factory=list)
    has_summary_json: bool = False


@dataclass
class Component:
    slug: str
    path: Path
    frontmatter: dict
    prompt_body: str
    readme: str
    changelog: str
    schema: dict | None
    has_skill: bool
    has_agent: bool
    eval_cases: list[EvalCase]
    eval_reports: list[EvalReport] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.frontmatter.get("name", self.slug)

    @property
    def version(self) -> str:
        return str(self.frontmatter.get("version", ""))

    @property
    def category(self) -> str:
        return self.frontmatter.get("category", "")

    @property
    def domain(self) -> str:
        return self.frontmatter.get("domain", "")

    @property
    def status(self) -> str:
        return self.frontmatter.get("status", "")

    @property
    def tags(self) -> list[str]:
        t = self.frontmatter.get("tags", []) or []
        return [str(x) for x in t]

    @property
    def audience(self) -> list[str]:
        a = self.frontmatter.get("audience", []) or []
        return [str(x) for x in a]

    @property
    def created(self) -> str:
        return str(self.frontmatter.get("created", ""))

    @property
    def updated(self) -> str:
        return str(self.frontmatter.get("updated", ""))

    @property
    def manifestations(self) -> list[str]:
        m = ["prompt"]
        if self.has_skill:
            m.append("skill")
        if self.has_agent:
            m.append("agent")
        return m

    @property
    def last_fully_evaluated_version(self) -> str | None:
        min_parsed: tuple[int, int, int] | None = None
        for case in self.eval_cases:
            validated = case.metadata.get("validated_against_version")
            if not isinstance(validated, str) or not SEMVER_RE.match(validated):
                continue
            parsed = tuple(int(part) for part in validated.split("."))
            if min_parsed is None or parsed < min_parsed:
                min_parsed = parsed
        if min_parsed is None:
            return None
        return ".".join(str(part) for part in min_parsed)

    @property
    def current_version_is_fully_evaluated(self) -> bool:
        return bool(
            self.last_fully_evaluated_version
            and self.last_fully_evaluated_version == self.version
        )

    @property
    def short_description(self) -> str:
        """Best-effort first-paragraph summary pulled from README.md."""
        lines = []
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
    fm, body = split_frontmatter(prompt_path.read_text(encoding="utf-8"))
    readme = (path / "README.md").read_text(encoding="utf-8") if (path / "README.md").is_file() else ""
    changelog = (path / "CHANGELOG.md").read_text(encoding="utf-8") if (path / "CHANGELOG.md").is_file() else ""
    schema = None
    schema_path = path / "schema.json"
    if schema_path.is_file():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            sys.stderr.write(f"warning: {schema_path} is not valid JSON: {e}\n")
    has_skill = (path / "skill" / "SKILL.md").is_file()
    has_agent = (path / "agent" / "AGENT.md").is_file()

    cases_dir = path / "evals" / "cases"
    cases: list[EvalCase] = []
    if cases_dir.is_dir():
        for c in sorted(p for p in cases_dir.iterdir() if p.is_dir()):
            meta_path = c / "metadata.yaml"
            metadata = {}
            if meta_path.is_file():
                try:
                    metadata = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
                except yaml.YAMLError as e:
                    sys.stderr.write(f"warning: {meta_path} is not valid YAML: {e}\n")
            has_expected = any((c / f).is_file() for f in ("expected.json", "expected.md"))
            has_input = any((c / f).is_file() for f in ("input.json", "input-source.md"))
            cases.append(
                EvalCase(
                    slug=c.name,
                    path=c,
                    metadata=metadata,
                    has_expected=has_expected,
                    has_input=has_input,
                )
            )

    reports_dir = path / "evals" / "reports"
    reports: list[EvalReport] = []
    if reports_dir.is_dir():
        for r in sorted(p for p in reports_dir.iterdir() if p.is_dir()):
            report_md = r / "REPORT.md"
            if not report_md.is_file():
                continue
            body_text = report_md.read_text(encoding="utf-8")
            title = _extract_h1(body_text) or r.name
            charts_dir = r / "charts"
            chart_files = sorted(charts_dir.iterdir()) if charts_dir.is_dir() else []
            reports.append(
                EvalReport(
                    run_id=r.name,
                    path=r,
                    body=body_text,
                    title=title,
                    chart_files=chart_files,
                    has_summary_json=(r / "summary.json").is_file(),
                )
            )

    return Component(
        slug=path.name,
        path=path,
        frontmatter=fm,
        prompt_body=body,
        readme=readme,
        changelog=changelog,
        schema=schema,
        has_skill=has_skill,
        has_agent=has_agent,
        eval_cases=cases,
        eval_reports=reports,
    )


def _extract_h1(markdown: str) -> str | None:
    for raw in markdown.splitlines():
        line = raw.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return None


def discover_components() -> list[Component]:
    comps: list[Component] = []
    for p in sorted(COMPONENTS_DIR.iterdir()):
        if not p.is_dir():
            continue
        c = load_component(p)
        if c is not None:
            comps.append(c)
    return comps


def load_component_catalog() -> dict[str, dict]:
    if not CATALOG_PATH.is_file():
        return {}
    try:
        payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"warning: component catalog is not valid JSON: {exc}\n")
        return {}
    components = payload.get("components")
    if not isinstance(components, list):
        return {}
    return {
        entry["slug"]: entry
        for entry in components
        if isinstance(entry, dict) and isinstance(entry.get("slug"), str)
    }


# --- rendering helpers ----------------------------------------------------


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def status_badge(status: str) -> str:
    s = (status or "").lower()
    cls = s if s in {"stable", "experimental", "deprecated"} else ""
    return f'<span class="status-badge {cls}">{html_escape(status)}</span>'


def chip(s: str) -> str:
    return f'<span class="chip">{html_escape(s)}</span>'


def repo_link(path: Path, *, line: int | None = None) -> str:
    rel = path.resolve().relative_to(REPO_ROOT)
    href = f"{REPO_URL}/blob/{BRANCH}/{rel.as_posix()}"
    if line:
        href += f"#L{line}"
    return href


def strip_prompt_intro(body: str) -> str:
    """Strip the '## Prompt' header (if present) so the prompt body flows naturally."""
    lines = body.lstrip().splitlines()
    if lines and lines[0].strip().startswith("## Prompt"):
        out = lines[1:]
        while out and not out[0].strip():
            out.pop(0)
        return "\n".join(out)
    return body


def render_tag_links(tags: list[str]) -> str:
    if not tags:
        return ""
    items = " ".join(chip(t) for t in tags)
    return f'<div class="tags-line">{items}</div>'


MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def rewrite_relative_links(
    markdown: str,
    component: "Component",
    component_slugs: set[str],
    components_prefix: str = "",
) -> str:
    """Rewrite relative links inside an embedded README/CHANGELOG so they still resolve.

    - `../<other-slug>` or `../<other-slug>/...` → MkDocs sibling page under
      `components/`. `components_prefix` controls the relative path to
      `docs/components/` from the page this content lives on:
      `""` for pages already inside `components/`, `"../components/"` for pages
      inside `docs/browse/`, `"components/"` for pages at the docs root.
    - `schema.json`, `prompt.md`, `skill/SKILL.md`, `agent/AGENT.md`, `CHANGELOG.md`,
      `evals/...`, or any other relative path within the component → absolute GitHub
      blob/tree URL.
    - URLs (`http://`, `https://`, `mailto:`, anchors starting with `#`) → unchanged.
    """

    component_base = f"{REPO_URL}/blob/{BRANCH}/components/{component.slug}"

    def rewrite(match: re.Match[str]) -> str:
        text = match.group(1)
        url = match.group(2).strip()

        if url.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        # Cross-component sibling reference: ../<other-slug>[/...]
        if url.startswith("../"):
            rest = url[3:]
            head = rest.rstrip("/").split("/", 1)
            other = head[0]
            if other in component_slugs:
                tail = head[1] if len(head) > 1 else ""
                if tail in ("", "README.md"):
                    return f"[{text}]({components_prefix}{other}.md)"
                return f"[{text}]({REPO_URL}/blob/{BRANCH}/components/{other}/{tail})"
            return match.group(0)

        # Same-component relative reference — resolve against the component's repo path.
        trimmed = url.rstrip("/")
        is_dir_link = url.endswith("/")
        kind = "tree" if is_dir_link else "blob"
        base = f"{REPO_URL}/{kind}/{BRANCH}/components/{component.slug}"
        if trimmed:
            return f"[{text}]({base}/{trimmed})"
        return f"[{text}]({component_base})"

    return MD_LINK_RE.sub(rewrite, markdown)


def rewrite_report_links(
    markdown: str,
    component: "Component",
    report: "EvalReport",
    sibling_run_ids: set[str],
) -> str:
    """Rewrite relative links inside a REPORT.md for placement at
    `docs/components/<slug>/reports/<run-id>/index.md`.

    - `charts/<file>` → unchanged (files are copied alongside the rendered page)
    - `../<other-run-id>/REPORT.md` where <other-run-id> is a sibling report →
      `../<other-run-id>/index.md` (MkDocs sibling page)
    - Any other relative path → absolute GitHub blob/tree URL, resolved from the
      report's filesystem location (`components/<slug>/evals/reports/<run-id>/`).
    - URLs (`http://`, `https://`, `mailto:`, anchors `#...`) → unchanged.
    """

    report_fs_base = Path("components") / component.slug / "evals" / "reports" / report.run_id

    def rewrite(match: re.Match[str]) -> str:
        text = match.group(1)
        url = match.group(2).strip()

        if url.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        # Charts live alongside the rendered page — leave them untouched.
        if url.startswith("charts/") or url == "charts":
            return match.group(0)

        # Sibling report cross-link.
        if url.startswith("../"):
            rest = url[3:]
            head = rest.split("/", 1)
            sibling = head[0]
            tail = head[1] if len(head) > 1 else ""
            if sibling in sibling_run_ids and tail in ("REPORT.md", "", "index.md"):
                return f"[{text}](../{sibling}/index.md)"

        # Everything else: resolve the path against the report's FS location
        # and emit a GitHub URL.
        trimmed = url.rstrip("/")
        is_dir_link = url.endswith("/")
        resolved = _resolve_relative(report_fs_base, trimmed)
        kind = "tree" if is_dir_link else "blob"
        href = f"{REPO_URL}/{kind}/{BRANCH}/{resolved.as_posix()}"
        return f"[{text}]({href})"

    return MD_LINK_RE.sub(rewrite, markdown)


def _resolve_relative(base: Path, rel: str) -> Path:
    """Resolve a relative path against a base repo-relative directory, without
    touching the filesystem. Returns a repo-relative Path."""
    parts = list(base.parts) + [p for p in rel.split("/") if p]
    out: list[str] = []
    for p in parts:
        if p == "." or p == "":
            continue
        if p == "..":
            if out:
                out.pop()
            continue
        out.append(p)
    return Path(*out) if out else Path(".")


# --- page generators ------------------------------------------------------


def render_index(components: list[Component]) -> str:
    categories = sorted({c.category for c in components if c.category})
    domains = sorted({c.domain for c in components if c.domain})
    statuses = sorted({c.status for c in components if c.status})

    def opt(value: str) -> str:
        return f'<option value="{html_escape(value)}">{html_escape(value)}</option>'

    category_options = "".join(opt(c) for c in categories)
    domain_options = "".join(opt(d) for d in domains)
    status_options = "".join(opt(s) for s in statuses)

    cards = []
    for c in sorted(components, key=lambda x: x.slug):
        search_blob = " ".join(
            [c.slug, c.name, c.short_description, c.category, c.domain, c.status]
            + c.tags
            + c.audience
        )
        manifs = ", ".join(c.manifestations)
        tags_html = " ".join(chip(t) for t in c.tags) if c.tags else ""
        description = html_escape(c.short_description) if c.short_description else ""
        card = (
            f'<a href="components/{c.slug}/" class="component-card component-row" '
            f'data-search="{html_escape(search_blob)}" '
            f'data-category="{html_escape(c.category)}" '
            f'data-domain="{html_escape(c.domain)}" '
            f'data-status="{html_escape(c.status)}">'
            f'<header>'
            f'<h3><code>{html_escape(c.slug)}</code></h3>'
            f'{status_badge(c.status)}'
            f'</header>'
            f'<p class="description">{description}</p>'
            f'<div class="meta">'
            f'{chip(c.category)}{chip(c.domain)}'
            f'<span class="version">v{html_escape(c.version)}</span>'
            f'<span class="manifs">{html_escape(manifs)}</span>'
            f'</div>'
            + (f'<div class="tags">{tags_html}</div>' if tags_html else '')
            + f'</a>'
        )
        cards.append(card)

    cards_html = "\n".join(cards)

    return f"""# AI4RA Prompt Library

Versioned prompts, skills, agents, schemas, and component contracts for research-administration work.

This repository is the prompt-library leg of the AI4RA evaluation triad. The evaluation harness discovers components here, pairs them with datasets from [`AI4RA/evaluation-data-sets`](https://github.com/AI4RA/evaluation-data-sets), and uses the shared [`ui-insight/AI4RA-UDM`](https://github.com/ui-insight/AI4RA-UDM) foundation where a component is UDM-aligned. Contract scope is recorded per component in [`component_catalog.json`]({REPO_URL}/blob/{BRANCH}/component_catalog.json).

Start by filtering below, or jump to:

- [Browse by category](browse/by-category.md) · [by domain](browse/by-domain.md) · [by status](browse/by-status.md) · [by tag](browse/by-tag.md)
- [Contracts](contracts.md) · [About](about.md) · [Taxonomy](taxonomy.md) · [Contributing](contributing.md)
- Source: [`AI4RA/prompt-library`]({REPO_URL}) · Machine discovery: [`component_catalog.json`]({REPO_URL}/blob/{BRANCH}/component_catalog.json)

## Browse all components

<div class="component-filter" data-table="all-components">
  <input class="q" type="search" placeholder="Search name, description, tags…" autocomplete="off">
  <select class="category"><option value="">All categories</option>{category_options}</select>
  <select class="domain"><option value="">All domains</option>{domain_options}</select>
  <select class="status"><option value="">All statuses</option>{status_options}</select>
  <span class="count"></span>
</div>

<div class="component-grid" id="all-components" markdown="0">
{cards_html}
</div>
"""


def render_component_index(components: list[Component]) -> str:
    lines = [
        "# Components",
        "",
        "Alphabetical index of every component. Use the [home page](../index.md) for filtering and [`component_catalog.json`](https://github.com/AI4RA/prompt-library/blob/main/component_catalog.json) for machine-readable discovery.",
        "",
        "| Component | Category | Domain | Status | Version | Last Fully Evaluated |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for c in sorted(components, key=lambda x: x.slug):
        last_eval = c.last_fully_evaluated_version or "none"
        lines.append(
            f"| [`{c.slug}`]({c.slug}.md) | {c.category} | {c.domain} | {c.status} | `{c.version}` | `{last_eval}` |"
        )
    lines.append("")
    return "\n".join(lines)


def render_component_page(
    c: Component, component_slugs: set[str], catalog_by_slug: dict[str, dict]
) -> str:
    manifest_links = [
        f"[`prompt.md`]({repo_link(c.path / 'prompt.md')})",
    ]
    if c.has_skill:
        manifest_links.append(f"[`skill/SKILL.md`]({repo_link(c.path / 'skill' / 'SKILL.md')})")
    if c.has_agent:
        manifest_links.append(f"[`agent/AGENT.md`]({repo_link(c.path / 'agent' / 'AGENT.md')})")

    last_eval = c.last_fully_evaluated_version or "none"
    eval_state = (
        "current"
        if c.current_version_is_fully_evaluated
        else (f"behind ({last_eval} validated)" if c.last_fully_evaluated_version else "no validated eval cases")
    )
    fact_rows = [
        ("Slug", f"<code>{html_escape(c.slug)}</code>"),
        ("Version", f"<code>{html_escape(c.version)}</code>"),
        ("Status", status_badge(c.status)),
        ("Last fully evaluated", f"<code>{html_escape(last_eval)}</code>"),
        ("Eval state", html_escape(eval_state)),
        ("Category", chip(c.category)),
        ("Domain", chip(c.domain)),
        ("Manifestations", ", ".join(c.manifestations)),
        ("Created", html_escape(c.created)),
        ("Updated", html_escape(c.updated)),
    ]
    facts_html = "".join(
        f'<div class="fact"><span class="label">{label}</span>'
        f'<span class="value">{value}</span></div>'
        for label, value in fact_rows
    )
    fact_block = f'<div class="fact-grid">{facts_html}</div>'

    tags_block = ""
    if c.tags:
        tags_block = "**Tags:** " + " ".join(chip(t) for t in c.tags) + "\n\n"
    audience_block = ""
    if c.audience:
        audience_block = "**Audience:** " + ", ".join(f"`{a}`" for a in c.audience) + "\n\n"

    # README (strip top-level H1 to avoid duplicate titles; MkDocs uses the page title)
    readme_body = c.readme
    if readme_body.lstrip().startswith("#"):
        first_nl = readme_body.find("\n")
        if first_nl != -1:
            readme_body = readme_body[first_nl + 1 :].lstrip()
    # Also collapse any repeated "Current version" line — the fact grid already shows it
    readme_body = re.sub(r"(?m)^\*\*Current version:\*\* .*\n", "", readme_body)
    readme_body = re.sub(r"(?m)^\*\*Category:\*\* .*\n", "", readme_body)
    readme_body = re.sub(r"(?m)^\*\*Domain:\*\* .*\n", "", readme_body)
    readme_body = re.sub(r"(?m)^\*\*Status:\*\* .*\n", "", readme_body)
    readme_body = re.sub(r"(?m)^\*\*Manifestations:\*\* .*\n", "", readme_body)
    readme_body = rewrite_relative_links(readme_body, c, component_slugs)

    sections: list[str] = []
    sections.append(f"# {c.slug}")
    sections.append(fact_block)
    sections.append(tags_block + audience_block)
    sections.append("**Manifestations in repo:** " + " · ".join(manifest_links) + "\n")
    sections.append(readme_body.strip())

    catalog_entry = catalog_by_slug.get(c.slug, {})
    output_contract = (
        catalog_entry.get("contracts", {}).get("output", {})
        if isinstance(catalog_entry, dict)
        else {}
    )
    triad = catalog_entry.get("triad_integration", {}) if isinstance(catalog_entry, dict) else {}
    related_components = catalog_entry.get("related_components", []) if isinstance(catalog_entry, dict) else []

    if output_contract:
        format_name = output_contract.get("format", "unknown")
        scope = output_contract.get("scope", "unknown")
        validation_surfaces = output_contract.get("validation_surfaces", [])
        schema_entrypoints = output_contract.get("schema_entrypoints", [])
        sections.append("## Contract scope")
        sections.append(
            f"- Output format: `{html_escape(str(format_name))}`"
        )
        sections.append(
            f"- Contract scope: `{html_escape(str(scope))}`"
        )
        if validation_surfaces:
            joined = ", ".join(f"`{surface}`" for surface in validation_surfaces)
            sections.append(f"- Validation surfaces: {joined}")
        if schema_entrypoints:
            joined = ", ".join(f"`{pointer}`" for pointer in schema_entrypoints)
            sections.append(f"- Schema entrypoints: {joined}")
        notes = output_contract.get("notes")
        if notes:
            sections.append(f"- Notes: {notes}")
        sections.append(
            f"- Machine-readable catalog entry: [`component_catalog.json`]({REPO_URL}/blob/{BRANCH}/component_catalog.json)"
        )
        sections.append("")

    if triad or related_components:
        sections.append("## Triad integration")
        udm_alignment = triad.get("udm_alignment", {}) if isinstance(triad, dict) else {}
        if udm_alignment:
            status = udm_alignment.get("status", "unknown")
            notes = udm_alignment.get("notes", "")
            sections.append(
                f"- UDM alignment: `{html_escape(str(status))}`"
                + (f" — {notes}" if notes else "")
            )
        evaluation_datasets = triad.get("evaluation_datasets", []) if isinstance(triad, dict) else []
        if evaluation_datasets:
            for dataset in evaluation_datasets:
                dataset_id = dataset.get("dataset_id", "unknown")
                relationship = dataset.get("relationship", "related")
                notes = dataset.get("notes", "")
                sections.append(
                    f"- Evaluation dataset: `{html_escape(str(dataset_id))}` ({html_escape(str(relationship))})"
                    + (f" — {notes}" if notes else "")
                )
        else:
            sections.append(
                "- Evaluation datasets: no shared `evaluation-data-sets` catalog entry recorded yet; current references are repo-local eval artifacts."
            )
        harness_notes = triad.get("harness_notes")
        if harness_notes:
            sections.append(f"- Harness notes: {harness_notes}")
        if related_components:
            for related in related_components:
                slug = related.get("slug")
                relationship = related.get("relationship", "related")
                notes = related.get("notes", "")
                label = (
                    f"[`{slug}`]({slug}.md)" if isinstance(slug, str) and slug in component_slugs else f"`{slug}`"
                )
                sections.append(
                    f"- Related component: {label} ({html_escape(str(relationship))})"
                    + (f" — {notes}" if notes else "")
                )
        sections.append("")

    # Prompt body (collapsible)
    prompt_clean = rewrite_relative_links(
        strip_prompt_intro(c.prompt_body).strip(), c, component_slugs
    )
    sections.append("## Prompt body")
    sections.append(
        f'_Source: [`prompt.md`]({repo_link(c.path / "prompt.md")})._\n'
    )
    sections.append("??? note \"Show prompt\"")
    for line in prompt_clean.splitlines():
        sections.append("    " + line if line else "")
    sections.append("")

    # Schema (collapsible)
    if c.schema is not None:
        sections.append("## Output schema")
        sections.append(
            f'_Source: [`schema.json`]({repo_link(c.path / "schema.json")})._\n'
        )
        schema_pretty = json.dumps(c.schema, indent=2)
        sections.append('??? info "Show schema.json"\n')
        sections.append("    ```json")
        for line in schema_pretty.splitlines():
            sections.append("    " + line)
        sections.append("    ```")
        sections.append("")

    # Evals
    if c.eval_cases or c.eval_reports:
        sections.append("## Evals")

        if c.eval_cases:
            sections.append("### Reference cases")
            sections.append(
                f"Golden cases under [`evals/cases/`]({REPO_URL}/tree/{BRANCH}/components/{c.slug}/evals/cases)."
            )
            sections.append("")
            for case in c.eval_cases:
                case_link = f"{REPO_URL}/tree/{BRANCH}/components/{c.slug}/evals/cases/{case.slug}"
                summary = case.metadata.get("case") or case.metadata.get("notes", "").strip().splitlines()[0] if case.metadata else ""
                artifact_bits = []
                if case.has_input:
                    artifact_bits.append("input")
                if case.has_expected:
                    artifact_bits.append("expected")
                artifacts = ", ".join(artifact_bits) if artifact_bits else "no artifacts"
                sections.append(f"- [`{case.slug}`]({case_link}) — {html_escape(summary)} _(artifacts: {artifacts})_")
            sections.append("")

        if c.eval_reports:
            sections.append("### Evaluation reports")
            sections.append(
                "Full evaluation runs — tables, charts, and findings rendered inline. "
                f"Source under [`evals/reports/`]({REPO_URL}/tree/{BRANCH}/components/{c.slug}/evals/reports)."
            )
            sections.append("")
            # Newest first (run_ids start with ISO dates).
            for report in sorted(c.eval_reports, key=lambda r: r.run_id, reverse=True):
                sections.append(
                    f"- [`{report.run_id}`]({c.slug}/reports/{report.run_id}/index.md) — {html_escape(report.title)}"
                )
            sections.append("")

    # Changelog
    if c.changelog.strip():
        sections.append("## Changelog")
        sections.append(
            f'_Source: [`CHANGELOG.md`]({repo_link(c.path / "CHANGELOG.md")})._\n'
        )
        changelog_body = c.changelog
        # Strip top-level H1
        if changelog_body.lstrip().startswith("#"):
            first_nl = changelog_body.find("\n")
            if first_nl != -1:
                changelog_body = changelog_body[first_nl + 1 :].lstrip()
        changelog_body = rewrite_relative_links(changelog_body, c, component_slugs)
        sections.append(changelog_body.strip())
        sections.append("")

    return "\n\n".join(s for s in sections if s is not None) + "\n"


def render_grouped(
    title: str,
    intro: str,
    components: list[Component],
    key: str,
    component_slugs: set[str],
) -> str:
    groups: dict[str, list[Component]] = defaultdict(list)
    for c in components:
        if key == "tag":
            for tag in c.tags:
                groups[tag].append(c)
        else:
            value = getattr(c, key) or "(unspecified)"
            groups[value].append(c)

    lines = [f"# {title}", "", intro, ""]
    for group_name in sorted(groups):
        lines.append(f"## {group_name}")
        lines.append("")
        for c in sorted(groups[group_name], key=lambda x: x.slug):
            lines.append(
                f"- [`{c.slug}`](../components/{c.slug}.md) "
                f"— {c.category} / {c.domain} / {c.status} — v{c.version}"
            )
            if c.short_description:
                desc = rewrite_relative_links(
                    c.short_description, c, component_slugs, components_prefix="../components/"
                )
                lines.append(f"    <br><small>{desc}</small>")
        lines.append("")
    return "\n".join(lines)


def render_report_page(c: Component, report: EvalReport) -> str:
    """Produce the MkDocs page content for a single evaluation report."""
    sibling_run_ids = {r.run_id for r in c.eval_reports}
    body = rewrite_report_links(report.body, c, report, sibling_run_ids)

    source_note = (
        f"_Source: [`evals/reports/{report.run_id}/REPORT.md`]"
        f"({REPO_URL}/blob/{BRANCH}/components/{c.slug}/evals/reports/{report.run_id}/REPORT.md). "
        f"Component: [`{c.slug}`](../../../{c.slug}.md)._"
    )

    # Splice the source note in after the first H1 so the component back-link is visible
    # without displacing the authored title.
    lines = body.splitlines()
    out_lines: list[str] = []
    inserted = False
    for line in lines:
        out_lines.append(line)
        if not inserted and line.strip().startswith("# "):
            out_lines.append("")
            out_lines.append(source_note)
            inserted = True
    if not inserted:
        out_lines.insert(0, source_note)
        out_lines.insert(1, "")
    return "\n".join(out_lines).rstrip() + "\n"


def render_reports_index(c: Component) -> str:
    lines = [
        f"# {c.slug} — evaluation reports",
        "",
        f"Evaluation runs for the [`{c.slug}`](../../{c.slug}.md) component. "
        "Each report is a full run: tables, charts, and findings.",
        "",
    ]
    for report in sorted(c.eval_reports, key=lambda r: r.run_id, reverse=True):
        lines.append(
            f"- [`{report.run_id}`]({report.run_id}/index.md) — {report.title}"
        )
    lines.append("")
    return "\n".join(lines)


# --- mkdocs.yml nav regeneration ------------------------------------------


def render_components_nav(components: list[Component]) -> str:
    """Build the `Components:` nav block as a YAML fragment. The fragment is
    spliced into mkdocs.yml in place of the existing `- Components:` entry."""
    out: list[str] = []
    out.append("  - Components:")
    out.append("      - Index: components/index.md")
    for c in sorted(components, key=lambda x: x.slug):
        if c.eval_reports:
            out.append(f"      - {c.slug}:")
            out.append(f"          - Overview: components/{c.slug}.md")
            out.append(f"          - Reports:")
            out.append(
                f"              - Index: components/{c.slug}/reports/index.md"
            )
            for report in sorted(c.eval_reports, key=lambda r: r.run_id, reverse=True):
                out.append(
                    f"              - {report.run_id}: "
                    f"components/{c.slug}/reports/{report.run_id}/index.md"
                )
        else:
            out.append(f"      - {c.slug}: components/{c.slug}.md")
    return "\n".join(out) + "\n"


def splice_mkdocs_nav(components: list[Component]) -> None:
    """Regenerate the `- Components:` block inside mkdocs.yml so the nav
    includes per-component report pages. Leaves all other YAML content
    (comments, ordering, other nav entries) untouched."""
    mkdocs_yml = REPO_ROOT / "mkdocs.yml"
    text = mkdocs_yml.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Find the `  - Components:` line under `nav:`
    start_idx = None
    for i, line in enumerate(lines):
        if line.rstrip() == "  - Components:":
            start_idx = i
            break
    if start_idx is None:
        sys.stderr.write(
            "warning: could not find `  - Components:` in mkdocs.yml; nav not updated\n"
        )
        return

    # The Components block ends at the next line that is either:
    #   - a sibling top-level nav entry (`  - `), OR
    #   - a new top-level YAML key (col-0 letter followed by ':'), OR
    #   - EOF.
    end_idx = len(lines)
    for j in range(start_idx + 1, len(lines)):
        stripped = lines[j].rstrip()
        if not stripped:
            continue
        # Sibling nav entry at the same indent level.
        if stripped.startswith("  - ") and not stripped.startswith("      "):
            end_idx = j
            break
        # A new top-level key (e.g. `extra:`).
        if stripped and lines[j][0].isalpha() and stripped.endswith(":"):
            end_idx = j
            break

    new_block = render_components_nav(components)
    new_text = "".join(lines[:start_idx]) + new_block + "".join(lines[end_idx:])

    if new_text != text:
        mkdocs_yml.write_text(new_text, encoding="utf-8")


def render_taxonomy() -> str:
    src = REPO_ROOT / "taxonomy.md"
    if not src.is_file():
        return "# Taxonomy\n\n(Not found in repo.)\n"
    return src.read_text(encoding="utf-8")


# --- file writing ---------------------------------------------------------


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8")


def main() -> int:
    if not COMPONENTS_DIR.is_dir():
        sys.stderr.write(f"components directory not found: {COMPONENTS_DIR}\n")
        return 1

    components = discover_components()
    if not components:
        sys.stderr.write("no components discovered; check components/ directory\n")
        return 1

    print(f"Found {len(components)} components:")
    for c in components:
        print(f"  - {c.slug} ({c.category}/{c.domain}/{c.status}, v{c.version})")

    component_slugs = {c.slug for c in components}
    catalog_by_slug = load_component_catalog()

    write(DOCS_DIR / "index.md", render_index(components))
    write(DOCS_DIR / "components" / "index.md", render_component_index(components))
    for c in components:
        write(
            DOCS_DIR / "components" / f"{c.slug}.md",
            render_component_page(c, component_slugs, catalog_by_slug),
        )

        # Reports: fully regenerate the per-component reports tree so removed
        # reports don't linger.
        reports_root = DOCS_DIR / "components" / c.slug / "reports"
        if reports_root.exists():
            shutil.rmtree(reports_root)
        if c.eval_reports:
            reports_root.mkdir(parents=True, exist_ok=True)
            write(reports_root / "index.md", render_reports_index(c))
            for report in c.eval_reports:
                report_dir = reports_root / report.run_id
                report_dir.mkdir(parents=True, exist_ok=True)
                write(report_dir / "index.md", render_report_page(c, report))
                if report.chart_files:
                    charts_out = report_dir / "charts"
                    charts_out.mkdir(parents=True, exist_ok=True)
                    for chart in report.chart_files:
                        if chart.is_file():
                            shutil.copy2(chart, charts_out / chart.name)

    write(
        DOCS_DIR / "browse" / "by-category.md",
        render_grouped(
            "Browse by category",
            "Components grouped by the task category they perform. See [Taxonomy](../taxonomy.md) for the controlled vocabulary.",
            components,
            "category",
            component_slugs,
        ),
    )
    write(
        DOCS_DIR / "browse" / "by-domain.md",
        render_grouped(
            "Browse by domain",
            "Components grouped by subject-matter domain.",
            components,
            "domain",
            component_slugs,
        ),
    )
    write(
        DOCS_DIR / "browse" / "by-status.md",
        render_grouped(
            "Browse by status",
            "Components grouped by lifecycle status: `stable` means the contract is intended for downstream use and has validated reference coverage, but you should still pin versions and check each component's last fully evaluated version. `experimental` is under active development and the output contract may change.",
            components,
            "status",
            component_slugs,
        ),
    )
    write(
        DOCS_DIR / "browse" / "by-tag.md",
        render_grouped(
            "Browse by tag",
            "Components grouped by tag. A component appears under every tag it declares.",
            components,
            "tag",
            component_slugs,
        ),
    )
    write(DOCS_DIR / "taxonomy.md", render_taxonomy())

    splice_mkdocs_nav(components)

    print(f"Wrote docs to {DOCS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
