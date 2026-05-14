"""Shared agent protocols + ``BaseAgent`` default implementation.

The executors of every SRBench benchmark drive two agents to a conclusion
without knowing how those agents are implemented. The contract surface they
depend on is the :class:`Agent` protocol; the role that drives a forced
opening action (calendar requestor, marketplace seller) additionally
satisfies :class:`CounterpartyAgent`.

Lifecycle
---------
The executor:

1. Constructs both agents via factories (passing an :class:`AgentContext`).
2. For the counterparty: composes the opening message body via
   :meth:`CounterpartyAgent.generate_text`, executes the deterministic
   opening action against the env, and records it on the agent's transcript
   via :meth:`CounterpartyAgent.add_forced_action`.
3. Awaits ``asyncio.wait({assistant.run(invoke_tool), counterparty.run(invoke_tool),
   env.end_event.wait()}, return_when=FIRST_COMPLETED)``. When one completes,
   the others are cancelled.
4. Calls :meth:`Agent.close` on both agents.

Inside :meth:`BaseAgent.run` the loop is:

    while remaining > 0:
        tool_call = await self.generate_tool_call()
        result = await invoke_tool(tool_call)
        self.add_tool_call_result(result)

The agent never inspects whether a particular tool ends the conversation;
that's the env's job (via ``env.end_event``). Cancellation propagates out
of any ``await`` to terminate the agent cleanly.
"""

from __future__ import annotations

import traceback
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Protocol, TypeAlias, cast

from openai.types.chat import (
    ChatCompletionFunctionToolParam,
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
)
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from pydantic import SkipValidation, ValidationError
from srbench_llm import SRBenchInputMessage, SRBenchModelClient

from .tool import Tool

# ---------------------------------------------------------------------------
# Public protocol surface
# ---------------------------------------------------------------------------

# Pydantic-friendly alias for stored transcripts: structurally identical to
# ``ChatCompletionMessageParam`` for type-checking, but flagged with
# ``SkipValidation`` so pydantic does not eagerly convert ``tool_calls``
# (typed as ``Iterable``) into a single-consume ValidatorIterator.
AgentMessage: TypeAlias = SkipValidation[ChatCompletionMessageParam]

# The agent's only env touchpoint: hand a Tool, get back a result string.
# The executor binds the env-specific resource execute method into this
# callback before passing it to ``Agent.run``.
InvokeTool: TypeAlias = Callable[[Tool], Awaitable[str]]


class Agent(Protocol):
    """Minimum surface for an agent under evaluation (assistant / buyer).

    Concrete implementations are constructed by per-role factories from an
    :class:`AgentContext`. The executor calls :meth:`run` (driving the
    agent's loop), reads :attr:`messages` and :attr:`tools` after the
    conversation ends (eval transcripts), and calls :meth:`close` for
    cleanup.
    """

    @property
    def messages(self) -> list[AgentMessage]: ...

    @property
    def tools(self) -> list[ChatCompletionFunctionToolParam]: ...

    async def run(self, invoke_tool: InvokeTool) -> None: ...

    async def close(self) -> None: ...


class CounterpartyAgent(Agent, Protocol):
    """Adds the capabilities needed to drive a deterministic opening action.

    The counterparty role (calendar requestor, marketplace seller) must
    satisfy this protocol so the harness can ask it to compose the
    natural-language body of the opening message and then record the
    resulting forced action on its transcript.
    """

    async def generate_text(self, prompt: str) -> str: ...

    def add_forced_action(self, action: Tool, result: str) -> None: ...


@dataclass(frozen=True)
class AgentContext:
    """Everything a factory needs to construct an :class:`Agent` for one role.

    Fields below ``explicit_cot`` are conveniences for the default
    :class:`BaseAgent`-derived implementations; BYO agents may ignore them or
    pull what they need from ``extras``.
    """

    role: str
    tools: list[type[Tool]]
    system_prompt: str | None
    instruction_message: str
    explicit_cot: bool
    model: str | None = None
    model_client: SRBenchModelClient | None = None
    max_actions: int = 50
    extras: dict[str, Any] = field(default_factory=dict)


AgentFactory: TypeAlias = Callable[[AgentContext], Agent]
CounterpartyAgentFactory: TypeAlias = Callable[[AgentContext], CounterpartyAgent]


# ---------------------------------------------------------------------------
# BaseAgent default implementation
# ---------------------------------------------------------------------------


class RetryException(Exception):
    """Raised when a model response cannot be parsed as a valid single tool call.

    Used internally by ``BaseAgent.generate_tool_call`` to trigger retries.
    """


class ToolCallRetriesExhausted(ExceptionGroup):
    """Raised when ``generate_tool_call`` exhausts all retries."""


class BaseAgent:
    """Default :class:`CounterpartyAgent` implementation backed by an LLM.

    Subclasses customize prompts (system message, instruction, role-specific
    user content) by appending to ``self._messages`` after ``super().__init__``.

    The class satisfies both :class:`Agent` and :class:`CounterpartyAgent`
    structurally — it exposes ``generate_text`` and ``add_forced_action`` even
    though the minimal Agent protocol does not require them. This lets the
    same concrete class be used in either role.
    """

    def __init__(
        self,
        *,
        model: str,
        model_client: SRBenchModelClient,
        tools: list[type[Tool]],
        explicit_cot: bool = False,
        temperature: float | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam = "auto",
        prompt_label: str = "unknown",
        max_actions: int = 50,
    ) -> None:
        self._model = model
        self._model_client = model_client
        self._prompt_label = prompt_label
        self._messages: list[SRBenchInputMessage] = []
        self._explicit_cot = explicit_cot
        self._temperature = temperature
        self._tool_choice = tool_choice
        self._max_actions = max_actions

        # Build tool registry: name -> Tool class
        self._tools: dict[str, type[Tool]] = {t.get_name(): t for t in tools}

        # Pre-compute OpenAI tool definitions
        self._openai_tools: list[ChatCompletionFunctionToolParam] = [
            t.get_openai_function_tool_param() for t in tools
        ]

    # ------------------------------------------------------------------ #
    # Agent protocol surface
    # ------------------------------------------------------------------ #

    @property
    def messages(self) -> list[AgentMessage]:
        """Return a shallow copy of the canonical transcript."""
        return cast(list[AgentMessage], list(self._messages))

    @property
    def tools(self) -> list[ChatCompletionFunctionToolParam]:
        """Return the agent's OpenAI-format tool definitions."""
        return list(self._openai_tools)

    async def run(self, invoke_tool: InvokeTool) -> None:
        """Drive the agent's tool-call loop until cancelled or exhausted.

        The loop:
          1. ``generate_tool_call`` (LLM + retries) → parsed Tool.
          2. ``await invoke_tool(tool)`` → result string (the executor's
             env-bound callback; raises ToolError-derived strings as a regular
             result, see env-side ``execute``).
          3. ``add_tool_call_result(result)`` → append to transcript.
          4. Decrement budget; repeat.

        Termination paths:
          - ``self._max_actions`` exhausted → return.
          - ``ToolCallRetriesExhausted`` from generate_tool_call → return.
          - Cancellation from outside (executor cancelling on end_event /
            wall-clock) → propagates out as ``CancelledError``.

        The loop does NOT inspect tool-call types to detect termination.
        ``EndConversation`` (or any benchmark-specific terminator) is the
        env's concern: its ``execute`` sets ``env.end_event`` and the
        executor cancels this task as a consequence.
        """
        remaining = self._max_actions
        while remaining > 0:
            try:
                tool_call = await self.generate_tool_call()
            except ToolCallRetriesExhausted:
                return
            result = await invoke_tool(tool_call)
            self.add_tool_call_result(result)
            remaining -= 1

    async def close(self) -> None:
        """No-op for pure in-process agents."""

    # ------------------------------------------------------------------ #
    # CounterpartyAgent protocol surface
    # ------------------------------------------------------------------ #

    async def generate_text(self, prompt: str) -> str:
        """Call the model without tools and return a plain text response.

        Used by ``_force_initial_*`` helpers to have the counterparty compose
        the natural-language body of the opening message.
        """
        from srbench_llm.concurrency import prompt_label

        messages: list[SRBenchInputMessage] = [
            *self._messages,
            {"role": "user", "content": prompt},
        ]
        token = prompt_label.set(self._prompt_label)
        try:
            response = await self._model_client.acomplete(
                model=self._model,
                messages=messages,
            )
        finally:
            prompt_label.reset(token)
        return response.content or ""

    def add_forced_action(self, action: Tool, result: str) -> None:
        """Record a deterministic harness-driven tool call + result on the transcript.

        Used at startup to seed the conversation with the predetermined
        opening action (initial RequestMeeting / MakeOffer) so the
        counterparty's transcript reflects the action as if it had called the
        tool itself.
        """
        tool_call_id = str(len(self._messages))
        self._messages.append(
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tool_call_id,
                        "type": "function",
                        "function": {
                            "name": action.get_name(),
                            "arguments": action.model_dump_json(),
                        },
                    }
                ],
            }
        )
        self._messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": result,
            }
        )

    # ------------------------------------------------------------------ #
    # Internal helpers used by ``run``
    # ------------------------------------------------------------------ #

    def add_tool_call_result(self, result: str) -> None:
        """Append a tool result message for the most recent tool call."""
        last = self._messages[-1] if self._messages else None
        tc = last.get("tool_calls") if last else None
        if not tc:
            raise ValueError("Expected previous message to be an assistant tool-call message")
        tool_calls = list(tc)
        if len(tool_calls) != 1:
            raise ValueError("Can only call add_tool_call_result after exactly one tool call")
        tool_call_id = tool_calls[0]["id"]
        self._messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": result,
            }
        )

    def on_retry_no_tool_calls(self) -> str:
        """Return the user message sent when the LLM produces no tool calls."""
        return "The user is unavailable. Work autonomously. You must call exactly one tool."

    def on_retry_invalid_tool_call(self, error: Exception) -> str:
        """Return the user message sent when a tool call fails parsing/validation."""
        return f"Your previous response was invalid: {error}. Return exactly one valid tool call."

    async def _generate_cot_reasoning(self, messages: list[SRBenchInputMessage]) -> str:
        from srbench_llm.concurrency import prompt_label

        cot_messages = list(messages)
        cot_messages.append(
            {
                "role": "user",
                "content": (
                    "Before taking your next action, think carefully about what "
                    "should be the one next action (ONE next tool call) to do. "
                    "Generate the thoughts here."
                ),
            }
        )
        token = prompt_label.set(self._prompt_label)
        try:
            response = await self._model_client.acomplete(
                model=self._model,
                messages=cot_messages,
            )
        finally:
            prompt_label.reset(token)
        return response.content or ""

    async def generate_tool_call(self, max_retries: int = 3) -> Tool:
        """Generate the next tool call from the LLM, with retries on parse errors."""
        messages = list(self._messages)
        exceptions: list[Exception] = []

        for _ in range(max(1, max_retries)):
            cot_thinking: str | None = None
            if self._explicit_cot:
                cot_thinking = await self._generate_cot_reasoning(messages)
                if cot_thinking:
                    messages.append({"role": "assistant", "content": cot_thinking})

            from srbench_llm.concurrency import prompt_label

            gen_kwargs: dict[str, Any] = {}
            if self._temperature is not None:
                gen_kwargs["temperature"] = self._temperature
            token = prompt_label.set(self._prompt_label)
            try:
                message = await self._model_client.acomplete(
                    model=self._model,
                    messages=messages,
                    tools=self._openai_tools,
                    tool_choice=self._tool_choice,
                    **gen_kwargs,
                )
            finally:
                prompt_label.reset(token)

            tool_calls = message.tool_calls or []

            try:
                if len(tool_calls) != 1:
                    if len(tool_calls) == 0:
                        raise RetryException(
                            f"Exactly one tool call is required, but got 0. "
                            f"Model text: {message.content!r}"
                        )
                    else:
                        names = [
                            tc.function.name
                            for tc in tool_calls
                            if isinstance(tc, ChatCompletionMessageToolCall)
                        ]
                        raise RetryException(
                            f"Exactly one tool call is required, but got {len(tool_calls)}: {names}"
                        )

                tool_call = tool_calls[0]
                if not isinstance(tool_call, ChatCompletionMessageToolCall):
                    raise RetryException(f"Unsupported tool call type: {type(tool_call)}")
                if tool_call.type != "function":
                    raise RetryException(f"Unsupported tool type '{tool_call.type}'")

                function = tool_call.function
                tool_type = self._tools.get(function.name)
                if tool_type is None:
                    raise RetryException(
                        f"Unrecognized function name '{function.name}'. "
                        f"Available tools: {list(self._tools.keys())}"
                    )

                parsed_tool_call = tool_type.model_validate_json(function.arguments)

                # Commit successful parse to canonical history.
                if cot_thinking:
                    self._messages.append({"role": "assistant", "content": cot_thinking})

                self._messages.append(
                    message.model_copy(update={"tool_calls": [tool_call]}).to_input_dict()
                )

                return parsed_tool_call

            except (ValidationError, RetryException) as e:
                exceptions.append(e)

                if not tool_calls:
                    messages.append({"role": "assistant", "content": message.content})
                    messages.append(
                        {"role": "user", "content": self.on_retry_no_tool_calls()},
                    )
                else:
                    messages.append(message.to_input_dict())
                    for tc in tool_calls:
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "content": traceback.format_exc(),
                            },
                        )

        raise ToolCallRetriesExhausted("Exceeded maximum retries generating tool call", exceptions)

    # ------------------------------------------------------------------ #
    # Back-compat aliases (existing callers reach for these names)
    # ------------------------------------------------------------------ #

    async def generate_text_response(self, prompt: str) -> str:
        """Alias retained for back-compat; prefer :meth:`generate_text`."""
        return await self.generate_text(prompt)
