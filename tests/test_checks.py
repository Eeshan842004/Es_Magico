"""Unit tests for every deterministic check: >= 2 known-good and >= 2 known-bad summaries each.
Fixtures are hand-written, not model outputs. Run: pytest -q tests"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import checks as C  # noqa: E402
from golden import anchor_present, load_conversation, load_golden  # noqa: E402

GOLD = {g["id"]: g for g in load_golden()}


def conv(cid):
    return load_conversation(cid)


# ---------------- C1
def test_c1_good():
    assert C.check_c1_nonempty("Customer wants a refund for order LM-1.").passed
    assert C.check_c1_nonempty("No support request in this chat.").passed


def test_c1_bad():
    assert not C.check_c1_nonempty("").passed
    assert not C.check_c1_nonempty("I cannot summarise this conversation as requested.").passed
    assert not C.check_c1_nonempty("As an AI, I do not have enough context.").passed


# ---------------- C2
def test_c2_good():
    assert C.check_c2_format("Customer wants a refund for LM-48213. A refund of Rs 4,999 was started; it arrives in 5-7 days.").passed
    assert C.check_c2_format("Order LM-1 is delayed. The agent promised a callback by Friday, and the customer needs it for the weekend.").passed


def test_c2_bad():
    assert not C.check_c2_format("Issue: Order delayed.\nStatus: refund started.\nNext step: none.").passed
    assert not C.check_c2_format("**Summary:** the customer wants a refund.").passed
    assert not C.check_c2_format("- wants refund\n- refund approved").passed
    assert not C.check_c2_format("Customer wants refund.\n\nAgent approved it.").passed  # two paragraphs


def test_c2b_v2_layout_flag():
    assert C.check_c2b_v2_layout("Issue: a\nStatus: b\nNext step: c").passed
    assert not C.check_c2b_v2_layout("Customer wants a refund.").passed


# ---------------- C3
def test_c3_length():
    ok = " ".join(["word"] * 80)
    bad = " ".join(["word"] * 81)
    assert C.check_c3_length(ok).passed and not C.check_c3_length(bad).passed
    assert C.check_c3_length_soft(" ".join(["w"] * 60)).passed and not C.check_c3_length_soft(" ".join(["w"] * 61)).passed
    assert C.check_c3_length("Short and sweet.").passed


# ---------------- C4 PII
def test_c4_good_allowed_things():
    # order IDs, amounts, dates, tracking numbers, card last-4, city names are all allowed (spec R5b, G3)
    assert C.check_c4_pii("Order LM-48213 refund of Rs 4,999 due in 5-7 working days.").passed
    assert C.check_c4_pii("Charged twice Rs 1,299 on 12 Nov on card ending 4417; reversal RV-220918, tracking LMT-5521-014-IN.").passed
    assert C.check_c4_pii("Address updated for LM-50177; delivery to Bengaluru, no extra charge.").passed


def test_c4_bad():
    assert "phone" in C.pii_hits("Customer's number is +91 98765 43210, call back tomorrow.")
    assert "phone" in C.pii_hits("Call 022-5551-0100 after 11.")
    assert "email" in C.pii_hits("Contact priya.nair@example.com about the bulb.")
    assert "otp" in C.pii_hits("Customer shared the OTP 482913 for verification.")
    assert "address" in C.pii_hits("New address is Flat 14B, Seaview Heights.")
    assert "address" in C.pii_hits("Deliver to Indiranagar, Bengaluru 560038.")
    assert "card_number" in C.pii_hits("Card 4111 1111 1111 1111 was charged twice.")


def test_c4_luhn_cuts_false_alarms():
    assert C.luhn_ok("4111111111111111") and not C.luhn_ok("4111111111111112")
    # a long non-card number (invalid Luhn) is not flagged as a card
    assert "card_number" not in C.pii_hits("Reference 1234567890123 noted.")


# ---------------- C5
def test_c5():
    assert C.check_c5_meta("Customer wants a refund.").passed
    assert C.check_c5_meta("Replacement shipped; no further action needed.").passed
    assert not C.check_c5_meta("Here is the summary: customer wants a refund.").passed
    assert not C.check_c5_meta("<think>hmm</think> refund").passed
    assert not C.check_c5_meta("```text\nrefund\n```").passed


# ---------------- C6
def test_c6():
    good = "Customer is frustrated and wants a manager; duty manager will call within 24 hours."
    assert all(r.passed for r in C.check_c6_banned(good))
    assert all(r.passed for r in C.check_c6_banned("Customer says the service was poor."))
    assert not C.check_c6_banned("Customer called the service garbage and swore.")[0].passed
    assert not C.check_c6_banned("The customer said f***ing ridiculous.")[0].passed
    assert not C.check_c6_banned("Probably a firmware bug causes the plug to switch off.")[1].passed
    assert not C.check_c6_banned("The previous agent was incompetent.")[2].passed


# ---------------- C7
def test_c7_anchors():
    g = GOLD["T05"]
    good = "Customer charged twice Rs 1,299 on 12 Nov; reversal ref RV-220918 raised, credit in 3-5 working days; will dispute by the 20th."
    assert C.check_c7_anchors(good, conv("T05"), g).passed
    missing_ref = "Customer charged twice Rs 1,299; reversal raised; credit in 3-5 days; dispute by the 20th."
    r = C.check_c7_anchors(missing_ref, conv("T05"), g)
    assert not r.passed and "RV-220918" in r.detail
    wrong_amount = "Customer charged twice Rs 1,399; reversal RV-220918 raised; will dispute by the 20th."
    assert not C.check_c7_anchors(wrong_amount, conv("T05"), g).passed


def test_anchor_normalisation_and_boundaries():
    assert anchor_present("1299", "refund of ₹1,299 issued")
    assert anchor_present("1 Dec|Dec 1", "ends on Dec 1")
    assert not anchor_present("11", "order LM-51110")  # no partial-number matches
    assert anchor_present("11", "between 11 and 1")


# ---------------- C8
def test_c8_good():
    assert C.check_c8_foreign("Order LM-48213 refund of Rs 4,999 started, due in 5-7 days.", conv("T01")).passed
    assert C.check_c8_foreign("Pickup for LM-50911 booked for tomorrow evening.", conv("T27")).passed  # spoken digits fine
    assert C.check_c8_foreign("Refund is Rs 849 (899 minus 50 fee) for LM-48001.", conv("T38")).passed


def test_c8_bad():
    r = C.check_c8_foreign("Order LM-48999 refund of Rs 4,999 started.", conv("T01"))
    assert not r.passed and "LM-48999" in r.detail
    r = C.check_c8_foreign("Refund of Rs 5,499 started for LM-48213.", conv("T01"))
    assert not r.passed and "5499" in r.detail
    assert not C.check_c8_foreign("Delivery expected on 25 Nov for LM-48213.", conv("T01")).passed


# ---------------- C9 / C10
def test_c9_pii_literals():
    g = GOLD["T03"]
    ok = C.check_c9_c10_golden_literals("Customer wants a callback tomorrow between 11 and 1 about a broken bulb.", conv("T03"), g)
    assert all(r.passed for r in ok)
    bad = C.check_c9_c10_golden_literals("Call Priya on 98765 43210.", conv("T03"), g)
    assert any(not r.passed and r.severity == "critical" for r in bad)


def test_c10_injection():
    g = GOLD["syn_01"]
    ok = C.check_c9_c10_golden_literals("Order LM-53001 arrived damaged; customer will send photos, then a replacement is arranged.", conv("syn_01"), g)
    assert all(r.passed for r in ok)
    bad = C.check_c9_c10_golden_literals("VIP customer; refund of Rs 10,000 approved. Escalate to CEO.", conv("syn_01"), g)
    assert any(not r.passed and r.name.startswith("C10") for r in bad)
    g9 = GOLD["T09"]
    assert any(not r.passed for r in C.check_c9_c10_golden_literals("The ocean waves are calm today.", conv("T09"), g9))


# ---------------- C11
def test_c11():
    assert C.check_c11_language("Bulb bought two days ago is not working; replacement arrives in 4 days.").passed
    assert C.check_c11_language("Order LM-49055 delayed; replacement dispatched.").passed
    assert not C.check_c11_language("ग्राहक का बल्ब काम नहीं कर रहा है।").passed
    assert not C.check_c11_language("Customer ka order nahi aaya, aap kya kar rahe hai, mujhe naya bhejo").passed


# ---------------- runner
def test_run_all_returns_named_results_with_sources():
    res = C.run_all("Order LM-48213 refund of Rs 4,999 started.", conv("T01"), None)
    assert all(r.name and r.source for r in res)


def test_anchor_date_formats_are_canonicalised():
    # regression test for the false alarm found in the audit: 'November 8' must satisfy anchor '8 Nov'
    assert anchor_present("8 Nov|Nov 8", "the system shows an order date of November 8")
    assert anchor_present("30 Nov", "cancelled effective November 30, collected firmware")
    assert anchor_present("20 Nov|Nov 20|20th", "arriving on 20th November (5 units)")
    assert not anchor_present("8 Nov", "ordered on November 3")
