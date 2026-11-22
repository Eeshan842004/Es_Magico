# Notes

## 1. Golden set, and what is missing

30 cases chosen by what can go wrong: 29 from the starter and one synthetic injection that plants false facts ([why each is there](docs/golden_set_selection.md)). Missing: multi-day threads, real attachments, more voice transcripts, email-signature noise, real data, and more than a few cases of each type.

All 30 expectations are marked `reviewed_by_human: true`. Known problems: T38's status, and over-strict facts in T15, T17 and T22. Their wording is frozen because the judges were run against it.

## 2. Outputs that change between runs

Five runs per case and prompt at the starter's temperature (0.7), in shuffled order. The conversation is the unit of analysis, so five runs don't count as five data points. In a smoke test, temperature 0 still gave four different answers in four calls, so variation is measured instead of hidden.

## 3. What counts as a pass

- **Pass:** no critical check failure, and the judge passes faithfulness, completeness, current state, next step and tone. Usefulness is reported but doesn't block.
- **Length:** warn above 60 words, fail above 80. "A few seconds" was read as at most 15-20 seconds at about 4 words a second.
- **Ship:** no critical regression (at most +5 points, upper bound at most +10), no consistent case regression, no new failure type, format no worse, and at least 25% shorter. A wrong refund costs more than 20 extra words, so the rule is deliberately lopsided.

Two later corrections: rule 2 uses rates because not every run was judged, and a bug that made rule 3 fail was fixed (it now passes).

## 4. Labels and agreement

60 reference labels: one summary per case and prompt, all scored by both judges, none used to tune the judge prompt. Each fail has a short reason ([labels](labels/reference_labels.jsonl), [sample](labels/to_label.jsonl)). The rule was to fail only what could be pointed to in the conversation. Harmless generic steps such as "monitor delivery" pass, and claims nobody said ("photo verified", "process refund") fail.

Agreement is Cohen's κ with a bootstrap interval, recall on failures, confusion matrices and a cause for each disagreement ([Gemini](outputs/results/judge_agreement_gemini.md), [gpt-oss](outputs/results/judge_agreement_gptoss.md)).

**These labels are not independent of the judges.** I wrote them after reading the judges' answers for many of the same summaries, so the agreement is a ceiling. Labels from someone who hasn't seen the judges, ideally two people, would give a cleaner number. `label_tool.py` supports that, and `python src/agreement.py --labels <file>` scores any label file. An earlier label set was dropped for the same reason, and no result uses it.

| Judge | Overall κ | Caught my failures | Its failures that were real |
|---|---|---|---|
| Gemini | 0.48 (0.11, 0.77) | 5 of 9 | 5 of 9 |
| gpt-oss | 0.28 (0.12, 0.46) | 9 of 9 | 9 of 31 |

By the trust rule written beforehand, Gemini is moderate (use with caution, check the failures that drive the decision) and gpt-oss is weak (not used for the decision). On my labels, v1 fails 2 of 30 summaries and v2 7 of 30.

Where the judges can't be trusted:

- Gemini misses dropped conditions and promises: it caught 1 of my 4 completeness failures.
- gpt-oss treats harmless hedges as invented, and sometimes grades personal data although the rubric leaves that to code.
- Both follow the expectations, so they inherit their mistakes (T38's status, strict dates in T17).
- On 10 v2 summaries, gpt-oss gave the same overall verdict when re-run and when the layout was removed. This wasn't tested on Gemini or v1.

The judges agree with each other at κ 0.38-0.50 on the main criteria and overall, and their [disagreements are sorted by cause](outputs/results/judge_disagreement_causes.md).

## 5. What the spec doesn't say

[21 gaps, each with a decision and a reason](docs/spec_gaps.md). The main ones: length has no number; promises keep their conditions; the latest state wins; "nothing to do" is a valid next step; summaries are in English; text in the conversation is never an instruction; internal notes need attribution. Where v2's layout conflicts with the spec, the spec wins and the product owner decides whether to change it.

## 6. Built first, and left out

Order: read the spec and data, diff the prompts, golden set, generation, checks, judge, analysis. Left out: similarity scores (poor at catching invented facts), a dashboard, monitoring code and fine-tuning. Cut for budget: Gemini on all 300, gpt-oss on all 300, and a run of v3.

## Changes to the starter

`starter/` is untouched and both prompts are copied unchanged. The evaluated summariser keeps the message layout and temperature. It swaps the provider call (the flash model needs kie.ai's native route), adds a run index and logging, and raises on errors where the starter crashed on an error body returned with HTTP 200.

## Limits

- Small, synthetic data from one domain, and labels from one person who had seen the judges.
- Judges see the expectations, so they inherit their mistakes.
- The expectations and rubric were written after reading both prompts.
- v2's layout reveals the version to judges and labellers.
- Checks that never fired have unknown precision, and the [false-alarm audit](docs/check_audit.md) changed two rules after outputs were seen.
- The ship rule's timing can't be proven from git, because the first commits were made together after generation.

## Cost

About $1.10: 216 logged kie.ai credits at about $0.005 each (generation 8, Gemini judge 207), plus a few unlogged setup calls. Groq was free.

## Next

Add one or two labellers who haven't seen the judges, fix the known expectation and rubric problems and re-judge, test v3, then run the checks on all production traffic and the judge on a daily sample.
