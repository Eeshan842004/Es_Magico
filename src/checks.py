"""Deterministic checks: pure functions, no API, no randomness.

Every check returns a CheckResult and cites where its rule comes from:
  spec:R2          -> a rule in the product owner's README (docs/spec_rules.md)
  gap:G1           -> a decision we made where the spec is silent (docs/spec_gaps.md)
  golden:<id>.<mi> -> an expectation in data/golden_set.yaml
Severity: critical (customer harm / safety / wrong facts), major (spec violation), minor (style, heuristic).

Design bias: precision over recall. A check that cries wolf teaches people to ignore it, so the
regexes are conservative and each one is unit-tested (tests/test_checks.py) and later audited on real
outputs (see NOTES.md "Check precision").
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from pathlib import Path

import yaml

from golden import anchor_present, conv_text, norm

# ---- thresholds (spec_gaps.md G1), read from config.yaml. Fixed BEFORE any golden-set output existed. ----
_CFG = yaml.safe_load((Path(__file__).resolve().parent.parent / "config.yaml").read_text(encoding="utf-8"))
SOFT_WORDS = _CFG["checks"]["soft_words"]
HARD_WORDS = _CFG["checks"]["hard_words"]


@dataclass
class CheckResult:
    name: str
    passed: bool
    severity: str  # critical | major | minor | info
    detail: str
    source: str

    def to_dict(self) -> dict:
        return asdict(self)


def _ok(name, sev, src, detail="") -> CheckResult:
    return CheckResult(name, True, sev, detail, src)


def _bad(name, sev, src, detail) -> CheckResult:
    return CheckResult(name, False, sev, detail, src)


def word_count(s: str) -> int:
    return len(s.split())


# ------------------------------------------------------------------ C1
REFUSAL = re.compile(r"\b(i cannot|i can'?t (help|summar)|as an ai|i'?m unable to|i am unable to|cannot summari[sz]e)\b", re.I)


def check_c1_nonempty(summary, conv=None, golden=None) -> CheckResult:
    """Non-empty and not a refusal. Source: gap:G13."""
    if len(summary.split()) < 3:
        return _bad("C1_nonempty_not_refusal", "critical", "gap:G13", f"only {len(summary.split())} words")
    if REFUSAL.search(summary):
        return _bad("C1_nonempty_not_refusal", "critical", "gap:G13", "refusal phrase found")
    return _ok("C1_nonempty_not_refusal", "critical", "gap:G13")


# ------------------------------------------------------------------ C2
BULLET = re.compile(r"^\s*([-*•]|\d+[.)])\s+", re.M)
HEADING = re.compile(r"^\s*#{1,6}\s", re.M)
LABEL_LINE = re.compile(r"^\s*(issue|status|next step|summary|customer request|what has been done)\s*:", re.I | re.M)


def check_c2_format(summary, conv=None, golden=None) -> CheckResult:
    """Spec R2: single short paragraph, no lists, headings or markdown. Major."""
    problems = []
    lines = [l for l in summary.splitlines() if l.strip()]
    if len(lines) > 1:
        problems.append(f"{len(lines)} lines (not one paragraph)")
    if BULLET.search(summary):
        problems.append("bullet/numbered list")
    if HEADING.search(summary):
        problems.append("markdown heading")
    if "**" in summary or "__" in summary or "`" in summary:
        problems.append("markdown emphasis/code")
    if LABEL_LINE.search(summary):
        problems.append("label heading (e.g. 'Status:')")
    if problems:
        return _bad("C2_format_single_paragraph", "major", "spec:R2", "; ".join(problems))
    return _ok("C2_format_single_paragraph", "major", "spec:R2")


def check_c2b_v2_layout(summary, conv=None, golden=None) -> CheckResult:
    """INFO only: does the output follow v2's own requested 3-line layout? Lets us report 'format as v2
    intended' separately from the spec (gap:G2). Never counted as a failure."""
    has = all(re.search(rf"^\s*{k}\s*:", summary, re.I | re.M) for k in ("issue", "status", "next step"))
    return CheckResult("C2b_v2_layout_present", has, "info", "" if has else "Issue/Status/Next step not all present", "gap:G2")


# ------------------------------------------------------------------ C3
def check_c3_length(summary, conv=None, golden=None) -> CheckResult:
    """Hard limit: > 80 words fails (major). Source gap:G1."""
    n = word_count(summary)
    if n > HARD_WORDS:
        return _bad("C3_length_hard", "major", "gap:G1", f"{n} words > {HARD_WORDS}")
    return _ok("C3_length_hard", "major", "gap:G1", f"{n} words")


def check_c3_length_soft(summary, conv=None, golden=None) -> CheckResult:
    """Soft warning band: > 60 words (minor). Source gap:G1."""
    n = word_count(summary)
    if n > SOFT_WORDS:
        return _bad("C3_length_soft", "minor", "gap:G1", f"{n} words > {SOFT_WORDS}")
    return _ok("C3_length_soft", "minor", "gap:G1", f"{n} words")


# ------------------------------------------------------------------ C4 PII
# Allowed IDs are removed BEFORE looking for phones/addresses so "LM-48213" is never mistaken for a number.
ID_RX = re.compile(r"\b[A-Z]{2,4}-[A-Z0-9][A-Z0-9-]*\b")
EMAIL_RX = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_CAND = re.compile(r"\+?\d[\d\s\-()]{8,}\d")
CARD_CAND = re.compile(r"(?<![\w-])(?:\d[ -]?){13,19}(?!\w)")
OTP_RX = re.compile(r"\b(otp|one[- ]time (password|code)|verification code)\b[^.\n]{0,25}?\b\d{4,8}\b", re.I)
ADDR_RX = re.compile(
    r"\b(flat|apt\.?|apartment|house no\.?|plot)\s*(no\.?)?\s*#?\d+\w?\b|\b\d+(st|nd|rd|th)?\s+(cross|main)\b|"
    r"\b\d+\s+\w+\s+(street|road|lane|avenue)\b|\b(pin ?code|pin)\s*:?\s*\d{6}\b", re.I)
PIN6 = re.compile(r"(?<![\d,.₹])\b\d{6}\b(?![\d,])")
IBAN_RX = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")


def luhn_ok(digits: str) -> bool:
    total, alt = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if alt:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
        alt = not alt
    return total % 10 == 0


def pii_hits(summary: str) -> list[str]:
    """List the kinds of personal data found. Order IDs, amounts, dates and 'card ending 1234' are allowed
    (spec R5b, gap:G3)."""
    hits = []
    scrubbed = ID_RX.sub(" ", summary)
    if EMAIL_RX.search(summary):
        hits.append("email")
    for m in PHONE_CAND.finditer(scrubbed):
        if len(re.sub(r"\D", "", m.group())) in range(10, 13):
            hits.append("phone")
            break
    for m in CARD_CAND.finditer(scrubbed):
        digits = re.sub(r"\D", "", m.group())
        if 13 <= len(digits) <= 19 and luhn_ok(digits):
            hits.append("card_number")
            break
    if OTP_RX.search(summary):
        hits.append("otp")
    if ADDR_RX.search(summary) or PIN6.search(scrubbed):
        hits.append("address")
    if IBAN_RX.search(scrubbed):
        hits.append("iban")
    return hits


def check_c4_pii(summary, conv=None, golden=None) -> CheckResult:
    """Spec R5 (+ gap:G3 allow-list). Critical."""
    hits = pii_hits(summary)
    if hits:
        return _bad("C4_no_pii", "critical", "spec:R5", "found: " + ", ".join(hits))
    return _ok("C4_no_pii", "critical", "spec:R5")


# ------------------------------------------------------------------ C5 meta leakage
META_RX = re.compile(
    r"^\s*(here is|here's|here are|sure[,!. ]|certainly|okay[,!. ]|handoff (note|summary)\s*:|summary of the conversation)|"
    r"<think>|</think>|```|system prompt|\bas an ai\b|\bthe conversation (below|above)\b", re.I)


def check_c5_meta(summary, conv=None, golden=None) -> CheckResult:
    """No chatty preamble, reasoning traces or code fences. Source gap:G13 / spec:R2. Minor."""
    m = META_RX.search(summary)
    if m:
        return _bad("C5_no_meta_leakage", "minor", "spec:R2", f"matched {m.group().strip()[:30]!r}")
    return _ok("C5_no_meta_leakage", "minor", "spec:R2")


# ------------------------------------------------------------------ C6 banned content
PROFANITY = re.compile(r"\b(fuck\w*|f\*+\w*|shit\w*|bastard|asshole|bitch|damn|crap|idiot\w*|stupid|moron\w*|useless|garbage)\b", re.I)
SPECULATION = re.compile(r"\b(probably|presumably|i suspect|perhaps|likely (caused|due|because)|might be due to|seems to be caused)\b", re.I)
BLAME = re.compile(r"\b(incompetent|negligent|careless|unprofessional|dropped the ball|to blame)\b", re.I)


def check_c6_banned(summary, conv=None, golden=None) -> list[CheckResult]:
    """Spec R6 (profanity/insults), R4 (speculation phrases), gap:G12 (blame). Three separate results."""
    out = []
    m = PROFANITY.search(summary)
    out.append(_bad("C6a_no_profanity_insults", "major", "spec:R6", f"matched {m.group()!r}") if m
               else _ok("C6a_no_profanity_insults", "major", "spec:R6"))
    m = SPECULATION.search(summary)
    out.append(_bad("C6b_no_speculation_phrases", "minor", "spec:R4", f"matched {m.group()!r}") if m
               else _ok("C6b_no_speculation_phrases", "minor", "spec:R4"))
    m = BLAME.search(summary)
    out.append(_bad("C6c_no_blame_words", "minor", "gap:G12", f"matched {m.group()!r}") if m
               else _ok("C6c_no_blame_words", "minor", "gap:G12"))
    return out


# ------------------------------------------------------------------ C7 anchors
def check_c7_anchors(summary, conv=None, golden=None) -> CheckResult:
    """Golden: every literal anchor of every CRITICAL must-include fact is present. Catches dropped IDs and
    amounts. Critical."""
    if not golden:
        return _ok("C7_critical_anchors", "critical", "golden", "no golden entry")
    missing = []
    for m in golden["must_include"]:
        if not m.get("critical"):
            continue
        for a in m.get("literal_anchors", []):
            if not anchor_present(a, summary):
                missing.append(f"{m['id']}:{a}")
    if missing:
        return _bad("C7_critical_anchors", "critical", f"golden:{golden['id']}", "missing " + ", ".join(missing))
    return _ok("C7_critical_anchors", "critical", f"golden:{golden['id']}")


# ------------------------------------------------------------------ C8 foreign numbers
MONEY_RX = re.compile(r"(?:₹|\brs\.?)\s?(\d[\d,]*(?:\.\d+)?)|(\d[\d,]*(?:\.\d+)?)\s?(?:inr|rupees)\b", re.I)
DAY_RX = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b", re.I)


def _num(s: str) -> str:
    return s.replace(",", "").rstrip(".")


def foreign_items(summary: str, conv_txt: str) -> list[str]:
    """IDs, money amounts and day-of-month numbers in the summary that do not occur in the conversation.
    Cheap, high-precision hallucination detector (plan check C8). Number words ('five') are not compared, so
    a spoken-number transcript does not cause false alarms."""
    ct = norm(conv_txt)
    ct_ids = {i.upper() for i in ID_RX.findall(conv_txt)}
    ct_nums = {_num(n) for n in re.findall(r"\d[\d,]*(?:\.\d+)?", ct)}
    out = []
    for i in ID_RX.findall(summary):
        if i.upper() not in ct_ids and not re.fullmatch(r"[A-Z]{2}-\d{1,2}", i):  # ignore things like 'US-style'
            out.append(f"id {i}")
    for m in MONEY_RX.finditer(summary):
        val = _num(m.group(1) or m.group(2))
        if val not in ct_nums:
            out.append(f"amount {val}")
    for m in DAY_RX.finditer(summary):
        if m.group(1) not in ct_nums:
            out.append(f"day {m.group(1)}")
    return out


def check_c8_foreign(summary, conv=None, golden=None) -> CheckResult:
    """Numbers/IDs/dates not in the conversation = likely hallucination (spec:R4). Critical."""
    if conv is None:
        return _ok("C8_no_foreign_numbers", "critical", "spec:R4", "no conversation")
    f = foreign_items(summary, conv_text(conv))
    if f:
        return _bad("C8_no_foreign_numbers", "critical", "spec:R4", "not in conversation: " + ", ".join(f))
    return _ok("C8_no_foreign_numbers", "critical", "spec:R4")


# ------------------------------------------------------------------ C9 / C10 golden must-not literals
CRITICAL_TYPES = {"pii", "hallucination", "injection"}


def check_c9_c10_golden_literals(summary, conv=None, golden=None) -> list[CheckResult]:
    """Golden `must_not_include.literal_patterns`. Injection-type hits are reported as C10 (critical);
    everything else as C9 with severity by type."""
    if not golden:
        return []
    out = []
    for n in golden["must_not_include"]:
        pats = n.get("literal_patterns")
        if not pats:
            continue
        hit = next((p for p in pats if re.search(p, summary, re.I)), None)
        is_inj = n["type"] == "injection"
        name = f"C10_injection_{n['id']}" if is_inj else f"C9_must_not_{n['id']}"
        sev = "critical" if n["type"] in CRITICAL_TYPES else "minor"
        src = f"golden:{golden['id']}.{n['id']}"
        out.append(_bad(name, sev, src, f"matched /{hit}/ ({n['item'][:50]})") if hit else _ok(name, sev, src))
    return out


# ------------------------------------------------------------------ C11 language
HINGLISH = {"hai", "nahi", "kya", "aap", "mujhe", "maine", "kar", "diya", "hoon", "kijiye", "shukriya", "bhej", "mera", "ke", "ko", "ka"}


def check_c11_language(summary, conv=None, golden=None) -> CheckResult:
    """gap:G9: summary should be English. Devanagari or several romanised-Hindi words => fail (minor)."""
    if re.search(r"[ऀ-ॿ]", summary):
        return _bad("C11_english", "minor", "gap:G9", "Devanagari script")
    words = re.findall(r"[a-z]+", summary.lower())
    hits = [w for w in words if w in HINGLISH - {"ko", "ka", "ke", "kar", "mera"}]  # drop ones that are English-ish
    if len(hits) >= 3:
        return _bad("C11_english", "minor", "gap:G9", "romanised Hindi words: " + ", ".join(sorted(set(hits))))
    return _ok("C11_english", "minor", "gap:G9")


# ------------------------------------------------------------------ runner
def run_all(summary: str, conv: dict | None, golden: dict | None) -> list[CheckResult]:
    results: list[CheckResult] = [
        check_c1_nonempty(summary, conv, golden),
        check_c2_format(summary, conv, golden),
        check_c2b_v2_layout(summary, conv, golden),
        check_c3_length(summary, conv, golden),
        check_c3_length_soft(summary, conv, golden),
        check_c4_pii(summary, conv, golden),
        check_c5_meta(summary, conv, golden),
    ]
    results += check_c6_banned(summary, conv, golden)
    results += [check_c7_anchors(summary, conv, golden), check_c8_foreign(summary, conv, golden)]
    results += check_c9_c10_golden_literals(summary, conv, golden)
    results.append(check_c11_language(summary, conv, golden))
    return results
