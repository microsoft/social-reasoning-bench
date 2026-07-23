"""A generic, LLM-driven BYOA agent built on the Claude Agent SDK.

:class:`ClaudeAgent` is a single "bring your own agent" implementation that
is *generic over the task*: it makes no assumption about which benchmark it is
running. It reads its private brief (whatever :class:`~srbench.shared.AssistantTask`
subclass it is handed) as JSON, exposes the environment's granted tool space to
Claude as in-process MCP tools, and lets Claude drive the conversation by
calling those tools. The exact same class therefore runs the calendar and the
marketplace benchmarks unchanged::

    srbench benchmark calendar \\
        --assistant-agent srbench_agents.claude_agent:ClaudeAgent ...
    srbench benchmark marketplace \\
        --buyer-agent srbench_agents.claude_agent:ClaudeAgent ...

This module depends on the optional ``claude-agent-sdk`` package. Install it
with ``pip install 'srbench-agents[claude]'`` and provide Claude credentials the
SDK understands (e.g. an ``ANTHROPIC_API_KEY`` environment variable).

Optional environment overrides:

- ``SRBENCH_CLAUDE_MODEL``            — model id for the run.
- ``SRBENCH_CLAUDE_REASONING_EFFORT`` — SDK ``effort`` level
  (``low``/``medium``/``high``/``xhigh``/``max``).
"""

from __future__ import annotations

import json
import os
from typing import Any, Literal, cast

from openai.types.chat import ChatCompletionFunctionToolParam
from srbench.mcp import build_server
from srbench.shared import AssistantTask, BaseAssistantAgent, InvokeTool

try:
    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        ClaudeSDKClient,
        TextBlock,
        ToolUseBlock,
    )
    from claude_agent_sdk.types import (
        PermissionResultAllow,
        PermissionResultDeny,
    )
except ImportError as exc:  # pragma: no cover - exercised only without the extra
    raise ImportError(
        "srbench_agents.claude_agent requires the optional 'claude-agent-sdk' "
        "dependency. Install it with: pip install 'srbench-agents[claude]'"
    ) from exc

_MCP_SERVER_NAME = "srbench"

# SDK ``effort`` levels; user-supplied effort is narrowed to this before use.
ClaudeEffort = Literal["low", "medium", "high", "xhigh", "max"]

_SYSTEM_PROMPT = """\
You are an autonomous agent participating in a social-reasoning benchmark. You \
can perceive and affect the world ONLY through the tools you are given; you \
have no other senses or abilities.

Ground rules:
- Your private task briefing arrives as JSON in the first message. Read it \
carefully to understand who you are, your objective, and any constraints.
- The other party has already made an opening move that is waiting for you. \
Call the `Wait` tool to receive it, and to receive anything they send later.
- Take exactly one concrete action at a time, then read its result before \
deciding your next action.
- After you act and are waiting on the other party to respond, call `Wait` to \
yield your turn. Do not poll repeatedly.
- When your objective is fully resolved, or you must refuse the request, call \
`EndConversation` with a brief reason. This permanently ends your participation.
- Rely only on tool results. Never invent facts, messages, or confirmations.
"""

_CONTINUE_PROMPT = (
    "Continue. Take your next action using a tool. If you are waiting on the "
    "other party, call `Wait`. If your objective is complete or you must "
    "refuse, call `EndConversation`."
)


class ClaudeAgent(BaseAssistantAgent[AssistantTask]):
    """A task-agnostic assistant agent powered by the Claude Agent SDK.

    The agent receives its task through the constructor and, in :meth:`run`,
    hands the environment's granted tool space and ``invoke_tool`` boundary to
    :func:`srbench.mcp.build_server`, then mounts the resulting MCP server
    in-process so Claude can call the tools. All tool logic and validation stay
    in the environment; this class only bridges Claude's tool calls to that
    boundary (and records a small debug transcript along the way).
    """

    def __init__(
        self,
        *,
        task: AssistantTask,
        model: str | None = None,
        reasoning_effort: str | None = None,
    ) -> None:
        self.task = task
        # Falls back to the SDK/CLI default model when unset.
        self._model = model or os.environ.get("SRBENCH_CLAUDE_MODEL")
        # Reasoning effort maps to the SDK ``effort`` option
        # (``low``/``medium``/``high``/``xhigh``/``max``); ``None`` uses the
        # SDK default. This forwards user-supplied input, so we narrow it to the
        # SDK's literal type for the option below.
        self._reasoning_effort = cast(
            "ClaudeEffort | None",
            reasoning_effort or os.environ.get("SRBENCH_CLAUDE_REASONING_EFFORT"),
        )
        self._ended = False
        self._transcript: list[dict[str, str]] = []

    @property
    def messages(self) -> list[dict[str, str]]:
        """Optional debugging transcript recorded by the executors."""
        return self._transcript

    def _opening_prompt(self) -> str:
        brief = self.task.model_dump_json(indent=2)
        return (
            "Here is your private task briefing as JSON. Read it, then begin by "
            "calling `Wait` to receive the other party's opening move.\n\n"
            f"```json\n{brief}\n```"
        )

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

    @staticmethod
    async def _permission(tool_name: str, input_data: dict[str, Any], context: Any):
        """Restrict Claude to the environment's tools only.

        The benchmark agent must never touch the host (no Bash/Read/Write); it
        may use only the in-process tools the environment granted.
        """
        if tool_name.startswith(f"mcp__{_MCP_SERVER_NAME}__"):
            return PermissionResultAllow(updated_input=input_data)
        return PermissionResultDeny(
            message="This benchmark agent may only use the tools provided by the environment."
        )

    def _observe(self, message: Any) -> None:
        """Record Claude's own text output for the debugging transcript."""
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock) and block.text.strip():
                    self._transcript.append({"role": "assistant", "content": block.text.strip()})
                elif isinstance(block, ToolUseBlock):
                    # Tool results are recorded by the handler; nothing to add.
                    pass

    async def run(
        self,
        invoke_tool: InvokeTool,
        tools: list[ChatCompletionFunctionToolParam],
    ) -> None:
        server = build_server(tools, self._bridge(invoke_tool), name=_MCP_SERVER_NAME)

        options = ClaudeAgentOptions(
            system_prompt=_SYSTEM_PROMPT,
            # Mount the reusable srbench MCP server in-process. The SDK routes
            # tool calls to ``server`` (a raw mcp.Server) directly; this is the
            # same shape ``create_sdk_mcp_server`` produces.
            mcp_servers={
                _MCP_SERVER_NAME: {
                    "type": "sdk",
                    "name": _MCP_SERVER_NAME,
                    "instance": server,
                }
            },
            # Disable every built-in Claude Code tool: this agent must act only
            # through the environment's tools, never the host (no Bash/Read/Write).
            tools=[],
            # Gate every remaining tool call through ``can_use_tool``: it
            # approves this environment's tools and denies anything else. We
            # deliberately do NOT list our tools in ``allowed_tools`` — that
            # would auto-approve them and shadow (bypass) the callback.
            can_use_tool=self._permission,
            model=self._model,
            effort=self._reasoning_effort,
            setting_sources=None,
            max_turns=self.task.max_actions * 4 + 10,
        )

        async with ClaudeSDKClient(options=options) as client:
            await client.query(self._opening_prompt())
            # Each pass drains one Claude response (which may itself chain many
            # tool calls). We re-prompt until the agent ends the conversation or
            # the environment cancels this coroutine when the run terminates.
            for _ in range(self.task.max_actions):
                async for message in client.receive_response():
                    self._observe(message)
                if self._ended:
                    break
                await client.query(_CONTINUE_PROMPT)
