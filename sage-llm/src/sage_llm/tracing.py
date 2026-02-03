"""LiteLLM trace collector using CustomLogger.

Module-level singleton pattern for collecting all LLM traces.

Usage:
    from sage_llm.tracing import get_tracer, get_traces, clear_traces, save_traces

    # Get the singleton tracer
    tracer = get_tracer()

    # Access collected traces
    traces = get_traces()

    # Save traces to JSON
    save_traces("traces.json")

    # Clear traces
    clear_traces()
"""

import json
import threading
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from litellm.integrations.custom_logger import CustomLogger


@dataclass
class CostBreakdown:
    """Detailed cost breakdown for an LLM call."""

    input_cost: Optional[float] = None
    output_cost: Optional[float] = None
    tool_usage_cost: Optional[float] = None
    total_cost: Optional[float] = None


@dataclass
class LLMTrace:
    """A single LLM call trace."""

    # Identifiers
    id: str
    trace_id: Optional[str]

    # Request info
    model: str
    messages: list[dict[str, Any]]
    call_type: str
    provider: Optional[str]
    api_base: Optional[str]

    # Response info
    response: Optional[dict[str, Any]]
    status: str  # "success" or "failure"
    error: Optional[str]

    # Timing
    start_time: datetime
    end_time: datetime
    duration_ms: float
    time_to_first_token_ms: Optional[float]

    # Token usage
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]
    reasoning_tokens: Optional[int]

    # Cost
    cost: Optional[float]
    cost_breakdown: Optional[CostBreakdown]

    # Additional info
    cache_hit: Optional[bool]
    stream: bool
    model_parameters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class LLMTracer(CustomLogger):
    """LiteLLM CustomLogger that collects all LLM call traces.

    Use get_tracer() to get the singleton instance.
    """

    def __init__(self):
        super().__init__()
        self._traces: list[LLMTrace] = []
        self._traces_lock = threading.Lock()

    def _extract_trace(
        self,
        kwargs: dict,
        response_obj: Any,
        start_time: float,
        end_time: float,
        status: str,
        error: Optional[str] = None,
    ) -> LLMTrace:
        """Extract trace information from LiteLLM callback parameters."""
        # Extract basic info
        model = kwargs.get("model", "unknown")
        messages = kwargs.get("messages", [])
        call_type = kwargs.get("call_type", "completion")
        provider = kwargs.get("custom_llm_provider")
        api_base = kwargs.get("api_base")
        stream = kwargs.get("stream", False)
        cache_hit = kwargs.get("cache_hit")

        # Extract full response as dict
        response_content: dict[str, Any] | None = None
        if response_obj:
            try:
                response_content = response_obj.model_dump(mode="json")
            except Exception:
                response_content = {"raw": str(response_obj)}

        # Extract usage info
        prompt_tokens = None
        completion_tokens = None
        total_tokens = None
        reasoning_tokens = None
        if response_obj and hasattr(response_obj, "usage") and response_obj.usage:
            usage = response_obj.usage
            prompt_tokens = getattr(usage, "prompt_tokens", None)
            completion_tokens = getattr(usage, "completion_tokens", None)
            total_tokens = getattr(usage, "total_tokens", None)
            # Extract reasoning/thinking tokens from completion_tokens_details
            if hasattr(usage, "completion_tokens_details") and usage.completion_tokens_details:
                details = usage.completion_tokens_details
                reasoning_tokens = getattr(details, "reasoning_tokens", None)

        # Extract from standard logging object
        cost = None
        cost_breakdown = None
        trace_id = None
        standard_logging = kwargs.get("standard_logging_object")
        if standard_logging and isinstance(standard_logging, dict):
            cost = standard_logging.get("response_cost")
            trace_id = standard_logging.get("trace_id")

            # Extract cost breakdown
            breakdown = standard_logging.get("cost_breakdown")
            if breakdown and isinstance(breakdown, dict):
                cost_breakdown = CostBreakdown(
                    input_cost=breakdown.get("input_cost"),
                    output_cost=breakdown.get("output_cost"),
                    tool_usage_cost=breakdown.get("tool_usage_cost"),
                    total_cost=breakdown.get("total_cost"),
                )

        # Convert timestamps
        if isinstance(start_time, (int, float)):
            start_dt = datetime.fromtimestamp(start_time)
        else:
            start_dt = start_time

        if isinstance(end_time, (int, float)):
            end_dt = datetime.fromtimestamp(end_time)
        else:
            end_dt = end_time

        # Calculate duration
        if isinstance(start_time, (int, float)) and isinstance(end_time, (int, float)):
            duration_ms = (end_time - start_time) * 1000
        elif isinstance(start_dt, datetime) and isinstance(end_dt, datetime):
            duration_ms = (end_dt - start_dt).total_seconds() * 1000
        else:
            duration_ms = 0

        # Calculate time to first token (for streaming)
        time_to_first_token_ms = None
        completion_start = kwargs.get("completion_start_time")
        if completion_start and start_dt:
            if isinstance(completion_start, datetime):
                time_to_first_token_ms = (completion_start - start_dt).total_seconds() * 1000

        # Generate call ID
        call_id = kwargs.get("litellm_call_id", f"trace_{int(time.time() * 1000)}")

        # Extract model parameters
        model_parameters = kwargs.get("optional_params", {})

        # Extract additional metadata
        metadata = {
            "litellm_params": kwargs.get("litellm_params", {}),
        }

        return LLMTrace(
            id=call_id,
            trace_id=trace_id,
            model=model,
            messages=messages,
            call_type=call_type,
            provider=provider,
            api_base=api_base,
            response=response_content,
            status=status,
            error=error,
            start_time=start_dt,
            end_time=end_dt,
            duration_ms=duration_ms,
            time_to_first_token_ms=time_to_first_token_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            reasoning_tokens=reasoning_tokens,
            cost=cost,
            cost_breakdown=cost_breakdown,
            cache_hit=cache_hit,
            stream=stream,
            model_parameters=model_parameters,
            metadata=metadata,
        )

    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        """Log successful LLM call."""
        trace = self._extract_trace(kwargs, response_obj, start_time, end_time, "success")
        with self._traces_lock:
            self._traces.append(trace)

    def log_failure_event(self, kwargs, response_obj, start_time, end_time):
        """Log failed LLM call."""
        error_str = None
        if isinstance(response_obj, Exception):
            error_str = str(response_obj)
        elif response_obj:
            error_str = str(response_obj)

        trace = self._extract_trace(
            kwargs, response_obj, start_time, end_time, "failure", error=error_str
        )
        with self._traces_lock:
            self._traces.append(trace)

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        """Async log successful LLM call."""
        self.log_success_event(kwargs, response_obj, start_time, end_time)

    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        """Async log failed LLM call."""
        self.log_failure_event(kwargs, response_obj, start_time, end_time)

    def get_traces(self) -> list[LLMTrace]:
        """Get all collected traces."""
        with self._traces_lock:
            return list(self._traces)

    def clear_traces(self) -> None:
        """Clear all collected traces."""
        with self._traces_lock:
            self._traces.clear()

    def get_trace_count(self) -> int:
        """Get the number of collected traces."""
        with self._traces_lock:
            return len(self._traces)


# Module-level singleton instance
_tracer: Optional[LLMTracer] = None
_tracer_lock = threading.Lock()


def get_tracer() -> LLMTracer:
    """Get the singleton LLMTracer instance.

    Also registers it with LiteLLM if not already registered.
    """
    global _tracer
    if _tracer is None:
        with _tracer_lock:
            if _tracer is None:
                _tracer = LLMTracer()
                _register_tracer(_tracer)
    return _tracer


def _register_tracer(tracer: LLMTracer) -> None:
    """Register the tracer with LiteLLM callbacks."""
    import litellm

    if tracer not in litellm.callbacks:
        litellm.callbacks.append(tracer)


def get_traces() -> list[LLMTrace]:
    """Get all collected traces from the singleton tracer."""
    return get_tracer().get_traces()


def clear_traces() -> None:
    """Clear all collected traces from the singleton tracer."""
    get_tracer().clear_traces()


def get_trace_count() -> int:
    """Get the number of collected traces."""
    return get_tracer().get_trace_count()


def _trace_to_dict(trace: LLMTrace) -> dict[str, Any]:
    """Convert an LLMTrace to a JSON-serializable dictionary."""
    d = asdict(trace)
    # Convert datetime objects to ISO format strings
    if d.get("start_time"):
        d["start_time"] = d["start_time"].isoformat()
    if d.get("end_time"):
        d["end_time"] = d["end_time"].isoformat()
    return d


def _dict_to_trace(d: dict[str, Any]) -> LLMTrace:
    """Convert a dictionary back to an LLMTrace."""
    # Convert ISO format strings back to datetime
    if d.get("start_time"):
        d["start_time"] = datetime.fromisoformat(d["start_time"])
    if d.get("end_time"):
        d["end_time"] = datetime.fromisoformat(d["end_time"])
    # Convert cost_breakdown dict to CostBreakdown object
    if d.get("cost_breakdown") and isinstance(d["cost_breakdown"], dict):
        d["cost_breakdown"] = CostBreakdown(**d["cost_breakdown"])
    return LLMTrace(**d)


def save_traces(
    path: str | Path,
    traces: list[LLMTrace] | None = None,
    indent: int = 2,
) -> None:
    """Save traces to a JSON file.

    Args:
        path: Path to the output JSON file
        traces: Traces to save. If None, saves all traces from the singleton tracer.
        indent: JSON indentation level (default: 2)

    Example:
        # Save all collected traces
        save_traces("traces.json")

        # Save specific traces
        save_traces("traces.json", traces=my_traces)
    """
    if traces is None:
        traces = get_traces()

    data = [_trace_to_dict(t) for t in traces]

    path = Path(path)
    with path.open("w") as f:
        json.dump(data, f, indent=indent)


def load_traces(path: str | Path) -> list[LLMTrace]:
    """Load traces from a JSON file.

    Args:
        path: Path to the JSON file

    Returns:
        List of LLMTrace objects

    Example:
        traces = load_traces("traces.json")
        for trace in traces:
            print(f"{trace.model}: {trace.duration_ms}ms")
    """
    path = Path(path)
    with path.open() as f:
        data = json.load(f)

    return [_dict_to_trace(d) for d in data]


def traces_to_dict(traces: list[LLMTrace] | None = None) -> list[dict[str, Any]]:
    """Convert traces to a list of JSON-serializable dictionaries.

    Args:
        traces: Traces to convert. If None, uses all traces from the singleton tracer.

    Returns:
        List of dictionaries suitable for JSON serialization

    Example:
        # Get traces as dicts for custom serialization
        data = traces_to_dict()
        df = pd.DataFrame(data)  # Convert to pandas DataFrame
    """
    if traces is None:
        traces = get_traces()
    return [_trace_to_dict(t) for t in traces]
