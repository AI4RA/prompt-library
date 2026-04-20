#!/usr/bin/env python3
"""Generate award × field agreement heatmaps from a Vandalizer-crossref summary.json.

Produces two PNGs per invocation:
  - `charts/agreement_scalars_<mode>.png`  — scalar fields
  - `charts/agreement_budget_<mode>.png`   — NSF-format budget line items

Cell coloring (both heatmaps):
  - Green ramp for agreement rate when both sides emitted a value
  - Light orange when only OpenERA emitted
  - Light blue when only Vandalizer emitted
  - Gray when neither emitted

Cell text:
  - "5/5", "3/4" agreement counts when comparable
  - "OE" or "V" for one-sided
  - "—" when neither

Vandalizer is NOT ground truth. The heatmap shows *agreement*, not correctness.
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
COLOR_OE_ONLY = "#ffd4a3"             # soft orange
COLOR_VAN_ONLY = "#a8d5e2"            # soft blue
COLOR_BOTH_NULL = "#e8e8e8"           # light gray
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


# ── Matrix assembly ─────────────────────────────────────────────────────


def build_scalar_matrix(run: dict, min_coverage: int = 1):
    """Return (awards, fields, cells) where cells[i][j] is a dict with
    {'agree_rate': float|None, 'n_agree': int, 'n_compared': int,
     'kind': 'agree'|'oe_only'|'van_only'|'none'}."""
    # Fields = scalar field_rollup slots, sorted by cross-award agreement desc.
    rollup_by_field = {r["field"]: r for r in run["field_rollup"]}
    # Keep only fields with *some* comparable data across awards.
    field_names = [
        r["field"] for r in run["field_rollup"]
        if (r.get("n_compared") or 0) >= min_coverage
    ]
    # Sort fields by agreement desc, Nones last.
    def _sort_key(f):
        pct = rollup_by_field[f]["agreement_pct"]
        return (-(pct if pct is not None else -1), f)
    field_names.sort(key=_sort_key)

    awards = run["per_award"]
    # Sort awards by mean agreement across comparable fields, desc.
    def _award_score(a):
        vals = []
        for f in field_names:
            fs = a["fields"].get(f, {})
            na = fs.get("n_agree", 0)
            nd = fs.get("n_disagree", 0)
            n = na + nd
            if n:
                vals.append(na / n)
        return sum(vals) / len(vals) if vals else 0.0
    awards = sorted(awards, key=_award_score, reverse=True)

    rows, cols = len(awards), len(field_names)
    cells = [[None] * cols for _ in range(rows)]
    for i, a in enumerate(awards):
        for j, f in enumerate(field_names):
            fs = a["fields"].get(f)
            if not fs:
                cells[i][j] = {"kind": "none", "n_agree": 0, "n_compared": 0,
                               "agree_rate": None}
                continue
            n_agree = fs.get("n_agree", 0)
            n_dis = fs.get("n_disagree", 0)
            n_comp = n_agree + n_dis
            rep_vals = fs.get("openera", []) or []
            van_val = fs.get("van")
            n_reps = len(rep_vals) if rep_vals else a.get("n_replicates", 0)
            n_oe_only = sum(1 for v in rep_vals if v is not None and van_val is None)
            n_van_only = sum(1 for v in rep_vals if v is None and van_val is not None)
            if n_comp:
                cells[i][j] = {
                    "kind": "agree",
                    "n_agree": n_agree,
                    "n_compared": n_comp,
                    "agree_rate": n_agree / n_comp,
                }
            elif n_oe_only > 0 and n_van_only == 0:
                cells[i][j] = {"kind": "oe_only", "n_agree": n_oe_only,
                               "n_compared": n_reps, "agree_rate": None}
            elif n_van_only > 0 and n_oe_only == 0:
                cells[i][j] = {"kind": "van_only", "n_agree": n_van_only,
                               "n_compared": n_reps, "agree_rate": None}
            else:
                cells[i][j] = {"kind": "none", "n_agree": 0,
                               "n_compared": 0, "agree_rate": None}
    return awards, field_names, cells


def build_budget_matrix(run: dict):
    """Same cell shape as build_scalar_matrix, but for budget slots."""
    # Slots = union across awards, sorted by a stable NSF-budget order.
    rollup_by_slot = {r["slot"]: r for r in run["budget_rollup"]}
    slots = list(rollup_by_slot.keys())
    slots.sort(key=_budget_slot_order)

    awards = run["per_award"]
    def _award_score(a):
        vals = []
        for s in slots:
            bl = a["budget_lines"].get(s, {})
            n_agree = bl.get("n_agree", 0)
            n_comp = bl.get("n_compared", 0)
            if n_comp:
                vals.append(n_agree / n_comp)
        return sum(vals) / len(vals) if vals else 0.0
    awards = sorted(awards, key=_award_score, reverse=True)

    rows, cols = len(awards), len(slots)
    cells = [[None] * cols for _ in range(rows)]
    for i, a in enumerate(awards):
        for j, s in enumerate(slots):
            bl = a["budget_lines"].get(s)
            n_reps = a.get("n_replicates", 0)
            if not bl:
                cells[i][j] = {"kind": "none", "n_agree": 0,
                               "n_compared": 0, "agree_rate": None}
                continue
            n_comp = bl.get("n_compared", 0)
            n_oe = bl.get("n_oe_only", 0)
            n_van = bl.get("n_van_only", 0)
            if n_comp:
                cells[i][j] = {
                    "kind": "agree",
                    "n_agree": bl.get("n_agree", 0),
                    "n_compared": n_comp,
                    "agree_rate": bl.get("n_agree", 0) / n_comp,
                }
            elif n_oe and not n_van:
                cells[i][j] = {"kind": "oe_only", "n_agree": n_oe,
                               "n_compared": n_reps, "agree_rate": None}
            elif n_van and not n_oe:
                cells[i][j] = {"kind": "van_only", "n_agree": n_van,
                               "n_compared": n_reps, "agree_rate": None}
            else:
                cells[i][j] = {"kind": "none", "n_agree": 0,
                               "n_compared": 0, "agree_rate": None}
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
    if kind == "agree":
        return AGREE_CMAP(cell["agree_rate"])
    if kind == "oe_only":
        return COLOR_OE_ONLY
    if kind == "van_only":
        return COLOR_VAN_ONLY
    return COLOR_BOTH_NULL


def _cell_text(cell: dict) -> str:
    kind = cell["kind"]
    if kind == "agree":
        return f"{cell['n_agree']}/{cell['n_compared']}"
    if kind == "oe_only":
        return f"OE{cell['n_agree']}"
    if kind == "van_only":
        return f"V{cell['n_agree']}"
    return "—"


def _cell_text_color(cell: dict) -> str:
    if cell["kind"] == "agree" and cell["agree_rate"] < 0.4:
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
        mpatches.Patch(color=AGREE_CMAP(1.0), label="100% agree"),
        mpatches.Patch(color=AGREE_CMAP(0.6), label="partial agree"),
        mpatches.Patch(color=AGREE_CMAP(0.0), label="0% agree"),
        mpatches.Patch(color=COLOR_OE_ONLY, label="OpenERA only"),
        mpatches.Patch(color=COLOR_VAN_ONLY, label="Vandalizer only"),
        mpatches.Patch(color=COLOR_BOTH_NULL, label="neither"),
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
    matched = run["matched_awards"]
    overall_scalar = run["overall_agreement_pct"]
    overall_budget = run["budget_overall_agreement_pct"]

    # Scalars
    awards_s, fields, cells_s = build_scalar_matrix(run)
    render_heatmap(
        awards_s, fields, cells_s,
        col_label_for=lambda f: f,
        title=f"Scalar-field agreement with Vandalizer  ({args.mode})",
        subtitle=(
            f"{matched} awards matched · overall {overall_scalar:.1f}% where both systems emit a value. "
            f"Vandalizer is not ground truth — green = the two systems agreed across replicates."
        ),
        out_path=out_dir / f"agreement_scalars_{args.mode}.png",
    )

    # Budget
    awards_b, slots, cells_b = build_budget_matrix(run)
    render_heatmap(
        awards_b, slots, cells_b,
        col_label_for=lambda s: s,
        title=f"Budget-line agreement with Vandalizer  ({args.mode})",
        subtitle=(
            f"{matched} awards matched · overall {overall_budget:.1f}% where both systems emit a line. "
            f"Orange = OpenERA emitted the line but Vandalizer did not (often totals rows H/I/J/L)."
        ),
        out_path=out_dir / f"agreement_budget_{args.mode}.png",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
