"""Shared BaseAgent class for all SRBench benchmarks.

Captures the common pattern across the benchmark agent implementations:
- calendar_scheduling/agents/calendar_base.py (CalendarAgent)
- marketplace/agents/marketplace_base.py (MarketplaceAgent)

Common patterns unified here:
- Message history management (append-only list of ChatCompletionMessageParam)
- Tool registry (name -> Tool class mapping)
- Tool call generation via LLM with JSON parsing and retries
- Optional explicit chain-of-thought reasoning
- Injecting tool call results into history

Benchmark-specific subclasses add:
- Custom retry error messages (calendar vs marketplace style)
"""

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

# Pydantic-friendly OpenAI message alias. Structurally identical to
# ``ChatCompletionMessageParam`` for type-checking; ``SkipValidation`` tells
# pydantic to store the dicts verbatim (avoids the ``ValidatorIterator``
# footgun on ``Iterable``-typed ``tool_calls`` fields).
AgentMessage: TypeAlias = SkipValidation[ChatCompletionMessageParam]

# The agent's only env touchpoint: pass a Tool, get back a result string.
# The executor binds env-specific resource ``execute`` into this callback
# before passing it to :meth:`Agent.run`.
InvokeTool: TypeAlias = Callable[[Tool], Awaitable[str]]


class Agent(Protocol):
    """Minimum surface for an agent under evaluation (assistant / buyer).

    The benchmark executors only depend on this surface; everything else
    (model client, prompting strategy, retry behavior, provider-specific
    metadata handling) is an implementation detail of the concrete agent.
    """

    @property
    def messages(self) -> list[AgentMessage]: ...

    @property
    def tools(self) -> list[ChatCompletionFunctionToolParam]: ...

    async def run(self, invoke_tool: InvokeTool) -> None: ...

    async def close(self) -> None: ...


class CounterpartyAgent(Agent, Protocol):
    """Extends :class:`Agent` with the capabilities the harness needs to
    drive the deterministic opening action in the counterparty's voice.

    The counterparty role (calendar requestor / marketplace seller) must
    satisfy this protocol because the harness asks it to compose the
    natural-language body of the opening action (initial ``RequestMeeting``
    / ``MakeOffer``) and then records the resulting forced action on its
    transcript.
    """

    async def generate_text(self, prompt: str) -> str: ...

    def add_forced_action(self, action: Tool, result: str) -> None: ...


@dataclass(frozen=True)
class AgentContext:
    """Everything a factory needs to construct an :class:`Agent` for one role.

    Fields below ``explicit_cot`` are conveniences for the default
    :class:`BaseAgent`-derived implementations; BYO agents may ignore them
    or pull what they need from ``extras``.
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


class RetryException(Exception):
    """Raised when a model response cannot be parsed as a valid single tool call.

    Used internally by generate_tool_call to trigger retry logic.
    """

    pass


class ToolCallRetriesExhausted(ExceptionGroup):
    """Raised when generate_tool_call exhausts all retries.

    Callers can catch this to handle gracefully (e.g., end the current turn)
    rather than treating it as a fatal error.
    """

    pass


class BaseAgent:
    """Base LLM agent with tool calling and retries.

    This class provides the common infrastructure shared by all benchmark agents:

    - **Tool registry**: Maps tool names to Tool subclasses for parsing.
    - **Message history**: Maintains the conversation as a list of
      ``ChatCompletionMessageParam`` dicts, supporting tool calls and results.
    - **Tool call generation**: Calls the LLM with tools, parses the response
      into a ``Tool`` instance, and handles retries on parse/validation errors.
    - **Explicit CoT**: Optionally generates chain-of-thought reasoning before
      each tool call to improve decision quality.

    Subclasses should:

    1. Call ``super().__init__(...)`` with their tool list and configuration.
    2. Set up initial messages (system prompt, instructions) by appending to
       ``self._messages``.
    3. Optionally override ``on_retry_no_tool_calls()`` and
       ``on_retry_invalid_tool_call()`` for custom retry error messages.
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
        """Initialize the base agent.

        Args:
            model: Model identifier for LLM calls (e.g., "gpt-4.1").
            model_client: ``SRBenchModelClient`` instance for API calls.
            tools: List of ``Tool`` subclasses this agent can use.
            explicit_cot: If ``True``, generate chain-of-thought reasoning
                before each tool call via a separate LLM call.
            temperature: Sampling temperature for LLM generation. If ``None``
                (default), the model's default temperature is used.
            tool_choice: Tool choice mode for the LLM (default ``"auto"``).
                Use ``"required"`` to force the model to always produce a
                tool call.
            prompt_label: Label for token tracking (e.g., "interviewer",
                "assistant"). Used by the concurrency module to report
                per-prompt token breakdowns.
            max_actions: Self-imposed budget on the number of tool calls
                :meth:`run` will issue before returning. The agent never
                inspects which tools terminate -- ``env.end_event`` plus
                executor cancellation handle that. ``max_actions`` is a
                belt-and-braces cap that bounds cost in pathological cases.
        """
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
    # :class:`Agent` protocol surface
    # ------------------------------------------------------------------ #

    async def run(self, invoke_tool: InvokeTool) -> None:
        """Drive the tool-call loop until ``max_actions`` is exhausted or
        retries are exhausted.

        The loop:
          1. :meth:`generate_tool_call` (LLM + retries) -> parsed Tool.
          2. ``await invoke_tool(tool)`` -> result string (the executor's
             env-bound callback; ToolError-derived errors come back as
             result strings, not exceptions).
          3. :meth:`add_tool_call_result` -> append to transcript.
          4. Decrement budget; repeat.

        The agent does NOT inspect which tools terminate -- ``env.end_event``
        and executor-driven cancellation handle that uniformly.
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
        """No-op for pure in-process agents. Subclasses that own external
        resources (subprocesses, sockets) override this for cleanup.
        """

    @property
    def messages(self) -> list[AgentMessage]:
        """Return the current message history (read-only view).

        Widened to the plain OpenAI union to match the :class:`Agent`
        protocol; provider-specific extension keys on assistant messages
        (e.g. Anthropic ``thinking_blocks``, Gemini ``thought_parts``)
        survive as extra dict keys.

        Returns:
            A shallow copy of the internal message list.
        """
        return cast(list[AgentMessage], list(self._messages))

    @property
    def tools(self) -> list[ChatCompletionFunctionToolParam]:
        """Return the tool definitions in OpenAI format.

        Returns:
            A list of OpenAI-compatible function tool parameter definitions.
        """
        return list(self._openai_tools)

    # ------------------------------------------------------------------ #
    # Message history helpers
    # ------------------------------------------------------------------ #

    def add_tool_call_result(self, result: str) -> None:
        """Append a tool result message for the most recent tool call.

        Expects the last message in history to be an assistant message with
        exactly one tool call.

        Args:
            result: The string result of executing the tool.

        Raises:
            ValueError: If the last message is not an assistant tool-call message.
        """
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

    def add_forced_action(self, action: Tool, result: str) -> None:
        """Record a programmatic (non-LLM) tool call and its result.

        Used when the harness forces an initial action (e.g., the first meeting
        request from the requestor in calendar scheduling).

        Args:
            action: The Tool instance representing the forced action.
            result: The string result of executing the action.
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
    # Retry message hooks (override in subclasses for custom wording)
    # ------------------------------------------------------------------ #

    def on_retry_no_tool_calls(self) -> str:
        """Return the user message to send when the LLM produces no tool calls.

        Override to customize the retry prompt for your benchmark.

        Returns:
            A user-role message string instructing the model to produce a tool call.
        """
        return "The user is unavailable. Work autonomously. You must call exactly one tool."

    def on_retry_invalid_tool_call(self, error: Exception) -> str:
        """Return the user message to send when a tool call fails validation.

        Override to customize the retry prompt for your benchmark.

        Args:
            error: The exception that caused the retry.

        Returns:
            A user-role message string describing the validation error and requesting a valid tool call.
        """
        return f"Your previous response was invalid: {error}. Return exactly one valid tool call."

    # ------------------------------------------------------------------ #
    # Explicit chain-of-thought
    # ------------------------------------------------------------------ #

    async def _generate_cot_reasoning(self, messages: list[SRBenchInputMessage]) -> str:
        """Generate chain-of-thought reasoning before a tool call.

        Makes a separate LLM call without tools to produce internal reasoning,
        which is then included in the context for the actual tool-calling step.

        Args:
            messages: The current message history to reason about.

        Returns:
            The generated reasoning text.
        """
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

    # ------------------------------------------------------------------ #
    # Core tool call generation
    # ------------------------------------------------------------------ #

    async def generate_tool_call(self, max_retries: int = 3) -> Tool:
        """Generate the next tool call from the LLM.

        Calls the model with the current message history and tool definitions,
        parses the response into a Tool instance, and appends the assistant
        message to history. On failure (parse error, validation error, wrong
        number of tool calls), retries up to ``max_retries`` times with error
        feedback injected into the conversation.

        Args:
            max_retries: Maximum number of attempts before raising.

        Returns:
            A parsed ``Tool`` instance representing the chosen action.

        Raises:
            ExceptionGroup: If all retries are exhausted, containing all
                collected exceptions.
        """
        # Work on a local copy so retries don't pollute the canonical history
        messages = list(self._messages)
        exceptions: list[Exception] = []

        for _ in range(max(1, max_retries)):
            # Optionally generate CoT reasoning
            cot_thinking: str | None = None
            if self._explicit_cot:
                cot_thinking = await self._generate_cot_reasoning(messages)
                if cot_thinking:
                    messages.append({"role": "assistant", "content": cot_thinking})

            # Call the LLM
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

                # Successfully parsed -- commit to canonical history
                if cot_thinking:
                    self._messages.append({"role": "assistant", "content": cot_thinking})

                # Keep the original message so provider-specific fields
                # (e.g. thought_signature for Gemini 3+) are preserved.
                self._messages.append(
                    message.model_copy(update={"tool_calls": [tool_call]}).to_input_dict()
                )

                return parsed_tool_call

            except (ValidationError, RetryException) as e:
                exceptions.append(e)

                if not tool_calls:
                    # No tool calls -- use plain assistant/user message for retry
                    messages.append({"role": "assistant", "content": message.content})
                    messages.append(
                        {"role": "user", "content": self.on_retry_no_tool_calls()},
                    )
                else:
                    # Invalid tool calls -- echo them back with error details.
                    # Preserve the original message to keep provider-specific
                    # fields (e.g. thought_signature).
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
    # Text-only generation (no tools)
    # ------------------------------------------------------------------ #

    async def generate_text(self, prompt: str) -> str:
        """Call the model without tools and return a plain text response.

        Satisfies the :class:`CounterpartyAgent` protocol surface used to
        compose the deterministic opening action body.

        Args:
            prompt: A user message to append (on a copy) before calling.

        Returns:
            The model's text response.
        """
        from srbench_llm.concurrency import prompt_label

        messages: list[SRBenchInputMessage] = [*self._messages, {"role": "user", "content": prompt}]
        token = prompt_label.set(self._prompt_label)
        try:
            response = await self._model_client.acomplete(
                model=self._model,
                messages=messages,
            )
        finally:
            prompt_label.reset(token)
        return response.content or ""
