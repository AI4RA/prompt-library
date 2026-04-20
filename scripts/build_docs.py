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
REPO_URL = "https://github.com/AI4RA/prompt-library"
BRANCH = "main"


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
    )


def discover_components() -> list[Component]:
    comps: list[Component] = []
    for p in sorted(COMPONENTS_DIR.iterdir()):
        if not p.is_dir():
            continue
        c = load_component(p)
        if c is not None:
            comps.append(c)
    return comps


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

    rows = []
    for c in sorted(components, key=lambda x: x.slug):
        search_blob = " ".join(
            [c.slug, c.name, c.short_description, c.category, c.domain, c.status]
            + c.tags
            + c.audience
        )
        manifs = ", ".join(c.manifestations)
        tags_html = " ".join(chip(t) for t in c.tags)
        row = (
            f'<tr class="component-row" '
            f'data-search="{html_escape(search_blob)}" '
            f'data-category="{html_escape(c.category)}" '
            f'data-domain="{html_escape(c.domain)}" '
            f'data-status="{html_escape(c.status)}">'
            f'<td><a href="components/{c.slug}/"><code>{html_escape(c.slug)}</code></a><br>'
            f'<small>{html_escape(c.short_description)}</small></td>'
            f'<td>{chip(c.category)}</td>'
            f'<td>{chip(c.domain)}</td>'
            f'<td>{status_badge(c.status)}</td>'
            f'<td><code>{html_escape(c.version)}</code></td>'
            f'<td>{html_escape(manifs)}</td>'
            f'<td class="tags">{tags_html}</td>'
            f'</tr>'
        )
        rows.append(row)

    rows_html = "\n".join(rows)

    return f"""# AI4RA Prompt Library

Versioned LLM components — prompts, skills, and agents — for research-administration work. Author a task once, reuse it across raw-prompt, Claude Skill, and agent manifestations without drift.

Start by filtering below, or jump to:

- [Browse by category](browse/by-category.md) · [by domain](browse/by-domain.md) · [by status](browse/by-status.md) · [by tag](browse/by-tag.md)
- [About](about.md) · [Taxonomy](taxonomy.md) · [Contributing](contributing.md)
- Source: [`AI4RA/prompt-library`]({REPO_URL}) · Canonical UDM: [`ui-insight/AI4RA-UDM`](https://github.com/ui-insight/AI4RA-UDM)

## Browse all components

<div class="component-filter" data-table="all-components">
  <input class="q" type="search" placeholder="Search name, description, tags…" autocomplete="off">
  <select class="category"><option value="">All categories</option>{category_options}</select>
  <select class="domain"><option value="">All domains</option>{domain_options}</select>
  <select class="status"><option value="">All statuses</option>{status_options}</select>
  <span class="count"></span>
</div>

<table class="component-table" id="all-components" markdown="0">
  <thead>
    <tr>
      <th>Component</th>
      <th>Category</th>
      <th>Domain</th>
      <th>Status</th>
      <th>Version</th>
      <th>Manifestations</th>
      <th>Tags</th>
    </tr>
  </thead>
  <tbody>
{rows_html}
  </tbody>
</table>
"""


def render_component_index(components: list[Component]) -> str:
    lines = [
        "# Components",
        "",
        "Alphabetical index of every component. Use the [home page](../index.md) for filtering.",
        "",
        "| Component | Category | Domain | Status | Version |",
        "| --- | --- | --- | --- | --- |",
    ]
    for c in sorted(components, key=lambda x: x.slug):
        lines.append(
            f"| [`{c.slug}`]({c.slug}.md) | {c.category} | {c.domain} | {c.status} | `{c.version}` |"
        )
    lines.append("")
    return "\n".join(lines)


def render_component_page(c: Component, component_slugs: set[str]) -> str:
    manifest_links = [
        f"[`prompt.md`]({repo_link(c.path / 'prompt.md')})",
    ]
    if c.has_skill:
        manifest_links.append(f"[`skill/SKILL.md`]({repo_link(c.path / 'skill' / 'SKILL.md')})")
    if c.has_agent:
        manifest_links.append(f"[`agent/AGENT.md`]({repo_link(c.path / 'agent' / 'AGENT.md')})")

    fact_rows = [
        ("Slug", f"<code>{html_escape(c.slug)}</code>"),
        ("Version", f"<code>{html_escape(c.version)}</code>"),
        ("Status", status_badge(c.status)),
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
    if c.eval_cases:
        sections.append("## Evals")
        sections.append(
            f"Reference cases under [`evals/cases/`]({REPO_URL}/tree/{BRANCH}/components/{c.slug}/evals/cases)."
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

    write(DOCS_DIR / "index.md", render_index(components))
    write(DOCS_DIR / "components" / "index.md", render_component_index(components))
    for c in components:
        write(DOCS_DIR / "components" / f"{c.slug}.md", render_component_page(c, component_slugs))

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
            "Components grouped by lifecycle status: `stable` has been validated against evals and is safe to depend on; `experimental` is under active development and the output contract may change.",
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

    print(f"Wrote docs to {DOCS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
