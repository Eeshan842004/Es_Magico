"""Cross-judge agreement: gemini-3-pro vs gpt-oss-120b on the summaries both judged (same rubric, same prompt).

Why this exists: kie.ai credits ran out and labels may not cover all items, so the strongest available evidence
about judge reliability is whether two strong judges from DIFFERENT model families agree. Agreement between judges is
NOT the same as correctness (both can share a blind spot), so this complements, never replaces, label check
in agreement.py. Disagreements are dumped for reading: they show where the rubric is ambiguous.

Run: python src/judge_vs_judge.py   ->  outputs/results/judge_vs_judge.md (+ .csv)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from summarise import CFG
from stats_utils import bootstrap_kappa_ci, cohen_kappa

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "outputs" / "results"
CRIT = ["J1", "J2", "J3", "J4", "J5", "J6", "overall_fail"]
KEY = ["conv_id", "version", "sample_idx"]
REASON_KEY = {"J1": "J1_faithfulness", "J2": "J2_critical_completeness", "J3": "J3_current_state", "J4": "J4_next_step",
              "J5": "J5_usefulness", "J6": "J6_tone_safety"}


def load(name: str) -> pd.DataFrame:
    return pd.DataFrame([json.loads(l) for l in (ROOT / "outputs" / name).read_text(encoding="utf-8").splitlines() if l.strip()])


def main() -> int:
    a, b = load("judge.jsonl"), load("judge_gptoss.jsonl")
    m = a.merge(b, on=KEY, suffixes=("_gem", "_oss"))
    rows = []
    for c in CRIT:
        x, y = m[f"{c}_gem"].astype(int).tolist(), m[f"{c}_oss"].astype(int).tolist()
        k = cohen_kappa(x, y)
        lo, hi = bootstrap_kappa_ci(x, y, CFG["bootstrap"]["agreement_resamples"], CFG["seed"])
        rows.append({"criterion": c, "n": len(m), "gemini_fail": sum(x), "gptoss_fail": sum(y),
                     "raw_agree_pct": round(100 * np.mean(np.array(x) == np.array(y)), 1),
                     "kappa": None if np.isnan(k) else round(k, 2), "ci": "n/a" if np.isnan(lo) else f"[{lo:.2f}, {hi:.2f}]",
                     "both_fail": int(sum(i and j for i, j in zip(x, y))), "only_gemini": int(sum(i and not j for i, j in zip(x, y))),
                     "only_gptoss": int(sum(j and not i for i, j in zip(x, y)))})
    t = pd.DataFrame(rows)
    t.to_csv(RES / "judge_vs_judge.csv", index=False)
    byv = []
    for v, g in m.groupby("version"):
        byv.append({"version": v, "n": len(g), "gemini_overall_fail": round(g.overall_fail_gem.mean(), 3),
                    "gptoss_overall_fail": round(g.overall_fail_oss.mean(), 3),
                    "kappa_overall": round(cohen_kappa(g.overall_fail_gem.tolist(), g.overall_fail_oss.tolist()), 2)})
    raw = {(r["conv_id"], r["version"], r["sample_idx"]): r["text"] for r in
           (json.loads(l) for l in (ROOT / "outputs" / "raw" / "all.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())}
    dis = ["", "## Every disagreement on a blocking criterion (J1-J4, J6)", ""]
    for r in m.itertuples():
        diffs = [c for c in ("J1", "J2", "J3", "J4", "J6") if getattr(r, f"{c}_gem") != getattr(r, f"{c}_oss")]
        if not diffs:
            continue
        dis.append(f"### {r.conv_id} {r.version} s{r.sample_idx}: {', '.join(diffs)}")
        dis.append(f"Summary: {raw[(r.conv_id, r.version, r.sample_idx)]!r}")
        for c in diffs:
            ga, gb = getattr(r, "parsed_gem")[REASON_KEY[c]], getattr(r, "parsed_oss")[REASON_KEY[c]]
            dis.append(f"- {c}: gemini={ga['verdict']} ({ga['reason'][:220]}) | gpt-oss={gb['verdict']} ({gb['reason'][:220]})")
        dis.append("")
    md = ["# Judge vs judge: gemini-3-pro vs gpt-oss-120b (same rubric)", "",
          f"{len(m)} summaries judged by both. Kappa with 95% bootstrap CI (2000 resamples). FAIL = 1.", "",
          t.to_markdown(index=False), "", "## By version (does either judge treat one version differently?)", "",
          pd.DataFrame(byv).to_markdown(index=False)] + dis
    (RES / "judge_vs_judge.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:12 + len(t)]))
    print(pd.DataFrame(byv).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
