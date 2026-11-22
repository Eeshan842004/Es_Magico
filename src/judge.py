"""`make judge`: LLM-as-judge over every raw summary (work plan section 9).

Design (all on purpose):
  - BINARY criteria J1-J6 with written anchors (labels/label_guide.md, the same text a labeller uses).
  - Reference-guided: the judge sees the conversation + our golden expectations, so "is it good?" becomes
    "is M2 conveyed?".
  - Evidence before verdict: in the JSON schema each `reason` comes before its `verdict`.
  - BLIND: the judge never sees the prompt version. Calls are made in a seeded shuffled order.
  - One strict-JSON-schema call per summary (budget). Tolerant parse + one retry as a fallback.
  - `overall` is recomputed in code from J1-J4 + J6 (we do not trust the model's own roll-up).

Usage:
  python src/judge.py                          # judge all raw summaries -> outputs/judge.jsonl
  python src/judge.py --repeat 60              # self-consistency: re-judge 60 random summaries -> judge_repeat.jsonl
  python src/judge.py --prompt prompts/judge_v2.txt --out outputs/judge_v2.jsonl   # a revised judge prompt
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

from golden import load_conversation, load_golden, render
from llm_client import LLMError, chat
from summarise import CFG

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "outputs" / "raw" / "all.jsonl"
RUBRIC = ROOT / "labels" / "label_guide.md"
CRITERIA = ["J1", "J2", "J3", "J4", "J5", "J6"]
BLOCKING = ["J1", "J2", "J3", "J4", "J6"]  # overall PASS needs all of these


def _crit_obj():
    return {"type": "object", "properties": {"reason": {"type": "string"}, "verdict": {"type": "string", "enum": ["PASS", "FAIL"]}},
            "required": ["reason", "verdict"], "additionalProperties": False}


SCHEMA = {"type": "json_schema", "json_schema": {"name": "handoff_judgement", "strict": True, "schema": {
    "type": "object",
    "properties": {
        "unsupported_claims": {"type": "array", "items": {"type": "string"}},
        "J1_faithfulness": _crit_obj(),
        "must_include_check": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "present": {"type": "string", "enum": ["yes", "partial", "no"]},
            "evidence": {"type": "string"}}, "required": ["id", "present", "evidence"], "additionalProperties": False}},
        "J2_critical_completeness": _crit_obj(),
        "J3_current_state": _crit_obj(),
        "J4_next_step": _crit_obj(),
        "J5_usefulness": _crit_obj(),
        "J6_tone_safety": _crit_obj(),
        "overall": {"type": "string", "enum": ["PASS", "FAIL"]},
        "holistic_score_1_5": {"type": "integer"},
    },
    "required": ["unsupported_claims", "J1_faithfulness", "must_include_check", "J2_critical_completeness", "J3_current_state",
                 "J4_next_step", "J5_usefulness", "J6_tone_safety", "overall", "holistic_score_1_5"],
    "additionalProperties": False}}}

KEYS = {"J1": "J1_faithfulness", "J2": "J2_critical_completeness", "J3": "J3_current_state",
        "J4": "J4_next_step", "J5": "J5_usefulness", "J6": "J6_tone_safety"}


def system_prompt(prompt_path: Path) -> str:
    return prompt_path.read_text(encoding="utf-8").replace("{{RUBRIC}}", RUBRIC.read_text(encoding="utf-8")).strip()


def expectations_text(g: dict) -> str:
    lines = [f"expected_status: {g['expected_status']}", "must_include:"]
    for m in g["must_include"]:
        lines.append(f"  - {m['id']} [{'CRITICAL' if m['critical'] else 'non-critical'}] {m['fact']}")
    lines.append("must_not_include:")
    for n in g["must_not_include"]:
        lines.append(f"  - {n['id']} ({n['type']}) {n['item']}")
    if g.get("notes"):
        lines.append(f"notes: {g['notes']}")
    return "\n".join(lines)


def user_message(conv: dict, g: dict, summary: str) -> str:
    return (f"## CONVERSATION\n{render(conv)}\n\n## EXPECTATIONS (written by the evaluation team)\n{expectations_text(g)}\n\n"
            f"## SUMMARY TO EVALUATE\n{summary}\n")


def parse_json(text: str) -> dict:
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    return json.loads(t)


def flatten(parsed: dict) -> dict:
    flat = {c: int(parsed[KEYS[c]]["verdict"] == "FAIL") for c in CRITERIA}  # 1 = FAIL
    flat["overall_fail"] = int(any(flat[c] for c in BLOCKING))
    flat["overall_model_says_fail"] = int(parsed.get("overall") == "FAIL")
    flat["holistic"] = parsed.get("holistic_score_1_5")
    flat["n_unsupported"] = len(parsed.get("unsupported_claims", []))
    return flat


def judge_one(rec: dict, conv: dict, g: dict, sys_prompt: str, run_tag: str, jcfg: dict) -> dict:
    msgs = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_message(conv, g, rec["text"])}]
    for attempt in range(2):  # one retry on a malformed JSON body
        extra = f"judge|{run_tag}|{rec['conv_id']}|{rec['version']}|s{rec['sample_idx']}|a{attempt}"
        try:
            r = chat(jcfg["model"], msgs, backend=jcfg["backend"], reasoning_effort=jcfg["reasoning_effort"], response_format=SCHEMA,
                     temperature=jcfg.get("temperature"), cache_key_extra=extra, purpose=f"judge:{jcfg['name']}",
                     retries=jcfg.get("retries", CFG["retries"]), timeout=300)
        except LLMError as e:
            # Groq's strict-schema mode returns HTTP 400 when the model's JSON doesn't validate. That is the same
            # problem as a malformed body, so it gets the same single retry (a fresh sample usually validates).
            if attempt == 0 and "expected schema" in str(e):
                continue
            raise
        try:
            parsed = parse_json(r["text"])
            flat = flatten(parsed)
            break
        except (json.JSONDecodeError, KeyError, TypeError):
            if attempt == 1:
                raise LLMError(f"unparseable judge output for {rec['conv_id']} {rec['version']} s{rec['sample_idx']}")
    return {"conv_id": rec["conv_id"], "version": rec["version"], "sample_idx": rec["sample_idx"], "run": run_tag, "judge": jcfg["name"],
            **flat, "parsed": parsed, "credits": r["credits"], "usage": r["usage"]}  # no 'cached' flag: it is run-time trivia and would make rebuilds differ (the cost log records real calls)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", default=str(ROOT / "prompts" / "judge.txt"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--repeat", type=int, default=0, help="self-consistency: re-judge N random summaries")
    ap.add_argument("--labelled-first", action="store_true", help="judge the labelled sample first (only changes the order)")
    ap.add_argument("--judge", default="gemini", choices=sorted(CFG["judges"]), help="which judge config in config.yaml")
    a = ap.parse_args()
    jcfg = {"name": a.judge, **CFG["judges"][a.judge]}

    prompt_path = Path(a.prompt)
    sys_prompt = system_prompt(prompt_path)
    psha = hashlib.sha256(sys_prompt.encode("utf-8")).hexdigest()[:12]
    gold = {g["id"]: g for g in load_golden()}
    convs = {cid: load_conversation(cid) for cid in gold}
    recs = [json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip()]
    rng = random.Random(CFG["seed"])
    rng.shuffle(recs)  # blind + order-independent
    if a.labelled_first:  # stable: labelled items first, the rest keep their seeded random order
        lab = {(k["conv_id"], k["version"], k["sample_idx"]) for k in map(json.loads, (ROOT / "labels" / "label_key.jsonl").read_text(encoding="utf-8").splitlines()) if k}
        recs.sort(key=lambda r: (r["conv_id"], r["version"], r["sample_idx"]) not in lab)
    run_tag = "run1"
    out = Path(a.out) if a.out else ROOT / "outputs" / jcfg["out"]
    if a.repeat:
        recs = random.Random(CFG["seed"] + 1).sample(recs, a.repeat)
        run_tag = "run2"
        out = ROOT / "outputs" / jcfg["out"].replace(".jsonl", "_repeat.jsonl")
    print(f"judging {len(recs)} summaries with judge={a.judge} ({jcfg['model']}), prompt {prompt_path.name} (sha {psha}), run={run_tag}")

    results, failures = [], []
    with ThreadPoolExecutor(max_workers=jcfg.get("concurrency", CFG["concurrency"])) as ex:
        futs = {ex.submit(judge_one, r, convs[r["conv_id"]], gold[r["conv_id"]], sys_prompt, run_tag, jcfg): r for r in recs}
        for f in tqdm(as_completed(futs), total=len(futs)):
            try:
                results.append({**f.result(), "judge_prompt_sha": psha})
            except LLMError as e:
                r = futs[f]
                failures.append((r["conv_id"], r["version"], r["sample_idx"], str(e)))
    results.sort(key=lambda r: (r["version"], r["conv_id"], r["sample_idx"]))
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n", encoding="utf-8")
    print(f"saved {len(results)} judgements -> {out}")
    if failures:
        print(f"{len(failures)} FAILED (re-run; finished calls are cached):", failures[:5])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
