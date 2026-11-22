"""The system under test: the starter's summariser, with the provider call swapped for llm_client.

What is deliberately UNCHANGED from starter/summariser/summarise.py:
  - the prompt files (prompts/summariser_v1.txt and _v2.txt are byte-for-byte copies),
  - the message layout: system = prompt text, user = "Conversation:\\n\\n" + render(thread),
  - the nominal temperature (0.7).
What changed, and why (also listed in NOTES.md):
  - provider call -> llm_client.chat (kie.ai native Gemini; the starter's OpenAI-style call cannot reach
    the flash model),
  - returns metadata (usage, credits, latency) and takes a sample index so N samples are N distinct,
    cacheable calls,
  - errors raise instead of calling sys.exit / crashing with KeyError (the starter crashed on an HTTP 200
    error body during recon).
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

import yaml

from golden import render
from llm_client import chat

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))


def gen_settings() -> dict:
    """Generator settings; identical for v1 and v2 (the prompt is the only variable)."""
    return {
        "model": os.environ.get("GEN_MODEL") or CFG["models"]["gen"],
        "backend": CFG["models"]["gen_backend"],
        "reasoning_effort": CFG["gen_params"]["reasoning_effort"],
        "temperature": CFG["gen_params"]["temperature"],
    }


def load_prompt(version: str) -> str:
    return (ROOT / "prompts" / f"summariser_{version}.txt").read_text(encoding="utf-8").strip()


def prompt_sha(version: str) -> str:
    return hashlib.sha256(load_prompt(version).encode("utf-8")).hexdigest()[:12]


def summarise(conv: dict, version: str, sample_idx: int = 0) -> dict:
    s = gen_settings()
    messages = [
        {"role": "system", "content": load_prompt(version)},
        {"role": "user", "content": "Conversation:\n\n" + render(conv)},
    ]
    r = chat(
        s["model"], messages, backend=s["backend"], reasoning_effort=s["reasoning_effort"],
        temperature=s["temperature"], cache_key_extra=f"gen|{version}|{conv['id']}|s{sample_idx}",
        purpose="gen", retries=CFG["retries"],
    )
    return {"text": r["text"].strip(), "usage": r["usage"], "credits": r["credits"],
            "latency_ms": r["latency_ms"], "cached": r["cached"], "settings": s}
