# Judge vs reference-label agreement: gptoss

60 of 60 labelled items scored by this judge (60 held-out, 0 calibration).

## Held-out set (headline)

| criterion   | name                  |   n |   label_fail |   judge_fail |   raw_agree_pct |   kappa |   ci_low |   ci_high |   tp |   fn |   fp |   tn |   recall_on_label_fail |   precision_on_judge_fail | trust                                                |
|:------------|:----------------------|----:|-------------:|-------------:|----------------:|--------:|---------:|----------:|-----:|-----:|-----:|-----:|-----------------------:|--------------------------:|:-----------------------------------------------------|
| J1          | Faithfulness          |  60 |            5 |           15 |            83.3 |   0.429 |    0.127 |     0.702 |    5 |    0 |   10 |   45 |                    1   |                     0.333 | moderate: use with caution, human-review judge FAILs |
| J2          | Critical completeness |  60 |            4 |           19 |            75   |   0.267 |    0.061 |     0.498 |    4 |    0 |   15 |   41 |                    1   |                     0.211 | weak: do not use for decisions                       |
| J3          | Current state         |  60 |            0 |            2 |            96.7 |   0     |    0     |     0     |    0 |    0 |    2 |   58 |                  nan   |                     0     | weak: do not use for decisions                       |
| J4          | Next step             |  60 |            4 |            8 |            86.7 |   0.268 |   -0.071 |     0.634 |    2 |    2 |    6 |   50 |                    0.5 |                     0.25  | weak: do not use for decisions                       |
| J5          | Usefulness/noise      |  60 |            1 |            1 |            96.7 |  -0.017 |   -0.042 |     0     |    0 |    1 |    1 |   58 |                    0   |                     0     | weak: do not use for decisions                       |
| J6          | Tone & safety         |  60 |            1 |            6 |            88.3 |  -0.029 |   -0.071 |     0     |    0 |    1 |    6 |   53 |                    0   |                     0     | weak: do not use for decisions                       |
| overall     | Overall (J1-4,J6)     |  60 |            9 |           31 |            63.3 |   0.283 |    0.121 |     0.462 |    9 |    0 |   22 |   29 |                    1   |                     0.29  | weak: do not use for decisions                       |

## Calibration set (the judge prompt may be tuned on this, so it is not the headline)

| note                                             |
|:-------------------------------------------------|
| none: the judge prompt was never tuned on labels |

## Version bias (overall verdict)

| version   |   n |   label_fail_rate |   judge_fail_rate |   raw_agree_pct |   kappa |
|:----------|----:|------------------:|------------------:|----------------:|--------:|
| v1        |  30 |             0.067 |             0.4   |            66.7 |   0.194 |
| v2        |  30 |             0.233 |             0.633 |            60   |   0.3   |

## Length bias

Spearman(words, label PASS) = 0.16; Spearman(words, judge PASS) = 0.01 (n=60)
