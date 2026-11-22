# Regression report: handoff summariser v1 vs v2

## Recommendation

**I would not ship v2 as written. Keep v1, and filter personal data out of its summaries now.**

v2 is much shorter, but it breaks the spec's single-paragraph rule in all 150 runs, adds things nobody said, and drops some commitments.

| How sure | About what | Why |
|---|---|---|
| High | Don't ship v2 as written | The format failure is deterministic and needs no judge |
| Medium | v2 is less faithful and complete | Both judges and my own labels point the same way (my labels fail 2 of 30 v1 summaries and 7 of 30 v2), and raw-text counts show examples. Gemini agrees only moderately with my labels |
| Low | The exact size of that gap | The judges differ a lot in strictness, and my labels cover only 60 summaries |

## What was tested

- 30 conversations (29 from the starter, 1 synthetic injection) × 2 prompts × 5 runs = 300 summaries, with the same model and settings for both prompts.
- 11 groups of automated checks on all 300.
- Two LLM judges with one rubric. Gemini 3 Pro, chosen first, scored a shuffled 181 before credits ran out. gpt-oss-120b scored 234 before its free quota ran out.
- 60 reference labels (one per case and prompt) as a consistency check on the judges. I wrote them after reading the judges' answers for many of the same summaries, so they are not an independent check.
- Each conversation counts once: failure rates are averaged over its runs, then compared in pairs with a bootstrap over conversations.

## Results

Change is v2 minus v1 in percentage points, with a 95% interval.

**Automated checks (all 300)**

| Measure | v1 | v2 | Change |
|---|---|---|---|
| Not a single paragraph | 18.7% | 100% | +81.3 (+68.7, +92.0) |
| Median length | 61.5 words | 35 words | 43% shorter |
| Over 80 words | 15.3% | 0% | −15.3 (−26.7, −6.0) |
| Personal data leaked | 6.7% | 6.7% | 0 |
| Injection text reproduced | 0% | 0% | 0 |
| Any critical check failure | 6.7% | 8.7% | +2.0 (0.0, +5.3) |

**Judges (critical criteria include the matching check)**

| Measure | Gemini v1 → v2 | Change | gpt-oss v1 → v2 | Change |
|---|---|---|---|---|
| Any critical failure | 14.7 → 36.3% | **+21.6 (+9.4, +34.6)** | 38.7 → 67.2% | **+28.5 (+13.4, +44.1)** |
| Faithfulness | 2.2 → 15.7% | +13.4 (+4.3, +24.4) | 17.7 → 33.1% | +15.4 (−0.6, +32.5) |
| Critical completeness | 5.8 → 16.6% | +10.8 (+2.5, +20.2) | 21.3 → 46.9% | +25.6 (+13.7, +38.2) |
| Actionable next step | 5.6 → 15.7% | +10.1 (−2.3, +22.9) | 5.7 → 26.3% | +20.7 (+8.2, +34.8) |
| Correct current state | 2.7 → 0.7% | −2.0 (−8.0, +2.0) | 4.3 → 3.9% | −0.4 (−6.0, +3.9) |

## What improved

v2 does what "tighter" promises: none of its summaries passes 60 words, while 52.7% of v1's do. It states the current status about as well as v1.

## What got worse

These counts come from the raw text of all five runs and need no judge. The cases were picked after reading failures, so they show how v2 fails, not how often ([counts](outputs/results/example_counts.csv)).

| Case | What happens | v1 | v2 |
|---|---|---|---|
| T27, return pickup | Adds a refund nobody mentioned | 0/5 | 4/5 |
| T07, broken bulb | Says the photo was verified. The agent never said so | 0/5 | 5/5 |
| T30, odd promise | Calls the promise unauthorised. Nobody said so | 0/5 | 4/5 |
| T39, missing hub | Keeps the promise to arrange a replacement | 5/5 | 0/5 |
| T29, late delivery | Keeps "no guarantee" on expediting | 3/5 | 1/5 |

T27, where the agent only said "Pickup booked for tomorrow evening":

> **v1:** Next, the courier will pick up the lamp tomorrow evening.
>
> **v2:** Next step: Confirm pickup completion and process refund upon receipt.

The next agent could issue a refund on the strength of that line. The mandatory `Next step:` slot and "as short as possible" are the likely causes, but changing one line at a time would be needed to confirm it.

One apparent regression did not hold up. Gemini failed v2 on the burning-plug case (T23) for omitting "keep away from flammable items", but passed v1 runs with the same omission. v1 keeps that line in 1 of 5 runs and v2 in none, so **both prompts are weak on safety instructions**.

## Run-to-run variation

- v1's format flips between runs in 8 of 30 conversations. v2 fails every time.
- Gemini's critical verdict flips in 3 of 24 v1 conversations and 9 of 28 v2 conversations that had at least two judged runs.
- v1 puts contact details or an address into 5 of 5 runs for both T03 and T04. That is a repeatable production bug.

## How far to trust this

**The judges against my reference labels** (60 summaries; [Gemini](outputs/results/judge_agreement_gemini.md), [gpt-oss](outputs/results/judge_agreement_gptoss.md)). I labelled after reading the judges' answers, so treat these figures as a ceiling.

| Judge | Overall κ (95% interval) | Failures I found that it caught | Its failures that were real |
|---|---|---|---|
| Gemini | 0.48 (0.11, 0.77) | 5 of 9 | 5 of 9 |
| gpt-oss | 0.28 (0.12, 0.46) | 9 of 9 | 9 of 31 |

Under the trust rule fixed in advance, Gemini is "moderate" (use with caution) and gpt-oss is "weak" (don't use for the decision). The gpt-oss rows above are supporting evidence only.

- **Gemini misses dropped conditions.** It caught 1 of the 4 completeness failures I found. It passed summaries that lost "no guarantee" (T29, twice) and the promise to arrange the replacement (T39). Its completeness gap is more likely understated than overstated.
- **gpt-oss over-flags.** Most of its 28 disagreements with me are harmless hedges such as "monitor delivery if needed", expectations that were too strict, or personal data judged under the wrong criterion. The [list with a cause for each](outputs/results/judge_disagreements_gptoss.md) is in the results.
- **Two weak spots in the test itself.** Several expectations are stricter than a next agent needs (purchase dates in T17, "could not transfer" in T08), and T38's expected status looks wrong. Both judges follow those expectations.
- **The judges agree with each other only moderately.** On 180 shared summaries κ is 0.42 for faithfulness, 0.42 for completeness and 0.38 overall. Their [105 disagreements are sorted by cause](outputs/results/judge_disagreement_causes.md).
- **The gap isn't one conversation.** Leaving out any one keeps Gemini's gap between +18.9 and +23.2 points. Without T23 it is +19.8 (+7.8, +33.2).
- **Multiple testing.** After Holm correction over four critical criteria, only faithfulness survives for Gemini (p = 0.046) and only completeness for gpt-oss (p = 0.003).
- **The test may favour v1.** The expectations and rubric were written after reading both prompts. Without the four cases whose expectations looked wrong, the gap is +23.6 (Gemini) and +29.4 (gpt-oss), but I chose that exclusion after seeing results.
- **Small sample.** Expect to detect only differences of roughly 15-20 points. Results for a single case type are directional.

## Ship rule and next steps

The [ship rule](docs/ship_rule.md) gives the same result under both judges, and the format rule needs neither: v2 **fails** rules 1 (critical regression), 2 (case regression) and 4 (format), and **passes** 3 (no new failure type) and 5 (shorter).

1. Add the personal-data check to v1 as an output filter.
2. Ask the product owner whether agents want labelled lines. If they do, change the spec on purpose.
3. Test the [proposed v3](prompts/summariser_v3_proposed.txt): one paragraph, no invented steps, conditions kept, safety first, no contact details. It is untested.
