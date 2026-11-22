"""Does the verdict survive if OUR golden set is wrong where we suspect it is?

While reading the judge's failures we found expectations we now consider contestable (see NOTES.md):
  T38  expected_status 'resolved' -- the refund had been agreed but not yet processed, so 'open' is defensible.
  T17  M1 demands the purchase date and the 28 Oct posting date as CRITICAL -- probably over-strict.
  T15  M2 demands the amount of a refund that was RETRACTED as critical -- probably over-strict.
  T22  M1 demands the word 'third' (complaint count) as critical -- borderline.
We do not edit the golden set after seeing results (that would be tuning the test to the answer). Instead we re-run
the key comparisons with these four conversations removed and report both.
Run after analyze.py:  python src/sensitivity_golden.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from analyze import compare

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "outputs" / "results"
CONTESTABLE = ["T38", "T17", "T15", "T22"]
COLS = [("faithfulness_fail", "Faithfulness fail (J1 or C8)"), ("completeness_fail", "Critical completeness fail (J2 or C7)"),
        ("critical_any", "ANY critical failure"), ("J3", "Wrong current state (J3)"), ("J4", "No actionable next step (J4)"),
        ("judge_overall_fail", "Judge overall FAIL")]


def main() -> int:
    rows = []
    for suffix, judge in (("", "gemini-3-pro"), ("_gptoss", "gpt-oss-120b")):
        p = RES / f"per_summary{suffix}.csv"
        if not p.exists():
            continue
        df = pd.read_csv(p)
        for subset, d in (("all 30", df), (f"without {','.join(CONTESTABLE)}", df[~df.conv_id.isin(CONTESTABLE)])):
            for col, label in COLS:
                r = compare(d, col, label)
                rows.append({"judge": judge, "subset": subset, "metric": label, "v1": round(r["v1_rate"], 3), "v2": round(r["v2_rate"], 3),
                             "delta_pp": round(100 * r["delta"], 1), "ci_pp": f"[{100 * r['delta_lo']:+.1f}, {100 * r['delta_hi']:+.1f}]",
                             "n_convs": r["n_conversations"], "verdict": r["verdict"]})
    out = pd.DataFrame(rows)
    out.to_csv(RES / "sensitivity_golden.csv", index=False)
    print(out.to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
