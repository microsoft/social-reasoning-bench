"""CI Judge implementation with exhaustive flow analysis."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Callable, Literal

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
)
from pydantic import ValidationError

from .models import CIFlowAnalysis, CIFlowExample, CIJudgment, CIVerdictExample
from .prompts import BASE_SYSTEM_PROMPT
from .tools import NoMoreFlows, ReportCIFlow

if TYPE_CHECKING:
    from sage_llm import ModelClient

ReasoningEffort = Literal["none", "minimal", "low", "medium", "high", "xhigh", "default"]


class CIJudge:
    """Evaluates information flows using Contextual Integrity framework.

    Uses iterative exhaustive analysis to discover ALL flows in the input.
    """

    DEFAULT_MAX_RETRIES = 3
    DEFAULT_MAX_ITERATIONS = 50

    def __init__(
        self,
        model: str,
        client: "ModelClient",
        *,
        domain: str = "",
        examples: list[CIFlowExample | CIVerdictExample] | None = None,
        max_retries: int | None = None,
        reasoning_effort: ReasoningEffort | None = None,
    ):
        """Initialize the CI Judge.

        Args:
            model: Model name/identifier for LLM calls
            client: ModelClient instance for API calls
            domain: Domain-specific context to inject into system prompt
            examples: Few-shot examples for calibration
            max_retries: Max retries per LLM call on validation failure (default: 3)
            reasoning_effort: Reasoning effort level for supported models
        """
        self._model = model
        self._client = client
        self._domain = domain
        self._examples = examples or []
        self._max_retries = max_retries if max_retries is not None else self.DEFAULT_MAX_RETRIES
        self._reasoning_effort = reasoning_effort
        self._tools = [ReportCIFlow.get_tool_param(), NoMoreFlows.get_tool_param()]

    def _build_system_prompt(self) -> str:
        """Build system prompt with domain context."""
        return BASE_SYSTEM_PROMPT.format(domain=self._domain)

    def _build_example_messages(self) -> list[ChatCompletionMessageParam]:
        """Build few-shot example messages as User/ToolCall/ToolResult sequences.

        Only CIFlowExample instances are used (CIVerdictExample has no flow data).
        """
        messages: list[ChatCompletionMessageParam] = []

        example_idx = 0
        for example in self._examples:
            # Only CIFlowExample has flow data for few-shot examples
            if not isinstance(example, CIFlowExample):
                continue

            # User content with input + optional context
            content = f"INPUT:\n{example.input}"
            if example.context:
                content = f"CONTEXT:\n{example.context}\n\n{content}"
            messages.append(ChatCompletionUserMessageParam(role="user", content=content))

            # Assistant tool call with the flow
            tool_call_id = f"example_{example_idx}"
            messages.append(
                ChatCompletionAssistantMessageParam(
                    role="assistant",
                    tool_calls=[
                        ChatCompletionMessageToolCallParam(
                            id=tool_call_id,
                            type="function",
                            function={
                                "name": ReportCIFlow.__name__,
                                "arguments": json.dumps(example.flow.model_dump()),
                            },
                        )
                    ],
                )
            )

            # Tool result
            messages.append(
                ChatCompletionToolMessageParam(
                    role="tool",
                    tool_call_id=tool_call_id,
                    content="Flow recorded.",
                )
            )
            example_idx += 1

        return messages

    def _build_user_content(self, input: str, context: str | None) -> str:
        """Build the user content."""
        parts = []

        if context:
            parts.append(f"CONTEXT:\n{context}")

        parts.append(f"INPUT:\n{input}")
        parts.append(
            "\nIdentify all information flows one at a time. "
            "Call ReportCIFlow for each flow, then call NoMoreFlows when done."
        )

        return "\n\n".join(parts)

    async def _iterate_once(
        self,
        messages: list[ChatCompletionMessageParam],
    ) -> tuple[CIFlowAnalysis | NoMoreFlows | None, list[ChatCompletionMessageParam]]:
        """Execute a single iteration of flow discovery.

        Returns:
            Tuple of (result, updated_messages) where result is:
            - CIFlowAnalysis if a flow was reported
            - NoMoreFlows if analysis is complete
            - None if retry needed (messages already updated with error feedback)
        """
        response = await self._client.chat.completions.acreate(
            model=self._model,
            messages=messages,
            tools=self._tools,
            tool_choice="required",
            reasoning_effort=self._reasoning_effort,  # type: ignore[arg-type]
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            # No tool calls - ask for one
            messages.append(
                ChatCompletionAssistantMessageParam(role="assistant", content=msg.content or "")
            )
            messages.append(
                ChatCompletionUserMessageParam(
                    role="user",
                    content="Please call ReportCIFlow for the next flow, "
                    "or NoMoreFlows if all flows have been identified.",
                )
            )
            return None, messages

        tool_call = msg.tool_calls[0]
        tool_name = tool_call.function.name
        arguments = tool_call.function.arguments

        # Build tool call message to append
        assistant_msg = ChatCompletionAssistantMessageParam(
            role="assistant",
            content=msg.content or "",
            tool_calls=[
                ChatCompletionMessageToolCallParam(
                    id=tool_call.id,
                    type="function",
                    function={
                        "name": tool_name,
                        "arguments": arguments,
                    },
                )
            ],
        )

        try:
            if tool_name == NoMoreFlows.__name__:
                result = NoMoreFlows.model_validate_json(arguments)
                messages.append(assistant_msg)
                return result, messages

            elif tool_name == ReportCIFlow.__name__:
                result = ReportCIFlow.model_validate_json(arguments)
                flow = CIFlowAnalysis(**result.model_dump())
                messages.append(assistant_msg)
                messages.append(
                    ChatCompletionToolMessageParam(
                        role="tool",
                        tool_call_id=tool_call.id,
                        content="Flow recorded. Identify the next flow, or call NoMoreFlows if done.",
                    )
                )
                return flow, messages

            else:
                # Unknown tool
                messages.append(assistant_msg)
                messages.append(
                    ChatCompletionToolMessageParam(
                        role="tool",
                        tool_call_id=tool_call.id,
                        content=f"Unknown tool '{tool_name}'. Use ReportCIFlow or NoMoreFlows.",
                    )
                )
                return None, messages

        except ValidationError as e:
            # Validation error - provide feedback
            messages.append(assistant_msg)
            messages.append(
                ChatCompletionToolMessageParam(
                    role="tool",
                    tool_call_id=tool_call.id,
                    content=f"Validation error: {e}. Please fix and try again.",
                )
            )
            return None, messages

    async def aevaluate(
        self,
        input: str,
        *,
        context: str | None = None,
        max_iterations: int | None = None,
        on_flow_found: Callable[[CIFlowAnalysis], None] | None = None,
    ) -> CIJudgment:
        """Analyze input for ALL information flow violations.

        Uses iterative exhaustive analysis to discover every flow.

        Args:
            input: Text to analyze
            context: Additional context (e.g., calendar JSON)
            max_iterations: Max LLM calls for iterative discovery (default: 50)
            on_flow_found: Callback for each flow discovered

        Returns:
            CIJudgment with overall verdict and list of all flows
        """
        max_iter = max_iterations if max_iterations is not None else self.DEFAULT_MAX_ITERATIONS

        # Build initial messages
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(role="system", content=self._build_system_prompt()),
        ]
        messages.extend(self._build_example_messages())
        messages.append(
            ChatCompletionUserMessageParam(
                role="user",
                content=self._build_user_content(input, context),
            )
        )

        flows: list[CIFlowAnalysis] = []
        iterations = 0
        retries_in_current_iteration = 0

        while iterations < max_iter:
            iterations += 1

            result, messages = await self._iterate_once(messages)

            if result is None:
                # Retry needed
                retries_in_current_iteration += 1
                if retries_in_current_iteration >= self._max_retries:
                    # Too many retries, give up on this iteration
                    break
                continue

            # Reset retry counter on successful result
            retries_in_current_iteration = 0

            if isinstance(result, NoMoreFlows):
                break
            elif isinstance(result, CIFlowAnalysis):
                flows.append(result)
                if on_flow_found:
                    on_flow_found(result)

        return CIJudgment.from_flows(flows, iterations)

    def evaluate(
        self,
        input: str,
        *,
        context: str | None = None,
        max_iterations: int | None = None,
        on_flow_found: Callable[[CIFlowAnalysis], None] | None = None,
    ) -> CIJudgment:
        """Sync wrapper for aevaluate."""
        return asyncio.run(
            self.aevaluate(
                input,
                context=context,
                max_iterations=max_iterations,
                on_flow_found=on_flow_found,
            )
        )
