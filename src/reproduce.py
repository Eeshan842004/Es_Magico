"""Rebuild every result from the committed cache, on any OS, without make, keys or network calls.

    python src/reproduce.py
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# (command, exit codes that are fine). The judges exit 1 because neither covers all 300; uncached items are skipped.
STEPS = [
    ("generate.py", {0}), ("run_checks.py", {0}),
    ("judge.py --judge gemini", {0, 1}), ("judge.py --judge gptoss --labelled-first", {0, 1}),
    ("judge_invariance.py --n 10 --v2-only", {0}), ("sample_labels.py", {0}),
    ("judge_vs_judge.py", {0}), ("judge_disagreements.py", {0}), ("analyze.py", {0}), ("sensitivity_golden.py", {0}),
    ("robustness.py", {0}), ("evidence.py", {0}), ("report_tables.py", {0}),
]


def main() -> int:
    env = {**os.environ, "CACHE_ONLY": "1", "FRESH": "", "PYTHONUTF8": "1"}
    steps = list(STEPS)
    if (ROOT / "labels" / "reference_labels.jsonl").exists():
        steps.append(("agreement.py", {0}))
    for cmd, fine in steps:
        script, *args = cmd.split()
        p = subprocess.run([sys.executable, str(ROOT / "src" / script), *args], cwd=ROOT, env=env,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if p.returncode not in fine or "Traceback" in p.stderr:
            print(f"FAILED  {cmd}\n{p.stdout[-1500:]}\n{p.stderr[-1500:]}")
            return 1
        print(f"ok      {cmd}", flush=True)
    print("Done. `git status` shows whether anything differs from the committed results.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
