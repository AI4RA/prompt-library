# AI4RA Evaluation Triad

The AI4RA evaluation stack is intentionally split across three repositories so prompts and contracts, datasets and scoring references, and execution evidence can evolve independently without hiding their dependencies.

## Repositories

| Repository | Owns | Primary machine surface |
| --- | --- | --- |
| `AI4RA/prompt-library` | prompts, skills, agents, schemas, and component contracts | `component_catalog.json` |
| `AI4RA/evaluation-data-sets` | datasets, artifacts, and scoring references | `dataset_catalog.json` |
| `AI4RA/evaluation-harness` | evaluation execution, provenance capture, vendored prompt snapshots, and run artifacts | `harness_catalog.json` |

Where a shared domain contract applies, `ui-insight/AI4RA-UDM` is the common UDM foundation. A repo-local schema that aligns to UDM semantics is not automatically the shared UDM contract.

## Default operating model

For humans and agentic tools:

- Start in the repository you were asked to change.
- Read that repo's `README.md`, machine catalog or manifest, and local agent guide first.
- Bring sibling repos into scope only when the task crosses a contract boundary, validation surface, discovery surface, or observed upstream ref.
- Record observed commit SHAs when upstream state matters instead of documenting against floating `main`.
- Keep human-facing docs and machine-readable catalogs or manifests aligned in the same change when practical.

## When to open sibling repos

Open `AI4RA/prompt-library` when:

- a dataset or harness change depends on a component id, prompt manifestation, schema, or contract-scope claim
- vendored prompts need to be refreshed or explained
- a repo-local schema must be distinguished from the shared UDM contract

Open `AI4RA/evaluation-data-sets` when:

- a prompt or harness change depends on dataset ids, file entrypoints, validation policy, or scoring references
- expected outputs or golden cases need to be updated together with a component contract
- observed upstream refs need to be re-pinned after dataset-side changes

Open `AI4RA/evaluation-harness` when:

- a prompt or dataset change affects vendored prompt snapshots, runnable dataset registration, or scoring implementation
- run provenance, catalog-driven discovery, or execution behavior needs to be updated to match a contract change
- the harness catalog or vendored prompt lockfile must be refreshed to match a newly observed upstream state

## Should agentic tools read all three repos at once?

Usually no. Reading every repo by default adds noise and makes it easier to change the wrong thing.

Usually yes when:

- a contract, schema, dataset id, validation policy, or prompt snapshot crosses repo boundaries
- you need to refresh observed upstream refs
- you need to verify whether a contract is repo-local or shared UDM
- you are changing discovery surfaces such as `component_catalog.json`, `dataset_catalog.json`, or `harness_catalog.json`

## Coordination checklist

1. Update the repo-local machine surface.
2. Update the matching human-facing docs.
3. Refresh observed upstream refs if the change depended on sibling state.
4. Run the repo-local validation commands described in `AGENTS.md` or `CLAUDE.md`.
5. Note any follow-on mirror work still needed in the other leg or legs.
