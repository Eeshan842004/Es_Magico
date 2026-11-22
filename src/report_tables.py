"""`make report`: render the markdown tables used in REPORT.md straight from outputs/results/*.csv.

REPORT.md numbers must be copied from outputs/results/report_tables.md (never typed from memory).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "outputs" / "results"


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def pp(x: float) -> str:
    return f"{100 * x:+.1f}"


def main() -> int:
    out = []
    t = pd.read_csv(RES / "results_table.csv")
    out += ["## Main results (per-conversation failure rates, 30 conversations x 5 samples; delta = v2 - v1 in percentage points)", "",
            "| criterion | v1 fail | v2 fail | delta pp (95% CI) | Wilcoxon p | verdict |", "|---|---|---|---|---|---|"]
    for r in t.itertuples():
        out.append(f"| {r.metric} | {pct(r.v1_rate)} | {pct(r.v2_rate)} | {pp(r.delta)} ({pp(r.delta_lo)}, {pp(r.delta_hi)}) | {r.wilcoxon_p:.3f} | {r.verdict} |")
    for title, f in (("Sensitivity: judge-only vs checks-only", "sensitivity.csv"), ("Worst-of-N (conversations with >=1 failing sample)", "worst_of_n.csv"),
                     ("Flakiness (conversations whose outcome flips across samples)", "flakiness.csv"),
                     ("Must-include facts conveyed (judge)", "must_include_recall.csv"), ("Hypotheses from the prompt diff", "hypotheses.csv"),
                     ("Slice breakdown (directional; tiny n)", "slice_breakdown.csv"), ("Case-level regressions (rule 2)", "case_regressions.csv"),
                     ("Labelled subset cross-check", "labelled_subset.csv")):
        p = RES / f
        if p.exists():
            d = pd.read_csv(p)
            if f == "sensitivity.csv":
                d = d[["metric", "v1_rate", "v2_rate", "delta", "delta_lo", "delta_hi", "verdict"]].round(3)
            out += ["", f"## {title}", "", d.round(3).to_markdown(index=False) if len(d) else "(none)"]
    lp = RES / "length.csv"
    if lp.exists():
        out += ["", "## Length (words)", "", pd.read_csv(lp).to_markdown(index=False)]
    (RES / "report_tables.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {RES / 'report_tables.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
