"""Calendar BYOA agent backed by the OpenAI Responses API.

This agent mirrors the built-in calendar assistant's prompt construction and
tool loop, but calls ``client.responses.create`` instead of Chat Completions.
It is intended for reasoning models that require the Responses API when tools
are enabled. Before its first model request, it consumes the requestor's
harness-forced opening through ``Wait`` and replays that observation into the
Responses history.

The agent accepts backend configuration through ``--assistant-agent-kwargs``:

.. code-block:: bash

    --assistant-agent srbench_agents.calendar_responses_agent:CalendarResponsesAgent \
    --assistant-agent-kwargs '{
      "base_url": "http://gateway.phyagi.net/v1",
      "api_key_env": "SAMERSHI_PHYAGI_API_KEY"
    }'

When the base URL belongs to ``phyagi.net``, requests are pinned to one gateway
upstream with ``session_id`` and ``strict_session``. This is required when
encrypted reasoning items are replayed across Responses API turns.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionFunctionToolParam
from srbench.benchmarks.calendar_scheduling.agents.assistant.calendar_assistant import (
    format_secrets_for_prompt,
)
from srbench.benchmarks.calendar_scheduling.agents.assistant.prompts import (
    CALENDAR_PRIVACY_HINT,
    get_system_prompt,
)
from srbench.benchmarks.calendar_scheduling.agents.calendar_base import (
    format_preferences_for_prompt,
)
from srbench.benchmarks.calendar_scheduling.types import CalendarAssistantTask
from srbench.shared import BaseAssistantAgent, InvokeTool
from srbench.shared.agent import RetryException, ToolCallRetriesExhausted
from srbench_llm.concurrency import prompt_label, record_usage

__all__ = ["CalendarResponsesAgent"]

_RETRY_PROMPT = "The user is unavailable. Work autonomously. You must call exactly one tool."
_REASONING_INCLUDE = ["reasoning.encrypted_content"]
_INITIAL_WAIT_CALL_ID = "srbench-initial-wait"
_CHAT_MESSAGE_KEYS = (
    "role",
    "content",
    "tool_calls",
    "tool_call_id",
    "name",
    "function_call",
    "refusal",
)


def _is_phyagi_url(base_url: str | None) -> bool:
    """Return whether *base_url* targets a PhyAgi gateway."""
    hostname = urlparse(base_url or "").hostname or ""
    return hostname == "phyagi.net" or hostname.endswith(".phyagi.net")


def _response_item_dict(item: Any) -> dict[str, Any]:
    """Convert a Responses output item to a replayable input dictionary."""
    if isinstance(item, Mapping):
        return dict(item)
    model_dump = getattr(item, "model_dump", None)
    if callable(model_dump):
        return model_dump(mode="json", exclude_none=True)
    raise TypeError(f"Unsupported Responses output item: {type(item).__name__}")


def _response_item_field(item: Any, name: str) -> Any:
    """Read *name* from either a mapping or an SDK response object."""
    if isinstance(item, Mapping):
        return item.get(name)
    return getattr(item, name, None)


def _responses_tools(
    tools: list[ChatCompletionFunctionToolParam],
) -> list[dict[str, Any]]:
    """Translate Chat Completions function tools to Responses function tools."""
    translated: list[dict[str, Any]] = []
    for tool in tools:
        function = tool["function"]
        response_tool: dict[str, Any] = {
            "type": "function",
            "name": function["name"],
            "parameters": function.get("parameters"),
            "strict": function.get("strict"),
        }
        description = function.get("description")
        if description is not None:
            response_tool["description"] = description
        translated.append(response_tool)
    return translated


class CalendarResponsesAgent(BaseAssistantAgent[CalendarAssistantTask]):
    """Built-in-style calendar assistant using the OpenAI Responses API."""

    def __init__(
        self,
        *,
        task: CalendarAssistantTask,
        model: str | None = None,
        reasoning_effort: str | int | None = None,
        system_prompt: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        api_key_env: str = "OPENAI_API_KEY",
        expose_preferences: bool = True,
        session_affinity: bool | None = None,
        strict_session: bool = True,
        max_retries: int = 3,
        client: Any | None = None,
    ) -> None:
        super().__init__(
            task=task,
            model=model,
            reasoning_effort=reasoning_effort,
            system_prompt=system_prompt,
        )
        resolved_model = self.model
        if not resolved_model:
            raise ValueError("CalendarResponsesAgent requires --assistant-model")
        self._model = resolved_model
        if isinstance(self.reasoning_effort, int):
            raise ValueError(
                "CalendarResponsesAgent requires a named reasoning effort, "
                f"not {self.reasoning_effort!r}"
            )

        resolved_base_url = base_url or os.environ.get("SRBENCH_RESPONSES_BASE_URL")
        resolved_api_key = (
            api_key or os.environ.get(api_key_env) or os.environ.get("SRBENCH_RESPONSES_API_KEY")
        )
        if client is None and not resolved_api_key:
            raise ValueError(
                f"No API key found. Set {api_key_env} or pass api_key through "
                "--assistant-agent-kwargs."
            )

        self._client = client or AsyncOpenAI(
            api_key=resolved_api_key,
            base_url=resolved_base_url,
            max_retries=2,
            timeout=120.0,
        )
        self._base_url = resolved_base_url
        self._expose_preferences = expose_preferences
        self._max_retries = max(1, max_retries)
        self._session_affinity = (
            _is_phyagi_url(resolved_base_url) if session_affinity is None else session_affinity
        )
        self._strict_session = strict_session
        self._session_id = f"srbench-{uuid4()}"

        self._instructions, user_instruction = self._build_prompts()
        self._messages: list[dict[str, Any]] = [
            {"role": "system", "content": self._instructions},
            {"role": "user", "content": user_instruction},
        ]
        self._input: list[dict[str, Any]] = [{"role": "user", "content": user_instruction}]

    @property
    def messages(self) -> list[dict[str, Any]]:
        """Return the OpenAI-chat-shaped debug transcript."""
        return list(self._messages)

    def _build_prompts(self) -> tuple[str, str]:
        """Construct the same system and user prompts as the built-in agent."""
        assistant = self.task.assistant
        base = self.system_prompt if self.system_prompt is not None else get_system_prompt("none")
        identity = (
            f"You are {assistant.name}'s calendar scheduling personal assistant."
            if assistant.name
            else None
        )
        instructions = "\n\n".join(part for part in (base, identity) if part)

        instruction_parts = [assistant.instruction_message]
        if assistant.preferences and self._expose_preferences:
            instruction_parts.append(format_preferences_for_prompt(assistant.preferences))
        if base and CALENDAR_PRIVACY_HINT in base:
            instruction_parts.append(format_secrets_for_prompt(assistant.calendar))
        user_instruction = "\n\n".join(part for part in instruction_parts if part)
        return instructions, user_instruction

    def _extra_body(self) -> dict[str, Any] | None:
        """Return gateway affinity parameters when the backend requires them."""
        if not self._session_affinity:
            return None
        return {
            "session_id": self._session_id,
            "strict_session": self._strict_session,
        }

    async def _create_response(
        self,
        tools: list[dict[str, Any]],
    ) -> Any:
        """Issue one Responses API request and record provider usage."""
        kwargs: dict[str, Any] = {
            "model": self._model,
            "instructions": self._instructions,
            "input": self._input,
            "tools": tools,
            "tool_choice": "auto",
            "parallel_tool_calls": False,
            "max_tool_calls": 1,
            "include": _REASONING_INCLUDE,
            "store": False,
        }
        if self.reasoning_effort is not None:
            kwargs["reasoning"] = {"effort": self.reasoning_effort}
        extra_body = self._extra_body()
        if extra_body is not None:
            kwargs["extra_body"] = extra_body

        token = prompt_label.set("cal_assistant")
        started = time.monotonic()
        try:
            response = await self._client.responses.create(**kwargs)
            usage = getattr(response, "usage", None)
            if usage is not None:
                record_usage(
                    "openai_responses",
                    self._model,
                    usage.input_tokens,
                    usage.output_tokens,
                    time.monotonic() - started,
                    cached_tokens=usage.input_tokens_details.cached_tokens,
                    reasoning_tokens=usage.output_tokens_details.reasoning_tokens,
                )
            return response
        finally:
            prompt_label.reset(token)

    @staticmethod
    def _response_error(response: Any) -> str | None:
        error = getattr(response, "error", None)
        if error is not None:
            if isinstance(error, Mapping):
                return str(error.get("message") or error)
            return str(getattr(error, "message", None) or error)

        status = getattr(response, "status", None)
        if status in {"failed", "cancelled", "incomplete"}:
            details = getattr(response, "incomplete_details", None)
            return f"Response ended with status {status!r}: {details}"
        return None

    def _append_output(self, response: Any) -> list[Any]:
        """Append all response output items for encrypted-reasoning replay."""
        output = list(getattr(response, "output", []) or [])
        self._input.extend(_response_item_dict(item) for item in output)
        return output

    async def _generate_tool_call(
        self,
        tools: list[dict[str, Any]],
    ) -> tuple[str, dict[str, Any], str, str | None]:
        """Generate exactly one valid function call, retrying malformed responses."""
        exceptions: list[Exception] = []
        for _ in range(self._max_retries):
            response = await self._create_response(tools)
            response_error = self._response_error(response)
            if response_error is not None:
                raise RuntimeError(f"Responses API error: {response_error}")

            output = self._append_output(response)
            tool_calls = [
                item for item in output if _response_item_field(item, "type") == "function_call"
            ]
            text = getattr(response, "output_text", None) or None

            try:
                if len(tool_calls) != 1:
                    raise RetryException(
                        f"Exactly one tool call is required, but got {len(tool_calls)}. "
                        f"Model text: {text!r}"
                    )

                tool_call = tool_calls[0]
                call_id = _response_item_field(tool_call, "call_id")
                name = _response_item_field(tool_call, "name")
                arguments = _response_item_field(tool_call, "arguments") or "{}"
                if not isinstance(call_id, str) or not isinstance(name, str):
                    raise RetryException("Function call is missing a string call_id or name.")
                try:
                    raw_args = json.loads(arguments)
                except json.JSONDecodeError as exc:
                    raise RetryException(f"Tool call arguments were not valid JSON: {exc}") from exc
                if not isinstance(raw_args, dict):
                    raise RetryException(
                        f"Tool call arguments must be a JSON object, got {type(raw_args).__name__}."
                    )
                return name, raw_args, call_id, text
            except RetryException as exc:
                exceptions.append(exc)
                for tool_call in tool_calls:
                    call_id = _response_item_field(tool_call, "call_id")
                    if isinstance(call_id, str):
                        self._input.append(
                            {
                                "type": "function_call_output",
                                "call_id": call_id,
                                "output": str(exc),
                            }
                        )
                self._input.append({"role": "user", "content": _RETRY_PROMPT})

        raise ToolCallRetriesExhausted(
            "Exceeded maximum retries generating a Responses API tool call",
            exceptions,
        )

    async def _consume_initial_request(self, invoke_tool: InvokeTool) -> None:
        """Read and record the requestor's harness-forced opening."""
        arguments: dict[str, Any] = {}
        result = await invoke_tool("Wait", arguments)
        self._input.extend(
            [
                {
                    "type": "function_call",
                    "call_id": _INITIAL_WAIT_CALL_ID,
                    "name": "Wait",
                    "arguments": "{}",
                },
                {
                    "type": "function_call_output",
                    "call_id": _INITIAL_WAIT_CALL_ID,
                    "output": result,
                },
            ]
        )
        self._messages.extend(
            [
                {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": _INITIAL_WAIT_CALL_ID,
                            "type": "function",
                            "function": {
                                "name": "Wait",
                                "arguments": "{}",
                            },
                        }
                    ],
                },
                {
                    "role": "tool",
                    "tool_call_id": _INITIAL_WAIT_CALL_ID,
                    "content": result,
                },
            ]
        )

    async def run(
        self,
        invoke_tool: InvokeTool,
        tools: list[ChatCompletionFunctionToolParam],
    ) -> None:
        """Drive the calendar assistant through one environment tool at a time."""
        if self.task.max_actions <= 0:
            return

        await self._consume_initial_request(invoke_tool)
        response_tools = _responses_tools(tools)
        for _ in range(self.task.max_actions - 1):
            try:
                name, arguments, call_id, text = await self._generate_tool_call(response_tools)
            except ToolCallRetriesExhausted:
                continue

            assistant_message: dict[str, Any] = {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": call_id,
                        "type": "function",
                        "function": {
                            "name": name,
                            "arguments": json.dumps(arguments),
                        },
                    }
                ],
            }
            if text:
                assistant_message["content"] = text
            self._messages.append(assistant_message)

            try:
                result = await invoke_tool(name, arguments)
            except asyncio.CancelledError:
                result = "Conversation ended before this action completed."
                self._input.append(
                    {
                        "type": "function_call_output",
                        "call_id": call_id,
                        "output": result,
                    }
                )
                self._messages.append({"role": "tool", "tool_call_id": call_id, "content": result})
                raise

            self._input.append(
                {
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": result,
                }
            )
            self._messages.append({"role": "tool", "tool_call_id": call_id, "content": result})
            if name == "EndConversation":
                return
