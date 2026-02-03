"""Unit tests for LLM tracing."""

import time
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from sage_llm.tracing import (
    LLMTrace,
    LLMTracer,
    clear_traces,
    get_trace_count,
    get_tracer,
    get_traces,
)


class TestLLMTracer:
    """Tests for LLMTracer class."""

    @pytest.fixture
    def tracer(self):
        """Create a fresh tracer for each test."""
        tracer = LLMTracer()
        tracer.clear_traces()
        return tracer

    @pytest.fixture
    def mock_response(self):
        """Create a mock LiteLLM response."""
        response = MagicMock()
        response.choices = [MagicMock()]
        response.choices[0].message = MagicMock()
        response.choices[0].message.content = "Hello, world!"
        response.usage = MagicMock()
        response.usage.prompt_tokens = 10
        response.usage.completion_tokens = 5
        response.usage.total_tokens = 15
        response.usage.completion_tokens_details = None
        # model_dump returns the full response as a dict
        response.model_dump.return_value = {
            "choices": [{"message": {"content": "Hello, world!"}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }
        return response

    @pytest.fixture
    def mock_response_with_reasoning(self):
        """Create a mock LiteLLM response with reasoning tokens."""
        response = MagicMock()
        response.choices = [MagicMock()]
        response.choices[0].message = MagicMock()
        response.choices[0].message.content = "The answer is 4."
        response.usage = MagicMock()
        response.usage.prompt_tokens = 10
        response.usage.completion_tokens = 25
        response.usage.total_tokens = 35
        response.usage.completion_tokens_details = MagicMock()
        response.usage.completion_tokens_details.reasoning_tokens = 20
        # model_dump returns the full response as a dict
        response.model_dump.return_value = {
            "choices": [{"message": {"content": "The answer is 4."}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 25, "total_tokens": 35},
        }
        return response

    def test_log_success_event(self, tracer, mock_response):
        """Test logging a successful LLM call."""
        kwargs = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hi"}],
            "litellm_call_id": "test-123",
        }
        start_time = time.time()
        end_time = start_time + 0.5

        tracer.log_success_event(kwargs, mock_response, start_time, end_time)

        traces = tracer.get_traces()
        assert len(traces) == 1
        trace = traces[0]
        assert trace.id == "test-123"
        assert trace.model == "gpt-4"
        assert trace.status == "success"
        assert trace.response == {
            "choices": [{"message": {"content": "Hello, world!"}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }
        assert trace.prompt_tokens == 10
        assert trace.completion_tokens == 5
        assert trace.total_tokens == 15
        assert trace.reasoning_tokens is None
        assert trace.error is None

    def test_log_success_event_with_reasoning_tokens(self, tracer, mock_response_with_reasoning):
        """Test logging a successful LLM call with reasoning tokens."""
        kwargs = {
            "model": "gpt-5.2",
            "messages": [{"role": "user", "content": "What is 2+2?"}],
            "litellm_call_id": "test-reasoning",
        }
        start_time = time.time()
        end_time = start_time + 1.0

        tracer.log_success_event(kwargs, mock_response_with_reasoning, start_time, end_time)

        traces = tracer.get_traces()
        assert len(traces) == 1
        trace = traces[0]
        assert trace.id == "test-reasoning"
        assert trace.model == "gpt-5.2"
        assert trace.reasoning_tokens == 20
        assert trace.completion_tokens == 25
        assert trace.total_tokens == 35

    def test_log_failure_event(self, tracer):
        """Test logging a failed LLM call."""
        kwargs = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hi"}],
            "litellm_call_id": "test-456",
        }
        error = Exception("API rate limit exceeded")
        start_time = time.time()
        end_time = start_time + 0.1

        tracer.log_failure_event(kwargs, error, start_time, end_time)

        traces = tracer.get_traces()
        assert len(traces) == 1
        trace = traces[0]
        assert trace.id == "test-456"
        assert trace.status == "failure"
        assert "rate limit" in trace.error

    def test_clear_traces(self, tracer, mock_response):
        """Test clearing traces."""
        kwargs = {"model": "gpt-4", "messages": []}
        tracer.log_success_event(kwargs, mock_response, time.time(), time.time())
        tracer.log_success_event(kwargs, mock_response, time.time(), time.time())

        assert tracer.get_trace_count() == 2
        tracer.clear_traces()
        assert tracer.get_trace_count() == 0

    def test_thread_safety(self, tracer, mock_response):
        """Test that tracing is thread-safe."""
        import threading

        kwargs = {"model": "gpt-4", "messages": []}
        num_threads = 10
        traces_per_thread = 100

        def add_traces():
            for _ in range(traces_per_thread):
                tracer.log_success_event(kwargs, mock_response, time.time(), time.time())

        threads = [threading.Thread(target=add_traces) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert tracer.get_trace_count() == num_threads * traces_per_thread


class TestLLMTracerSingleton:
    """Tests for singleton behavior."""

    def test_singleton_returns_same_instance(self):
        """Test that get_tracer returns the same instance."""
        tracer1 = get_tracer()
        tracer2 = get_tracer()
        assert tracer1 is tracer2

    def test_singleton_is_registered_with_litellm(self):
        """Test that the tracer is registered with LiteLLM."""
        import litellm

        tracer = get_tracer()
        assert tracer in litellm.callbacks


class TestModuleFunctions:
    """Tests for module-level convenience functions."""

    def test_get_traces_returns_list(self):
        """Test get_traces returns a list."""
        traces = get_traces()
        assert isinstance(traces, list)

    def test_clear_traces_clears_all(self):
        """Test clear_traces clears the tracer."""
        # Add a trace first
        tracer = get_tracer()
        initial_count = get_trace_count()

        clear_traces()
        assert get_trace_count() == 0


class TestTracingIntegration:
    """Integration tests for tracing with ModelClient."""

    @pytest.fixture
    def client(self):
        """Create a ModelClient."""
        from sage_llm.client import ModelClient

        return ModelClient()

    def test_tracing_captures_real_llm_call(self, client):
        """Test that a real LLM call is captured in traces."""
        # Ensure tracer is initialized
        get_tracer()
        clear_traces()

        # Make a real LLM call
        response = client.chat.completions.create(
            model="trapi/msraif/shared/gpt-4.1-nano",
            messages=[{"role": "user", "content": "Say 'traced'"}],
            max_tokens=10,
            timeout=15,
        )

        # Verify response
        assert response.choices[0].message.content is not None

        # Wait for background callback thread (litellm calls callbacks asynchronously)
        time.sleep(0.5)

        # Verify trace was captured
        traces = get_traces()
        assert len(traces) >= 1

        # Find our trace
        latest_trace = traces[-1]
        assert latest_trace.status == "success"
        assert latest_trace.model is not None
        assert latest_trace.prompt_tokens is not None
        assert latest_trace.completion_tokens is not None
        assert latest_trace.duration_ms > 0

        print(
            f"\n✓ Trace captured: {latest_trace.model}, {latest_trace.duration_ms:.0f}ms, "
            f"{latest_trace.total_tokens} tokens"
        )
