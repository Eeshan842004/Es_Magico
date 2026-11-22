# Judge vs reference-label agreement: gemini

60 of 60 labelled items scored by this judge (60 held-out, 0 calibration).

## Held-out set (headline)

| criterion   | name                  |   n |   label_fail |   judge_fail |   raw_agree_pct |   kappa |   ci_low |   ci_high |   tp |   fn |   fp |   tn |   recall_on_label_fail |   precision_on_judge_fail | trust                                                |
|:------------|:----------------------|----:|-------------:|-------------:|----------------:|--------:|---------:|----------:|-----:|-----:|-----:|-----:|-----------------------:|--------------------------:|:-----------------------------------------------------|
| J1          | Faithfulness          |  60 |            5 |            5 |            96.7 |   0.782 |    0.302 |     1     |    4 |    1 |    1 |   54 |                  0.8   |                     0.8   | substantial: trust for aggregate comparison          |
| J2          | Critical completeness |  60 |            4 |            4 |            90   |   0.196 |   -0.087 |     0.64  |    1 |    3 |    3 |   53 |                  0.25  |                     0.25  | weak: do not use for decisions                       |
| J3          | Current state         |  60 |            0 |            1 |            98.3 |   0     |    0     |     0     |    0 |    0 |    1 |   59 |                nan     |                     0     | weak: do not use for decisions                       |
| J4          | Next step             |  60 |            4 |            6 |            96.7 |   0.783 |    0.314 |     1     |    4 |    0 |    2 |   54 |                  1     |                     0.667 | substantial: trust for aggregate comparison          |
| J5          | Usefulness/noise      |  60 |            1 |            0 |            98.3 |   0     |    0     |     0     |    0 |    1 |    0 |   59 |                  0     |                   nan     | weak: do not use for decisions                       |
| J6          | Tone & safety         |  60 |            1 |            0 |            98.3 |   0     |    0     |     0     |    0 |    1 |    0 |   59 |                  0     |                   nan     | weak: do not use for decisions                       |
| overall     | Overall (J1-4,J6)     |  60 |            9 |            9 |            86.7 |   0.477 |    0.109 |     0.772 |    5 |    4 |    4 |   47 |                  0.556 |                     0.556 | moderate: use with caution, human-review judge FAILs |

## Calibration set (the judge prompt may be tuned on this, so it is not the headline)

| note                                             |
|:-------------------------------------------------|
| none: the judge prompt was never tuned on labels |

## Version bias (overall verdict)

| version   |   n |   label_fail_rate |   judge_fail_rate |   raw_agree_pct |   kappa |
|:----------|----:|------------------:|------------------:|----------------:|--------:|
| v1        |  30 |             0.067 |               0.1 |            90   |   0.348 |
| v2        |  30 |             0.233 |               0.2 |            83.3 |   0.51  |

## Length bias

Spearman(words, label PASS) = 0.16; Spearman(words, judge PASS) = 0.11 (n=60)
