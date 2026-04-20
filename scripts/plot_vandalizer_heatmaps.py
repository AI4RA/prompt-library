#!/usr/bin/env python3
"""Generate award × field accuracy heatmaps from an extraction-accuracy summary.json.

Produces up to four PNGs per invocation, partitioned by the validation state
of each ground-truth case:

  Validated cases (treated as ground truth, reported as accuracy):
  - `charts/accuracy_scalars_<mode>.png`
  - `charts/accuracy_budget_<mode>.png`

  In-progress cases (reference produced by automated pipeline, reported as agreement):
  - `charts/agreement_scalars_<mode>_in_progress.png`
  - `charts/agreement_budget_<mode>_in_progress.png`

Empty partitions are skipped.

Cell coloring (all heatmaps):
  - Green ramp for correct/agree rate when both sides emitted a value
  - Light orange when extractor emitted but reference did not (hallucinated)
  - Light blue when reference emitted but extractor did not (missing)
  - Gray when neither emitted (correct_absent)

Cell text:
  - "5/5", "3/4" correct-replicate counts when comparable
  - "E<N>" for extractor-only replicate count
  - "R<N>" for reference-only replicate count
  - "—" when neither emitted
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# ── Colors ──────────────────────────────────────────────────────────────

AGREE_CMAP = plt.get_cmap("RdYlGn")   # red → yellow → green
COLOR_HALLUCINATED = "#ffd4a3"        # soft orange — extractor emitted, reference null
COLOR_MISSING = "#a8d5e2"             # soft blue — reference emitted, extractor null
COLOR_CORRECT_ABSENT = "#e8e8e8"      # light gray — both null
COLOR_EDGE = "#ffffff"


# ── Data loading ────────────────────────────────────────────────────────


def load_run(summary_path: Path, mode: str) -> dict:
    data = json.loads(summary_path.read_text())
    for run in data["runs"]:
        if run["run_name"] == mode:
            return run
    raise SystemExit(
        f"mode '{mode}' not found in {summary_path}; "
        f"available: {[r['run_name'] for r in data['runs']]}"
    )


def filter_awards(run: dict, validation_state: str) -> list[dict]:
    """Return per_award entries matching a validation state."""
    if validation_state == "validated":
        return [a for a in run["per_award"] if a.get("validation_state") == "validated"]
    return [a for a in run["per_award"] if a.get("validation_state", "in_progress") != "validated"]


# ── Matrix assembly ─────────────────────────────────────────────────────


def build_scalar_matrix(awards: list[dict], field_rollup: list[dict], min_coverage: int = 1):
    """Return (awards, fields, cells) where cells[i][j] is a dict with
    {'correct_rate': float|None, 'n_correct': int, 'n_compared': int,
     'kind': 'correct'|'hallucinated'|'missing'|'none'}."""
    rollup_by_field = {r["field"]: r for r in field_rollup}
    field_names = [
        r["field"] for r in field_rollup
        if (r.get("n_compared") or 0) >= min_coverage
    ]
    def _sort_key(f):
        pct = rollup_by_field[f]["accuracy_pct"]
        return (-(pct if pct is not None else -1), f)
    field_names.sort(key=_sort_key)

    def _award_score(a):
        vals = []
        for f in field_names:
            fs = a["fields"].get(f, {})
            nc = fs.get("n_correct", 0)
            ni = fs.get("n_incorrect", 0)
            n = nc + ni
            if n:
                vals.append(nc / n)
        return sum(vals) / len(vals) if vals else 0.0
    awards = sorted(awards, key=_award_score, reverse=True)

    rows, cols = len(awards), len(field_names)
    cells = [[None] * cols for _ in range(rows)]
    for i, a in enumerate(awards):
        for j, f in enumerate(field_names):
            fs = a["fields"].get(f)
            if not fs:
                cells[i][j] = {"kind": "none", "n_correct": 0, "n_compared": 0,
                               "correct_rate": None}
                continue
            n_correct = fs.get("n_correct", 0)
            n_incorrect = fs.get("n_incorrect", 0)
            n_comp = n_correct + n_incorrect
            n_halluc = fs.get("n_hallucinated", 0)
            n_missing = fs.get("n_missing", 0)
            n_reps = a.get("n_replicates", 0)
            if n_comp:
                cells[i][j] = {
                    "kind": "correct",
                    "n_correct": n_correct,
                    "n_compared": n_comp,
                    "correct_rate": n_correct / n_comp,
                }
            elif n_halluc > 0 and n_missing == 0:
                cells[i][j] = {"kind": "hallucinated", "n_correct": n_halluc,
                               "n_compared": n_reps, "correct_rate": None}
            elif n_missing > 0 and n_halluc == 0:
                cells[i][j] = {"kind": "missing", "n_correct": n_missing,
                               "n_compared": n_reps, "correct_rate": None}
            else:
                cells[i][j] = {"kind": "none", "n_correct": 0,
                               "n_compared": 0, "correct_rate": None}
    return awards, field_names, cells


def build_budget_matrix(awards: list[dict], budget_rollup: list[dict]):
    """Same cell shape as build_scalar_matrix, but for budget slots."""
    rollup_by_slot = {r["slot"]: r for r in budget_rollup}
    slots = list(rollup_by_slot.keys())
    slots.sort(key=_budget_slot_order)

    def _award_score(a):
        vals = []
        for s in slots:
            bl = a["budget_lines"].get(s, {})
            n_correct = bl.get("n_correct", 0)
            n_comp = bl.get("n_compared", 0)
            if n_comp:
                vals.append(n_correct / n_comp)
        return sum(vals) / len(vals) if vals else 0.0
    awards = sorted(awards, key=_award_score, reverse=True)

    rows, cols = len(awards), len(slots)
    cells = [[None] * cols for _ in range(rows)]
    for i, a in enumerate(awards):
        for j, s in enumerate(slots):
            bl = a["budget_lines"].get(s)
            n_reps = a.get("n_replicates", 0)
            if not bl:
                cells[i][j] = {"kind": "none", "n_correct": 0,
                               "n_compared": 0, "correct_rate": None}
                continue
            n_comp = bl.get("n_compared", 0)
            n_halluc = bl.get("n_hallucinated", 0)
            n_missing = bl.get("n_missing", 0)
            if n_comp:
                cells[i][j] = {
                    "kind": "correct",
                    "n_correct": bl.get("n_correct", 0),
                    "n_compared": n_comp,
                    "correct_rate": bl.get("n_correct", 0) / n_comp,
                }
            elif n_halluc and not n_missing:
                cells[i][j] = {"kind": "hallucinated", "n_correct": n_halluc,
                               "n_compared": n_reps, "correct_rate": None}
            elif n_missing and not n_halluc:
                cells[i][j] = {"kind": "missing", "n_correct": n_missing,
                               "n_compared": n_reps, "correct_rate": None}
            else:
                cells[i][j] = {"kind": "none", "n_correct": 0,
                               "n_compared": 0, "correct_rate": None}
    return awards, slots, cells


# NSF-format budget ordering: A, B.*, C, D, E.*, F.*, G.*, H, I, J, K, L, M, fees
_CODE_ORDER = {c: i for i, c in enumerate("ABCDEFGHIJKLM")}


def _budget_slot_order(slot: str) -> tuple:
    if slot == "fees":
        return (99, 0, "")
    parts = slot.split(".", 1)
    head = parts[0]
    sub = parts[1] if len(parts) > 1 else ""
    return (_CODE_ORDER.get(head, 100), 0 if not sub else 1, sub)


# ── Rendering ───────────────────────────────────────────────────────────


def _cell_color(cell: dict) -> tuple:
    kind = cell["kind"]
    if kind == "correct":
        return AGREE_CMAP(cell["correct_rate"])
    if kind == "hallucinated":
        return COLOR_HALLUCINATED
    if kind == "missing":
        return COLOR_MISSING
    return COLOR_CORRECT_ABSENT


def _cell_text(cell: dict) -> str:
    kind = cell["kind"]
    if kind == "correct":
        return f"{cell['n_correct']}/{cell['n_compared']}"
    if kind == "hallucinated":
        return f"E{cell['n_correct']}"
    if kind == "missing":
        return f"R{cell['n_correct']}"
    return "—"


def _cell_text_color(cell: dict) -> str:
    if cell["kind"] == "correct" and cell["correct_rate"] < 0.4:
        return "white"
    return "black"


def render_heatmap(
    awards,
    cols,
    cells,
    *,
    col_label_for,
    title: str,
    subtitle: str,
    out_path: Path,
    row_labels: list[str] | None = None,
):
    rows = len(awards)
    ncols = len(cols)
    if rows == 0 or ncols == 0:
        print(f"skip: {out_path.name} (empty)")
        return

    # Size: ~0.42" per column + ~0.35" per row, with min/max clamps.
    fig_w = max(9.0, min(22.0, 2.2 + 0.42 * ncols))
    fig_h = max(5.0, min(14.0, 1.6 + 0.35 * rows))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    for i in range(rows):
        for j in range(ncols):
            cell = cells[i][j]
            color = _cell_color(cell)
            ax.add_patch(
                mpatches.Rectangle(
                    (j, rows - 1 - i), 1, 1,
                    facecolor=color, edgecolor=COLOR_EDGE, linewidth=1.5,
                )
            )
            ax.text(
                j + 0.5, rows - 1 - i + 0.5,
                _cell_text(cell),
                ha="center", va="center",
                fontsize=7.5, color=_cell_text_color(cell),
            )

    ax.set_xlim(0, ncols)
    ax.set_ylim(0, rows)

    ax.set_xticks([j + 0.5 for j in range(ncols)])
    ax.set_xticklabels([col_label_for(c) for c in cols],
                       rotation=60, ha="right", fontsize=8)

    if row_labels is None:
        row_labels = [f"{a['award']}/{a.get('amendment', '')}" for a in awards]
    ax.set_yticks([rows - 1 - i + 0.5 for i in range(rows)])
    ax.set_yticklabels(row_labels, fontsize=8)

    ax.set_xlabel("")
    ax.set_ylabel("Award / amendment", fontsize=9)
    ax.set_title(f"{title}\n{subtitle}", fontsize=11, loc="left", pad=10)

    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Legend
    legend_handles = [
        mpatches.Patch(color=AGREE_CMAP(1.0), label="100% correct"),
        mpatches.Patch(color=AGREE_CMAP(0.6), label="partial"),
        mpatches.Patch(color=AGREE_CMAP(0.0), label="0% correct"),
        mpatches.Patch(color=COLOR_HALLUCINATED, label="extractor-only (E)"),
        mpatches.Patch(color=COLOR_MISSING, label="reference-only (R)"),
        mpatches.Patch(color=COLOR_CORRECT_ABSENT, label="both absent"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.18 - 0.005 * max(0, 8 - rows)),
        ncol=6, frameon=False, fontsize=8,
    )

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote: {out_path}")


# ── CLI ─────────────────────────────────────────────────────────────────


def _plot_partition(
    run: dict,
    awards: list[dict],
    partition_summary: dict,
    *,
    mode: str,
    out_dir: Path,
    filename_kind: str,         # "accuracy" | "agreement"
    filename_suffix: str,       # "" | "_in_progress"
    label_noun: str,            # "accuracy" | "agreement"
    reference_label: str,       # "ground truth" | "reference"
) -> None:
    if not awards:
        print(f"skip: no {filename_suffix or 'validated'} cases for mode={mode}")
        return

    # Scalars
    awards_s, fields, cells_s = build_scalar_matrix(awards, partition_summary["field_rollup"])
    overall_s = partition_summary["overall_accuracy_pct"]
    subtitle_s = (
        f"{len(awards)} cases ({filename_suffix.lstrip('_').replace('_', ' ') or 'validated'}) · "
        f"overall {overall_s:.1f}% {label_noun} on replicates where both sides emit a value. "
        if overall_s is not None else
        f"{len(awards)} cases · no replicate pairs had values on both sides."
    )
    render_heatmap(
        awards_s, fields, cells_s,
        col_label_for=lambda f: f,
        title=f"Scalar-field {label_noun} vs. {reference_label}  ({mode})",
        subtitle=subtitle_s,
        out_path=out_dir / f"{filename_kind}_scalars_{mode}{filename_suffix}.png",
    )

    # Budget
    awards_b, slots, cells_b = build_budget_matrix(awards, partition_summary["budget_rollup"])
    overall_b = partition_summary["budget_overall_accuracy_pct"]
    subtitle_b = (
        f"{len(awards)} cases · overall {overall_b:.1f}% {label_noun} on replicates where both "
        f"sides emit a budget line."
        if overall_b is not None else
        f"{len(awards)} cases · no budget slots had values on both sides."
    )
    render_heatmap(
        awards_b, slots, cells_b,
        col_label_for=lambda s: s,
        title=f"Budget-line {label_noun} vs. {reference_label}  ({mode})",
        subtitle=subtitle_b,
        out_path=out_dir / f"{filename_kind}_budget_{mode}{filename_suffix}.png",
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--summary", required=True,
                   help="Path to summary.json produced by compare_to_vandalizer.py")
    p.add_argument("--mode", default="json_schema",
                   help="Which run/mode to plot (default: json_schema)")
    p.add_argument("--out-dir", default=None,
                   help="Output directory (default: <summary-dir>/charts)")
    args = p.parse_args()

    summary_path = Path(args.summary).expanduser().resolve()
    out_dir = (Path(args.out_dir).expanduser().resolve()
               if args.out_dir else summary_path.parent / "charts")

    run = load_run(summary_path, args.mode)

    validated = filter_awards(run, "validated")
    in_progress = filter_awards(run, "in_progress")

    _plot_partition(
        run, validated, run["validated"],
        mode=args.mode, out_dir=out_dir,
        filename_kind="accuracy", filename_suffix="",
        label_noun="accuracy", reference_label="ground truth",
    )
    _plot_partition(
        run, in_progress, run["in_progress"],
        mode=args.mode, out_dir=out_dir,
        filename_kind="agreement", filename_suffix="_in_progress",
        label_noun="agreement", reference_label="reference (pending validation)",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
