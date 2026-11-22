# False-alarm audit of the automated checks

Flags for C4, C7, C9 and C11 were read individually. C2 and C3 are mechanical, so their flag details were tabulated and sampled. Precision = true failures / flagged.

| Check | Flagged first run | True | Precision | Change | After |
|---|---|---|---|---|---|
| C4 personal data | 20 | 20 | 100% | none | 20/20 |
| C7 critical anchors | 13 | 3 | 23% | dates normalised ("November 8" = "8 Nov"). All 10 false alarms were on v1 | 3/3 |
| C9 golden patterns | 36 | 29 | 81% | T10 `abuse` pattern removed: its 7 flags were attributed mentions, which gap G12 allows | 29/29 |
| C11 language | 1 | 1 | 100% | none | 1/1 |
| C2 single paragraph | 178 | not all read | | none. v1 28, v2 150 | |
| C3 over 80 words | 23 | word count | | none | |
| C3 over 60 words | 79 | word count | | none. A warning only | |
| C1, C5, C6, C8, C10 | 0 | | unknown | unit fixtures only | |

A check with zero flags is not proof that nothing is wrong. C8 sees IDs, amounts and dates, so it cannot see an invented refund with no number (T27). The C7 and C9 changes were made after outputs were seen and before any judge verdict was produced.
