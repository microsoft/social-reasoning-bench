"""Tests for sage tracing module."""

import tempfile
from datetime import datetime
from pathlib import Path

from openai.types.completion_usage import CompletionUsage
from sage_llm.tracing import LLMTrace, LLMTracer, SageRequest, tracer
from sage_llm.types import (
    SageChatCompletionInfo,
    SageChatCompletionMessage,
    SageMessage,
)


def _make_response_msg() -> SageChatCompletionMessage:
    return SageChatCompletionMessage(
        role="assistant",
        content="Hello!",
        completion_info=SageChatCompletionInfo(
            id="resp_123",
            model="gpt-4o",
            finish_reason="stop",
            usage=CompletionUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        ),
    )


class TestLLMTrace:
    def test_build_with_sage_types(self):
        msgs: list[SageMessage] = [{"role": "user", "content": "hi"}]
        trace = LLMTrace(
            sage_request=SageRequest(
                model="gpt-4o",
                messages=msgs,
                temperature=0.5,
            ),
            start_time=datetime.now(),
        )
        assert trace.sage_request is not None
        assert trace.sage_request.model == "gpt-4o"
        assert len(trace.sage_request.messages) == 1
        assert trace.sage_request.temperature == 0.5

    def test_sage_response_is_sage_message(self):
        trace = LLMTrace()
        msg = _make_response_msg()
        trace.sage_response = msg
        assert trace.sage_response is not None
        assert trace.sage_response.content == "Hello!"
        assert trace.sage_response.completion_info is not None
        assert trace.sage_response.completion_info.id == "resp_123"

    def test_provider_fields(self):
        trace = LLMTrace()
        trace.provider_name = "openai"
        trace.provider_request = {"model": "gpt-4o", "messages": []}
        trace.provider_response = {"id": "chatcmpl-123", "choices": []}
        trace.prompt_tokens = 10
        trace.completion_tokens = 5
        trace.total_tokens = 15
        assert trace.provider_name == "openai"
        assert trace.prompt_tokens == 10

    def test_status_and_error(self):
        trace = LLMTrace(status="failure", error="boom")
        assert trace.status == "failure"
        assert trace.error == "boom"


class TestLLMTracer:
    def test_record_and_get(self):
        t = LLMTracer()
        trace = LLMTrace(status="success")
        t.record(trace)
        assert t.count() == 1
        assert t.get_traces()[0].status == "success"

    def test_clear(self):
        t = LLMTracer()
        t.record(LLMTrace(status="success"))
        assert t.count() == 1
        t.clear()
        assert t.count() == 0

    def test_count(self):
        t = LLMTracer()
        for _ in range(3):
            t.record(LLMTrace())
        assert t.count() == 3


class TestTraceSerialization:
    def test_save_and_load(self):
        t = LLMTracer()
        msgs: list[SageMessage] = [{"role": "user", "content": "hi"}]
        trace = LLMTrace(
            sage_request=SageRequest(
                model="gpt-4o",
                messages=msgs,
            ),
            sage_response=_make_response_msg(),
            provider_name="openai",
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            status="success",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration_ms=100.0,
        )
        t.record(trace)

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = Path(f.name)

        t.save(path)
        loaded = LLMTracer.load(path)

        assert len(loaded) == 1
        assert loaded[0].status == "success"
        assert loaded[0].prompt_tokens == 10
        assert loaded[0].provider_name == "openai"
        path.unlink()


class TestModuleLevelTracer:
    def test_module_tracer_exists(self):
        assert isinstance(tracer, LLMTracer)
