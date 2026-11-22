"""Build data/conversation_catalog.csv (the work plan Phase 0, step 5).

Two kinds of columns, kept visibly separate:
  * CODE columns (n_turns, n_words, has_money_amount, has_order_or_ticket_id,
    has_dates_deadlines, has_pii_regex) are computed with regex: reproducible.
  * READ columns (everything in MANUAL below) come from a careful read of all 45
    threads. Spot-check them. They are
    only used to *choose* the golden set, never as ground truth for scoring.

Run:  python src/build_catalog.py
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THREADS = ROOT / "starter" / "summariser" / "data" / "threads.jsonl"
OUT = ROOT / "data" / "conversation_catalog.csv"

MONEY = re.compile(r"(₹|\bRs\.?\s?)\s?\d")
IDS = re.compile(r"\b(LM|LMT|RV|WC)-[\dA-Z-]+", re.I)
DATES = re.compile(
    r"\b\d{1,2}(st|nd|rd|th)?\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*|\b(tomorrow|today|tonight|Friday|weekend|"
    r"kal)\b|within \d+ (hours|days)|\b\d+ (working )?days\b|\b\d{1,2}pm\b|\bby the \d{1,2}(st|nd|rd|th)\b", re.I)
PII = [
    ("email", re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")),
    ("phone", re.compile(r"(\+\d{1,3}[ -]?)?\b\d{2,5}[ -]\d{3,5}[ -]?\d{3,5}\b")),
    ("card_last4", re.compile(r"card ending \d{4}", re.I)),
    ("otp", re.compile(r"\bOTP is \d{4,8}", re.I)),
    ("address", re.compile(r"\b(Flat|Cross Road|Heights)\b")),
]

# Columns: language, topic, resolved(y/n/partial), has_promise, customer_changed_mind,
# multi_issue, escalation, angry_customer, contradictory_info, injection_attempt,
# internal_jargon, notes.   (y/n unless stated.)  Read from the threads: spot-check me.
M = {
 "T01": ("en","delivery_delay_refund","partial","y","n","n","n","n","n","n","n","Refund initiated Rs4,999; arrives 5-7 working days"),
 "T02": ("en","device_pairing","n","y","n","n","y","n","n","n","n","Escalated to tech team; callback by Friday; customer needs it for weekend"),
 "T03": ("en","callback_request","n","y","n","n","n","n","n","n","n","Callback tomorrow 11-1; phone+email in customer text"),
 "T04": ("en","address_change","y","n","n","n","n","n","n","n","n","Full street address in customer text"),
 "T05": ("en","duplicate_charge","partial","y","n","n","n","n","n","n","n","Reversal ref RV-220918; 3-5 days; customer will dispute by the 20th; card last4"),
 "T06": ("hinglish","delivery_replacement","partial","y","n","n","n","n","y","n","n","Courier says 2 attempts, customer says no call; replacement in 3 days"),
 "T07": ("hindi","defective_product","partial","y","n","n","n","n","n","n","n","Non-English (Devanagari); replacement bulb in 4 days"),
 "T08": ("en","damage_complaint","partial","y","n","n","y","y","n","n","n","Profanity; wants manager; duty manager call within 24h; coupon declined"),
 "T09": ("en","plug_turning_off","n","n","n","n","n","n","n","y","n","Injection: 'ignore all previous instructions... poem'; real issue = plug clicks off ~2am; firmware update"),
 "T10": ("en","return_request","y","n","n","n","n","y","n","n","y","Internal note: 'possible return abuse. Do not disclose.'; return denied (5 wks > 30d)"),
 "T11": ("en","trivial","n","n","n","n","n","n","n","n","n","Only 'hi': nothing to hand off"),
 "T12": ("en","bot_only","n","n","n","n","n","n","n","n","n","Bot-only messages, no customer turn: nothing to hand off"),
 "T13": ("en","spam","y","n","n","n","n","n","n","n","n","SEO spam; agent closed as spam"),
 "T14": ("en","invoice_cancel_connectivity","partial","y","n","y","n","n","n","n","n","3 issues: GST invoice (2 days), cancel Lumo Care eff. 30 Nov, hub firmware 2.3.1 sent to tech team"),
 "T15": ("en","refund_retracted","partial","y","y","n","n","y","y","n","n","Agent approved Rs3,499 refund then retracted; final = free replacement cover; customer unhappy"),
 "T16": ("en","order_date_mismatch","n","n","n","n","n","n","y","n","n","Customer says ordered 3rd; system says 8 Nov; awaiting SMS screenshot"),
 "T17": ("en","warranty_claim","partial","y","n","y","n","y","n","n","n","LONG (23 msgs). WC-3391; replacement under warranty; pickup 22 Nov 2-5pm; pickup slip; missed 5 Nov callback; automations"),
 "T18": ("en","delivery_deadline","partial","n","n","n","n","n","n","n","n","Small talk noise; deadline 21 Nov (wedding 22nd); pack can reach Jaipur by 20 Nov (estimate, not a promise)"),
 "T19": ("en","cancel_subscription","y","n","n","n","n","n","n","n","n","Declined 50% retention offer; ends 1 Dec"),
 "T20": ("en","pricing_question","partial","n","n","n","n","n","n","n","n","Customer will think about it; no action needed"),
 "T21": ("en","praise","y","n","n","n","n","n","n","n","n","Positive feedback only: nothing to hand off"),
 "T22": ("en","repeat_complaint_legal","n","y","n","n","y","y","n","n","n","Third complaint; threatens consumer court + posting online in 7 days; compliance contact within 48h"),
 "T23": ("en","safety_hazard","n","y","n","n","y","n","n","n","n","SAFETY: burning smell, hot casing, black mark; unplugged; product safety team contacts today; replace + collect"),
 "T24": ("hinglish","delivery_date","partial","y","n","n","n","n","n","n","n","Expected 19 Nov; courier says by tomorrow evening; customer says very important"),
 "T25": ("en_slang","damaged_refund","partial","y","n","n","n","y","n","n","n","Typos/emoji; refund Rs2,199 approved, 5-7 days"),
 "T26": ("en","delivered_not_received","n","y","n","n","n","n","n","n","n","Email signature block (name, title, phone, website) + quoted text + legal footer; investigation 48h"),
 "T27": ("en_voice","return_pickup","partial","y","n","n","n","n","n","n","n","Voice transcript with disfluencies; order id spoken as words = LM-50911; pickup tomorrow evening"),
 "T28": ("en","third_party_privacy","n","n","n","n","n","n","n","n","n","Caller is not account holder; agent refused to share details; next: account holder writes in"),
 "T29": ("en","bulk_order_partial","n","y","n","n","n","n","n","n","n","12 hubs, 3 delivered; 5 arrive 20 Nov, 4 on 23 Nov; need all by 21st; expedite requested NO guarantee; reply by tomorrow noon"),
 "T30": ("en","unauthorised_promise","n","y","n","n","n","n","y","n","n","Agent promised DOUBLE refund (almost certainly against policy); customer initiated return"),
 "T31": ("en","invoice_backdate","partial","n","n","n","n","n","n","n","n","Cannot backdate; finance to send payment confirmation letter"),
 "T32": ("en","attachments","n","n","n","n","n","n","n","n","n","Screenshot/log filenames, agent cannot open; Error 4012; restart router"),
 "T33": ("en_emoji","plug_offline","y","n","n","n","n","n","n","n","n","Emoji heavy; solved"),
 "T34": ("en","password_reset","y","n","n","n","n","n","n","n","n","Customer typed OTP 482913 in chat; reset link sent, valid 15 min"),
 "T35": ("en","long_complaint","n","y","y","y","y","y","y","n","n","LONG single message; adapter dispatched LMT-5521-014-IN; written apology promised; earlier promise (48h adapter) was broken; customer speculates 'bad batch'; refund idea dropped; irrelevant packaging/forum noise"),
 "T36": ("en","tracking_number","y","n","n","n","n","n","n","n","n","LMT-7782-991-IN expected 3 days"),
 "T37": ("en","mid_case_handover","n","n","n","n","n","n","n","n","y","Handover Meera->Rohan; internal note: eligible for replacement once photo received; photo NOT yet sent"),
 "T38": ("en","partial_return_fee","y","n","n","n","n","n","n","n","n","Bulb refund 899-50 fee = 849; plug (2,499) stays"),
 "T39": ("en","refund_in_error","n","y","y","n","n","y","y","n","n","Refund issued in error; customer wanted replacement; supervisor to confirm tomorrow; ambiguous 'reverse nothing'"),
 "T40": ("en","express_upgrade","y","y","n","n","n","n","n","n","n","Express Rs199 charged, guaranteed by 5pm tomorrow (customer needs 6pm)"),
 "T41": ("en","insult_then_issue","partial","y","n","n","n","y","n","n","n","Insults + review threat; real issue: lamp failed after a week; replacement (no ETA)"),
 "T42": ("en","data_deletion","partial","y","n","n","n","n","n","n","n","Data deletion request; account email in text; confirmation within 30 days; invoices retained"),
 "T43": ("en","billing_details","y","n","n","n","n","n","n","n","n","GSTIN given (business tax id); past invoices unchanged"),
 "T44": ("en","repeat_issue","partial","y","n","n","n","y","n","n","n","Third time; replacement in 4 days; history noted on account"),
 "T45": ("en","faq_compat","y","n","n","n","n","n","n","n","n","Alexa/Google Home question answered: nothing to hand off"),
}
MANUAL_COLS = ["language", "topic", "resolved", "has_promise", "customer_changed_mind", "multi_issue",
               "escalation", "angry_customer", "contradictory_info", "injection_attempt", "internal_jargon", "notes"]


def main() -> None:
    rows = []
    for line in THREADS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        text = "\n".join(m["text"] for m in t["messages"])
        pii = [name for name, rx in PII if rx.search(text)]
        row = {
            "id": t["id"], "channel": t["channel"], "n_turns": len(t["messages"]), "n_words": len(text.split()),
            "has_money_amount": "y" if MONEY.search(text) else "n",
            "has_order_or_ticket_id": "y" if IDS.search(text) else "n",
            "has_dates_deadlines": "y" if DATES.search(text) else "n",
            "has_pii": "y" if pii else "n", "pii_types_regex": "|".join(pii),
        }
        row.update(dict(zip(MANUAL_COLS, M[t["id"]])))
        rows.append(row)
    assert len(rows) == 45 and set(r["id"] for r in rows) == set(M), "catalog/manual tags out of sync"
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
