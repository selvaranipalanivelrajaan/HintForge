import pytest
from fastapi.testclient import TestClient

from app import llm
from app.config import get_settings
from app.main import app

client = TestClient(app)


@pytest.fixture
def keys(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-groq")
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_usage_endpoint():
    r = client.get("/usage")
    assert r.status_code == 200
    assert "cost_usd" in r.json()


def test_fallback_when_primary_fails(keys, monkeypatch):
    def fake_call(provider, messages, max_tokens):
        if provider["name"] == "groq":
            raise RuntimeError("primary down")
        return "hello", 10, 5

    monkeypatch.setattr(llm, "_call", fake_call)
    out = llm.chat([{"role": "user", "content": "hi"}])
    assert out["provider"] == "gemini"
    assert out["prompt_tokens"] == 10


def test_chat_endpoint_503_when_all_fail(keys, monkeypatch):
    def always_fail(provider, messages, max_tokens):
        raise RuntimeError("down")

    monkeypatch.setattr(llm, "_call", always_fail)
    r = client.post("/chat", json={"prompt": "hi"})
    assert r.status_code == 503
