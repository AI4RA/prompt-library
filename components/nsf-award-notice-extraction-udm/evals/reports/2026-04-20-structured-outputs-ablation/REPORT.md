# Structured-output ablation — `openai/gpt-oss-120b`

**Date:** 2026-04-20
**Prompt:** `components/nsf-award-notice-extraction-udm/prompt.md`
**Schema:** `components/nsf-award-notice-extraction-udm/schema.json` (41 declared properties, 12 required)
**Model:** `openai/gpt-oss-120b` via Mindrouter
**OCR:** `mindrouter` (dots.OCR) — byte-identical OCR reused across all three runs
**Documents:** 28 real NSF Award Notice PDFs (local, not published)
**Replicates per document:** 5
**Temperature:** 0.1
**max_tokens:** 16384

## Question

The original [baseline run](../2026-04-18-gpt-oss-120b-dots-r5/REPORT.md) used **no structured-output enforcement** — the prompt asked for JSON in prose, and the model was trusted to comply. That run had a 0% strict schema-validity rate because the model freely renamed top-level keys (e.g. emitted `total_intended_award_amount` when the schema specifies `total_intended_amount`).

Three natural questions:

1. Does **`response_format: {type: "json_object"}`** — OpenAI's "basic JSON mode" — fix the drift?
2. Does **`response_format: {type: "json_schema", json_schema: {strict: true, schema: <schema.json>}}`** fix the drift?
3. What does each cost?

This ablation holds prompt, model, OCR output, temperature, and documents constant — only the `response_format` field of the Mindrouter request varies.

## Headline

| mode | replicates OK | strict schema validity | validity ignoring extra top keys | p50 chat latency | p50 completion tokens | hits 80% of 16k cap |
|---|---|---|---|---|---|---|
| [`none`](../2026-04-18-gpt-oss-120b-dots-r5/REPORT.md) (prompt-only) | 140/140 | **0.0%** | 55.7% | 66.9s | 7821 | 1 / 140 |
| [`json_object`](../2026-04-20-gpt-oss-120b-json_object/REPORT.md) | 140/140 | **0.0%** | 57.1% | 62.7s | 7755 | 0 / 140 |
| [`json_schema`](../2026-04-20-gpt-oss-120b-json_schema/REPORT.md) (strict) | 138/140 | **100.0%** | 100.0% | 63.5s | 7472 | 2 / 140 |

## Finding 1 — `json_object` is a no-op for this task

`json_object` mode makes one guarantee: the response parses as JSON. On a model that already returns parseable JSON (gpt-oss-120b returned 140/140 parseable outputs even under `none`), that guarantee is free but useless.

Crucially, `json_object` imposes **no constraint on shape**. The naming drift that killed the baseline's strict validity is present in identical form under `json_object`:

| schema key expected | model actually emitted | occurrences (json_object) |
|---|---|---|
| `total_intended_amount` | `total_intended_award_amount` | 138 / 140 |
| `total_obligated_to_date` | `total_amount_obligated_to_date` | 136 / 140 |
| *(various)* | `total_approved_cost_share_or_matching_amount` | 123 / 140 |
| `start_date`, `end_date` | `award_period_start_date`, `award_period_end_date` | 40 / 140 |

The 1.4-point bump in "validity ignoring extras" (55.7% → 57.1%) is within noise. The model's choice of shape is not influenced by `json_object`. **If you are using `json_object` expecting schema-like enforcement, you are getting parseability and nothing else.**

## Finding 2 — `json_schema` is the step change

Switching the same request from `json_object` to `json_schema: {strict: true, schema: <schema.json>}`:

- **Strict schema validity: 0% → 100%.** Every replicate matches the schema's declared shape: every required top-level key is present, every value is the right type, and no un-declared top-level keys appear.
- **Naming drift: eliminated.** Zero extra top-level keys emitted across 138 successful replicates. The model produced exactly the keys the schema names.
- **Completion tokens: comparable.** Median went *down* slightly (7821 → 7472) — the model isn't being forced to emit everything, only to emit *only* what the schema allows.

This is the result the prompt's output contract was *asking for*. `json_schema` turns the contract from a request into a constraint the gateway enforces.

## Finding 3 — `json_schema` can rarely truncate on outlier documents

Two of the 140 replicates (1.4%) under `json_schema` failed as `parse_error`. Both hit the completion-token cap (`completion_tokens: 16384 == cap`) and got truncated mid-string, and both were replicates of the same document:

- `Strickland 2021` replicate 2: `Expecting ',' delimiter: line 3575 column 39` — truncated at 16384 tokens
- `Strickland 2021` replicate 3: `Unterminated string starting at: line 2689 column 3` — truncated at 16384 tokens

This is not a structured-output failure. The other three replicates of the same document succeeded cleanly (two used 8–12k tokens). p95 completion length across the whole 140-replicate run was 10367 tokens; the 16k cap does not bind for the median document. The Strickland 2021 truncations are **outlier behavior on one long doc**, not a systemic issue with `json_schema`.

We verified this by re-running the same matrix at `max_tokens=32768`: cap truncations went to zero, but the 32k budget traded 2 truncations for 9 `ReadTimeout` failures as the longer generation budget let hard docs hang past the client's 240s timeout. Net success rate went **down** (138/140 → 130/140). For this task, at this gateway, `max_tokens=16384` is a reasonable operating point — the 1.4% outlier truncation rate is lower than the transient-timeout rate exposed by a higher budget.

**Operational recommendations:**

1. Leave `max_tokens=16384` for gpt-oss-120b + this schema.
2. Use `analyze_run.py`'s `completion_tokens.n_over_80pct_of_cap` counter to detect if a specific document class starts systematically pressuring the cap — that's the signal to raise it (and the client timeout alongside).

## Finding 4 — latency and token cost are roughly free

Across the three modes, p50 chat latency was 62.7–66.9s and p50 completion tokens was 7472–7821. The differences are noise. **Adopting `json_schema` did not make requests noticeably slower or more expensive**, at least at Mindrouter's current queue depth on gpt-oss-120b.

## Implications for prompt library authors

1. **If your component ships a `schema.json`, wire it to `response_format: json_schema` at call time.** The shape contract in the prompt body becomes a gateway-enforced constraint instead of a suggestion the model may rephrase.
2. **Do not assume `json_object` does anything useful.** For well-behaved models it's a no-op; for worse-behaved models (e.g. `openai/gpt-oss-20b`, where our preliminary probe found `json_object` returned *invalid* JSON) it can actively mislead.
3. **Measure before raising `max_tokens`.** The intuition that strict-schema generation needs a bigger budget is not free — a larger budget lets hard documents hang longer against the client timeout and can trade truncations for timeouts (see Finding 3). Treat 16k as a working default for this task and raise only when the 80%-of-cap counter shows real pressure.
4. **Test `json_schema` per model, not per gateway.** Mindrouter passes the constraint through; the model either honors it or doesn't. In a separate probe we saw `llama3.3:70b` truncate mid-strict-JSON and `openai/gpt-oss-20b` fail `json_object`. The next ablation should quantify this across the portability slate.

## Reproduction

Byte-identical OCR inputs were reused across all three runs via:

```bash
python scripts/extract_only.py \
  --pdf-dir <local NSF PDFs> \
  --prompt components/nsf-award-notice-extraction-udm/prompt.md \
  --model openai/gpt-oss-120b \
  --ocr mindrouter \
  --replicates 5 \
  --max-tokens 16384 \
  --pdf-concurrency 3 \
  --structured-output json_object \
  --reuse-ocr-from <path to baseline run dir> \
  --run-name nsf-udm-gpt-oss-120b-dots-r5-json_object

# then again with --structured-output=json_schema and --json-schema-file=components/.../schema.json
```

See each per-mode report for the full run-level headline, schema-validation detail, per-field consistency, and coverage tables.

## Open follow-ups

- **Portability.** Repeat this ablation on `qwen2.5:72b`, `microsoft/phi-4`, and `openai/gpt-oss-20b`. The probe suggests `json_schema` enforcement varies per model.
- **Prompt-only vs `json_schema` on a prompt that spells out exact key names.** Roughly half of baseline's ignoring-extras 55.7% → 100% gap is naming drift that a more explicit prompt could have closed. Worth measuring how much of the remaining gap is type/shape errors vs naming.
- **Harness client hardening.** A 32k re-run showed that lifting `max_tokens` alone surfaces a latency/timeout interaction (Finding 3). If future work wants to eliminate the 1.4% truncation rate, the fix is a combined bump of `max_tokens` + `httpx` client timeout + lower `pdf-concurrency` to reduce Mindrouter queue depth — not `max_tokens` alone.
