# Vandalizer RA builds changelog

Drafts carry no version. Each entry names the source commit the files came from; `drafts.json` pins every file by SHA256.

## 2026-11-24: collection added

- Add 25 draft import files: 12 under `new/` (7 Skills, 5 workflows), 4 browser Skills under `companion/`, and 9 workflow variants under `variants/`.
- Files match `ui-insight/ProcessMapping` `drafts/vandalizer` at commit `52c7b257ba9196928c6e0207472b0745f93e67fd` byte for byte, except `add-sponsor-research`, which omits one institution-specific sentence (see `source.differences_from_source` in `drafts.json`). They include three rounds of fixes made after test runs on November 20, 2026 and the November 23 revisions to Prior Approval Tracking, Award Compliance Analysis and the five browser Skills.
- Add the generator scripts. A rebuild from vandalizer seed commit `1453fc46ea022b9e2e9d6a783a3c86731485437d` reproduces every file.
- Add `drafts.json` with per-item evaluation outcomes as of November 23, 2026.
