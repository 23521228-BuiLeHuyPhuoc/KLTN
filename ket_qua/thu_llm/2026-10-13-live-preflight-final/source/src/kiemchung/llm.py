"""Text-only Gemini/Groq calls, persistent JSON cache and JSONL audit trail.

Credentials are read only from environment variables, never from request config.
Transport injection is for offline tests and always uses a separate mock cache.
Use one caller at a time: the file cache does not coalesce concurrent requests.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import tempfile
import time
from typing import Any, Callable

KEY_ENV = {"gemini": "GEMINI_API_KEY", "groq": "GROQ_API_KEY"}
COMMON_PARAMS = {"temperature", "top_p", "max_output_tokens", "seed", "stop"}
PROVIDER_PARAMS = {"gemini": {"thinking_budget"}, "groq": {"reasoning_effort"}}


def canonical_json(value: Any) -> str:
    """Preserve list/message order and exact prompt text, sort object keys."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact(text: str) -> str:
    # Include all credential-shaped environment names, but never enumerate values.
    for name, value in os.environ.items():
        if value and re.search(r"KEY|TOKEN|SECRET|PASSWORD", name, re.I):
            text = text.replace(value, "[REDACTED]")
    return re.sub(r"(?:AIza[\w-]{20,}|gsk_[\w-]{16,}|sk-[\w-]{16,})",
                  "[REDACTED]", text)


class LLMError(RuntimeError):
    """Safe error without upstream exception text, URLs, headers or credentials."""

    def __init__(self, code: str, *, retryable: bool = False,
                 status_code: int | None = None):
        self.code, self.retryable, self.status_code = code, retryable, status_code
        super().__init__(code)


@dataclass
class LLMResult:
    text: str
    provider: str
    model: str
    actual_model: str | None
    usage: dict[str, int | None]
    finish_reason: str | None
    request_hash: str = ""
    cache_hit: bool = False
    elapsed_ms: float = 0.0
    generation_ms: float = 0.0
    mode: str = "live"


def build_request(provider: str, model: str, messages: list[dict[str, str]],
                  parameters: dict[str, Any] | None = None, *,
                  json_output: bool = False,
                  output_schema: dict[str, Any] | None = None,
                  mode: str = "live") -> dict[str, Any]:
    if provider not in KEY_ENV or not isinstance(model, str) or not model.strip():
        raise LLMError("invalid_provider_or_model")
    if not messages:
        raise LLMError("empty_messages")
    for i, msg in enumerate(messages):
        if (set(msg) != {"role", "content"} or
                msg["role"] not in {"system", "user", "assistant"} or
                not isinstance(msg["content"], str)):
            raise LLMError("invalid_message")
        if msg["role"] == "system" and i != 0:
            raise LLMError("system_message_must_be_first")
    if not any(m["role"] == "user" for m in messages):
        raise LLMError("user_message_required")
    params = parameters or {}
    if set(params) - COMMON_PARAMS - PROVIDER_PARAMS[provider]:
        raise LLMError("unsupported_parameter_or_credential_in_config")
    request = {"cache_version": 1, "adapter_version": 1, "mode": mode,
               "provider": provider, "model": model, "messages": messages,
               "parameters": params, "json_output": json_output,
               "output_schema": output_schema}
    try:
        encoded = canonical_json(request)
    except (TypeError, ValueError):
        raise LLMError("request_must_be_finite_json") from None
    if redact(encoded) != encoded:
        raise LLMError("credential_in_request")
    return json.loads(encoded)  # Detach nested mutable inputs.


def request_hash(request: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(request).encode("utf-8")).hexdigest()


def _safe_error(exc: Exception) -> LLMError:
    if isinstance(exc, LLMError):
        return exc
    status = getattr(exc, "status_code", None) or getattr(exc, "code", None)
    status = status if isinstance(status, int) else None
    if status in {401, 403}:
        return LLMError("authentication_or_permission_denied", status_code=status)
    if status == 404:
        return LLMError("model_not_found_or_unavailable", status_code=status)
    if status == 400:
        return LLMError("invalid_request_check_api_key_model_parameters", status_code=status)
    if status in {408, 409, 429, 500, 502, 503, 504}:
        return LLMError("temporary_api_error", retryable=True, status_code=status)
    if isinstance(exc, (TimeoutError, ConnectionError)) or type(exc).__name__ in {
        "APITimeoutError", "APIConnectionError", "ConnectError", "ReadTimeout",
        "ConnectTimeout", "WriteTimeout", "PoolTimeout", "RemoteProtocolError",
    }:
        return LLMError("network_or_timeout", retryable=True)
    return LLMError("provider_error", status_code=status)


def _gemini(request: dict[str, Any], timeout_s: float) -> LLMResult:
    from google import genai
    from google.genai import types

    params = dict(request["parameters"])
    if "stop" in params:
        params["stop_sequences"] = params.pop("stop")
    if "thinking_budget" in params:
        params["thinking_config"] = {"thinking_budget": params.pop("thinking_budget")}
    if request["json_output"] or request["output_schema"] is not None:
        params["response_mime_type"] = "application/json"
    if request["output_schema"] is not None:
        params["response_json_schema"] = request["output_schema"]
    contents = []
    for msg in request["messages"]:
        if msg["role"] == "system":
            params["system_instruction"] = msg["content"]
        else:
            contents.append(types.Content(
                role="model" if msg["role"] == "assistant" else "user",
                parts=[types.Part.from_text(text=msg["content"])],
            ))
    # SDK retries disabled; the common caller owns the bounded retry policy.
    with genai.Client(api_key=os.environ[KEY_ENV["gemini"]], vertexai=False,
                      http_options=types.HttpOptions(
                          timeout=int(timeout_s * 1000),
                          retry_options=types.HttpRetryOptions(attempts=1))) as client:
        response = client.models.generate_content(
            model=request["model"], contents=contents,
            config=types.GenerateContentConfig(**params))
    usage = response.usage_metadata
    candidates = response.candidates or []
    finish = candidates[0].finish_reason if candidates else None
    finish = getattr(finish, "value", finish)
    # Read only textual non-thinking parts; do not persist hidden reasoning.
    parts = candidates[0].content.parts if candidates and candidates[0].content else []
    output = "".join(p.text for p in (parts or []) if p.text and not p.thought)
    return LLMResult(output, "gemini", request["model"], response.model_version,
                     {"input_tokens": getattr(usage, "prompt_token_count", None),
                      "output_tokens": getattr(usage, "candidates_token_count", None),
                      "total_tokens": getattr(usage, "total_token_count", None),
                      "reasoning_tokens": getattr(usage, "thoughts_token_count", None)},
                     finish)


def _groq(request: dict[str, Any], timeout_s: float) -> LLMResult:
    from groq import Groq

    params = dict(request["parameters"])
    if "max_output_tokens" in params:
        params["max_completion_tokens"] = params.pop("max_output_tokens")
    if request["output_schema"] is not None:
        params["response_format"] = {"type": "json_schema", "json_schema": {
            "name": "extraction", "schema": request["output_schema"], "strict": False}}
    elif request["json_output"]:
        params["response_format"] = {"type": "json_object"}
    with Groq(api_key=os.environ[KEY_ENV["groq"]], timeout=timeout_s,
              max_retries=0) as client:
        response = client.chat.completions.create(
            model=request["model"], messages=request["messages"], **params)
    usage = response.usage
    choice = response.choices[0] if response.choices else None
    return LLMResult(choice.message.content or "" if choice else "", "groq",
                     request["model"], response.model,
                     {"input_tokens": getattr(usage, "prompt_tokens", None),
                      "output_tokens": getattr(usage, "completion_tokens", None),
                      "total_tokens": getattr(usage, "total_tokens", None),
                      "reasoning_tokens": getattr(getattr(usage, "completion_tokens_details", None),
                                                   "reasoning_tokens", None)},
                     choice.finish_reason if choice else None)


class LLMClient:
    def __init__(self, cache_dir: str | Path = "ket_qua/llm_cache",
                 log_path: str | Path = "ket_qua/llm_calls.jsonl", *,
                 timeout_s: float = 30, max_retries: int = 2,
                 transport: Callable[[dict[str, Any], float], LLMResult] | None = None):
        if not math.isfinite(timeout_s) or timeout_s <= 0 or not 0 <= max_retries <= 5:
            raise ValueError("timeout_s > 0; 0 <= max_retries <= 5")
        self.cache_dir, self.log_path = Path(cache_dir), Path(log_path)
        self.timeout_s, self.max_retries = timeout_s, max_retries
        self.transport = transport
        self.mode = "mock" if transport is not None else "live"

    def _log(self, request: dict, digest: str, status: str, started: float,
             **extra: Any) -> None:
        event = {"timestamp": utc_now(), "provider": request["provider"],
                 "model": request["model"], "mode": self.mode,
                 "parameters": request["parameters"], "request_hash": digest,
                 "request": request,
                 "timeout_s": self.timeout_s, "max_retries": self.max_retries,
                 "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
                 "status": status, **extra}
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as stream:
            stream.write(redact(canonical_json(event)) + "\n")

    def call(self, provider: str, model: str, messages: list[dict[str, str]],
             parameters: dict[str, Any] | None = None, *, json_output: bool = False,
             output_schema: dict[str, Any] | None = None) -> LLMResult:
        started = time.perf_counter()
        request = build_request(provider, model, messages, parameters,
                                json_output=json_output, output_schema=output_schema,
                                mode=self.mode)
        digest = request_hash(request)
        cache_file = self.cache_dir / f"{digest}.json"
        if cache_file.exists():
            try:
                entry = json.loads(cache_file.read_text(encoding="utf-8"))
                if entry["request"] != request or entry["status"] != "success":
                    raise ValueError("invalid cache")
                if entry["result_sha256"] != request_hash(entry["result"]):
                    raise ValueError("cache checksum mismatch")
                result = LLMResult(**entry["result"])
                if redact(canonical_json(entry)) != canonical_json(entry):
                    raise ValueError("unsafe cache")
            except (ValueError, KeyError, TypeError):
                self._log(request, digest, "cache_error", started)
                raise LLMError("cache_corrupt_or_unsafe_remove_entry_and_retry") from None
            result.cache_hit = True
            result.elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
            self._log(request, digest, "cache_hit", started, usage=None,
                      source_usage=result.usage, generation_ms=result.generation_ms)
            return result
        if self.mode == "live" and not os.environ.get(KEY_ENV[provider]):
            self._log(request, digest, "blocked", started, error="missing_api_key", usage=None)
            raise LLMError(f"missing_api_key:{KEY_ENV[provider]}")
        transport = self.transport or {"gemini": _gemini, "groq": _groq}[provider]
        for attempt in range(1, self.max_retries + 2):
            attempt_started = time.perf_counter()
            error = None
            result = None
            try:
                result = transport(request, self.timeout_s)
                if not result.text.strip() or result.finish_reason not in {"stop", "STOP"}:
                    raise LLMError("empty_blocked_or_incomplete_response")
                if redact(canonical_json(asdict(result))) != canonical_json(asdict(result)):
                    raise LLMError("credential_in_response")
            except Exception as exc:
                error = _safe_error(exc)
            if error is not None:
                self._log(request, digest, "api_error", attempt_started,
                          attempt=attempt, error=error.code, http_status=error.status_code,
                          retryable=error.retryable, usage=result.usage if result else None)
                if not error.retryable or attempt > self.max_retries:
                    raise error from None
                time.sleep(min(2 ** (attempt - 1), 4))
                continue
            result.request_hash, result.mode = digest, self.mode
            result.elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
            result.generation_ms = result.elapsed_ms
            payload = {"status": "success", "created_at": utc_now(), "request": request,
                       "result": asdict(result), "result_sha256": request_hash(asdict(result))}
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            # Atomic replacement: interrupted writes cannot become valid cache hits.
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".tmp",
                                             dir=self.cache_dir, delete=False) as stream:
                temp_path = Path(stream.name)
                stream.write(canonical_json(payload) + "\n")
            temp_path.replace(cache_file)
            self._log(request, digest, "success", started, attempt=attempt,
                      usage=result.usage, generation_ms=result.generation_ms,
                      actual_model=result.actual_model, finish_reason=result.finish_reason)
            return result
        raise AssertionError("unreachable")
