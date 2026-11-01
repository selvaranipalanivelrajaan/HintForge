"""LLM calls with automatic fallback, plus token and cost tracking."""

import threading

from openai import OpenAI

from app.config import get_settings

# USD per 1M tokens (input, output). Check each provider's pricing page and
# update these numbers; they drive the cost shown at /usage.
PRICES = {
    "groq": (0.59, 0.79),
    "gemini": (0.30, 2.50),
}

USAGE = {
    "calls": 0,
    "fallbacks": 0,
    "errors": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "cost_usd": 0.0,
}
_lock = threading.Lock()


class LLMUnavailable(RuntimeError):
    """Raised when every configured provider failed."""


def _providers() -> list[dict]:
    s = get_settings()
    groq = {
        "name": "groq",
        "base_url": "https://api.groq.com/openai/v1",
        "api_key": s.groq_api_key,
        "model": s.primary_model,
    }
    gemini = {
        "name": "gemini",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "api_key": s.gemini_api_key,
    }
    if s.groq_api_key:
        # two providers: Groq first, Gemini as fallback
        return [groq, {**gemini, "model": s.fallback_model}]
    # one key: Gemini main model first, lighter Gemini model as fallback
    return [{**gemini, "model": s.gemini_model}, {**gemini, "model": s.fallback_model}]


def _call(provider: dict, messages: list[dict], max_tokens: int):
    client = OpenAI(
        api_key=provider["api_key"],
        base_url=provider["base_url"],
        timeout=20,
        max_retries=1,
    )
    r = client.chat.completions.create(model=provider["model"], messages=messages, max_tokens=max_tokens)
    return r.choices[0].message.content, r.usage.prompt_tokens, r.usage.completion_tokens


def chat(messages: list[dict], max_tokens: int = 500) -> dict:
    errors = []
    for i, p in enumerate(_providers()):
        if not p["api_key"]:
            continue
        try:
            text, pt, ct = _call(p, messages, max_tokens)
        except Exception as e:  # any failure -> try the next model
            errors.append(f"{p['name']}/{p['model']}: {type(e).__name__}")
            with _lock:
                USAGE["errors"] += 1
            continue
        in_price, out_price = PRICES[p["name"]]
        cost = pt / 1e6 * in_price + ct / 1e6 * out_price
        with _lock:
            USAGE["calls"] += 1
            USAGE["fallbacks"] += 1 if i > 0 else 0
            USAGE["prompt_tokens"] += pt
            USAGE["completion_tokens"] += ct
            USAGE["cost_usd"] = round(USAGE["cost_usd"] + cost, 6)
        return {
            "answer": text,
            "provider": p["name"],
            "model": p["model"],
            "prompt_tokens": pt,
            "completion_tokens": ct,
            "cost_usd": round(cost, 6),
        }
    raise LLMUnavailable("; ".join(errors) or "no API keys configured")


def get_usage() -> dict:
    with _lock:
        return dict(USAGE)
