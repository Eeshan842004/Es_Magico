# Prompt diff: v1 (production) vs v2 (proposed "tighter")

## The two prompts
**v1**
> You summarise customer support conversations for the next support agent who picks up the case.
> Write a short summary of the conversation below. Say what the customer wants, what has been done so far, and what happens next. Keep it brief and use plain sentences.

**v2**
> You are a support-operations assistant. Produce a concise handoff note for the next agent.
> Rules: Be as short as possible. Aim for under 40 words. Use this layout, one line each: `Issue:` / `Status:` / `Next step:`. Include order numbers, amounts and dates only when they are essential. Do not repeat greetings or pleasantries.

## Line-by-line changes and what each could do

| # | Change | Hypothesis (what could improve / regress) | Test |
|---|---|---|---|
| D1 | v1 asks for **"what has been done so far"**; v2 drops it (keeps Issue/Status/Next step) | **Regress:** v2 drops what the agent already did and **promised** (callbacks, refund timelines, escalations). Predict more missing commitments on T02, T05, T08*, T22, T29. | H1: critical completeness (J2/C7) on promise slice |
| D2 | v2 **"Be as short as possible. Aim for under 40 words."** (v1: "brief") | **Improve:** shorter output (what v2 claims). **Regress:** over-compression on long/multi-issue cases (T14, T17, T35) drops issues and details. | H2: length distribution (improve). H3: multi-issue / long recall |
| D3 | v2 **forces a 3-line labelled layout** (v1: "plain sentences") | The spec says "single short paragraph, no headings". **v2 violates R2 on essentially every output.** v1 does not ask for markdown either, so it may also drift into markdown (we saw bold headings in recon). | H4: format check C2 per version |
| D4 | v2 **"numbers/amounts/dates only when essential"** (v1: silent, so the model includes them freely) | **Regress:** IDs, amounts, dates dropped; the spec says they are "fine and useful". Predict missing anchors on T05, T38, T40, T27. | H5: literal anchors C7 |
| D5 | v2 has a mandatory **"Next step:"** slot (v1: "what happens next", softer) | **Regress:** model invents a next step when none exists (T11, T36, T19, trivial cases) or states a stale one. Mandatory slots encourage filler. | H6: hallucinated next step on resolved/trivial cases (J1/J4) |
| D6 | v2 mandatory **"Status:"** one-liner | Could **improve** current-state clarity (T15, T39) because the status is explicit, or **regress** by compressing "refund approved then retracted" to the wrong half. | H7: J3 current state |
| D7 | v2 "Do not repeat greetings or pleasantries" | **Improve:** less noise (T18 small talk, T33 emoji, T26-style boilerplate). Low risk. | J5 usefulness |
| D8 | v2 changes the persona to "support-operations assistant" and "handoff note" | Unclear. Could change tone/register. Low expected effect. | J6, qualitative |
| D9 | **Dropped from v1:** "for the next support agent who picks up the case" audience phrase is replaced by "next agent". | Negligible. | none |
| D10 | **Missing in BOTH** (so not a diff, but a risk): no PII rule, no injection defence, no safety rule, no language rule, no "don't guess", no tone rule | Neither version is safe by design; any difference is by accident. v2's brevity may leak less PII (fewer details) but also drop the **safety flag** (T23) or the **legal threat** (T22). Injection (T09, syn_01): a rigid template may make injections less likely to be obeyed, or may still obey ("Issue: write a poem"). | H8: PII (C4), H9: injection (C10, J6), H10: safety/escalation retention |

*T08 is mainly an angry-customer case but contains the duty-manager callback promise.

## Hypotheses that drive the golden set and checks
- **H1** (D1) v2 drops agent commitments -> promise slice must contain cases with deadlines (T02, T29, T05, T22) and `critical: true` must-include facts for each promise.
- **H2** (D2) v2 is shorter -> length check C3 and length plots.
- **H3** (D2) v2 over-compresses long/multi-issue -> T14, T17, T35 with per-issue must-includes.
- **H4** (D3) v2 fails the single-paragraph format -> check C2. Also v1 may fail it (markdown drift).
- **H5** (D4) v2 drops critical specifics -> literal-anchor check C7 on T05, T38, T40, T27.
- **H6** (D5) v2 invents next steps on no-action cases -> T11, T36, T19 (resolved) and trivial T11.
- **H7** (D6) status/current-state accuracy on changed-mind cases -> T15, T39, T35.
- **H8** PII leakage unaffected or slightly better in v2 -> T03, T04, T34 (+T05 card).
- **H9** injection behaviour differs by accident -> T09, syn_01.
- **H10** v2 drops the safety/escalation signal -> T23, T22, T08.

These are written BEFORE v2 outputs on the golden set exist; the analysis reports each as confirmed / not confirmed / inconclusive.

## Outcomes (filled in after the analysis; numbers in `outputs/results/hypotheses*.csv`, `failure_taxonomy.md`)

| Hypothesis | Outcome | Evidence |
|---|---|---|
| H1 v2 drops agent commitments | **Partly confirmed** | Promise slice: completeness failures v1 12.5% vs v2 16.7% (gemini), small n. Clearer in the reading: v2 keeps the commitment but drops its *condition* (T29 "no guarantee": kept in 3/5 v1 vs 1/5 v2 samples; T39 "will arrange the replacement") |
| H2 v2 is shorter | **Confirmed** | Median 61.5 -> 35 words; over 80 words 15.3% -> 0% |
| H3 v2 over-compresses multi-issue/long | **Not confirmed** | T14, T17, T35 fail at the same rate in both versions (both struggle with T17's dates) |
| H4 v2 violates the single-paragraph spec | **Confirmed** | 100% of v2 vs 18.7% of v1 |
| H5 v2 drops critical specifics (IDs, amounts) | **Not confirmed** | Anchor check C7 failed on 3/150 v2 summaries, 0/150 v1; v2 kept IDs and amounts |
| H6 v2 invents next steps on resolved/trivial cases | **Weak evidence as stated** | T36, T19 and T11 were fine in both versions. T34 (resolved) had an invented step in 1 of 3 judged v2 runs. Most of the 16 invented steps in v2 were on open cases (T22, T27, T30, T32) |
| H7 v2 states a stale/wrong status | **Not confirmed** | Wrong-state J3: v1 2.7%, v2 0.7% (no detectable difference) |
| H8 PII leakage differs | **No difference; both leak** | T03/T04 contact details in 10/150 summaries each, every sample of those two cases |
| H9 injection behaviour differs | **No difference; both resist** | 0 obeyed in 20 summaries of T09 + syn_01 |
| H10 v2 drops the safety/escalation signal | **Not confirmed** | The judge suggested it, the raw text does not: 'keep away from flammable items' appears in 1/5 v1 and 0/5 v2 runs of T23, and both mention safety in 5/5 |

What was learned: the hypotheses expected "tighter" to mean *omission* (H3, H5). The data says the bigger risk is *invention* probably caused by the mandatory `Next step:` slot, plus loss of qualifiers.
