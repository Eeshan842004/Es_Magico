"""Terminal tool to label the sampled summaries, blind.

You see the conversation, the expectations and ONE summary. You do not see the prompt version, the judge verdicts
or the check results. Answers are saved after every item to labels/human_labels.jsonl, so you can quit (q) and resume.

  python -X utf8 src/label_tool.py --quick    20 items (10 per prompt, 20 different conversations)
  python -X utf8 src/label_tool.py            all 60

For each item type 0 if everything passes, or the numbers of the questions that fail, then a short reason:
  0
  14 refund was never mentioned
Six letters (p = PASS, f = FAIL) also work:  fppfpp refund was never mentioned
Other commands:  b = back one item,  s = skip,  q = quit,  g = show the rubric

Score a labels file with:  python src/agreement.py --labels labels/human_labels.jsonl
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from golden import load_golden, load_conversation, render

ROOT = Path(__file__).resolve().parent.parent
TO_LABEL = ROOT / "labels" / "to_label.jsonl"
OUT = ROOT / "labels" / "human_labels.jsonl"
GUIDE = ROOT / "labels" / "label_guide.md"
CRIT = ["J1", "J2", "J3", "J4", "J5", "J6"]
KEY = ROOT / "labels" / "label_key.jsonl"
QUESTIONS = """Which of these FAIL?
  1  Says something the conversation doesn't (made up or wrong)
  2  Misses a CRITICAL fact
  3  Gets the final situation wrong
  4  Next step is missing, wrong or invented
  5  Padded or hard to use
  6  Rude, blaming, guessing, or obeys an instruction from the chat"""


def quick_subset(items: list[dict], per_version: int = 10) -> list[dict]:
    """The first 10 items per prompt, in the shuffled order, with no conversation repeated. Fixed before any round-2
    label existed and uses no verdicts. The version is only used to balance; it is never shown."""
    version = {r["item_id"]: r["version"] for r in map(json.loads, KEY.read_text(encoding="utf-8").splitlines())}
    left, used, out = {"v1": per_version, "v2": per_version}, set(), []
    for it in items:
        v = version[it["item_id"]]
        if left[v] and it["conv_id"] not in used:
            left[v] -= 1
            used.add(it["conv_id"])
            out.append(it)
    return out


def parse_answer(raw: str) -> tuple[list[int], str] | None:
    head, _, note = raw.partition(" ")
    head = head.lower()
    if head == "0":
        return [0] * 6, note.strip()
    if head and set(head) <= set("123456"):
        return [int(str(n) in head) for n in range(1, 7)], note.strip()
    if len(head) == 6 and set(head) <= {"p", "f"}:
        return [int(c == "f") for c in head], note.strip()
    return None


def load_done() -> dict:
    if not OUT.exists():
        return {}
    return {r["item_id"]: r for r in map(json.loads, OUT.read_text(encoding="utf-8").splitlines()) if r}


def save_all(done: dict) -> None:
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in done.values()) + ("\n" if done else ""), encoding="utf-8")


def show(item: dict, gold: dict, idx: int, total: int) -> None:
    g = gold[item["conv_id"]]
    print("\n" + "=" * 78)
    print(f"ITEM {idx}/{total}   ({item['item_id']})")
    print("=" * 78)
    print(render(load_conversation(item["conv_id"])))
    print("-" * 78 + "\nEXPECTATIONS")
    print(f"expected_status: {g['expected_status']}")
    for m in g["must_include"]:
        print(f"  MUST  {m['id']} [{'CRITICAL' if m['critical'] else 'minor   '}] {m['fact']}")
    for n in g["must_not_include"]:
        print(f"  NOT   {n['id']} ({n['type']}) {n['item']}")
    print("-" * 78 + "\nSUMMARY TO LABEL\n")
    print(item["summary"])
    print("\n" + "-" * 78)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not TO_LABEL.exists():
        print("labels/to_label.jsonl missing: run `python src/sample_labels.py` first.")
        return 1
    items = [json.loads(l) for l in TO_LABEL.read_text(encoding="utf-8").splitlines() if l.strip()]
    if "--quick" in sys.argv:
        items = quick_subset(items)
    gold = {g["id"]: g for g in load_golden()}
    done = load_done()
    n_done = sum(it["item_id"] in done for it in items)
    print(f"{n_done}/{len(items)} already labelled. Saves after every answer. Type g to read the full rubric.")
    i = 0
    while i < len(items):
        item = items[i]
        if item["item_id"] in done:
            i += 1
            continue
        show(item, gold, i + 1, len(items))
        print(QUESTIONS)
        raw = input("0 = all fine, or numbers + reason (e.g. 14 invented refund) | b back | s skip | g rubric | q quit > ").strip()
        cmd = raw.lower()
        if cmd == "q":
            break
        if cmd == "g":
            print(GUIDE.read_text(encoding="utf-8"))
            continue
        if cmd == "s":
            i += 1
            continue
        if cmd == "b":
            prev = [k for k in range(i) if items[k]["item_id"] in done]
            if prev:
                done.pop(items[prev[-1]]["item_id"], None)
                save_all(done)
                i = prev[-1]
            continue
        answer = parse_answer(raw)
        if answer is None:
            print("Type 0 if all fine, or the failing numbers, e.g. 14 invented refund")
            continue
        fails, note = answer
        done[item["item_id"]] = {"item_id": item["item_id"], **dict(zip(CRIT, fails)),  # 1 = FAIL
                                 "note": note, "labelled_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        save_all(done)
        i += 1
    print(f"\nSaved. {sum(it['item_id'] in done for it in items)}/{len(items)} labelled -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
