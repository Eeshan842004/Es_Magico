# Walkthrough

**Would you ship v2?**
Not as written. It fails the format spec in 150 of 150 runs, which needs no judge. It also adds things nobody said (T27 refund in 4 of 5 runs, against 0 for v1) and drops commitments (T39).

**Why these 30?**
They were picked by what can go wrong: promises, numbers, changed minds, personal data, injection, safety, language. Missing are real data, long-running threads and more cases of each type.

**Why five runs?**
The same input gives different answers, even at temperature 0. v1's format flips between runs in 8 of 30 cases.

**Why pass/fail instead of 1-10?**
It is easier to apply the same way twice, and it maps to a decision.

**Why kappa?**
If 90% pass, a judge that always says pass agrees 90% of the time. Kappa removes agreement by chance. Recall on failures matters too, because a missed failure is the expensive error.

**How far do you trust the judge?**
Against my 60 reference labels, Gemini is at κ 0.48 overall (moderate) and gpt-oss at 0.28 (weak). Gemini misses dropped conditions and gpt-oss over-flags. I wrote the labels after reading the judges' answers, so those figures are a ceiling. Between the judges κ is 0.38 overall, so the exact rates are soft. The shared direction and the raw-text counts are firmer.

**Show a judge mistake.**
Gemini failed v2 on T23 for dropping "keep away from flammable items" and passed v1 runs that dropped it too. gpt-oss called "failed to reach support by phone" invented on T08, although the customer said "nobody answers my calls".

**Why bootstrap over conversations?**
Five runs of one conversation are not independent, so whole conversations are resampled.

**Why is the ship rule lopsided?**
A wrong refund or a leaked address costs more than 20 extra words.

**Why do the checks alone show almost no critical gap?**
They see missing IDs, strange numbers and personal data. "Process refund" has no number, so they can't see it.

**What is weakest?**
The small sample, expectations written after reading both prompts, partial judge coverage, and labels from one person who had seen the judges.

**What next?**
Labels from people who haven't seen the judges, a fixed rubric, a v3 run, and the checks on all production traffic.
