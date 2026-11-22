"""Unit tests for the logic that produces the verdict: judge roll-up, paired comparison with missing judge data,
cache-only mode and Groq key rotation. No network calls."""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import llm_client  # noqa: E402
from analyze import compare  # noqa: E402
from judge import flatten, parse_json  # noqa: E402


def _parsed(**fails):
    keys = {"J1": "J1_faithfulness", "J2": "J2_critical_completeness", "J3": "J3_current_state", "J4": "J4_next_step",
            "J5": "J5_usefulness", "J6": "J6_tone_safety"}
    p = {v: {"reason": "r", "verdict": "FAIL" if fails.get(k) else "PASS"} for k, v in keys.items()}
    p.update({"overall": "PASS", "holistic_score_1_5": 4, "unsupported_claims": []})
    return p


def test_overall_is_recomputed_and_ignores_j5():
    assert flatten(_parsed(J5=1))["overall_fail"] == 0      # J5 (noise) never blocks
    assert flatten(_parsed(J6=1))["overall_fail"] == 1      # J6 blocks
    f = flatten(_parsed(J1=1))
    assert f["overall_fail"] == 1 and f["overall_model_says_fail"] == 0  # we do not trust the model's own roll-up


def test_parse_json_tolerates_code_fences():
    assert parse_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json('{"a": 2}') == {"a": 2}


def test_compare_drops_conversations_missing_a_version():
    rows = []
    for cid, (v1, v2) in {"A": (0, 1), "B": (0, 1), "C": (0, np.nan)}.items():
        rows += [{"conv_id": cid, "version": "v1", "x": v1}, {"conv_id": cid, "version": "v2", "x": v2}]
    r = compare(pd.DataFrame(rows), "x", "x")
    assert r["n_conversations"] == 2 and r["delta"] == pytest.approx(1.0)


def test_compare_is_paired_and_signed():
    rows = [{"conv_id": c, "version": v, "x": val} for c in "ABCDEF" for v, val in (("v1", 0.2), ("v2", 0.0))]
    r = compare(pd.DataFrame(rows), "x", "x")
    assert r["delta"] == pytest.approx(-0.2) and r["verdict"] == "improved"


def test_cache_only_never_calls_the_network(monkeypatch, tmp_path):
    monkeypatch.setattr(llm_client, "CACHE_DIR", tmp_path)
    monkeypatch.setenv("CACHE_ONLY", "1")
    monkeypatch.setattr(llm_client.requests, "post", lambda *a, **k: (_ for _ in ()).throw(AssertionError("network used")))
    with pytest.raises(llm_client.LLMError, match="not in cache"):
        llm_client.chat("m", [{"role": "user", "content": "hi"}], backend="groq", use_cache=True)


def test_cache_hit_returns_stored_answer(monkeypatch, tmp_path):
    monkeypatch.setattr(llm_client, "CACHE_DIR", tmp_path)
    msgs = [{"role": "user", "content": "hi"}]
    body = {k: v for k, v in llm_client._build_groq(msgs, "low", None, None).items() if k != "messages"}
    body["model"] = "m"
    path = llm_client._cache_path("groq", "m", msgs, body, "x")
    path.write_text(json.dumps({"text": "cached!", "usage": None, "credits": None, "latency_ms": 1, "raw": {}}), encoding="utf-8")
    assert llm_client.chat("m", msgs, backend="groq", reasoning_effort="low", cache_key_extra="x", use_cache=True)["text"] == "cached!"


def test_groq_keys_rotate_and_stop_on_long_limits(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY_1", "k1")
    monkeypatch.setenv("GROQ_API_KEY_2", "k2")
    monkeypatch.delenv("GROQ_API_KEY_3", raising=False)
    keys = llm_client._GroqKeys()
    assert {keys.pick()[1], keys.pick()[1]} == {"k1", "k2"}      # round robin
    keys.park(0, 60)
    assert all(keys.pick()[1] == "k2" for _ in range(3))           # parked key is skipped
    keys.park(1, 3600)
    keys.parked_until[0] = time.time() + 3600
    with pytest.raises(llm_client.LLMError, match="rate-limited"):  # all keys on a long limit: stop, don't sleep for an hour
        keys.pick()
