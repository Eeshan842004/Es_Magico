"""Sort every judge-vs-judge disagreement into a cause: where can each judge not be trusted?

The exceptions below come from going through each disagreement and the failing judge's reason. The rest follow the
criterion's default. It is a triage of causes, not ground truth about which judge is right.
Run: python src/judge_disagreements.py  ->  outputs/results/judge_disagreement_causes.md
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEYS = {"J1": "J1_faithfulness", "J2": "J2_critical_completeness", "J3": "J3_current_state", "J4": "J4_next_step", "J6": "J6_tone_safety"}

MISSED = "Gemini too lenient: missed a real problem"
WRONG = "gpt-oss wrong: the claim is supported"
SCOPE = "gpt-oss out of scope: graded PII under J6"
GOLDEN = "Golden expectation flawed (T38 status)"
COMPOUND = "Rubric ambiguous: part of a compound fact missing"
INFER = "Rubric ambiguous: implied step or inference"

EXCEPTIONS = {
    MISSED: """T23 v1 2 J2; T23 v1 4 J2; T23 v2 2 J2; T29 v1 1 J2; T29 v2 2 J2; T37 v2 0 J1; T37 v2 0 J2; T37 v2 0 J3;
               T39 v2 0 J2""",
    WRONG: """T03 v1 2 J1; T07 v1 4 J4; T08 v1 4 J1; T09 v1 2 J1; T09 v1 2 J2; T09 v1 2 J4; T35 v1 0 J1; T36 v1 3 J1;
              T39 v2 0 J1; T39 v2 3 J1; syn_01 v2 0 J1""",
    SCOPE: "T03 v2 2 J6; T03 v2 4 J6; T04 v1 0 J6; T04 v2 0 J6; T04 v2 1 J6",
}


def read(name: str) -> dict:
    rows = [json.loads(l) for l in (ROOT / "outputs" / name).read_text(encoding="utf-8").splitlines() if l.strip()]
    return {(r["conv_id"], r["version"], r["sample_idx"]): r for r in rows}


def main() -> int:
    listed = {tuple(x.split()): cause for cause, text in EXCEPTIONS.items() for x in text.split(";")}
    gem, oss = read("judge.jsonl"), read("judge_gptoss.jsonl")
    rows, counts = [], Counter()
    for k in sorted(set(gem) & set(oss)):
        for c, field in KEYS.items():
            if gem[k][c] == oss[k][c]:
                continue
            cause = listed.get((k[0], k[1], str(k[2]), c))
            if not cause:
                cause = GOLDEN if k[0] == "T38" and c in ("J3", "J4") else COMPOUND if c == "J2" else INFER
            counts[cause] += 1
            who, rec = ("Gemini", gem[k]) if gem[k][c] else ("gpt-oss", oss[k])
            reason = " ".join(rec["parsed"][field]["reason"].split()).replace("|", "/")
            rows.append(f"| {k[0]} {k[1]} run {k[2]} | {c} | {who} | {cause} | {reason} |")
    md = ["# Where the two judges disagree, and why", "",
          f"{len(rows)} criterion-level disagreements on {len(set(gem) & set(oss))} shared summaries.", "",
          "| cause | count |", "|---|---|"] + [f"| {c} | {n} |" for c, n in counts.most_common()]
    md += ["", "| summary | criterion | failed by | cause | that judge's reason |", "|---|---|---|---|---|"] + rows
    (ROOT / "outputs" / "results" / "judge_disagreement_causes.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:6 + len(counts)]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
