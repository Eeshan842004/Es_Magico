PY ?= python
# FRESH=1 makes every step bypass the cache (re-calls the API). Default: cached, free.
export FRESH

.PHONY: reproduce smoke generate check sample judge label agree analyze report test all

reproduce: ; $(PY) src/reproduce.py   # free: cache only, no API calls
smoke:     ; $(PY) src/smoke.py
generate:  ; $(PY) src/generate.py
check:     ; $(PY) src/run_checks.py
sample:    ; $(PY) src/sample_labels.py   # blind 60-item labelling sample (refuses to overwrite once labels exist)
# gemini: pre-registered judge, rebuilt from cache only (kie.ai credits ran out at 181/300).
# gptoss: cross-family judge on Groq's free tier (labelled items first, then random order until quota ends).
judge:
	-CACHE_ONLY=1 $(PY) src/judge.py --judge gemini
	-$(PY) src/judge.py --judge gptoss --labelled-first
label:     ; $(PY) src/label_tool.py
agree:     ; -$(PY) src/agreement.py   # warns (does not stop `all`) if the labels file is missing
	-$(PY) src/judge_vs_judge.py
analyze:   ; $(PY) src/analyze.py
	$(PY) src/sensitivity_golden.py
	$(PY) src/robustness.py
	$(PY) src/evidence.py
	$(PY) src/judge_disagreements.py
report:    ; $(PY) src/report_tables.py
test:      ; $(PY) -m pytest -q tests

# `label` is not part of `all`: it needs a person at the keyboard.
all: generate check judge sample agree analyze report test
