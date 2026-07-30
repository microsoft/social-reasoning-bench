"""A bring-your-own-agent implementation driven by the OpenClaw Gateway.

This agent exposes the environment's granted tools to OpenClaw as an HTTP MCP
server and lets OpenClaw drive the conversation to ``EndConversation``.

How it talks to OpenClaw
------------------------
Each task:

1. Builds an MCP server around the environment's live, stateful ``invoke_tool``
   boundary (via :func:`srbench.mcp.build_server`) and serves it over
   streamable-HTTP on an ephemeral loopback port. HTTP (rather than in-process
   MCP) is required because OpenClaw runs in a separate process and must reach a
   server bound to *this* process's live state.
2. Borrows a Gateway from :class:`~srbench_agents.openclaw_gateway.GatewayPool`.
   The Gateway is a long-lived OpenClaw process; the pool is sized to task
   concurrency and each task holds one Gateway exclusively. That exclusivity is
   what keeps the task's tool space private: ``mcp.servers`` is global to a
   Gateway, so a worker with exactly one registration at a time cannot leak one
   task's tools into another.
3. Registers the MCP server, pins the model and thinking level, runs one agent
   turn over WebSocket RPC, and then deregisters.

An earlier version of this agent spawned a one-shot ``openclaw agent --local``
subprocess per task and scraped its stdout. That cost a Node cold start per task
and collapsed every failure into ``exited with code 1`` plus a stderr tail.

Pin: this agent targets **OpenClaw v2026.5.28** and asserts the installed CLI
reports that version at runtime. Install the pinned CLI with::

    npm install -g openclaw@2026.5.28   # tag v2026.5.28 == e93216080aa1f425d3ab127014603eba8e365b2d

Provider credentials are read from the environment (e.g. ``ANTHROPIC_API_KEY``);
each Gateway runs in a throwaway profile, so no ``openclaw onboard`` step is
needed. Models are ``provider/model`` ids such as ``anthropic/claude-sonnet-4-6``
or ``phyagi/gpt-5.5``. The phyagi gateway is always registered as the ``phyagi``
provider (Responses API, with per-Gateway session affinity); see
:mod:`srbench_agents.openclaw_gateway`. ``openai/*`` ids are unaffected and
still mean real OpenAI.

Optional environment overrides:

- ``SRBENCH_OPENCLAW_BIN``   — path to the ``openclaw`` binary (default ``openclaw``).
- ``SRBENCH_OPENCLAW_MODEL`` — ``provider/model`` override for the run.
- ``SRBENCH_OPENCLAW_REASONING_EFFORT`` — thinking level (``off``/``minimal``/
  ``low``/``medium``/``high``, plus provider ``xhigh``/``adaptive``/``max``).
- ``SRBENCH_OPENCLAW_MAX_RETRIES`` — retries for an invocation that fails before
  the agent makes any tool call (default ``2``); absorbs transient provider
  errors such as rate limits.
- ``SRBENCH_OPENCLAW_POOL_SIZE`` — number of Gateways to run concurrently
  (default ``1``). A task holds one Gateway exclusively, so set this to the
  harness's ``batch_size`` (concurrent tasks) or tasks queue behind one Gateway.
- ``SRBENCH_OPENCLAW_SYSTEM_PROMPT`` — operating system prompt, prepended to the
  opening message (defaults to
  :data:`srbench_agents.prompts.DEFAULT_ASSISTANT_SYSTEM_PROMPT`).
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import socket
from typing import Any
from uuid import uuid4

import uvicorn
from openai.types.chat import ChatCompletionFunctionToolParam
from srbench.mcp import build_asgi_app, build_server
from srbench.shared import AssistantTask, BaseAssistantAgent, InvokeTool

from srbench_agents.openclaw_gateway import (
    OPENCLAW_VERSION,
    GatewayWorker,
    get_pool,
    is_error_message,
)
from srbench_agents.prompts import DEFAULT_ASSISTANT_SYSTEM_PROMPT

__all__ = ["OPENCLAW_VERSION", "OpenClawAgent"]

_MCP_SERVER_NAME = "srbench"


def _bind_socket(port: int) -> socket.socket:
    """Bind ``127.0.0.1:port`` and return the socket, still open.

    The bound socket is handed directly to uvicorn (``Server.serve(sockets=...)``)
    rather than passing a port number, which would reopen a TOCTOU window between
    allocation and bind.

    ``port`` is the one its Gateway worker reserved and registered with OpenClaw,
    so every task on that worker serves at the same URL. ``SO_REUSEADDR`` lets the
    next task rebind immediately after the previous one released the port instead
    of waiting out ``TIME_WAIT``.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", port))
    return sock


async def _wait_until_listening(host: str, port: int, *, timeout: float = 10.0) -> None:
    """Block until ``host:port`` accepts connections, or raise on timeout."""
    deadline = asyncio.get_event_loop().time() + timeout
    while True:
        try:
            _, writer = await asyncio.open_connection(host, port)
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()
            return
        except OSError:
            if asyncio.get_event_loop().time() >= deadline:
                raise TimeoutError(f"MCP HTTP server did not start listening on {host}:{port}")
            await asyncio.sleep(0.05)


async def _stop_server(
    http: uvicorn.Server, serve_task: asyncio.Task[None], sock: socket.socket
) -> None:
    """Shut the per-task MCP server down without orphaning its listening socket.

    ``uvicorn.Server.serve`` has no ``finally``: cancelling it skips uvicorn's own
    shutdown, so the asyncio server keeps a reader registered on the listening fd.
    Closing that fd underneath the loop then floods it with ``EBADF`` on every
    accept and wedges the next task that binds the same port. So ask uvicorn to
    stop cooperatively first, and only fall back to cancellation — followed by an
    explicit ``Server.shutdown`` — if it refuses to.

    The loop tolerates a cancellation delivered *into* teardown (the harness
    cancelling the task) rather than letting it abort the cleanup.
    """
    http.should_exit = True
    for _ in range(3):
        try:
            done, _pending = await asyncio.wait({serve_task}, timeout=10.0)
        except asyncio.CancelledError:
            continue
        if done:
            break
    if not serve_task.done():
        serve_task.cancel()
        with contextlib.suppress(BaseException):
            await serve_task
        with contextlib.suppress(BaseException):
            await http.shutdown(sockets=[sock])
    # uvicorn closes the socket on shutdown; close defensively in case startup
    # never handed it off (a double close is harmless).
    with contextlib.suppress(Exception):
        sock.close()


class OpenClawAgent(BaseAssistantAgent[AssistantTask]):
    """A task-agnostic assistant agent that drives OpenClaw over its Gateway.

    The agent receives its task through the constructor and, in :meth:`run`,
    exposes the environment's granted tools to OpenClaw as an HTTP MCP server
    (built with :func:`srbench.mcp.build_server`). All tool logic and validation
    stay in the environment; this class only bridges OpenClaw's tool calls to
    that boundary (and records a small debug transcript along the way).
    """

    def __init__(
        self,
        *,
        task: AssistantTask,
        model: str | None = None,
        reasoning_effort: str | int | None = None,
        system_prompt: str | None = None,
    ) -> None:
        super().__init__(
            task=task,
            model=model,
            reasoning_effort=reasoning_effort,
            system_prompt=system_prompt,
        )
        self._model = self.model or os.environ.get("SRBENCH_OPENCLAW_MODEL")
        # Reasoning effort maps to OpenClaw's thinking level
        # (``off``/``minimal``/``low``/``medium``/``high``, plus
        # provider-supported ``xhigh``/``adaptive``/``max``); ``None`` uses the
        # OpenClaw default. Levels are named, so a numeric effort cannot be
        # honoured and is rejected rather than silently dropped.
        effort = self.reasoning_effort
        if isinstance(effort, int):
            raise ValueError(
                f"OpenClaw thinking levels are named, not numeric: got {effort!r}. "
                "Use one of off/minimal/low/medium/high (or a provider-supported "
                "xhigh/adaptive/max)."
            )
        self._reasoning_effort = effort or os.environ.get("SRBENCH_OPENCLAW_REASONING_EFFORT")
        # The harness may supply the operating system prompt; otherwise fall
        # back to this agent's built-in benchmark ground rules. The opening turn
        # has no separate system-prompt channel, so it is prepended to the
        # opening message.
        self._system_prompt = (
            self.system_prompt
            or os.environ.get("SRBENCH_OPENCLAW_SYSTEM_PROMPT")
            or DEFAULT_ASSISTANT_SYSTEM_PROMPT
        )
        self._binary = os.environ.get("SRBENCH_OPENCLAW_BIN", "openclaw")
        self._pool_size = int(os.environ.get("SRBENCH_OPENCLAW_POOL_SIZE", "1"))
        self._timeout = float(self.task.max_actions) * 30.0 + 120.0
        # How many times to retry an invocation that failed *before* the agent
        # engaged (no MCP tool calls yet, so no environment state to corrupt).
        # This absorbs transient provider errors (e.g. rate limits) that tend to
        # appear once a sweep has been running for a few minutes.
        self._max_retries = int(os.environ.get("SRBENCH_OPENCLAW_MAX_RETRIES", "2"))
        self._ended = False
        self._transcript: list[dict[str, str]] = []
        self._tool_calls = 0

    @property
    def messages(self) -> list[dict[str, str]]:
        """Optional debugging transcript recorded by the executors."""
        return self._transcript

    def _bridge(self, invoke_tool: InvokeTool) -> InvokeTool:
        """Wrap ``invoke_tool`` to record the transcript and detect the end.

        The environment still owns every tool's logic and validation; this
        wrapper only observes the call/result for debugging and notices when the
        agent ends the conversation.
        """

        async def bridged(name: str, arguments: Any) -> str:
            args = arguments or {}
            result = await invoke_tool(name, args)
            self._tool_calls += 1
            self._transcript.append(
                {"role": "assistant", "content": f"{name}({json.dumps(args)}) -> {result}"}
            )
            if name == "EndConversation":
                self._ended = True
            return result

        return bridged

    def _opening_message(self) -> str:
        brief = self.task.model_dump_json(indent=2)
        return f"{self._system_prompt}\n\nYour private task briefing (JSON):\n```json\n{brief}\n```"

    async def run(
        self,
        invoke_tool: InvokeTool,
        tools: list[ChatCompletionFunctionToolParam],
    ) -> None:
        pool = await get_pool(self._pool_size, binary=self._binary)
        async with pool.acquire() as worker:
            # Preflight before anything is served: an unresolvable model should
            # fail with an actionable message, not as a mysterious empty run.
            await worker.ensure_model(self._model)
            await worker.ensure_registered(mcp_name=_MCP_SERVER_NAME)
            await self._serve_and_run(worker, invoke_tool, tools)

    async def _serve_and_run(
        self,
        worker: GatewayWorker,
        invoke_tool: InvokeTool,
        tools: list[ChatCompletionFunctionToolParam],
    ) -> None:
        """Serve this task's tools on the worker's MCP port for one run.

        The server is bound to the port the worker already registered with
        OpenClaw, and is torn down when the task finishes. OpenClaw rediscovers
        the tool list on every run, so the next task on this worker sees only
        its own tools.
        """
        server = build_server(tools, self._bridge(invoke_tool), name=_MCP_SERVER_NAME)
        sock = _bind_socket(worker.mcp_port)
        http = uvicorn.Server(
            uvicorn.Config(
                build_asgi_app(server),
                host="127.0.0.1",
                port=worker.mcp_port,
                log_level="critical",
            )
        )
        serve_task = asyncio.create_task(http.serve(sockets=[sock]))
        try:
            await _wait_until_listening("127.0.0.1", worker.mcp_port)
            await self._run_with_retries(worker)
        finally:
            # Teardown must survive cancellation (e.g. the harness hit max
            # rounds), or the port stays busy and the next task cannot bind.
            await _stop_server(http, serve_task, sock)

    async def _run_with_retries(self, worker: GatewayWorker) -> None:
        """Run the agent turn, retrying no-op failures and raising on error.

        A failure that occurs *before* the agent makes any MCP tool call has not
        mutated environment state, so it is safe to retry (this absorbs transient
        provider errors such as rate limits). Once the agent has engaged, the run
        is not retried; if it still fails, the error is raised so the harness
        records the real cause instead of silently returning an empty trace.
        """
        last_error: str | None = None
        for attempt in range(self._max_retries + 1):
            calls_before = self._tool_calls
            # A fresh session per attempt so a retry starts a clean conversation
            # rather than resuming the failed one.
            session_key = f"agent:main:srbench-{uuid4().hex[:8]}-r{attempt}"
            run_id = uuid4().hex
            try:
                messages = await worker.run_turn(
                    session_key=session_key,
                    message=self._opening_message(),
                    run_id=run_id,
                    timeout=self._timeout,
                    model=self._model,
                    thinking=self._reasoning_effort,
                )
                last_error = self._record(messages)
            except asyncio.CancelledError:
                await worker.abort(session_key=session_key, run_id=run_id)
                await worker.delete_session(session_key)
                raise
            except Exception as exc:
                last_error = str(exc)
            await worker.delete_session(session_key)

            engaged = self._tool_calls > calls_before
            # Success: the agent engaged with the environment and did not error.
            if last_error is None and engaged:
                return
            # Only retry when nothing was done yet — otherwise retrying would
            # replay actions against already-mutated environment state.
            if engaged or attempt >= self._max_retries:
                break
            await asyncio.sleep(2.0 * (attempt + 1))

        raise RuntimeError(self._failure_message(last_error))

    def _record(self, messages: list[dict[str, Any]]) -> str | None:
        """Append assistant text to the transcript, returning any failure text.

        OpenClaw reports run failures inside the transcript rather than through
        the RPC result, so the transcript is also the error channel.
        """
        error: str | None = None
        for msg in messages:
            failure = is_error_message(msg)
            if failure:
                error = failure
                continue
            if msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            if isinstance(content, list):
                text = " ".join(
                    str(part.get("text", "")) for part in content if isinstance(part, dict)
                ).strip()
            else:
                text = str(content or "").strip()
            if text:
                self._transcript.append({"role": "assistant", "content": text})
        return error

    def _failure_message(self, error: str | None) -> str:
        """Human-readable explanation of why an OpenClaw run failed."""
        if error:
            return f"openclaw run failed: {error[-800:]}"
        # Completed without erroring but never called a tool: nothing to score.
        return "openclaw completed without performing any actions (no MCP tool calls)"
