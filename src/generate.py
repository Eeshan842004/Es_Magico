"""`make generate`: golden set x {v1, v2} x N samples -> outputs/raw/.

Non-determinism design (work plan section 7):
  - N samples per (conversation, version) at the PRODUCTION temperature; we do not set temperature to 0.
  - Identical model/params/code for v1 and v2.
  - The call order is shuffled (seeded) so v1 and v2 are interleaved and provider drift over time cannot
    systematically favour one version.
  - Every summary is saved as its own file AND appended to outputs/raw/all.jsonl with model, params,
    timestamp, usage and credits, so every number in the report traces to a raw record.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

from golden import load_conversation, load_golden
from llm_client import LLMError
from summarise import CFG, gen_settings, prompt_sha, summarise

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "outputs" / "raw"
VERSIONS = ["v1", "v2"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--versions", nargs="+", default=VERSIONS, help="prompt versions (prompts/summariser_<v>.txt)")
    ap.add_argument("--raw-dir", default=str(RAW), help="where to write; use a new dir for v3 so v1/v2 evidence is untouched")
    a = ap.parse_args()
    versions, raw_dir = a.versions, Path(a.raw_dir)
    n = CFG["n_samples"]
    gold = load_golden()
    convs = {g["id"]: load_conversation(g["id"]) for g in gold}
    jobs = [(cid, v, k) for cid in convs for v in versions for k in range(n)]
    random.Random(CFG["seed"]).shuffle(jobs)
    print(f"{len(jobs)} generation jobs ({len(convs)} conversations x {len(versions)} versions x {n} samples)")

    shas = {v: prompt_sha(v) for v in versions}
    records, failures = [], []

    def run(job):
        cid, v, k = job
        out = summarise(convs[cid], v, k)
        return {"conv_id": cid, "version": v, "sample_idx": k, "text": out["text"], "model": out["settings"]["model"],
                "params": out["settings"], "prompt_sha": shas[v], "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "usage": out["usage"], "credits": out["credits"], "latency_ms": out["latency_ms"],
                "cached": out["cached"]}

    with ThreadPoolExecutor(max_workers=CFG["concurrency"]) as ex:
        futs = {ex.submit(run, j): j for j in jobs}
        for f in tqdm(as_completed(futs), total=len(futs)):
            try:
                records.append(f.result())
            except LLMError as e:  # fail loudly: report, do not invent
                failures.append((futs[f], str(e)))

    # Keep the ORIGINAL record (its timestamp and 'cached' flag are audit evidence) when a re-run, served from the
    # cache, produced the same text. Only genuinely new or changed outputs are written.
    for i, r in enumerate(records):
        old = raw_dir / r["version"] / f"{r['conv_id']}__s{r['sample_idx']}.json"
        if old.exists():
            prev = json.loads(old.read_text(encoding="utf-8"))
            if prev.get("text") == r["text"]:
                records[i] = prev
    records.sort(key=lambda r: (r["version"], r["conv_id"], r["sample_idx"]))
    for r in records:
        d = raw_dir / r["version"]
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{r['conv_id']}__s{r['sample_idx']}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    raw_dir.mkdir(parents=True, exist_ok=True)
    with (raw_dir / "all.jsonl").open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"saved {len(records)} summaries; settings = {gen_settings()}")
    if failures:
        print(f"{len(failures)} FAILED jobs (re-run `make generate`; completed calls are cached):")
        for j, e in failures[:10]:
            print("  ", j, e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
