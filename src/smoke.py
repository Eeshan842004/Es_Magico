"""`make smoke`: find out what actually works on kie.ai before building on it.

Checks each candidate (model, backend) with a trivial prompt, then response_format
on the judge, then whether temperature changes anything. Uses FRESH calls and
never prints the key. Results observed on 2026-11-20 are in docs/decision_log.md.
"""
from __future__ import annotations

import json
import os
import sys

os.environ["FRESH"] = "1"
from llm_client import LLMError, chat  # noqa: E402

MSG = [{"role": "user", "content": "Reply with the word OK."}]
CANDIDATES = [
    ("gemini-3-8-flash", "native"), ("gemini-3-8-flash", "openai"),
    ("gemini-3-flash", "native"), ("gemini-3-flash", "openai"),
    ("gemini-2.5-flash", "openai"),
    ("gemini-3-pro", "openai"), ("gemini-3.1-pro", "openai"),
]


def attempt(model, backend, **kw):
    try:
        r = chat(model, MSG, backend=backend, retries=0, purpose="smoke", timeout=90, **kw)
        return True, "OK " + r["text"].strip()[:20].replace("\n", " ") + f" credits={r['credits']}"
    except (LLMError, KeyError, ValueError) as e:
        return False, "FAIL " + str(e)[:80]


def main() -> int:
    ok = {}
    print(f"{'model':18} {'backend':8} result")
    for model, backend in CANDIDATES:
        good, msg = attempt(model, backend)
        print(f"{model:18} {backend:8} {msg}")
        if good:
            ok[(model, backend)] = True
    if not ok:
        print("Nothing worked: check the key.")
        return 1

    print("\n-- response_format (strict JSON schema) on judge --")
    schema = {"type": "json_schema", "json_schema": {"name": "t", "strict": True, "schema": {
        "type": "object", "properties": {"answer": {"type": "string"}},
        "required": ["answer"], "additionalProperties": False}}}
    try:
        r = chat("gemini-3-pro", [{"role": "user", "content": 'Return JSON {"answer":"OK"}'}], backend="openai",
                 response_format=schema, reasoning_effort="high", purpose="smoke", retries=0)
        print("parsed:", json.loads(r["text"]))
    except Exception as e:  # noqa: BLE001
        print("FAIL:", str(e)[:100])

    print("\n-- is temperature honoured on the generator? (4 calls each, same prompt) --")
    q = [{"role": "user", "content": "Write a 12-word sentence about a lamp."}]
    for temp in (0.0, 1.5):
        outs = {chat("gemini-3-8-flash", q, backend="native", temperature=temp, purpose="smoke",
                     cache_key_extra=f"smoke{i}")["text"].strip()[:80] for i in range(4)}
        print(f"temperature={temp}: {len(outs)} distinct outputs of 4")
    print("If temperature=0 still gives several distinct outputs, it is not controllable: say so in NOTES.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
