"""`make check`: apply every deterministic check to every raw summary.

Output: outputs/checks.jsonl, one row per summary per check (long form, easy to audit), and a per-summary
wide table outputs/results/checks_wide.csv used by analyze.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

from checks import run_all, word_count
from golden import load_conversation, load_golden

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "outputs" / "raw" / "all.jsonl"


def load_raw(path: Path = RAW) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    if not RAW.exists():
        print("outputs/raw/all.jsonl missing: run `make generate` first")
        return 1
    gold = {g["id"]: g for g in load_golden()}
    rows, wide = [], []
    for rec in load_raw():
        conv = load_conversation(rec["conv_id"])
        results = run_all(rec["text"], conv, gold[rec["conv_id"]])
        key = {"conv_id": rec["conv_id"], "version": rec["version"], "sample_idx": rec["sample_idx"]}
        for r in results:
            rows.append({**key, **r.to_dict()})
        w = {**key, "words": word_count(rec["text"]), "slice": gold[rec["conv_id"]]["primary_slice"]}
        for r in results:
            w[r.name] = int(not r.passed)  # 1 = FAILED
        w["any_critical_fail"] = int(any((not r.passed) and r.severity == "critical" for r in results))
        wide.append(w)
    out = ROOT / "outputs" / "checks.jsonl"
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    (ROOT / "outputs" / "results").mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(wide).fillna(0)
    df.to_csv(ROOT / "outputs" / "results" / "checks_wide.csv", index=False)
    print(f"{len(rows)} check results for {len(df)} summaries -> {out}")
    fails = df.drop(columns=["conv_id", "sample_idx", "words", "slice"]).groupby("version").sum(numeric_only=True).T
    print(fails.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
