# Drafts

Draft collections hold work that is ready for subject-matter review but is not yet a component or a manifest-built workflow. A draft is an idea with enough substance to run: an import file that loads into Vandalizer as a private item, so reviewers can try it and say what to keep.

Drafts are a separate surface from `components/` and `workflows/`:

| | `components/`, `workflows/` | `drafts/` |
| --- | --- | --- |
| Source of truth | `prompt.md`, `manifest.yaml` | the import JSON itself, plus the generator scripts when a collection has them |
| Versioning | semver per component or workflow | none; the collection index pins each file by SHA256 |
| Evaluation | golden cases under `evals/` | whatever the collection's index records; never a claim of validation |
| Catalog | `components` and `workflows` arrays | `drafts` array, one entry per collection |

## Layout

```
drafts/
  <collection-slug>/
    README.md        # what the collection is, how to load it, what reviewers should check
    CHANGELOG.md
    drafts.json      # machine-readable index: one entry per draft file
    ...              # the import files, grouped however the collection needs
    scripts/         # optional generators
```

## Draft kinds

The index records a `kind` for every file. Both kinds are Vandalizer export schema version 2 and are listed in [`taxonomy.md`](../taxonomy.md).

- **`vandalizer-skill`**: a chat Skill. The file has `export_type: search_set` and one item with `set_type: prompt`. The Skill's instructions are in `extraction_config.content` and its one-line trigger is in `extraction_config.when_to_use`. This kind is new to the repository: `searchsets/` holds extraction search sets, which share the envelope but list fields to extract and carry no instructions.
- **`vandalizer-workflow`**: a workflow import file with `export_type: workflow`, stored as generated rather than built from a `manifest.yaml`. Drafts may use task kinds the manifest builder does not compile yet. The ones in use so far are `Formatter`, `Approval`, `CreateProject`, `InboxDeadlines` and `AwardSnapshotPage`.

## Index contract

`drafts.json` has `schema_version`, `artifact: vandalizer_draft_collection`, `slug`, `status`, `summary`, `counts`, and an `items` array. Every item has:

| Field | Meaning |
| --- | --- |
| `id` | Unique within the collection |
| `title` | The item's name as Vandalizer shows it on import |
| `kind` | `vandalizer-skill` or `vandalizer-workflow` |
| `group` | A draft group from the taxonomy: `new`, `companion` or `variant` |
| `path` | File path relative to the collection directory |
| `sha256` | Hash of the file's bytes |
| `related_workflows` | Slugs under `workflows/` that cover the same task, possibly empty |

Collections may add fields such as `summary`, `test_fixtures` or `evaluation`. `python3 .github/scripts/lint_components.py` checks that every file is indexed, every hash matches, each `kind` matches the file's export envelope, each `title` matches the file, and each related workflow exists.

## Promoting a draft

A draft that reviewers want kept moves into the versioned surfaces and leaves the collection:

1. Put the task's prompt in `components/<slug>/` with at least one eval case.
2. For a workflow, author `workflows/<wf-slug>/manifest.yaml` and build the export. If the draft uses a task kind the builder does not compile, extend `scripts/build_vandalizer_workflows.py` in the same change.
3. For a Skill, add a `skill/SKILL.md` manifestation when a Claude Skill form is wanted. A manifest-built form for Vandalizer Skills does not exist yet.
4. Remove the draft file and its index entry, and note the promotion in the collection's changelog.

## Collections

- [`vandalizer-ra-builds/`](vandalizer-ra-builds/): 11 Skills and 14 workflows for research administrators, drafted in November 2026.
