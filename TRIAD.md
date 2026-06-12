# AI4RA Evaluation Stack

> **Naming:** this system was originally described as a three-repository *evaluation triad*. It has since grown to **four repositories plus the shared UDM foundation** — `AI4RA/evaluation-explorer` joined as the index-and-visualization layer. This file keeps the legacy `TRIAD.md` filename so cross-repo tooling still finds the connection doc in the same place; some other docs may still use the older "triad" label.

The AI4RA evaluation stack is intentionally split across repositories so prompts and contracts, datasets and scoring references, execution evidence, and the analysis/visualization surface can evolve independently without hiding their dependencies.

## Repositories

| Repository | Role | Owns | Primary machine surface |
| --- | --- | --- | --- |
| `AI4RA/prompt-library` | what is evaluated | prompts, skills, agents, schemas, component contracts, workflows | `component_catalog.json` |
| `AI4RA/evaluation-data-sets` | inputs + answers | datasets, artifacts, scoring references | `dataset_catalog.json` |
| `AI4RA/evaluation-harness` | execution + evidence | evaluation execution, provenance capture, vendored prompt snapshots, run artifacts | `harness_catalog.json` |
| `AI4RA/evaluation-explorer` | index + visualization | a rebuildable Postgres index over the other three, web UI, NIST-aligned metrics, validation workbench | read API / `backend/app/models.py` (consumer — no published catalog) |

Where a shared domain contract applies, `ui-insight/AI4RA-UDM` is the common UDM foundation. A repo-local schema that aligns to UDM semantics is not automatically the shared UDM contract.

## Data flow and system of record

The first three repositories are **systems of record** (git). `evaluation-explorer` is a **downstream, rebuildable index** — its Postgres database can be dropped and re-ingested from the repositories at any time, and every row it stores carries `source_repo`, `commit_sha`, `source_path`, and a content hash.

```
prompt-library (components / workflows) ─┐
evaluation-data-sets (documents + gold) ─┤  pinned by commit SHA
                                         v
                evaluation-harness  ──  runs campaigns; emits RUN ARTIFACTS
                (config.json + per-document ocr.md / summary.json /
                 replicate_N.json / replicate_N.raw.txt)
                                         │   ← the durable interchange contract
                                         v
                evaluation-explorer  ──  ingests catalogs + dataset cases +
                harness run artifacts + eval reports into Postgres; serves the UI;
                the validation workbench writes back to evaluation-data-sets via PRs
```

The harness **run-artifact format** is the interchange contract: any runner that emits it (or calls the explorer publish API) can publish evidence, and the explorer never depends on harness internals.

## Default operating model

For humans and agentic tools:

- Start in the repository you were asked to change.
- Read that repo's `README.md`, its machine catalog or manifest (for the explorer: `PROJECT_PLAN.md` + `backend/app/models.py`), and its local agent guide first.
- Bring sibling repos into scope only when the task crosses a contract boundary, validation surface, discovery surface, ingestion contract, or observed upstream ref.
- Record observed commit SHAs when upstream state matters instead of documenting against floating `main`.
- Keep human-facing docs and machine-readable catalogs or manifests aligned in the same change when practical.

## When to open sibling repos

Open `AI4RA/prompt-library` when:

- a dataset, harness, or explorer change depends on a component id, prompt manifestation, schema, or contract-scope claim
- vendored prompts need to be refreshed or explained
- a repo-local schema must be distinguished from the shared UDM contract

Open `AI4RA/evaluation-data-sets` when:

- a prompt, harness, or explorer change depends on dataset ids, file entrypoints, validation policy, or scoring references
- expected outputs or golden cases need to be updated together with a component contract
- observed upstream refs need to be re-pinned after dataset-side changes

Open `AI4RA/evaluation-harness` when:

- a prompt or dataset change affects vendored prompt snapshots, runnable dataset registration, or scoring implementation
- run provenance, catalog-driven discovery, or execution behavior needs to be updated to match a contract change
- the harness catalog or vendored prompt lockfile must be refreshed to match a newly observed upstream state
- the **run-artifact format** changes (it is the explorer's ingestion contract)

Open `AI4RA/evaluation-explorer` when:

- the way runs, datasets, or catalogs are ingested or displayed must change
- a sibling's catalog, dataset metadata, or run-artifact format changes in a way that affects ingestion
- you need to investigate or visualize evaluation results, or run the validation workbench

## Should agentic tools read every repo at once?

Usually no. Reading every repo by default adds noise and makes it easier to change the wrong thing.

Usually yes when:

- a contract, schema, dataset id, validation policy, prompt snapshot, or run-artifact / ingestion format crosses repo boundaries
- you need to refresh observed upstream refs
- you need to verify whether a contract is repo-local or shared UDM
- you are changing discovery surfaces such as `component_catalog.json`, `dataset_catalog.json`, `harness_catalog.json`, or the explorer ingestion connectors

## Coordination checklist

1. Update the repo-local machine surface (catalog / manifest, or — for the explorer — the ingestion / model code).
2. Update the matching human-facing docs.
3. Refresh observed upstream refs if the change depended on sibling state.
4. Run the repo-local validation commands described in `AGENTS.md` or `CLAUDE.md`.
5. Note any follow-on mirror work still needed in the other repositories.
