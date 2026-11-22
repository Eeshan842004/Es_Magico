"""Choose the 60 summaries to label (seeded, so the sample can be rebuilt exactly).

The sample:
  - excludes the summaries listed in labels/excluded_from_sample.jsonl (an earlier sample whose labels were dropped);
  - has one summary per (conversation, version): 60 items, every case and both prompts;
  - draws only from summaries both judges scored, so each judge is compared on all 60. Only WHETHER a judge scored
    a summary is used here, never what the verdict was;
  - is all held-out: the judge prompt was never tuned on labels, so no calibration split is needed;
  - uses ids H01-H60.
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

from summarise import CFG

ROOT = Path(__file__).resolve().parent.parent
LABELS = ROOT / "labels"
KEY = ("conv_id", "version", "sample_idx")


def read(rel: str) -> list[dict]:
    return [json.loads(l) for l in (ROOT / rel).read_text(encoding="utf-8").splitlines() if l.strip()]


def keys(rel: str) -> set[tuple]:
    return {tuple(r[c] for c in KEY) for r in read(rel)}


def main() -> int:
    if (LABELS / "reference_labels.jsonl").exists() and "--force" not in sys.argv:
        print("labels/reference_labels.jsonl exists: refusing to re-sample (it would invalidate the labels). Use --force to override.")
        return 0
    seed = CFG["labelling"]["round2_seed"]
    rng = random.Random(seed)
    raw = {tuple(r[c] for c in KEY): r["text"] for r in read("outputs/raw/all.jsonl")}
    pool = (keys("outputs/judge.jsonl") & keys("outputs/judge_gptoss.jsonl")) - keys("labels/excluded_from_sample.jsonl")
    cells = sorted({k[:2] for k in raw})
    picks = [rng.choice(sorted(k for k in pool if k[:2] == cell)) for cell in cells]
    rng.shuffle(picks)

    items, key = [], []
    for n, k in enumerate(picks, 1):
        items.append({"item_id": f"H{n:02d}", "conv_id": k[0], "summary": raw[k]})  # no version here
        key.append({"item_id": f"H{n:02d}", **dict(zip(KEY, k)), "split": "heldout"})
    for name, rows in (("to_label.jsonl", items), ("label_key.jsonl", key)):
        (LABELS / name).write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    report = ["# Label sample", "",
              f"- seed {seed}; {len(picks)} items; per version {dict(sorted(Counter(k[1] for k in picks).items()))}",
              f"- drawn from {len(pool)} summaries scored by both judges and absent from the excluded earlier sample",
              "- all held-out; one per conversation and version; order shuffled; version label hidden",
              "- quick option, fixed before any round-2 label existed: 20 of these (10 per prompt, 20 conversations), "
              "`python -X utf8 src/label_tool.py --quick`",
              "- v2's layout is recognisable, so blinding to version is imperfect"]
    (LABELS / "sampling_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
