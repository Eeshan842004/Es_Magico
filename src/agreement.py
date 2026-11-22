"""`make agree`: how far can the judge be trusted? (work plan section 10)

Reads the reference labels (labels/reference_labels.jsonl; pass --labels to use another file), the secret key
(labels/label_key.jsonl) and the judge output, then reports per criterion and for the overall verdict:
  raw agreement, Cohen's kappa + 95% bootstrap CI (2000 resamples), confusion matrix, judge recall and precision on
  FAILs (missing a real failure is the costly error for a ship gate), class balance, and a trust level taken from the
  pre-registered table in docs/ship_rule.md. Held-out items (40) are the headline; calibration items (20) are shown
  separately because the judge prompt may be tuned on them.
Also: version bias, length bias, judge self-consistency (judge_repeat.jsonl), and a disagreement dump.

Usage: python src/agreement.py [--judge outputs/judge.jsonl] [--tag judge_v1]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from golden import load_conversation, load_golden, render
from summarise import CFG
from stats_utils import bootstrap_kappa_ci, cohen_kappa, confusion, recall_precision

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "outputs" / "results"
CRITERIA = ["J1", "J2", "J3", "J4", "J5", "J6", "overall"]
BLOCKING = ["J1", "J2", "J3", "J4", "J6"]
NAMES = {"J1": "Faithfulness", "J2": "Critical completeness", "J3": "Current state", "J4": "Next step",
         "J5": "Usefulness/noise", "J6": "Tone & safety", "overall": "Overall (J1-4,J6)"}


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def trust_level(kappa: float) -> str:
    if np.isnan(kappa):
        return "undefined (no variation)"
    if kappa >= 0.61:
        return "substantial: trust for aggregate comparison"
    if kappa >= 0.41:
        return "moderate: use with caution, human-review judge FAILs"
    return "weak: do not use for decisions"


def load_joined(judge_path: Path, labels_path: Path = ROOT / "labels" / "reference_labels.jsonl") -> pd.DataFrame:
    human = pd.DataFrame(read_jsonl(labels_path))
    key = pd.DataFrame(read_jsonl(ROOT / "labels" / "label_key.jsonl"))
    judge = pd.DataFrame(read_jsonl(judge_path))
    human["overall"] = human[BLOCKING].max(axis=1)
    judge = judge.rename(columns={"overall_fail": "overall"})
    h = human.rename(columns={c: f"h_{c}" for c in CRITERIA if c in human.columns})
    j = judge[["conv_id", "version", "sample_idx"] + [c for c in CRITERIA if c in judge.columns]].rename(columns={c: f"j_{c}" for c in CRITERIA})
    df = key.merge(h, on="item_id", how="inner").merge(j, on=["conv_id", "version", "sample_idx"], how="left")
    return df


def metrics_table(df: pd.DataFrame, label: str) -> pd.DataFrame:
    rows = []
    for c in CRITERIA:
        h, j = df[f"h_{c}"].astype(int).tolist(), df[f"j_{c}"].astype(int).tolist()
        k = cohen_kappa(h, j)
        lo, hi = bootstrap_kappa_ci(h, j, CFG["bootstrap"]["agreement_resamples"], CFG["seed"])
        cm = confusion(h, j)
        rec, prec = recall_precision(cm)
        rows.append({"set": label, "criterion": c, "name": NAMES[c], "n": len(h), "label_fail": sum(h), "judge_fail": sum(j),
                     "raw_agree_pct": round(100 * np.mean(np.array(h) == np.array(j)), 1), "kappa": round(k, 3) if not np.isnan(k) else np.nan,
                     "ci_low": round(lo, 3) if not np.isnan(lo) else np.nan, "ci_high": round(hi, 3) if not np.isnan(hi) else np.nan,
                     **cm, "recall_on_label_fail": round(rec, 3) if not np.isnan(rec) else np.nan,
                     "precision_on_judge_fail": round(prec, 3) if not np.isnan(prec) else np.nan,
                     "trust": trust_level(k)})
    return pd.DataFrame(rows)


def length_bias(df: pd.DataFrame) -> str:
    raw = {(r["version"], r["conv_id"], r["sample_idx"]): len(r["text"].split()) for r in read_jsonl(ROOT / "outputs" / "raw" / "all.jsonl")}
    df = df.copy()
    df["words"] = [raw[(r.version, r.conv_id, r.sample_idx)] for r in df.itertuples()]
    out = []
    for who, col in (("label", "h_overall"), ("judge", "j_overall")):
        rho = pd.Series(df["words"]).corr(pd.Series(1 - df[col].astype(int)), method="spearman")
        out.append(f"Spearman(words, {who} PASS) = {rho:.2f}")
    return "; ".join(out) + f" (n={len(df)})"


def version_bias(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for v, g in df.groupby("version"):
        h, j = g["h_overall"].astype(int).tolist(), g["j_overall"].astype(int).tolist()
        rows.append({"version": v, "n": len(g), "label_fail_rate": round(np.mean(h), 3), "judge_fail_rate": round(np.mean(j), 3),
                     "raw_agree_pct": round(100 * np.mean(np.array(h) == np.array(j)), 1), "kappa": round(cohen_kappa(h, j), 3)})
    return pd.DataFrame(rows)


def self_consistency(first: str = "judge_gptoss.jsonl", repeat: str = "judge_gptoss_repeat.jsonl") -> str:
    p1, p2 = ROOT / "outputs" / first, ROOT / "outputs" / repeat
    if not p2.exists():
        return f"{repeat} not found (run `python src/judge.py --judge gptoss --repeat 40`)."
    a = pd.DataFrame(read_jsonl(p1)).rename(columns={"overall_fail": "overall"})
    b = pd.DataFrame(read_jsonl(p2)).rename(columns={"overall_fail": "overall"})
    m = a.merge(b, on=["conv_id", "version", "sample_idx"], suffixes=("_1", "_2"))
    lines = [f"| criterion | n | flip rate | kappa run1 vs run2 |", "|---|---|---|---|"]
    for c in CRITERIA:
        x, y = m[f"{c}_1"].astype(int).tolist(), m[f"{c}_2"].astype(int).tolist()
        flips = np.mean(np.array(x) != np.array(y))
        k = cohen_kappa(x, y)
        lines.append(f"| {c} | {len(m)} | {100 * flips:.1f}% | {'n/a' if np.isnan(k) else f'{k:.2f}'} |")
    return "\n".join(lines)


def disagreement_dump(df: pd.DataFrame, judge_path: Path, tag: str = "") -> str:
    gold = {g["id"]: g for g in load_golden()}
    raw = {(r["version"], r["conv_id"], r["sample_idx"]): r["text"] for r in read_jsonl(ROOT / "outputs" / "raw" / "all.jsonl")}
    jud = {(r["version"], r["conv_id"], r["sample_idx"]): r for r in read_jsonl(judge_path)}
    out = ["# Judge vs reference-label disagreements", "",
           "Each block = one item where the judge and the label differ on at least one criterion.",
           "The cause of each disagreement is in `labels/disagreement_causes.json`. It was decided after reading each case, and no label was changed afterwards.", ""]
    causes = json.loads((ROOT / "labels" / "disagreement_causes.json").read_text(encoding="utf-8")).get(tag, {}) if (ROOT / "labels" / "disagreement_causes.json").exists() else {}
    counts: dict[str, int] = {}
    n = 0
    for r in df.sort_values(["split", "item_id"]).itertuples():
        diffs = [c for c in CRITERIA if int(getattr(r, f"h_{c}")) != int(getattr(r, f"j_{c}"))]
        if not diffs:
            continue
        n += 1
        key = (r.version, r.conv_id, r.sample_idx)
        parsed = jud[key]["parsed"]
        out += [f"## {r.item_id} ({r.split}) conv {r.conv_id} version {r.version}: differs on {', '.join(diffs)}", "",
                "<details><summary>conversation</summary>", "", "```", render(load_conversation(r.conv_id)), "```", "</details>", "",
                f"**Summary:** {raw[key]}", ""]
        for c in diffs:
            h = "FAIL" if int(getattr(r, f"h_{c}")) else "PASS"
            j = "FAIL" if int(getattr(r, f"j_{c}")) else "PASS"
            reason = parsed.get({"J1": "J1_faithfulness", "J2": "J2_critical_completeness", "J3": "J3_current_state", "J4": "J4_next_step",
                                 "J5": "J5_usefulness", "J6": "J6_tone_safety"}.get(c, ""), {}).get("reason", "(roll-up)") if c != "overall" else "(roll-up)"
            out.append(f"- **{c}**: label={h}, judge={j}. Judge reason: {reason}")
        out.append(f"- Label note: {getattr(r, 'note', '') or '(none)'}")
        for c in diffs:
            cause = causes.get(r.item_id, {}).get(c, "not classified" if c != "overall" else "")
            if cause:
                counts[cause] = counts.get(cause, 0) + 1
                out.append(f"- cause ({c}): {cause}")
        out.append("")
    out.insert(2, f"{n} items with at least one disagreement (of {len(df)} labelled).")
    out[3:3] = ["", "| cause | count |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])]
    return "\n".join(out)


def plot_confusions(df: pd.DataFrame, path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(CRITERIA), figsize=(2.6 * len(CRITERIA), 3.0))
    for ax, c in zip(axes, CRITERIA):
        cm = confusion(df[f"h_{c}"].astype(int).tolist(), df[f"j_{c}"].astype(int).tolist())
        mat = np.array([[cm["tn"], cm["fp"]], [cm["fn"], cm["tp"]]])
        ax.imshow(mat, cmap="Blues")
        for (i, j), v in np.ndenumerate(mat):
            ax.text(j, i, str(v), ha="center", va="center", color="white" if v > mat.max() / 2 else "black")
        ax.set_xticks([0, 1], ["PASS", "FAIL"])
        ax.set_yticks([0, 1], ["PASS", "FAIL"])
        ax.set_xlabel("judge")
        ax.set_ylabel("label")
        ax.set_title(c, fontsize=10)
    fig.suptitle("Judge vs reference label (all labelled items)", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


NL = chr(10)
JUDGES = [("judge.jsonl", "gemini"), ("judge_gptoss.jsonl", "gptoss")]


def run_one(judge_path: Path, tag: str, labels_path: Path, out: Path) -> str | None:
    """Agreement report for one judge. Only labelled items that this judge actually scored are used (gemini covers a
    random 181 of 300 summaries, so it has a verdict for roughly 60% of the labelled items)."""
    df = load_joined(judge_path, labels_path)
    n_lab = len(df)
    if not n_lab:
        print("No label ids match labels/label_key.jsonl (round-2 ids are H01-H60).")
        return None
    df = df[df["j_overall"].notna()].copy()
    if df.empty:
        return None
    print(f"{tag}: {len(df)} of {n_lab} labelled items have a verdict from this judge")
    held, cal = df[df.split == "heldout"], df[df.split == "calibration"]
    empty = pd.DataFrame([{"set": "calibration", "note": "none: the judge prompt was never tuned on labels"}])
    tables = [metrics_table(held, "heldout"), metrics_table(cal, "calibration") if len(cal) else empty, metrics_table(df, "all")]
    full = pd.concat(tables)
    full.insert(0, "judge", tag)
    full.to_csv(out / f"judge_agreement_{tag}.csv", index=False)
    plot_confusions(held if len(held) else df, out / f"fig4_judge_vs_labels_{tag}.png")
    (out / f"judge_disagreements_{tag}.md").write_text(disagreement_dump(df, judge_path, tag), encoding="utf-8")
    md = [f"# Judge vs reference-label agreement: {tag}", "", f"{len(df)} of {n_lab} labelled items scored by this judge "
          f"({len(held)} held-out, {len(cal)} calibration).", "", "## Held-out set (headline)", "",
          tables[0].drop(columns=["set"]).to_markdown(index=False), "",
          "## Calibration set (the judge prompt may be tuned on this, so it is not the headline)", "",
          tables[1].drop(columns=["set"]).to_markdown(index=False), "",
          "## Version bias (overall verdict)", "", version_bias(df).to_markdown(index=False), "",
          "## Length bias", "", length_bias(df), ""]
    (out / f"judge_agreement_{tag}.md").write_text(NL.join(md), encoding="utf-8")
    return NL.join(md)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default=str(ROOT / "labels" / "reference_labels.jsonl"))
    ap.add_argument("--out", default=str(RES), help="output folder (tests point this at a temp dir)")
    a = ap.parse_args()
    labels_path, out = Path(a.labels), Path(a.out)
    if not labels_path.exists():
        print("labels/reference_labels.jsonl not found.")
        return 1
    out.mkdir(parents=True, exist_ok=True)
    for fname, tag in JUDGES:
        if (ROOT / "outputs" / fname).exists():
            md = run_one(ROOT / "outputs" / fname, tag, labels_path, out)
            if md:
                print(md)
    sc = self_consistency()
    (out / "judge_self_consistency.md").write_text("# Judge self-consistency (gpt-oss-120b, same summary judged twice)" + NL + NL + sc + NL, encoding="utf-8")
    print(sc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
