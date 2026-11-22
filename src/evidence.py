"""Judge-free counts behind the examples in REPORT.md, over all 5 runs of each prompt.

These cases were chosen AFTER reading failures, so they illustrate failure modes; they are not an unbiased rate.
Run: python src/evidence.py  ->  outputs/results/example_counts.csv
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CASES = [
    ("T27", "adds a refund nobody mentioned", r"refund"),
    ("T07", "says the photo was verified; the agent never said so", r"verified"),
    ("T30", "calls the promise unauthorised; nobody said so", r"unauthori[sz]"),
    ("T39", "keeps the commitment to arrange the replacement", r"arrang|dispatch|ship|send"),
    ("T29", "keeps the 'no guarantee' condition", r"guarantee"),
    ("T23", "keeps 'away from flammable items'", r"flammab"),
    ("T23", "mentions safety", r"safety"),
]


def main() -> int:
    raw = [json.loads(l) for l in (ROOT / "outputs" / "raw" / "all.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = []
    for cid, what, pattern in CASES:
        row = {"conv_id": cid, "what": what, "pattern": pattern, "runs": 5}
        for v in ("v1", "v2"):
            row[v] = sum(bool(re.search(pattern, r["text"], re.I)) for r in raw if (r["conv_id"], r["version"]) == (cid, v))
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "outputs" / "results" / "example_counts.csv", index=False)
    print(df.to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
