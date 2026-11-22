"""Is the v1 -> v2 regression carried by a few conversations, and does it survive multiple-comparison correction?

Three cheap checks on the per-conversation failure rates written by analyze.py (both judges):
  1. Sign test: in how many conversations is v2 worse, better, or tied? (exact binomial on non-ties)
  2. Leave-one-conversation-out: drop each conversation in turn; report the smallest and largest delta. If one
     conversation drives the result, this range will cross zero.
  3. Holm-Bonferroni on the Wilcoxon p-values of the four pre-registered critical criteria (we test four things,
     so an uncorrected p < 0.05 is easier to get by chance than it looks).
Run after analyze.py:  python src/robustness.py  ->  outputs/results/robustness.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "outputs" / "results"
CRITICAL = [("faithfulness_fail", "Faithfulness"), ("completeness_fail", "Critical completeness"),
            ("pii_fail", "PII"), ("injection_fail", "Injection")]
HEADLINE = [("critical_any", "Any critical failure"), ("judge_overall_fail", "Judge overall FAIL")] + CRITICAL[:2]


def per_conv(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df.pivot_table(index="conv_id", columns="version", values=col, aggfunc="mean").dropna()


def holm(pvals: list[float]) -> list[float]:
    """Holm step-down adjusted p-values (monotone, capped at 1)."""
    order = np.argsort(pvals)
    m, adj, running = len(pvals), [0.0] * len(pvals), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i]))
        adj[i] = running
    return adj


def analyse(suffix: str, label: str) -> list[str]:
    df = pd.read_csv(RES / f"per_summary{suffix}.csv")
    out = [f"## Judge: {label}", "", "| metric | convs | v2 worse | v2 better | tied | sign-test p | leave-one-out delta range (pp) |",
           "|---|---|---|---|---|---|---|"]
    for col, name in HEADLINE:
        r = per_conv(df, col)
        d = (r["v2"] - r["v1"]).values
        worse, better = int((d > 0).sum()), int((d < 0).sum())
        p = stats.binomtest(worse, worse + better, 0.5).pvalue if worse + better else 1.0
        loo = [np.delete(d, i).mean() for i in range(len(d))]
        out.append(f"| {name} | {len(d)} | {worse} | {better} | {len(d) - worse - better} | {p:.3f} | "
                   f"{100 * min(loo):+.1f} to {100 * max(loo):+.1f} |")
    raw_p = []
    for col, _ in CRITICAL:
        d = (lambda r: (r["v2"] - r["v1"]).values)(per_conv(df, col))
        raw_p.append(float(stats.wilcoxon(d).pvalue) if np.any(d != 0) else 1.0)
    adj = holm(raw_p)
    out += ["", "Holm-adjusted Wilcoxon p, four pre-registered critical criteria:", "", "| criterion | raw p | Holm-adjusted p |", "|---|---|---|"]
    out += [f"| {name} | {p:.4f} | {a:.4f} |" for (col, name), p, a in zip(CRITICAL, raw_p, adj)]

    # Pooled (sample-weighted) rates: the main analysis weights every conversation equally even when it has 1 judged
    # sample and another has 5. Pooling all judged samples is the other reasonable weighting; both should agree.
    j = df.dropna(subset=["critical_any"])
    pooled = j.groupby("version")["critical_any"].agg(["mean", "size"])
    out += ["", f"Pooled any-critical failure rate over all judged samples: v1 {pooled.loc['v1', 'mean']:.1%} "
            f"(n={int(pooled.loc['v1', 'size'])}), v2 {pooled.loc['v2', 'mean']:.1%} (n={int(pooled.loc['v2', 'size'])})."]

    # Length bias WITHIN a version: if the judge rewarded longer text, longer summaries would fail less often.
    # v2 is much shorter than v1, so such a bias would inflate v2's failure rate.
    out += ["", "Length association inside each version (Spearman rho between word count and judge overall FAIL; "
            "a negative rho would mean longer summaries are passed more often; harder conversations also get longer summaries, so this is an association and cannot isolate a bias):", ""]
    for v, g in j.groupby("version"):
        rho, p = stats.spearmanr(g["words"], g["judge_overall_fail"])
        out.append(f"- {v}: rho = {rho:+.2f} (p = {p:.2f}, n = {len(g)}; words {int(g.words.min())}-{int(g.words.max())})")
    return out + [""]


def main() -> int:
    md = ["# Robustness of the v1 vs v2 result", "",
          "Unit = conversation. 'v2 worse' = the conversation's v2 failure rate is higher than its v1 rate.", ""]
    for suffix, label in (("", "gemini-3-pro"), ("_gptoss", "gpt-oss-120b")):
        if (RES / f"per_summary{suffix}.csv").exists():
            md += analyse(suffix, label)
    (RES / "robustness.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
