# Robustness of the v1 vs v2 result

Unit = conversation. 'v2 worse' = the conversation's v2 failure rate is higher than its v1 rate.

## Judge: gemini-3-pro

| metric | convs | v2 worse | v2 better | tied | sign-test p | leave-one-out delta range (pp) |
|---|---|---|---|---|---|---|
| Any critical failure | 30 | 11 | 1 | 18 | 0.006 | +18.9 to +23.2 |
| Judge overall FAIL | 30 | 11 | 2 | 17 | 0.022 | +15.5 to +22.4 |
| Faithfulness | 30 | 8 | 0 | 22 | 0.008 | +10.5 to +13.9 |
| Critical completeness | 30 | 6 | 1 | 23 | 0.125 | +8.6 to +12.0 |

Holm-adjusted Wilcoxon p, four pre-registered critical criteria:

| criterion | raw p | Holm-adjusted p |
|---|---|---|
| Faithfulness | 0.0115 | 0.0461 |
| Critical completeness | 0.0274 | 0.0823 |
| PII | 1.0000 | 1.0000 |
| Injection | 1.0000 | 1.0000 |

Pooled any-critical failure rate over all judged samples: v1 14.1% (n=85), v2 37.5% (n=96).

Length association inside each version (Spearman rho between word count and judge overall FAIL; a negative rho would mean longer summaries are passed more often; harder conversations also get longer summaries, so this is an association and cannot isolate a bias):

- v1: rho = +0.04 (p = 0.75, n = 85; words 32-218)
- v2: rho = -0.08 (p = 0.46, n = 96; words 19-53)

## Judge: gpt-oss-120b

| metric | convs | v2 worse | v2 better | tied | sign-test p | leave-one-out delta range (pp) |
|---|---|---|---|---|---|---|
| Any critical failure | 30 | 15 | 6 | 9 | 0.078 | +26.0 to +30.4 |
| Judge overall FAIL | 30 | 16 | 8 | 6 | 0.152 | +24.7 to +29.1 |
| Faithfulness | 30 | 14 | 8 | 8 | 0.286 | +12.5 to +18.2 |
| Critical completeness | 30 | 16 | 3 | 11 | 0.004 | +23.0 to +27.5 |

Holm-adjusted Wilcoxon p, four pre-registered critical criteria:

| criterion | raw p | Holm-adjusted p |
|---|---|---|
| Faithfulness | 0.0880 | 0.2639 |
| Critical completeness | 0.0007 | 0.0029 |
| PII | 1.0000 | 1.0000 |
| Injection | 1.0000 | 1.0000 |

Pooled any-critical failure rate over all judged samples: v1 40.9% (n=115), v2 65.5% (n=119).

Length association inside each version (Spearman rho between word count and judge overall FAIL; a negative rho would mean longer summaries are passed more often; harder conversations also get longer summaries, so this is an association and cannot isolate a bias):

- v1: rho = +0.29 (p = 0.00, n = 115; words 32-218)
- v2: rho = +0.09 (p = 0.35, n = 119; words 19-56)
