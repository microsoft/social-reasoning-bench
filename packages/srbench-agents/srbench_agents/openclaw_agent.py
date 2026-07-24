"""A generic, LLM-driven BYOA agent that drives the OpenClaw CLI.

:class:`OpenClawAgent` is a single "bring your own agent" implementation
that is *generic over the task*: it reads whatever
:class:`~srbench.shared.AssistantTask` it is handed as JSON and therefore runs
the calendar and marketplace benchmarks unchanged::

    srbench benchmark calendar \\
        --assistant-agent srbench_agents.openclaw_agent:OpenClawAgent ...
    srbench benchmark marketplace \\
        --buyer-agent srbench_agents.openclaw_agent:OpenClawAgent ...

Unlike the in-process Claude agent, `OpenClaw <https://github.com/openclaw/openclaw>`_
ships no Python SDK — it is a Node CLI. This agent therefore drives it as a
subprocess:

1. It builds an MCP server from the environment's granted tools and its
   ``invoke_tool`` boundary (via :func:`srbench.mcp.build_server`) and serves it
   over streamable-HTTP on an ephemeral localhost port. HTTP (not stdio) is
   required because the OpenClaw subprocess must reach a server bound to *this*
   process's live, stateful ``invoke_tool``.
2. It registers that server in an isolated OpenClaw ``--profile`` with
   ``openclaw mcp set``, so the agent run can call the environment's tools.
3. It runs a one-shot embedded turn (``openclaw agent --local``) with the task
   JSON as the message and lets OpenClaw drive the conversation to
   ``EndConversation``.

Pin: this agent targets **OpenClaw v2026.5.28** and asserts the installed CLI
reports that version at runtime. Install the pinned CLI with::

    npm install -g openclaw@2026.5.28   # tag v2026.5.28 == e93216080aa1f425d3ab127014603eba8e365b2d

OpenClaw must be onboarded with a model provider (or pass ``--model``/
``SRBENCH_OPENCLAW_MODEL``). Optional environment overrides:

- ``SRBENCH_OPENCLAW_BIN``   — path to the ``openclaw`` binary (default ``openclaw``).
- ``SRBENCH_OPENCLAW_MODEL`` — ``provider/model`` override for the run.
- ``SRBENCH_OPENCLAW_REASONING_EFFORT`` — ``--thinking`` level (``off``/``minimal``/
  ``low``/``medium``/``high``, plus provider ``xhigh``/``adaptive``/``max``).
- ``SRBENCH_OPENCLAW_AGENT`` — a configured OpenClaw agent id to target.
- ``SRBENCH_OPENCLAW_SYSTEM_PROMPT`` — operating system prompt, prepended to the
  opening message (defaults to
  :data:`srbench_agents.prompts.DEFAULT_ASSISTANT_SYSTEM_PROMPT`).
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import shutil
import socket
from pathlib import Path
from typing import Any
from uuid import uuid4

from openai.types.chat import ChatCompletionFunctionToolParam
from srbench.mcp import build_asgi_app, build_server
from srbench.shared import AssistantTask, BaseAssistantAgent, InvokeTool

from srbench_agents.prompts import DEFAULT_ASSISTANT_SYSTEM_PROMPT

try:
    import uvicorn
except ImportError as exc:  # pragma: no cover - exercised only without the extra
    raise ImportError(
        "srbench_agents.openclaw_agent requires the optional 'mcp' HTTP stack. "
        "Install it with: pip install 'srbench-agents'"
    ) from exc

#: The pinned OpenClaw release this agent targets (npm tag ``openclaw@2026.5.28``,
#: git ``e93216080aa1f425d3ab127014603eba8e365b2d``).
OPENCLAW_VERSION = "2026.5.28"

_MCP_SERVER_NAME = "srbench"
_PROFILE_PREFIX = "srbench-"
#: Grace period (seconds) to let the CLI exit after EndConversation before we
#: terminate it, and slack added on top of the agent timeout.
_GRACE_SECONDS = 30.0


def _bind_socket() -> socket.socket:
    """Bind an ephemeral localhost TCP socket and return it, still open.

    The bound socket is handed directly to uvicorn (``Server.serve(sockets=...)``)
    so the reserved port cannot be claimed by another concurrent OpenClaw agent
    between allocation and bind. Returning a port number instead would reopen a
    TOCTOU window that, under task concurrency, intermittently fails the bind and
    surfaces as an execution error.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
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


class OpenClawAgent(BaseAssistantAgent[AssistantTask]):
    """A task-agnostic assistant agent that drives the OpenClaw CLI.

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
        reasoning_effort: str | None = None,
        system_prompt: str | None = None,
    ) -> None:
        self.task = task
        self._model = model or os.environ.get("SRBENCH_OPENCLAW_MODEL")
        # Reasoning effort maps to the CLI ``--thinking`` level
        # (``off``/``minimal``/``low``/``medium``/``high``, plus
        # provider-supported ``xhigh``/``adaptive``/``max``); ``None`` uses the
        # CLI default.
        self._reasoning_effort = reasoning_effort or os.environ.get(
            "SRBENCH_OPENCLAW_REASONING_EFFORT"
        )
        # The harness may supply the operating system prompt; otherwise fall
        # back to this agent's built-in benchmark ground rules. OpenClaw's
        # one-shot CLI has no separate system-prompt channel, so it is prepended
        # to the opening message.
        self._system_prompt = (
            system_prompt
            or os.environ.get("SRBENCH_OPENCLAW_SYSTEM_PROMPT")
            or DEFAULT_ASSISTANT_SYSTEM_PROMPT
        )
        self._binary = os.environ.get("SRBENCH_OPENCLAW_BIN", "openclaw")
        self._agent_id = os.environ.get("SRBENCH_OPENCLAW_AGENT") or None
        self._timeout = float(self.task.max_actions) * 30.0 + 120.0
        self._ended = False
        self._proc: asyncio.subprocess.Process | None = None
        self._transcript: list[dict[str, str]] = []

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

    async def _openclaw(self, *args: str, profile: str) -> tuple[int, str, str]:
        """Run an ``openclaw`` management subcommand and capture its output."""
        proc = await asyncio.create_subprocess_exec(
            self._binary,
            "--profile",
            profile,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate()
        return proc.returncode or 0, out.decode(errors="replace"), err.decode(errors="replace")

    async def _verify_cli(self) -> None:
        """Ensure the OpenClaw CLI is installed and matches the pinned version."""
        try:
            proc = await asyncio.create_subprocess_exec(
                self._binary,
                "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"OpenClaw CLI {self._binary!r} not found. Install the pinned "
                f"release with: npm install -g openclaw@{OPENCLAW_VERSION}"
            ) from exc

        out, err = await proc.communicate()
        reported = (out or err).decode(errors="replace").strip()
        if OPENCLAW_VERSION not in reported:
            raise RuntimeError(
                f"OpenClaw CLI reports {reported!r}, but this agent is pinned to "
                f"v{OPENCLAW_VERSION}. Install it with: "
                f"npm install -g openclaw@{OPENCLAW_VERSION}"
            )

    async def run(
        self,
        invoke_tool: InvokeTool,
        tools: list[ChatCompletionFunctionToolParam],
    ) -> None:
        await self._verify_cli()

        server = build_server(tools, self._bridge(invoke_tool), name=_MCP_SERVER_NAME)
        sock = _bind_socket()
        port = sock.getsockname()[1]
        http = uvicorn.Server(
            uvicorn.Config(
                build_asgi_app(server), host="127.0.0.1", port=port, log_level="critical"
            )
        )
        # Hand the already-bound socket to uvicorn so the port cannot be stolen
        # by another concurrent agent between allocation and bind.
        serve_task = asyncio.create_task(http.serve(sockets=[sock]))
        profile = f"{_PROFILE_PREFIX}{uuid4().hex[:8]}"
        try:
            await _wait_until_listening("127.0.0.1", port)
            url = f"http://127.0.0.1:{port}/mcp"
            code, _out, err = await self._openclaw(
                "mcp",
                "set",
                _MCP_SERVER_NAME,
                json.dumps({"url": url, "transport": "streamable-http"}),
                profile=profile,
            )
            if code != 0:
                raise RuntimeError(f"`openclaw mcp set` failed (exit {code}): {err.strip()}")

            cmd = [self._binary, "--profile", profile, "agent", "--local"]
            if self._agent_id:
                cmd += ["--agent", self._agent_id]
            if self._model:
                cmd += ["--model", self._model]
            if self._reasoning_effort:
                cmd += ["--thinking", self._reasoning_effort]
            cmd += [
                "--session-key",
                profile,
                "--message",
                self._opening_message(),
                "--json",
                "--timeout",
                str(int(self._timeout)),
            ]
            self._proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await self._drive(self._proc)
        finally:
            # Critical, synchronous teardown first, so nothing leaks even if this
            # coroutine is being cancelled (e.g. the harness hit max rounds):
            # kill the subprocess, signal uvicorn to stop, and delete the
            # isolated profile (which also drops the MCP registration).
            self._terminate()
            http.should_exit = True
            _cleanup_profile(profile)
            if not serve_task.done():
                serve_task.cancel()
            with contextlib.suppress(BaseException):
                await serve_task
            # uvicorn closes the socket on shutdown; close defensively in case
            # startup never handed it off (double close is harmless).
            with contextlib.suppress(Exception):
                sock.close()

    async def _drive(self, proc: asyncio.subprocess.Process) -> None:
        """Wait for the OpenClaw run to finish and record its output."""
        try:
            out, err = await asyncio.wait_for(
                proc.communicate(), timeout=self._timeout + _GRACE_SECONDS
            )
        except asyncio.TimeoutError:
            self._terminate()
            self._transcript.append(
                {"role": "assistant", "content": "openclaw run timed out; terminated."}
            )
            return
        if out.strip():
            self._transcript.append({"role": "assistant", "content": out.decode(errors="replace")})
        if proc.returncode not in (0, None) and err.strip():
            self._transcript.append(
                {"role": "assistant", "content": f"openclaw stderr: {err.decode(errors='replace')}"}
            )

    def _terminate(self) -> None:
        """Terminate the OpenClaw subprocess if it is still running."""
        proc = self._proc
        if proc is not None and proc.returncode is None:
            with contextlib.suppress(ProcessLookupError):
                proc.terminate()


def _cleanup_profile(profile: str) -> None:
    """Remove the isolated OpenClaw profile directory we created for this run."""
    if not profile.startswith(_PROFILE_PREFIX):  # defensive: never touch other state
        return
    profile_dir = Path.home() / f".openclaw-{profile}"
    with contextlib.suppress(Exception):
        shutil.rmtree(profile_dir, ignore_errors=True)
