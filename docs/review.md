# Review: problems found in this evaluation, and what changed

| Question | Found | Change |
|---|---|---|
| Were the first labels independent of the judges? | No. They were written after the judge verdicts had been read | Dropped, with their kappa. Fresh sample of 60 with no overlap, and the limit stated in NOTES |
| Do the headline examples hold in the raw text? | T23 did not: v1 drops the same safety instruction in 4 of 5 runs | Removed as a regression. Examples are now counted by `src/evidence.py` |
| Is the ship rule computed as written? | Rule 3 compared detectors instead of failure types | Fixed. It now passes; rules 1, 2 and 4 still fail |
| Is the gap one conversation? | No. Leave-one-out stays above zero for both judges | `src/robustness.py` |
| Does it survive multiple testing? | One critical criterion per judge, a different one for each | Reported |
| Does the judge reward length? | No association for Gemini. For gpt-oss, longer v1 summaries fail more, which can't be separated from harder conversations | Reported as an association |
| Does the judge punish v2's layout? | gpt-oss: 0 of 10 overall verdicts changed. Gemini untested | Reported with that scope |
| Where do the judges disagree? | Mostly rubric ambiguity, plus errors on both sides | `src/judge_disagreements.py` |
| Can a stranger re-run it? | `make` is often missing and dependencies were unpinned | `python src/reproduce.py`, pinned versions |
| Would the agreement script run? | It failed on partial judge coverage | Fixed and tested on fixture labels |
| Can a failed run corrupt results? | It could write empty tables | Partial experiments write nothing |
| Are the thresholds in config? | Length limits were hard-coded | Moved to `config.yaml` |

Decided against: editing expectations after results (cases excluded in a sensitivity run instead), testing v3 on a different generator, and mixing the two judges into one dataset.
