"""Load + validate the golden set, and the shared text helpers (normalising, anchors).

Run `python src/golden.py` to validate: it checks every conversation exists and that every
literal anchor / critical fact is actually grounded in the conversation text. This catches
typos in OUR expectations before they turn into fake "failures" of the summariser.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "data" / "golden_set.yaml"
CONV_DIR = ROOT / "data" / "conversations"


def load_golden() -> list[dict]:
    return yaml.safe_load(GOLDEN.read_text(encoding="utf-8"))


def load_conversation(cid: str) -> dict:
    return json.loads((CONV_DIR / f"{cid}.json").read_text(encoding="utf-8"))


def render(conv: dict) -> str:
    """Same rendering as the starter's summarise.render(): keeps the system under test unchanged."""
    lines = [f"[{conv['channel']}]"]
    for m in conv["messages"]:
        lines.append(f"{m['role'].upper()}: {m['text']}")
    return "\n".join(lines)


def conv_text(conv: dict) -> str:
    return "\n".join(m["text"] for m in conv["messages"])


def norm(s: str) -> str:
    """Lower-case; drop currency markers; remove thousands commas; collapse spaces and hyphen-likes.
    So 'Rs 1,299', '₹1299' and '1299' all compare equal."""
    s = s.lower()
    # Canonical dates: 'November 8th', 'Nov 8', '8 November', '8th of Nov' -> '8 nov' (found by the false-alarm audit:
    # the model wrote 'November 8' and our anchors only listed 'Nov 8').
    mon = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?"
    s = re.sub(rf"\b{mon}\s+(\d{{1,2}})(?:st|nd|rd|th)?\b", r"\2 \1", s)
    s = re.sub(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+(?:of\s+)?{mon}", r"\1 \2", s)
    s = re.sub(r"₹|\brs\.?|\binr\b", " ", s)
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)
    s = re.sub(r"[‐-―]", "-", s)
    return re.sub(r"\s+", " ", s).strip()


def anchor_present(anchor: str, text: str) -> bool:
    """True if ANY alternative ('a|b') of the anchor occurs in text. Pure-number anchors must not be
    part of a longer number (so '11' does not match '51110')."""
    t = norm(text)
    for alt in anchor.split("|"):
        a = norm(alt)
        if not a:
            continue
        pat = rf"(?<!\d){re.escape(a)}(?!\d)" if a.isdigit() else re.escape(a)
        if re.search(pat, t):
            return True
    return False


def main() -> int:
    gold = load_golden()
    problems = []
    ids = [g["id"] for g in gold]
    if len(ids) != len(set(ids)):
        problems.append("duplicate ids")
    for g in gold:
        conv = load_conversation(g["id"])
        text = conv_text(conv)
        for m in g["must_include"]:
            for a in m.get("literal_anchors", []):
                if not anchor_present(a, text):
                    problems.append(f"{g['id']}.{m['id']}: anchor {a!r} not found in the conversation")
        for n in g["must_not_include"]:
            for p in n.get("literal_patterns", []):
                try:
                    re.compile(p)
                except re.error as e:
                    problems.append(f"{g['id']}.{n['id']}: bad regex {p!r}: {e}")
        if not any(m["critical"] for m in g["must_include"]):
            problems.append(f"{g['id']}: no critical must_include")
    n_h = sum(1 for g in gold if g.get("reviewed_by_human"))
    print(f"{len(gold)} golden entries; {n_h} reviewed by human; {sum(1 for g in gold if g['id'].startswith('syn_'))} synthetic")
    for p in problems:
        print("PROBLEM:", p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
