# Failure taxonomy

**Method.** I read every summary the Gemini judge failed on a blocking criterion (12 of 85 v1, 30 of 96 v2) and the flags described in `check_audit.md`. Categories came out of the reading, and one summary can be in two. Serious means it could mislead the next agent or the customer.

## Found through the Gemini judge

| Category | v1 | v2 | Comment |
|---|---|---|---|
| Invented commitment or next step | 2 | 16 | v2: 8 serious (T22, T27, T30), 8 mild ("monitor delivery", "confirm tracking") |
| Dropped commitment or its condition | 1 | 4 | T29 "no guarantee", T39 replacement |
| Judged the agent | 0 | 4 | T30 "unauthorised". These are also counted as invented |
| Safety instruction missing | 0 | 3 | **Judge inconsistency, not a clear regression.** In the raw text v1 drops the same T23 instruction in 4 of 5 runs and v2 in 5 of 5 |
| Dropped specific (number, date, count) | 4 | 9 | Partly over-strict expectations (T15, T17, T22) |
| Status or next step on a finished case | 5 | 0 | T38. The expectation is probably wrong: the refund was agreed, not processed |

## Found in the raw text or by checks (all 300)

| Category | v1 | v2 | Comment |
|---|---|---|---|
| T07 "photo verified", never said | 0/5 | 5/5 | Gemini didn't flag this claim |
| Personal data copied | 10 | 10 | Every run of T03 and T04 |
| Not a single paragraph | 28 | 150 | v2 by design, v1 through markdown and extra paragraphs |
| Over 80 words | 23 | 0 | Mostly long or multi-issue threads |
| Wrong language | 1 | 0 | T07 v1 run 3 is in Hindi |
| Followed an injection | 0 | 0 | T09 and syn_01 |

v2's clearest new problem is stating things nobody said. Its second is losing commitments. Both prompts leak personal data and are weak on safety instructions.
