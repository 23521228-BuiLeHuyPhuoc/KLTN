import json
import os
from pathlib import Path
import socket
import subprocess
import sys

import httpx
import pytest

from kiemchung.llm import LLMClient, LLMError, LLMResult, build_request, request_hash

MESSAGES = [{"role": "system", "content": "Return JSON."},
            {"role": "user", "content": "Pin 6 giờ"}]


@pytest.fixture(autouse=True)
def no_network_or_real_credentials(monkeypatch):
    for name in ["GEMINI_API_KEY", "GROQ_API_KEY", "GOOGLE_API_KEY"]:
        monkeypatch.delenv(name, raising=False)
    def blocked(*args, **kwargs):
        raise AssertionError("Automated tests must not access the network")
    monkeypatch.setattr(socket.socket, "connect", blocked)


def result(request, timeout):
    return LLMResult('{"value":6}', request["provider"], request["model"],
                     "model-revision", {"input_tokens": 10, "output_tokens": 5,
                     "total_tokens": 15}, "stop")


def client(tmp_path, transport=result, **kwargs):
    return LLMClient(tmp_path / "cache", tmp_path / "calls.jsonl", transport=transport, **kwargs)


def call(c, **kwargs):
    return c.call("groq", "model-a", MESSAGES, **kwargs)


def test_same_request_once_and_new_client_cache(tmp_path):
    calls = []
    def provider(req, timeout):
        calls.append(req)
        return result(req, timeout)
    first = call(client(tmp_path, provider))
    second = call(client(tmp_path, provider))
    assert len(calls) == 1 and not first.cache_hit and second.cache_hit
    assert first.text == second.text
    events = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
    assert [e["status"] for e in events] == ["success", "cache_hit"]
    assert events[1]["usage"] is None  # Cached token counts are not newly billed usage.
    entry = json.loads(next((tmp_path / "cache").glob("*.json")).read_text())
    assert entry["request"]["messages"] == MESSAGES
    assert entry["result"]["text"] == first.text


def test_cache_survives_new_process(tmp_path):
    call(client(tmp_path))
    code = '''
import sys
from kiemchung.llm import LLMClient
def forbidden(*args):
    raise AssertionError("Provider must not run in second process")
c = LLMClient(sys.argv[1], sys.argv[2], transport=forbidden)
r = c.call("groq", "model-a", [{"role":"system","content":"Return JSON."}, {"role":"user","content":"Pin 6 giờ"}])
assert r.cache_hit
print("persistent-cache-ok")
'''
    proc = subprocess.run([sys.executable, "-c", code, str(tmp_path / "cache"),
                           str(tmp_path / "second.jsonl")], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert "persistent-cache-ok" in proc.stdout


def test_hash_canonicalizes_dict_order_and_preserves_messages():
    a = build_request("groq", "a", MESSAGES, {"temperature": 0, "top_p": 1})
    b = build_request("groq", "a", MESSAGES, {"top_p": 1, "temperature": 0})
    assert request_hash(a) == request_hash(b)


@pytest.mark.parametrize("change", [
    {"model": "b"}, {"provider": "gemini"}, {"parameters": {"temperature": 1}},
    {"messages": [{"role": "user", "content": "Other prompt"}]},
    {"messages": [{"role": "system", "content": "New system"}, MESSAGES[1]]},
    {"json_output": True}, {"output_schema": {"type": "object"}}, {"mode": "mock"},
])
def test_hash_changes_for_every_output_affecting_input(change):
    args = dict(provider="groq", model="a", messages=MESSAGES, parameters={})
    a = build_request(**args)
    b = build_request(**(args | change))
    assert request_hash(a) != request_hash(b)


def test_temporary_failure_retried_without_caching_error(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr("kiemchung.llm.time.sleep", lambda delay: None)
    def flaky(req, timeout):
        calls.append(timeout)
        if len(calls) == 1:
            raise LLMError("temporary_api_error", status_code=429, retryable=True)
        return result(req, timeout)
    assert not call(client(tmp_path, flaky, timeout_s=7)).cache_hit
    assert calls == [7, 7]
    assert len(list((tmp_path / "cache").glob("*.json"))) == 1
    assert call(client(tmp_path, flaky)).cache_hit


@pytest.mark.parametrize("status,retryable,count,code", [
    (401, False, 1, "authentication_or_permission_denied"),
    (403, False, 1, "authentication_or_permission_denied"),
    (404, False, 1, "model_not_found_or_unavailable"),
    (400, False, 1, "invalid_request_check_api_key_model_parameters"),
    (429, True, 3, "temporary_api_error"), (503, True, 3, "temporary_api_error"),
])
def test_upstream_errors_safe_bounded_and_not_cached(tmp_path, monkeypatch, status, retryable, count, code):
    secret = "private-credential-not-for-logs"
    monkeypatch.setenv("GROQ_API_KEY", secret)
    monkeypatch.setattr("kiemchung.llm.time.sleep", lambda delay: None)
    calls = []
    class UpstreamError(Exception):
        status_code = status
    def fail(*args):
        calls.append(1)
        raise UpstreamError(f"Authorization: Bearer {secret}")
    c = client(tmp_path, fail)
    with pytest.raises(LLMError, match=code) as exc:
        call(c)
    assert len(calls) == count
    assert exc.value.retryable == retryable
    assert secret not in str(exc.value)
    assert not list((tmp_path / "cache").glob("*.json"))
    assert secret not in (tmp_path / "calls.jsonl").read_text()
    assert not call(client(tmp_path)).cache_hit


def test_timeout_retries_are_bounded(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr("kiemchung.llm.time.sleep", lambda delay: None)
    def fail(*args):
        calls.append(1)
        raise TimeoutError("unsafe external message")
    with pytest.raises(LLMError, match="network_or_timeout"):
        call(client(tmp_path, fail, max_retries=1))
    assert len(calls) == 2


def test_credentials_rejected_in_requests_and_responses(tmp_path, monkeypatch):
    secret = "gsk_" + "a" * 48
    monkeypatch.setenv("GROQ_API_KEY", secret)
    with pytest.raises(LLMError, match="credential_in_request"):
        client(tmp_path).call("groq", "a", [{"role": "user", "content": secret}])
    with pytest.raises(LLMError, match="unsupported_parameter"):
        call(client(tmp_path), parameters={"api_key": secret})
    def leaks(req, timeout):
        r = result(req, timeout)
        r.text = secret
        return r
    with pytest.raises(LLMError, match="credential_in_response"):
        call(client(tmp_path, leaks))
    assert not list((tmp_path / "cache").glob("*.json"))
    assert secret not in (tmp_path / "calls.jsonl").read_text()


def test_mock_cannot_satisfy_live_cache(tmp_path):
    call(client(tmp_path))
    with pytest.raises(LLMError, match="missing_api_key:GROQ_API_KEY"):
        call(client(tmp_path, transport=None))


@pytest.mark.parametrize("text,finish", [("", "stop"), ('{"cut":', "length"), ("blocked", "SAFETY")])
def test_incomplete_and_blocked_responses_not_cached(tmp_path, text, finish):
    def incomplete(req, timeout):
        r = result(req, timeout)
        r.text, r.finish_reason = text, finish
        return r
    with pytest.raises(LLMError, match="incomplete"):
        call(client(tmp_path, incomplete))
    assert not list((tmp_path / "cache").glob("*.json"))


def test_corrupt_cache_fails_without_spending_api_call(tmp_path):
    call(client(tmp_path))
    next((tmp_path / "cache").glob("*.json")).write_text('{}')
    with pytest.raises(LLMError, match="cache_corrupt"):
        call(client(tmp_path))


def test_groq_sdk_adapter_serialization(tmp_path, monkeypatch):
    import groq
    original = groq.Groq
    sent = []
    monkeypatch.setenv("GROQ_API_KEY", "test-only-groq-secret")
    def handle(request):
        sent.append(json.loads(request.content))
        assert request.extensions["timeout"]["read"] == 7
        return httpx.Response(200, json={"id": "mock-http", "object": "chat.completion",
            "created": 0, "model": "actual-model", "choices": [{"index": 0,
            "finish_reason": "stop", "message": {"role": "assistant", "content": '{"a":1}'}}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 4, "total_tokens": 15}})
    def factory(**kwargs):
        assert kwargs["max_retries"] == 0
        return original(**kwargs, http_client=httpx.Client(transport=httpx.MockTransport(handle)))
    monkeypatch.setattr(groq, "Groq", factory)
    r = call(client(tmp_path, None, timeout_s=7), parameters={"max_output_tokens": 200, "temperature": 0}, json_output=True)
    assert r.usage["total_tokens"] == 15 and r.actual_model == "actual-model"
    assert sent[0]["max_completion_tokens"] == 200
    assert sent[0]["response_format"] == {"type": "json_object"}
    assert sent[0]["messages"] == MESSAGES


def test_gemini_sdk_adapter_serialization(tmp_path, monkeypatch):
    from google import genai
    original = genai.Client
    sent = []
    monkeypatch.setenv("GEMINI_API_KEY", "test-only-google-secret")
    def handle(request):
        sent.append(json.loads(request.content))
        return httpx.Response(200, json={"modelVersion": "actual-gemini", "candidates": [{
            "content": {"role": "model", "parts": [{"text": '{"a":1}'}]}, "finishReason": "STOP"}],
            "usageMetadata": {"promptTokenCount": 11, "candidatesTokenCount": 4,
                              "totalTokenCount": 15, "thoughtsTokenCount": 0}})
    def factory(**kwargs):
        assert kwargs["vertexai"] is False
        options = kwargs["http_options"]
        assert options.timeout == 7000 and options.retry_options.attempts == 1
        options.client_args = {"transport": httpx.MockTransport(handle)}
        return original(**kwargs)
    monkeypatch.setattr(genai, "Client", factory)
    c = client(tmp_path, None, timeout_s=7)
    r = c.call("gemini", "model-a", MESSAGES, {"max_output_tokens": 200, "temperature": 0},
               json_output=True, output_schema={"type": "object", "properties": {"a": {"type": "integer"}}})
    assert r.usage["total_tokens"] == 15 and r.actual_model == "actual-gemini"
    assert sent[0]["systemInstruction"]["parts"][0]["text"] == MESSAGES[0]["content"]
    assert sent[0]["generationConfig"]["maxOutputTokens"] == 200
    assert sent[0]["generationConfig"]["responseMimeType"] == "application/json"
    assert "responseJsonSchema" in sent[0]["generationConfig"]


def test_git_ignore_and_tracking():
    root = Path(__file__).resolve().parents[1]
    assert subprocess.check_output(["git", "check-ignore", ".env"], cwd=root, text=True).strip() == ".env"
    assert not subprocess.check_output(["git", "ls-files", "--", ".env"], cwd=root, text=True).strip()
    for path in [".env.example", "data/thu_llm/cases.json", "ket_qua/llm_cache/probe.json", "ket_qua/calls.jsonl"]:
        assert subprocess.run(["git", "check-ignore", path], cwd=root, capture_output=True).returncode == 1
