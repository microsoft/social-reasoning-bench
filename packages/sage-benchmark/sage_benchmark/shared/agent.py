"""Shared BaseAgent class for all SAGE benchmarks.

Captures the common pattern across all three benchmark agent implementations:
- calendar_scheduling/agents/calendar_base.py (CalendarAgent)
- marketplace/agents/marketplace_base.py (MarketplaceAgent)
- form_filling/agents/assistant.py (AssistantAgent)

Common patterns unified here:
- Message history management (append-only list of ChatCompletionMessageParam)
- Tool registry (name -> Tool class mapping)
- Tool call generation via LLM with JSON parsing and retries
- Optional explicit chain-of-thought reasoning
- Injecting tool call results into history

Benchmark-specific subclasses add:
- Custom tool validation (e.g., SendEmail recipient checks in calendar)
- Custom retry error messages (calendar vs marketplace style)
- Domain-specific message injection (add_new_messages, add_turn_marker)
- Non-tool-call generation (generate_text_response in marketplace)
"""

import traceback
from typing import Any

from openai.types.chat import ChatCompletionFunctionToolParam, ChatCompletionToolChoiceOptionParam
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from pydantic import ValidationError
from sage_llm import SageChatCompletionMessage, SageMessage, SageModelClient

from .tool import Tool


class RetryException(Exception):
    """Raised when a model response cannot be parsed as a valid single tool call.

    Used internally by generate_tool_call to trigger retry logic. Subclasses
    may raise this from validate_tool_call to reject a parsed tool call.
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
    3. Optionally override ``validate_tool_call()`` for domain-specific checks.
    4. Optionally override ``on_retry_no_tool_calls()`` and
       ``on_retry_invalid_tool_call()`` for custom retry error messages.
    5. Add domain-specific methods (e.g., ``add_new_messages``,
       ``add_turn_marker``) that manipulate ``self._messages``.
    """

    def __init__(
        self,
        *,
        model: str,
        model_client: SageModelClient,
        tools: list[type[Tool]],
        explicit_cot: bool = False,
        temperature: float | None = None,
        tool_choice: ChatCompletionToolChoiceOptionParam = "auto",
        prompt_label: str = "unknown",
    ) -> None:
        """Initialize the base agent.

        Args:
            model: Model identifier for LLM calls (e.g., "gpt-4.1").
            model_client: ``SageModelClient`` instance for API calls.
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
        """
        self._model = model
        self._model_client = model_client
        self._prompt_label = prompt_label
        self._messages: list[SageMessage] = []
        self._explicit_cot = explicit_cot
        self._temperature = temperature
        self._tool_choice = tool_choice

        # Build tool registry: name -> Tool class
        self._tools: dict[str, type[Tool]] = {t.get_name(): t for t in tools}

        # Pre-compute OpenAI tool definitions
        self._openai_tools: list[ChatCompletionFunctionToolParam] = [
            t.get_openai_function_tool_param() for t in tools
        ]

    @property
    def messages(self) -> list[SageMessage]:
        """Return the current message history (read-only view).

        Returns:
            A shallow copy of the internal message list.
        """
        return list(self._messages)

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
        # Support both dicts (TypedDicts) and pydantic models (SageChatCompletionMessage)
        tc = last.get("tool_calls") if isinstance(last, dict) else getattr(last, "tool_calls", None)
        if not tc:
            raise ValueError("Expected previous message to be an assistant tool-call message")
        tool_calls = list(tc)
        if len(tool_calls) != 1:
            raise ValueError("Can only call add_tool_call_result after exactly one tool call")
        tc0 = tool_calls[0]
        tool_call_id = tc0["id"] if isinstance(tc0, dict) else tc0.id
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
            SageChatCompletionMessage(
                role="assistant",
                tool_calls=[
                    ChatCompletionMessageToolCall(
                        id=tool_call_id,
                        type="function",
                        function=Function(
                            name=action.get_name(),
                            arguments=action.model_dump_json(),
                        ),
                    )
                ],
            )
        )
        self._messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": result,
            }
        )

    # ------------------------------------------------------------------ #
    # Validation hook (override in subclasses)
    # ------------------------------------------------------------------ #

    def validate_tool_call(self, tool_call: Tool) -> None:
        """Validate a parsed tool call before accepting it.

        Override this in subclasses to add domain-specific validation
        (e.g., checking that email recipients are in an allowed list).

        Args:
            tool_call: The parsed Tool instance.

        Raises:
            RetryException: If the tool call is invalid and should be retried.
        """

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

    async def _generate_cot_reasoning(self, messages: list[SageMessage]) -> str:
        """Generate chain-of-thought reasoning before a tool call.

        Makes a separate LLM call without tools to produce internal reasoning,
        which is then included in the context for the actual tool-calling step.

        Args:
            messages: The current message history to reason about.

        Returns:
            The generated reasoning text.
        """
        from sage_llm.concurrency import prompt_label

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
                    messages.append(
                        SageChatCompletionMessage(
                            role="assistant",
                            content=cot_thinking,
                        )
                    )

            # Call the LLM
            from sage_llm.concurrency import prompt_label

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

                # Domain-specific validation hook
                self.validate_tool_call(parsed_tool_call)

                # Successfully parsed -- commit to canonical history
                if cot_thinking:
                    self._messages.append(
                        SageChatCompletionMessage(role="assistant", content=cot_thinking)
                    )

                self._messages.append(
                    SageChatCompletionMessage(
                        role="assistant",
                        content=message.content,
                        tool_calls=[
                            ChatCompletionMessageToolCall(
                                id=tool_call.id,
                                type="function",
                                function=Function(
                                    name=tool_call.function.name,
                                    arguments=tool_call.function.arguments,
                                ),
                            )
                        ],
                    )
                )

                return parsed_tool_call

            except (ValidationError, RetryException) as e:
                exceptions.append(e)

                if not tool_calls:
                    # No tool calls -- use plain assistant/user message for retry
                    messages.append(
                        SageChatCompletionMessage(
                            role="assistant",
                            content=message.content,
                        )
                    )
                    messages.append(
                        {"role": "user", "content": self.on_retry_no_tool_calls()},
                    )
                else:
                    # Invalid tool calls -- echo them back with error details
                    messages.append(
                        SageChatCompletionMessage(
                            role="assistant",
                            content=message.content,
                            tool_calls=[
                                ChatCompletionMessageToolCall(
                                    **tc.model_dump(include={"id", "type", "function"})
                                )
                                for tc in tool_calls
                            ],
                        )
                    )
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

    async def generate_text_response(self, prompt: str) -> str:
        """Call the model without tools and return a plain text response.

        Useful for post-hoc probing (e.g., privacy probes in marketplace)
        without affecting the canonical message history.

        Args:
            prompt: A user message to append (on a copy) before calling.

        Returns:
            The model's text response.
        """
        from sage_llm.concurrency import prompt_label

        messages: list[SageMessage] = [*self._messages, {"role": "user", "content": prompt}]
        token = prompt_label.set(self._prompt_label)
        try:
            response = await self._model_client.acomplete(
                model=self._model,
                messages=messages,
            )
        finally:
            prompt_label.reset(token)
        return response.content or ""
