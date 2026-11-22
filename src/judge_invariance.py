"""Two checks on the gpt-oss judge, run as one small controlled experiment (60 free-tier calls).

1. Self-consistency: re-judge 40 summaries (20 v1, 20 v2) exactly as they are. Any verdict change here is pure
   judge noise. -> outputs/judge_gptoss_repeat.jsonl
2. Format invariance: take the same 20 v2 summaries, remove ONLY the 'Issue:/Status:/Next step:' labels and line
   breaks (the words stay identical) and judge them again. If the judge were punishing v2's layout rather than its
   content, verdicts would change here more than they do in check 1. -> outputs/judge_invariance.jsonl

Run (after judge.py --judge gptoss):  python src/judge_invariance.py   ->  outputs/results/judge_invariance.md
"""
from __future__ import annotations

import json
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from golden import load_conversation, load_golden
from judge import ROOT, judge_one, system_prompt
from llm_client import LLMError
from stats_utils import cohen_kappa
from summarise import CFG

OUT = ROOT / "outputs"
CRIT = ["J1", "J2", "J3", "J4", "J5", "J6", "overall_fail"]
LABEL = re.compile(r"^\s*(issue|status)\s*:\s*", re.I)


def to_paragraph(text: str) -> str:
    """'Issue: A\\nStatus: B\\nNext step: C' -> 'A. B. Next step: C.' One paragraph, same words. The content-free
    'Issue:'/'Status:' headings and the line breaks go; 'Next step:' stays inline because it carries meaning
    (without it, 'None; monitor.' would become ambiguous and confound the test)."""
    parts = [LABEL.sub("", ln).strip().rstrip(".") for ln in text.splitlines() if ln.strip()]
    return ". ".join(p for p in parts if p) + "."


def read(name: str) -> list[dict]:
    return [json.loads(l) for l in (OUT / name).read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20, help="summaries per version (shrink to fit a free-tier quota)")
    ap.add_argument("--v2-only", action="store_true", help="skip the v1 self-consistency part; the format test needs only v2")
    a = ap.parse_args()
    jcfg = {"name": "gptoss", **CFG["judges"]["gptoss"]}
    sysp = system_prompt(ROOT / "prompts" / "judge.txt")
    gold = {g["id"]: g for g in load_golden()}
    raw = {(r["conv_id"], r["version"], r["sample_idx"]): r for r in read("raw/all.jsonl")}
    first = {(r["conv_id"], r["version"], r["sample_idx"]): r for r in read("judge_gptoss.jsonl")}
    rng = random.Random(CFG["seed"] + 7)
    # same seed, so a smaller --n is a prefix of the larger sample and earlier cached calls are reused
    pick = {v: rng.sample(sorted(k for k in first if k[1] == v), 20)[:a.n] for v in ("v1", "v2")}
    if a.v2_only:
        pick["v1"] = []
    jobs = [("repeat", raw[k]) for v in pick for k in pick[v]]
    jobs += [("reformat", {**raw[k], "text": to_paragraph(raw[k]["text"])}) for k in pick["v2"]]

    def run(job):
        tag, rec = job
        return tag, rec["text"], judge_one(rec, load_conversation(rec["conv_id"]), gold[rec["conv_id"]], sysp,
                                           "run2" if tag == "repeat" else "invariance", jcfg)

    results, failed = [], 0
    with ThreadPoolExecutor(max_workers=jcfg["concurrency"]) as ex:
        for fut in [ex.submit(run, j) for j in jobs]:
            try:
                results.append(fut.result())
            except LLMError as e:
                failed += 1
                print("failed:", str(e)[:100])
    if failed:  # never write half an experiment: finished calls are cached, so a re-run only pays for the missing ones
        print(f"{failed} of {len(jobs)} calls failed (usually the Groq quota). Nothing written; re-run later.")
        return 1
    rep = [r for t, _, r in results if t == "repeat"]
    inv = [{**r, "reformatted_text": txt} for t, txt, r in results if t == "reformat"]
    (OUT / "judge_gptoss_repeat.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rep) + "\n", encoding="utf-8")
    (OUT / "judge_invariance.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in inv) + "\n", encoding="utf-8")

    def compare(pairs, title):
        lines = [f"### {title} (n={len(pairs)})", "", "| criterion | FAIL rate before | FAIL rate after | verdict flips | kappa |", "|---|---|---|---|---|"]
        for c in CRIT:
            a = [first[(r["conv_id"], r["version"], r["sample_idx"])][c] for r in pairs]
            b = [r[c] for r in pairs]
            k = cohen_kappa(a, b)
            lines.append(f"| {c} | {np.mean(a):.2f} | {np.mean(b):.2f} | {sum(x != y for x, y in zip(a, b))} ({100 * np.mean(np.array(a) != np.array(b)):.0f}%) | "
                         f"{'n/a' if np.isnan(k) else f'{k:.2f}'} |")
        return lines + [""]

    rep_v2 = [r for r in rep if r["version"] == "v2"]
    md = ["# gpt-oss judge: self-consistency and format invariance", "",
          "'Before' is the first judgement of each summary (outputs/judge_gptoss.jsonl).", ""]
    md += compare(rep, "Self-consistency: the same summary judged again, unchanged (judge noise), " + " + ".join(sorted({r['version'] for r in rep})))
    md += compare(rep_v2, "Self-consistency, v2 only (the noise baseline for the test below)")
    md += compare(inv, "Format invariance: the same v2 summaries with labels and line breaks removed")
    md += ["Reading: if the flips in the format test are about the same as the v2 noise baseline, the judge is grading "
           "content, not layout. If FAIL rates drop a lot once the labels are removed, the judge was penalising v2's format.",
           "", f"Calls failed: {failed}."]
    (ROOT / "outputs" / "results" / "judge_invariance.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
