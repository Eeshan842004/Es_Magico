"""kie.ai (Gemini) client: retries, disk cache, cost log. Two backends.

This is the ONLY file that talks to the provider. To switch provider, change
only this file (README, "how to switch provider").

Why two backends (found with the smoke test, see docs/decision_log.md):
- "native"  -> POST https://api.kie.ai/gemini/v1/models/{model}:generateContent
               The only route that serves gemini-3-8-flash (the generator).
- "openai"  -> POST https://api.kie.ai/{model}/v1/chat/completions
               Serves gemini-3-pro / 3.1-pro (the judge) and supports a strict
               JSON schema via response_format.
- "groq"    -> POST https://api.groq.com/openai/v1/chat/completions (free tier)
               Second, cross-family judge (openai/gpt-oss-120b) added when the kie.ai
               credits ran out. Several keys (GROQ_API_KEY_1, _2, ...) are rotated:
               on a 429 we switch key, and honour `retry-after` when all are busy.

Design choices (all about "never re-spend money, never leak the key"):
- Every call is cached on disk, keyed by a hash of everything that could change
  the answer. `cache_key_extra` (we pass the sample index) makes N samples N
  distinct calls, while a re-run of the whole pipeline is free.
- Every real (non-cached) call appends a line to outputs/cost_log.jsonl.
- The API key comes from the environment and is never printed or logged.
- Set env FRESH=1 to bypass the cache.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import threading
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache"
COST_LOG = ROOT / "outputs" / "cost_log.jsonl"
_log_lock = threading.Lock()

load_dotenv(ROOT / ".env")

NATIVE_URL = "https://api.kie.ai/gemini/v1/models/{model}:generateContent"
OPENAI_URL = "https://api.kie.ai/{model}/v1/chat/completions"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class _GroqKeys:
    """Round-robin over the Groq keys; a key that hits a long (daily) limit is parked until its reset time."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.i = 0
        self.parked_until: dict[int, float] = {}

    def keys(self) -> list[str]:
        out, n = [], 1
        while os.environ.get(f"GROQ_API_KEY_{n}"):
            out.append(os.environ[f"GROQ_API_KEY_{n}"].strip())
            n += 1
        if not out:
            raise LLMError("No GROQ_API_KEY_1 in .env")
        return out

    def pick(self) -> tuple[int, str]:
        ks = self.keys()
        with self.lock:
            now = time.time()
            for _ in range(len(ks)):
                idx = self.i % len(ks)
                self.i += 1
                if self.parked_until.get(idx, 0) <= now:
                    return idx, ks[idx]
            idx = min(self.parked_until, key=self.parked_until.get)  # all parked: wait for the soonest
            wait = self.parked_until[idx] - now
        if wait > 300:  # every key is on a long (daily) limit: stop cleanly instead of sleeping for hours
            raise LLMError(f"all Groq keys rate-limited for {wait / 60:.0f} more minutes (daily quota)")
        time.sleep(max(0.0, wait))
        return idx, ks[idx]

    def park(self, idx: int, seconds: float) -> None:
        with self.lock:
            self.parked_until[idx] = time.time() + seconds


GROQ_KEYS = _GroqKeys()


class LLMError(RuntimeError):
    """Raised when a call fails after all retries. We fail loudly on purpose."""


def _api_key() -> str:
    key = os.environ.get("KIE_API_KEY", "").strip()
    if not key:
        raise LLMError("KIE_API_KEY is not set. Copy .env.example to .env and add it.")
    return key


def _cache_path(backend, model, messages, params, extra) -> Path:
    blob = json.dumps(
        {"backend": backend, "model": model, "messages": messages, "params": params, "extra": extra},
        sort_keys=True, ensure_ascii=False,
    )
    return CACHE_DIR / (hashlib.sha256(blob.encode("utf-8")).hexdigest() + ".json")


def _log_cost(record: dict) -> None:
    COST_LOG.parent.mkdir(parents=True, exist_ok=True)
    with _log_lock, COST_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _build_native(messages, reasoning_effort, temperature, response_format):
    """Convert OpenAI-style messages to the native Gemini body."""
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    contents = [
        {"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
        for m in messages if m["role"] != "system"
    ]
    gen_cfg: dict = {"thinkingConfig": {"includeThoughts": False, "thinkingLevel": reasoning_effort}}
    if temperature is not None:
        gen_cfg["temperature"] = temperature
    body = {"contents": contents, "generationConfig": gen_cfg}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    return body


def _build_openai(messages, reasoning_effort, temperature, response_format):
    # stream/include_thoughts default to TRUE on this provider: always override.
    body: dict = {"messages": messages, "stream": False, "include_thoughts": False,
                  "reasoning_effort": reasoning_effort}
    if response_format is not None:
        body["response_format"] = response_format
    if temperature is not None:
        body["temperature"] = temperature
    return body


def _build_groq(messages, reasoning_effort, temperature, response_format):
    body: dict = {"messages": messages, "reasoning_effort": reasoning_effort, "include_reasoning": False}
    if response_format is not None:
        body["response_format"] = response_format
    if temperature is not None:
        body["temperature"] = temperature
    return body


def _parse_native(data: dict) -> tuple[str, dict | None]:
    cand = data["candidates"][0]
    parts = cand.get("content", {}).get("parts", [])
    # Drop any "thought" parts defensively even though includeThoughts is False.
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    if not text.strip():
        raise KeyError(f"empty candidate, finishReason={cand.get('finishReason')}")
    return text, data.get("usageMetadata")


def _parse_openai(data: dict) -> tuple[str, dict | None]:
    return data["choices"][0]["message"]["content"], data.get("usage")


def chat(
    model: str,
    messages: list[dict],
    *,
    backend: str = "native",
    reasoning_effort: str = "low",
    response_format: dict | None = None,
    temperature: float | None = None,
    cache_key_extra: str | None = None,
    purpose: str = "gen",
    retries: int = 5,
    use_cache: bool | None = None,
    timeout: int = 180,
) -> dict:
    """One chat completion -> dict(text, usage, credits, latency_ms, cached, raw)."""
    if use_cache is None:
        use_cache = os.environ.get("FRESH", "") not in ("1", "true")
    if backend == "native":
        url, body, parse = NATIVE_URL.format(model=model), _build_native(messages, reasoning_effort, temperature, response_format), _parse_native
    elif backend == "openai":
        url, body, parse = OPENAI_URL.format(model=model), _build_openai(messages, reasoning_effort, temperature, response_format), _parse_openai
    elif backend == "groq":
        url, body, parse = GROQ_URL, _build_groq(messages, reasoning_effort, temperature, response_format), _parse_openai
        body["model"] = model
    else:
        raise ValueError(f"unknown backend {backend}")

    cpath = _cache_path(backend, model, messages, {k: v for k, v in body.items() if k != "messages"}, cache_key_extra)
    if backend == "groq":
        # Set AFTER the cache key on purpose: the free tier seems to count the completion budget against tokens/minute,
        # so a cap (about 2x the ~1.7K tokens a judgement uses) speeds things up without changing answers.
        body["max_completion_tokens"] = 3500
    if use_cache and cpath.exists():
        out = json.loads(cpath.read_text(encoding="utf-8"))
        out["cached"] = True
        return out
    if os.environ.get("CACHE_ONLY") == "1":  # rebuild outputs from cache without spending anything
        raise LLMError("not in cache (CACHE_ONLY=1)")

    headers = {"Authorization": f"Bearer {_api_key()}" if backend != "groq" else "", "Content-Type": "application/json"}
    last_err = "unknown"
    key_idx = None
    for attempt in range(retries + 1):
        if backend == "groq":
            key_idx, key = GROQ_KEYS.pick()
            headers["Authorization"] = f"Bearer {key}"
        t0 = time.time()
        try:
            resp = requests.post(url, headers=headers, json=body, timeout=timeout)
        except requests.RequestException as e:
            last_err, resp = f"network error: {type(e).__name__}", None
        if resp is not None:
            if resp.status_code == 401:
                raise LLMError("401 Unauthorized: check KIE_API_KEY.")
            if resp.status_code == 200:
                data = resp.json()
                # kie.ai returns HTTP 200 with {"code": 4xx, "msg": ...} for some errors.
                if isinstance(data, dict) and "code" in data and "choices" not in data and "candidates" not in data:
                    last_err = f"body code {data.get('code')}: {data.get('msg')}"
                    if data.get("code") in (401, 402, 404, 410, 422):  # not retryable
                        raise LLMError(last_err)
                else:
                    try:
                        text, usage = parse(data)
                    except (KeyError, IndexError, TypeError) as e:
                        last_err = f"bad response shape: {e}"  # e.g. empty output: retry
                    else:
                        latency_ms = int((time.time() - t0) * 1000)
                        out = {"text": text, "usage": usage, "credits": data.get("credits_consumed"),
                               "latency_ms": latency_ms, "raw": data}
                        CACHE_DIR.mkdir(exist_ok=True)
                        cpath.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
                        _log_cost({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "purpose": purpose,
                                   "model": model, "backend": backend, "usage": usage,
                                   "credits": data.get("credits_consumed"), "latency_ms": latency_ms,
                                   "cache_key_extra": cache_key_extra})
                        out["cached"] = False
                        return out
            elif resp.status_code == 429 and backend == "groq":
                wait = float(resp.headers.get("retry-after", "10") or 10)
                GROQ_KEYS.park(key_idx, wait)  # rotate to the other key; this one rests
                last_err = f"HTTP 429 (key {key_idx + 1}, retry-after {wait:.0f}s)"
                continue  # no extra sleep: pick() waits only if every key is parked
            elif resp.status_code == 429 or resp.status_code >= 500:
                last_err = f"HTTP {resp.status_code}"
            else:
                raise LLMError(f"HTTP {resp.status_code}: {resp.text[:300]}")
        if attempt < retries:
            time.sleep(min(2 ** attempt, 30) + random.random())  # 1,2,4,8,16s (capped) + jitter
    raise LLMError(f"Failed after {retries + 1} attempts: {last_err}")
