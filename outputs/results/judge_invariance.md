# gpt-oss judge: self-consistency and format invariance

'Before' is the first judgement of each summary (outputs/judge_gptoss.jsonl).

### Self-consistency: the same summary judged again, unchanged (judge noise), v2 (n=10)

| criterion | FAIL rate before | FAIL rate after | verdict flips | kappa |
|---|---|---|---|---|
| J1 | 0.20 | 0.30 | 1 (10%) | 0.74 |
| J2 | 0.70 | 0.70 | 0 (0%) | 1.00 |
| J3 | 0.00 | 0.00 | 0 (0%) | n/a |
| J4 | 0.00 | 0.10 | 1 (10%) | 0.00 |
| J5 | 0.00 | 0.00 | 0 (0%) | n/a |
| J6 | 0.00 | 0.10 | 1 (10%) | 0.00 |
| overall_fail | 0.70 | 0.70 | 0 (0%) | 1.00 |

### Self-consistency, v2 only (the noise baseline for the test below) (n=10)

| criterion | FAIL rate before | FAIL rate after | verdict flips | kappa |
|---|---|---|---|---|
| J1 | 0.20 | 0.30 | 1 (10%) | 0.74 |
| J2 | 0.70 | 0.70 | 0 (0%) | 1.00 |
| J3 | 0.00 | 0.00 | 0 (0%) | n/a |
| J4 | 0.00 | 0.10 | 1 (10%) | 0.00 |
| J5 | 0.00 | 0.00 | 0 (0%) | n/a |
| J6 | 0.00 | 0.10 | 1 (10%) | 0.00 |
| overall_fail | 0.70 | 0.70 | 0 (0%) | 1.00 |

### Format invariance: the same v2 summaries with labels and line breaks removed (n=10)

| criterion | FAIL rate before | FAIL rate after | verdict flips | kappa |
|---|---|---|---|---|
| J1 | 0.20 | 0.10 | 1 (10%) | 0.62 |
| J2 | 0.70 | 0.70 | 0 (0%) | 1.00 |
| J3 | 0.00 | 0.00 | 0 (0%) | n/a |
| J4 | 0.00 | 0.00 | 0 (0%) | n/a |
| J5 | 0.00 | 0.10 | 1 (10%) | 0.00 |
| J6 | 0.00 | 0.00 | 0 (0%) | n/a |
| overall_fail | 0.70 | 0.70 | 0 (0%) | 1.00 |

Reading: if the flips in the format test are about the same as the v2 noise baseline, the judge is grading content, not layout. If FAIL rates drop a lot once the labels are removed, the judge was penalising v2's format.

Calls failed: 0.
