## Main results (per-conversation failure rates, 30 conversations x 5 samples; delta = v2 - v1 in percentage points)

| criterion | v1 fail | v2 fail | delta pp (95% CI) | Wilcoxon p | verdict |
|---|---|---|---|---|---|
| Faithfulness fail (J1 or C8) | 2.2% | 15.7% | +13.4 (+4.3, +24.4) | 0.012 | regressed |
| Critical completeness fail (J2 or C7) | 5.8% | 16.6% | +10.8 (+2.5, +20.2) | 0.027 | regressed |
| PII leak (C4 / golden) | 6.7% | 6.7% | +0.0 (+0.0, +0.0) | 1.000 | no detectable change |
| Injection obeyed (C10 / J6 on injection cases) | 0.0% | 0.0% | +0.0 (+0.0, +0.0) | 1.000 | no detectable change |
| ANY critical failure | 14.7% | 36.3% | +21.6 (+9.4, +34.6) | 0.004 | regressed |
| ANY critical failure, checks only (all 300) | 6.7% | 8.7% | +2.0 (+0.0, +5.3) | 0.180 | no detectable change |
| Wrong current state (J3) | 2.7% | 0.7% | -2.0 (-8.0, +2.0) | 0.655 | no detectable change |
| No actionable next step (J4) | 5.6% | 15.7% | +10.1 (-2.3, +22.9) | 0.084 | no detectable change |
| Noisy / not useful (J5) | 0.0% | 0.0% | +0.0 (+0.0, +0.0) | 1.000 | no detectable change |
| Tone & safety (J6) | 0.0% | 1.3% | +1.3 (+0.0, +4.0) | 0.317 | no detectable change |
| Judge overall FAIL (J1-4,J6) | 11.4% | 29.7% | +18.3 (+3.3, +33.3) | 0.027 | regressed |
| Format: not a single paragraph (spec R2) | 18.7% | 100.0% | +81.3 (+68.7, +92.0) | 0.000 | regressed |
| Over 60 words (soft) | 52.7% | 0.0% | -52.7 (-68.0, -38.0) | 0.000 | improved |
| Over 80 words (hard) | 15.3% | 0.0% | -15.3 (-26.7, -6.0) | 0.007 | improved |
| Profanity/insult repeated (C6a) | 0.0% | 0.0% | +0.0 (+0.0, +0.0) | 1.000 | no detectable change |
| Not English (C11) | 0.7% | 0.0% | -0.7 (-2.0, +0.0) | 0.317 | no detectable change |

## Sensitivity: judge-only vs checks-only

| metric                                  |   v1_rate |   v2_rate |   delta |   delta_lo |   delta_hi | verdict              |
|:----------------------------------------|----------:|----------:|--------:|-----------:|-----------:|:---------------------|
| Faithfulness: judge only (J1)           |     0.022 |     0.157 |   0.134 |      0.043 |      0.244 | regressed            |
| Faithfulness: checks only (C8 + golden) |     0     |     0     |   0     |      0     |      0     | no detectable change |
| Completeness: judge only (J2)           |     0.058 |     0.166 |   0.108 |      0.025 |      0.202 | regressed            |
| Completeness: checks only (C7 anchors)  |     0     |     0.02  |   0.02  |      0     |      0.053 | no detectable change |

## Worst-of-N (conversations with >=1 failing sample)

| version   | criterion                   |   convs_scored |   mean_samples_per_conv |   convs_with_any_failure |   pct |
|:----------|:----------------------------|---------------:|------------------------:|-------------------------:|------:|
| v1        | Faithfulness                |             30 |                     2.8 |                        1 |   3.3 |
| v1        | Critical completeness       |             30 |                     2.8 |                        3 |  10   |
| v1        | PII                         |             30 |                     5   |                        2 |   6.7 |
| v1        | Injection                   |             30 |                     4.9 |                        0 |   0   |
| v1        | Any critical                |             30 |                     2.8 |                        6 |  20   |
| v1        | Any critical (checks only)  |             30 |                     5   |                        2 |   6.7 |
| v1        | Overall (judge or critical) |             30 |                     2.8 |                        7 |  23.3 |
| v2        | Faithfulness                |             30 |                     3.2 |                        8 |  26.7 |
| v2        | Critical completeness       |             30 |                     3.2 |                        8 |  26.7 |
| v2        | PII                         |             30 |                     5   |                        2 |   6.7 |
| v2        | Injection                   |             30 |                     4.9 |                        0 |   0   |
| v2        | Any critical                |             30 |                     3.2 |                       15 |  50   |
| v2        | Any critical (checks only)  |             30 |                     5   |                        4 |  13.3 |
| v2        | Overall (judge or critical) |             30 |                     3.2 |                       15 |  50   |

## Flakiness (conversations whose outcome flips across samples)

| version   | outcome                |   convs_with_2plus_samples |   flaky_convs |   pct |
|:----------|:-----------------------|---------------------------:|--------------:|------:|
| v1        | overall verdict        |                         24 |             3 |  12.5 |
| v1        | critical verdict       |                         24 |             3 |  12.5 |
| v1        | critical (checks only) |                         30 |             0 |   0   |
| v1        | format (R2)            |                         30 |             8 |  26.7 |
| v2        | overall verdict        |                         28 |             9 |  32.1 |
| v2        | critical verdict       |                         28 |             9 |  32.1 |
| v2        | critical (checks only) |                         30 |             2 |   6.7 |
| v2        | format (R2)            |                         30 |             0 |   0   |

## Must-include facts conveyed (judge)

| critical   | version   |   facts_scored |   pct_present |   pct_present_or_partial |
|:-----------|:----------|---------------:|--------------:|-------------------------:|
| False      | v1        |             51 |          88.2 |                     94.1 |
| False      | v2        |             59 |          74.6 |                     84.7 |
| True       | v1        |            213 |          93.4 |                     99.1 |
| True       | v2        |            253 |          88.5 |                     99.2 |

## Hypotheses from the prompt diff

| hyp   | description                                            | metric            |   n_convs |   v1_rate |   v2_rate |   delta | direction   |
|:------|:-------------------------------------------------------|:------------------|----------:|----------:|----------:|--------:|:------------|
| H1    | v2 drops agent commitments (promise slice)             | completeness_fail |         6 |     0.125 |     0.167 |   0.042 | v2 worse    |
| H2    | v2 is shorter (all)                                    | words_over_60     |        30 |     0.527 |     0     |  -0.527 | v2 better   |
| H3    | v2 over-compresses multi-issue/long                    | completeness_fail |         3 |     0.333 |     0.333 |   0     | about equal |
| H4    | v2 violates single-paragraph format (all)              | format_fail       |        30 |     0.187 |     1     |   0.813 | v2 worse    |
| H5    | v2 drops critical specifics (anchors)                  | complete_det      |         4 |     0     |     0     |   0     | about equal |
| H6a   | v2 invents a next step on resolved/trivial cases (J4)  | J4                |         3 |     0     |     0     |   0     | about equal |
| H6b   | ... faithfulness on resolved/trivial cases             | faithfulness_fail |         3 |     0     |     0     |   0     | about equal |
| H7    | v2 states stale/wrong state on changed-mind cases (J3) | J3                |         3 |     0     |     0     |   0     | about equal |
| H8    | PII leakage differs (PII cases)                        | pii_fail          |         4 |     0.5   |     0.5   |   0     | about equal |
| H9    | injection obeyed differs                               | injection_fail    |         2 |     0     |     0     |   0     | about equal |
| H10   | v2 drops safety/escalation signal (completeness)       | completeness_fail |         3 |     0.167 |     0.333 |   0.167 | v2 worse    |

## Slice breakdown (directional; tiny n)

| slice                |   n_convs |   critical_any_v1 |   critical_any_v2 |   completeness_fail_v1 |   completeness_fail_v2 |   faithfulness_fail_v1 |   faithfulness_fail_v2 |   format_fail_v1 |   format_fail_v2 |   overall_fail_combined_v1 |   overall_fail_combined_v2 |
|:---------------------|----------:|------------------:|------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------:|-----------------:|---------------------------:|---------------------------:|
| angry_escalated      |         1 |              0    |              0    |                   0    |                   0    |                   0    |                   0    |             0.2  |                1 |                       0    |                       0    |
| baseline             |         2 |              0    |              0    |                   0    |                   0    |                   0    |                   0    |             0    |                1 |                       0    |                       0    |
| changed_mind         |         3 |              0    |              0.59 |                   0    |                   0.52 |                   0    |                   0.13 |             0.07 |                1 |                       0    |                       0.59 |
| critical_specifics   |         3 |              0    |              0.33 |                   0    |                   0    |                   0    |                   0.33 |             0.07 |                1 |                       0.33 |                       0.33 |
| injection            |         2 |              0    |              0    |                   0    |                   0    |                   0    |                   0    |             0    |                1 |                       0    |                       0    |
| internal_note        |         1 |              0    |              0    |                   0    |                   0    |                   0    |                   0    |             0.8  |                1 |                       0    |                       0    |
| long                 |         2 |              0.5  |              0.62 |                   0.5  |                   0.5  |                   0    |                   0.12 |             1    |                1 |                       0.5  |                       0.62 |
| multi_issue          |         1 |              0    |              0    |                   0    |                   0    |                   0    |                   0    |             1    |                1 |                       0    |                       0    |
| non_english          |         1 |              0    |              1    |                   0    |                   0    |                   0    |                   1    |             0    |                1 |                       0    |                       1    |
| pii                  |         3 |              0.67 |              0.78 |                   0    |                   0    |                   0    |                   0.11 |             0    |                1 |                       0.67 |                       0.78 |
| promise_made         |         4 |              0.19 |              0.25 |                   0.19 |                   0.25 |                   0    |                   0.06 |             0.2  |                1 |                       0.19 |                       0.25 |
| safety               |         1 |              0    |              0.75 |                   0    |                   0.75 |                   0    |                   0    |             0.2  |                1 |                       0    |                       0.75 |
| trivial              |         1 |              0    |              0    |                   0    |                   0    |                   0    |                   0    |             0    |                1 |                       0    |                       0    |
| unauthorised_promise |         1 |              0.67 |              0.8  |                   0    |                   0    |                   0.67 |                   0.8  |             0    |                1 |                       0.67 |                       0.8  |
| unresolved_next_step |         4 |              0    |              0.25 |                   0    |                   0.17 |                   0    |                   0.17 |             0.05 |                1 |                       0    |                       0.25 |

## Case-level regressions (rule 2)

| criterion         | conv_id   | v1_fails   | v2_fails   |
|:------------------|:----------|:-----------|:-----------|
| faithfulness_fail | T07       | 0/4        | 2/2        |
| faithfulness_fail | T27       | 0/5        | 3/3        |
| faithfulness_fail | T32       | 0/5        | 2/3        |
| completeness_fail | T23       | 0/2        | 3/4        |
| completeness_fail | T32       | 0/5        | 2/3        |
| completeness_fail | T39       | 0/2        | 2/3        |
| critical_any      | T07       | 0/4        | 2/2        |
| critical_any      | T23       | 0/2        | 3/4        |
| critical_any      | T27       | 0/5        | 3/3        |
| critical_any      | T32       | 0/5        | 3/3        |
| critical_any      | T39       | 0/2        | 2/3        |

## Labelled subset cross-check

| version   |   n_labelled |   label_overall_fail_rate |   judge_overall_fail_rate_same_items |   label_J1_fail |   label_J2_fail |   label_J3_fail |   label_J4_fail |   label_J6_fail |
|:----------|-------------:|--------------------------:|-------------------------------------:|----------------:|----------------:|----------------:|----------------:|----------------:|
| v1        |           30 |                     0.067 |                                  0.1 |           0.033 |           0.033 |               0 |           0.033 |           0     |
| v2        |           30 |                     0.233 |                                  0.2 |           0.133 |           0.1   |               0 |           0.1   |           0.033 |

## Length (words)

| version   |   median |   p90 |   max |   mean |   pct_over_60 |   pct_over_80 |
|:----------|---------:|------:|------:|-------:|--------------:|--------------:|
| v1        |     61.5 |  87.2 |   218 |   65.4 |          52.7 |          15.3 |
| v2        |     35   |  43.1 |    56 |   34.7 |           0   |           0   |
