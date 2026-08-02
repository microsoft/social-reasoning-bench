"""Behavioural tests for :class:`srbench_agents.openclaw_agent.OpenClawAgent`.

These drive the real agent against a fake :class:`GatewayWorker` and a fake
pool, so the MCP server, the retry contract, and teardown are exercised without
a Node process. The agent's HTTP MCP server is genuinely served on an ephemeral
port, so the transport plumbing around it is covered too.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import socket
from pathlib import Path
from typing import Any

import pytest
import uvicorn
from srbench.shared import AssistantTask
from srbench_agents import openclaw_agent
from srbench_agents.openclaw_agent import OpenClawAgent

TOOLS: list[Any] = [
    {
        "type": "function",
        "function": {
            "name": "EndConversation",
            "description": "End the conversation.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    }
]


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def make_task() -> AssistantTask:
    return AssistantTask(max_actions=3)


def assistant_text(text: str) -> dict[str, Any]:
    return {"role": "assistant", "content": [{"type": "text", "text": text}]}


class FakeWorker:
    """Records the calls the agent makes and replays scripted turn outcomes."""

    def __init__(self, turns: list[Any] | None = None) -> None:
        #: Each entry is either a list of transcript messages or an exception.
        self.turns = list(turns or [[assistant_text("done")]])
        self.events: list[str] = []
        self.registrations = 0
        self._registered = False
        self.session_keys: list[str] = []
        self.mcp_port = _free_port()
        self.model: str | None = None
        self.thinking: str | None = None
        self.on_turn: Any = None
        #: Optional hook run inside :meth:`ensure_model`, to simulate preflight
        #: rejecting the requested model.
        self.on_ensure_model: Any = None
        #: What the agent asked OpenClaw to use as its system prompt, if
        #: anything. ``None`` means OpenClaw's own prompt was left in place.
        self.system_prompt: str | None = None
        #: What the trace would report the provider was sent. ``None`` mirrors
        #: tracing being off, which is the default.
        self.context: dict[str, Any] | None = None

    def captured_context(self, session_key: str) -> dict[str, Any] | None:
        self.events.append("captured_context")
        return self.context

    def set_system_prompt(self, prompt: str | None) -> None:
        self.events.append("set_system_prompt")
        self.system_prompt = prompt

    async def ensure_model(self, model: str | None) -> None:
        self.events.append("ensure_model")
        if self.on_ensure_model is not None:
            await self.on_ensure_model(model)
        self.model = model

    async def ensure_registered(self, *, mcp_name: str = "srbench") -> None:
        self.events.append("ensure_registered")
        # Mirrors the real worker: the config write happens once per Gateway
        # lifetime, because control-plane writes are rate limited to 3 per 60s.
        if not self._registered:
            self._registered = True
            self.registrations += 1

    async def run_turn(
        self,
        *,
        session_key: str,
        message: str,
        run_id: str,
        timeout: float,
        model: str | None = None,
        thinking: str | None = None,
    ) -> list[dict[str, Any]]:
        self.events.append("run_turn")
        self.session_keys.append(session_key)
        self.model = model
        self.thinking = thinking
        if self.on_turn is not None:
            await self.on_turn(self)
        outcome = self.turns.pop(0) if self.turns else [assistant_text("done")]
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

    async def abort(self, *, session_key: str, run_id: str | None = None) -> None:
        self.events.append("abort")

    async def delete_session(self, session_key: str) -> None:
        self.events.append("delete_session")


class FakePool:
    def __init__(self, worker: FakeWorker) -> None:
        self.worker = worker

    @contextlib.asynccontextmanager
    async def acquire(self):
        yield self.worker


_real_sleep = asyncio.sleep


@pytest.fixture(autouse=True)
def no_backoff(monkeypatch: pytest.MonkeyPatch):
    """Collapse the retry backoff so tests do not wait seconds per attempt."""

    async def instant(delay: float, *args: Any, **kwargs: Any) -> None:
        await _real_sleep(0)

    monkeypatch.setattr(asyncio, "sleep", instant)


@pytest.fixture
def gateway(monkeypatch: pytest.MonkeyPatch):
    """Patch the agent's pool so it never spawns a real Gateway."""
    worker = FakeWorker()

    async def get_pool(size: int = 1, *, binary: str = "openclaw") -> FakePool:
        return FakePool(worker)

    monkeypatch.setattr(openclaw_agent, "get_pool", get_pool)
    monkeypatch.delenv("SRBENCH_OPENCLAW_MAX_RETRIES", raising=False)
    return worker


async def noop_invoke(name: str, arguments: Any) -> str:
    return "ok"


async def test_a_successful_run_serves_tools_and_passes_model_per_session(gateway: FakeWorker):
    async def invoke(name: str, arguments: Any) -> str:
        return "ended"

    gateway.on_turn = _call_tool("EndConversation")
    agent = OpenClawAgent(
        task=make_task(), model="anthropic/claude-sonnet-4-6", reasoning_effort="high"
    )
    await agent.run(invoke, TOOLS)

    assert gateway.events == [
        "ensure_model",
        "ensure_registered",
        "set_system_prompt",
        "run_turn",
        "captured_context",
        "delete_session",
    ]
    # Model and thinking ride on the session, not on the rate-limited config.
    assert gateway.model == "anthropic/claude-sonnet-4-6"
    assert gateway.thinking == "high"


async def test_preflight_runs_before_the_mcp_server_is_registered(gateway: FakeWorker):
    """A bad model id should fail before any environment-visible setup."""

    async def reject(model: str | None) -> None:
        raise RuntimeError(f"OpenClaw does not know the model {model!r}")

    gateway.on_ensure_model = reject
    agent = OpenClawAgent(task=make_task(), model="openai/claude-sonnet-4-6")
    with pytest.raises(RuntimeError, match="does not know the model"):
        await agent.run(noop_invoke, TOOLS)
    # Nothing was served and no config write was spent on a doomed run.
    assert "ensure_registered" not in gateway.events
    assert gateway.registrations == 0


async def test_the_mcp_port_is_freed_even_when_the_run_raises(gateway: FakeWorker):
    gateway.turns = [RuntimeError("boom"), RuntimeError("boom"), RuntimeError("boom")]
    agent = OpenClawAgent(task=make_task())
    with pytest.raises(RuntimeError, match="openclaw run failed"):
        await agent.run(noop_invoke, TOOLS)
    # The next task on this worker binds the same port, so a leaked listener
    # would make every later task on this Gateway fail to start.
    assert _port_is_free(gateway.mcp_port)


async def test_cancelling_a_run_shuts_the_server_down_cleanly(
    gateway: FakeWorker, monkeypatch: pytest.MonkeyPatch
):
    """Cancellation must not orphan the listening socket.

    ``uvicorn.Server.serve`` skips its own shutdown when cancelled, leaving the
    event loop with a reader on a socket we then close — which floods the loop
    with ``OSError: [Errno 9] Bad file descriptor`` on every accept and leaves
    the port unusable for the next task.
    """
    started = asyncio.Event()

    async def hang(worker: FakeWorker) -> None:
        started.set()
        await asyncio.sleep(3600)

    gateway.on_turn = hang
    errors: list[dict[str, Any]] = []
    asyncio.get_running_loop().set_exception_handler(lambda _loop, ctx: errors.append(ctx))

    shutdowns: list[int] = []
    original_shutdown = uvicorn.Server.shutdown

    async def spy(self: uvicorn.Server, sockets: Any = None) -> None:
        shutdowns.append(1)
        await original_shutdown(self, sockets=sockets)

    monkeypatch.setattr(uvicorn.Server, "shutdown", spy)

    run = asyncio.create_task(OpenClawAgent(task=make_task()).run(noop_invoke, TOOLS))
    await asyncio.wait_for(started.wait(), timeout=10)
    run.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await run

    await asyncio.sleep(0.1)  # give any orphaned accept callback a chance to fire
    # uvicorn only unregisters the listening socket from the event loop inside
    # its own shutdown; skipping it is what leaves the orphan behind.
    assert shutdowns
    assert _port_is_free(gateway.mcp_port)
    assert not [e for e in errors if isinstance(e.get("exception"), OSError)]

    # The decisive check: an orphaned listener silently swallows the next task's
    # connections, so this run would hang rather than fail. Bound so a
    # regression fails the suite instead of wedging it.
    gateway.on_turn = _call_tool("EndConversation")
    await asyncio.wait_for(OpenClawAgent(task=make_task()).run(noop_invoke, TOOLS), timeout=30)


async def test_context_is_captured_when_the_harness_cancels_the_run(gateway: FakeWorker):
    """Cancellation is how a real run ends, so capture has to survive it.

    The harness cancels the agent as soon as the conversation is over, so a
    turn that returns normally is the exception rather than the rule. A capture
    placed only after a returning turn silently never fires on a live run.
    """
    started = asyncio.Event()

    async def engage_then_hang(worker: FakeWorker) -> None:
        # Engaging first pins this to a single attempt, so the capture under
        # test is the cancelled one and not a retry's tidy return.
        await _call_tool("ListMeetings")(worker)
        started.set()
        await _real_sleep(3600)

    gateway.on_turn = engage_then_hang
    run = asyncio.create_task(OpenClawAgent(task=make_task()).run(noop_invoke, TOOLS))
    await asyncio.wait_for(started.wait(), timeout=10)
    run.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await run

    assert gateway.events.count("run_turn") == 1
    assert "captured_context" in gateway.events


async def test_two_sequential_tasks_reuse_one_registration_and_one_port(
    gateway: FakeWorker, monkeypatch: pytest.MonkeyPatch
):
    async def get_pool(size: int = 1, *, binary: str = "openclaw") -> FakePool:
        return FakePool(gateway)

    monkeypatch.setattr(openclaw_agent, "get_pool", get_pool)
    gateway.on_turn = _call_tool("EndConversation")
    for _ in range(2):
        await asyncio.wait_for(OpenClawAgent(task=make_task()).run(noop_invoke, TOOLS), timeout=30)
    # One control-plane write for both tasks: the Gateway allows only 3 per 60s.
    assert gateway.registrations == 1
    assert gateway.events.count("run_turn") == 2
    # Both tasks served on the same registered port, and it is free again.
    assert _port_is_free(gateway.mcp_port)


async def test_transcript_failure_is_raised_not_silently_swallowed(gateway: FakeWorker):
    error = {
        "role": "assistant",
        "content": [],
        "stopReason": "error",
        "errorMessage": "FailoverError: Unknown model: openai/claude-sonnet-4-6",
    }
    gateway.turns = [[error], [error], [error]]
    agent = OpenClawAgent(task=make_task())
    with pytest.raises(RuntimeError, match="Unknown model"):
        await agent.run(noop_invoke, TOOLS)


async def test_a_run_with_no_tool_calls_is_reported_as_a_failure(gateway: FakeWorker):
    gateway.turns = [[assistant_text("I'm done")]] * 3
    agent = OpenClawAgent(task=make_task())
    with pytest.raises(RuntimeError, match="without performing any actions"):
        await agent.run(noop_invoke, TOOLS)


# --- retry contract ---------------------------------------------------------


def _call_tool(name: str):
    """Make the fake worker invoke ``name`` through the live MCP server."""

    async def hook(worker: FakeWorker) -> None:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamable_http_client

        url = f"http://127.0.0.1:{worker.mcp_port}/mcp"
        async with streamable_http_client(url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                await session.call_tool(name, {})

    return hook


async def test_a_failure_before_any_tool_call_is_retried(gateway: FakeWorker):
    gateway.turns = [RuntimeError("rate limited"), [assistant_text("done")]]

    calls: list[str] = []

    async def invoke(name: str, arguments: Any) -> str:
        calls.append(name)
        return "ok"

    # Only the second attempt engages with the environment.
    async def hook(worker: FakeWorker) -> None:
        if len(worker.session_keys) == 2:
            await _call_tool("EndConversation")(worker)

    gateway.on_turn = hook
    agent = OpenClawAgent(task=make_task())
    await agent.run(invoke, TOOLS)

    assert gateway.events.count("run_turn") == 2
    assert calls == ["EndConversation"]
    # A fresh session per attempt, so a retry never resumes the failed run.
    assert len(set(gateway.session_keys)) == 2


async def test_a_failure_after_a_tool_call_is_not_retried(gateway: FakeWorker):
    gateway.turns = [RuntimeError("crashed mid-run"), [assistant_text("done")]]
    gateway.on_turn = _call_tool("EndConversation")

    agent = OpenClawAgent(task=make_task())
    with pytest.raises(RuntimeError, match="crashed mid-run"):
        await agent.run(noop_invoke, TOOLS)
    # Retrying here would replay actions against already-mutated environment state.
    assert gateway.events.count("run_turn") == 1


async def test_retry_budget_is_configurable(gateway: FakeWorker, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SRBENCH_OPENCLAW_MAX_RETRIES", "4")
    gateway.turns = [RuntimeError("nope")] * 5
    agent = OpenClawAgent(task=make_task())
    with pytest.raises(RuntimeError, match="openclaw run failed"):
        await agent.run(noop_invoke, TOOLS)
    assert gateway.events.count("run_turn") == 5


# --- System prompt ---------------------------------------------------------


async def _ended(name: str, arguments: Any) -> str:
    return "ended"


async def test_the_base_agent_leaves_openclaws_system_prompt_alone(gateway: FakeWorker):
    """A task-agnostic agent has no prompt of its own, so it must not clear one.

    ``set_system_prompt(None)`` is still called, because a pooled Gateway may
    have served a task that did set one.
    """
    gateway.on_turn = _call_tool("EndConversation")
    agent = OpenClawAgent(task=AssistantTask(), model="m")

    await agent.run(_ended, TOOLS)

    assert gateway.system_prompt is None
    assert "set_system_prompt" in gateway.events
    assert agent.messages[0]["role"] == "user"
    assert not [m for m in agent.messages if m["role"] == "system"]


async def test_a_subclass_prompt_is_sent_and_recorded_verbatim(gateway: FakeWorker):
    """The recorded transcript is the evidence for what a run was actually told."""

    class Prompted(OpenClawAgent):
        def _system_prompt_message(self) -> str:
            return "You are a calendar assistant."

    gateway.on_turn = _call_tool("EndConversation")
    agent = Prompted(task=AssistantTask(), model="m")

    await agent.run(_ended, TOOLS)

    assert gateway.system_prompt == "You are a calendar assistant."
    assert agent.messages[0] == {"role": "system", "content": "You are a calendar assistant."}
    assert agent.messages[1]["role"] == "user"


async def test_the_prompt_is_set_before_the_first_turn(gateway: FakeWorker):
    """Setting it after the model had already replied would change nothing."""

    class Prompted(OpenClawAgent):
        def _system_prompt_message(self) -> str:
            return "You are a calendar assistant."

    gateway.on_turn = _call_tool("EndConversation")

    await Prompted(task=AssistantTask(), model="m").run(_ended, TOOLS)

    assert gateway.events.index("set_system_prompt") < gateway.events.index("run_turn")


# --- Trace dumps -----------------------------------------------------------


async def test_the_trace_dump_names_the_cell_it_came_from(
    gateway: FakeWorker, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """A dump carries no variant label, so it has to identify itself.

    Several cells share an opening turn, so the tool setting and the prompt
    srbench composed are what tell two dumps apart after the fact.
    """

    class Prompted(OpenClawAgent):
        def _system_prompt_message(self) -> str:
            return "You are a calendar assistant."

    monkeypatch.setenv("SRBENCH_OPENCLAW_TRACE_DIR", str(tmp_path))
    monkeypatch.setenv("SRBENCH_OPENCLAW_TOOLS", "sandbox")
    gateway.context = {"system": "openclaw's own", "messages": [{"role": "user"}], "modelId": "m"}
    gateway.on_turn = _call_tool("EndConversation")

    await Prompted(task=AssistantTask(), model="m").run(_ended, TOOLS)

    dumps = list(tmp_path.glob("*.json"))
    assert len(dumps) == 1
    payload = json.loads(dumps[0].read_text())
    assert payload["tools"] == "sandbox"
    assert payload["srbench_system_prompt"] == "You are a calendar assistant."
    assert payload["system"] == "openclaw's own"
    assert payload["messages"] == [{"role": "user"}]


async def test_openclaws_own_prompt_is_recorded_as_a_marker_not_pasted_in(
    gateway: FakeWorker, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """The transcript is graded, so one arm must not carry a 36 KB manual.

    The judge reads ``assistant_context``. Pasting OpenClaw's operating manual
    into the stock arm alone would change what it sees for reasons that have
    nothing to do with how the assistant behaved.
    """
    monkeypatch.setenv("SRBENCH_OPENCLAW_TRACE_DIR", str(tmp_path))
    gateway.context = {"system": "openclaw's own prompt", "messages": [], "modelId": "m"}
    gateway.on_turn = _call_tool("EndConversation")
    agent = OpenClawAgent(task=AssistantTask(), model="m")

    await agent.run(_ended, TOOLS)

    first = agent.messages[0]
    assert first["role"] == "system"
    assert first["content"].startswith("[OpenClaw's own system prompt, not composed by srbench:")
    assert "openclaw's own prompt" not in first["content"]
    # The full text is still recoverable, just not from the graded transcript.
    assert json.loads(next(tmp_path.glob("*.json")).read_text())["system"] == (
        "openclaw's own prompt"
    )


async def test_tracing_is_off_unless_a_directory_is_set(
    gateway: FakeWorker, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    monkeypatch.delenv("SRBENCH_OPENCLAW_TRACE_DIR", raising=False)
    gateway.context = {"system": "openclaw's own", "messages": [], "modelId": "m"}
    gateway.on_turn = _call_tool("EndConversation")

    await OpenClawAgent(task=AssistantTask(), model="m").run(_ended, TOOLS)

    assert not list(tmp_path.glob("*.json"))


async def test_a_retry_does_not_add_a_second_marker(
    gateway: FakeWorker, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """Every attempt captures, but the transcript describes one run."""
    monkeypatch.setenv("SRBENCH_OPENCLAW_TRACE_DIR", str(tmp_path))
    gateway.context = {"system": "openclaw's own", "messages": [], "modelId": "m"}
    gateway.turns = [RuntimeError("rate limited"), [assistant_text("done")]]

    # Only the second attempt engages, which is what makes the first retryable.
    async def hook(worker: FakeWorker) -> None:
        if len(worker.session_keys) == 2:
            await _call_tool("EndConversation")(worker)

    gateway.on_turn = hook
    agent = OpenClawAgent(task=AssistantTask(), model="m")

    await agent.run(_ended, TOOLS)

    assert gateway.events.count("run_turn") == 2
    assert sum(m["role"] == "system" for m in agent.messages) == 1
