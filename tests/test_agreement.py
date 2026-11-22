"""End-to-end test of src/agreement.py on FAKE labels in a temp folder.

The fake labels are derived from a judge's verdicts with deliberate flips, so the code paths (joins, kappa, CIs,
confusion plots, disagreement dump, partial labelling) are exercised. They are test fixtures only: this test never
reads or writes the real label file.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import agreement  # noqa: E402

KEY = ROOT / "labels" / "label_key.jsonl"
JUDGE = ROOT / "outputs" / "judge_gptoss.jsonl"
CRIT = ["J1", "J2", "J3", "J4", "J5", "J6"]


def _fake_labels(tmp_path: Path, keep_every: int = 1) -> Path:
    key = [json.loads(l) for l in KEY.read_text(encoding="utf-8").splitlines() if l.strip()]
    jud = {(r["conv_id"], r["version"], r["sample_idx"]): r for r in map(json.loads, JUDGE.read_text(encoding="utf-8").splitlines()) if r}
    rows = []
    for i, k in enumerate(key):
        if i % keep_every:
            continue
        j = jud.get((k["conv_id"], k["version"], k["sample_idx"]))
        labs = {c: (j[c] if j else 0) for c in CRIT}
        if i % 4 == 0:
            labs["J1"] = 1 - labs["J1"]  # deliberate disagreements
        rows.append({"item_id": k["item_id"], **labs, "note": "fixture"})
    p = tmp_path / "fake_labels.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return p


@pytest.mark.skipif(not JUDGE.exists(), reason="needs outputs/judge_gptoss.jsonl")
def test_agreement_runs_on_full_and_partial_labels(tmp_path):
    real = ROOT / "labels" / "reference_labels.jsonl"
    before = real.read_bytes() if real.exists() else None
    for keep in (1, 3):  # all 60 items, then a partial labelling session (every 3rd item)
        out = tmp_path / f"out{keep}"
        out.mkdir()
        labels = _fake_labels(tmp_path, keep)
        md = agreement.run_one(JUDGE, "gptoss", labels, out)
        assert md and "Held-out set" in md
        assert (out / "judge_agreement_gptoss.csv").exists()
        assert (out / "fig4_judge_vs_labels_gptoss.png").exists()
        assert (out / "judge_disagreements_gptoss.md").exists()
    # gemini only covers a random subset of summaries: must not crash, must use only the scored items
    md = agreement.run_one(ROOT / "outputs" / "judge.jsonl", "gemini", _fake_labels(tmp_path), tmp_path / "out1")
    assert md is None or "labelled items scored by this judge" in md
    after = real.read_bytes() if real.exists() else None
    assert before == after, "the test must never touch the real label file"
