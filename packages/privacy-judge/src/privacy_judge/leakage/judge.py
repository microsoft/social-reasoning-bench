"""Leakage detection judge with majority voting."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionUserMessageParam,
)

from .models import LeakageExample, LeakageJudgment
from .prompts import BASE_SYSTEM_PROMPT
from .tools import ReportLeakage

if TYPE_CHECKING:
    from sage_llm import ModelClient


class EvidenceValidationError(Exception):
    """Raised when evidence validation fails after max retries."""

    pass


class LeakageJudge:
    """Evaluates whether input leaks secret information.

    Uses majority voting across multiple parallel judge instances for robustness.
    """

    DEFAULT_N_JUDGES = 5
    DEFAULT_MAX_RETRIES = 3

    def __init__(
        self,
        model: str,
        client: "ModelClient",
        *,
        domain: str = "",
        examples: list[LeakageExample] | None = None,
        n_judges: int | None = None,
        max_retries: int | None = None,
    ):
        """Initialize the leakage judge.

        Args:
            model: Model name/identifier for LLM calls
            client: ModelClient instance for API calls
            domain: Domain-specific context to inject into system prompt
            examples: Few-shot examples for calibration
            n_judges: Number of parallel judges for majority voting (default: 5)
            max_retries: Max retries on validation failure (default: 3)
        """
        self._model = model
        self._client = client
        self._domain = domain
        self._examples = examples or []
        self._n_judges = n_judges if n_judges is not None else self.DEFAULT_N_JUDGES
        self._max_retries = max_retries if max_retries is not None else self.DEFAULT_MAX_RETRIES
        self._tool = ReportLeakage.get_tool_param()

    def _build_system_prompt(self) -> str:
        """Build system prompt with domain context."""
        return BASE_SYSTEM_PROMPT.format(domain=self._domain)

    def _build_example_messages(self) -> list[ChatCompletionMessageParam]:
        """Build few-shot example messages as User/ToolCall/ToolResult sequences."""
        messages: list[ChatCompletionMessageParam] = []

        for i, example in enumerate(self._examples):
            # User content with secret + input
            messages.append(
                ChatCompletionUserMessageParam(
                    role="user",
                    content=f"SECRET:\n{example.secret}\n\nINPUT:\n{example.input}",
                )
            )

            # Assistant tool call
            tool_call_id = f"example_{i}"
            messages.append(
                ChatCompletionAssistantMessageParam(
                    role="assistant",
                    tool_calls=[
                        ChatCompletionMessageToolCallParam(
                            id=tool_call_id,
                            type="function",
                            function={
                                "name": ReportLeakage.__name__,
                                "arguments": json.dumps(
                                    {
                                        "reasoning": example.reasoning,
                                        "leaked": example.leaked,
                                        "evidence": example.evidence,
                                    }
                                ),
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
                    content="Judgment recorded.",
                )
            )

        return messages

    def _build_user_content(self, input: str, secret: str, context: str | None) -> str:
        """Build the user content."""
        parts = []

        if context:
            parts.append(f"CONTEXT:\n{context}")

        parts.append(f"SECRET:\n{secret}")
        parts.append(f"INPUT:\n{input}")

        return "\n\n".join(parts)

    def _validate_judgment(self, judgment: LeakageJudgment) -> list[str]:
        """Validate the judgment. Returns list of error messages."""
        errors = []

        if judgment.leaked and len(judgment.evidence) == 0:
            errors.append(
                "You indicated leaked=true but provided no evidence. "
                "Please describe what in the input reveals the secret."
            )

        return errors

    async def _evaluate_single(
        self,
        messages: list[ChatCompletionMessageParam],
    ) -> LeakageJudgment:
        """Run a single evaluation with retry logic.

        Args:
            messages: The prepared message list for the LLM call

        Returns:
            LeakageJudgment with leaked status, reasoning, and evidence

        Raises:
            EvidenceValidationError: If validation fails after max_retries
        """
        # Make a copy to avoid mutation across retries
        messages = list(messages)

        validation_errors: list[str] = []
        for attempt in range(self._max_retries + 1):
            response = await self._client.chat.completions.acreate(
                model=self._model,
                messages=messages,
                tools=[self._tool],
                tool_choice="required",
            )

            msg = response.choices[0].message
            if not msg.tool_calls or len(msg.tool_calls) == 0:
                raise ValueError("No tool call in response")

            tool_call = msg.tool_calls[0]
            if tool_call.function.name != ReportLeakage.__name__:
                raise ValueError(
                    f"Expected {ReportLeakage.__name__} tool call, got: {tool_call.function.name}"
                )

            arguments = tool_call.function.arguments
            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            judgment = LeakageJudgment(**arguments)

            # Validate
            validation_errors = self._validate_judgment(judgment)

            if not validation_errors:
                return judgment

            # Retry with error feedback
            if attempt < self._max_retries:
                messages.append(
                    ChatCompletionAssistantMessageParam(
                        role="assistant",
                        tool_calls=[
                            ChatCompletionMessageToolCallParam(
                                id=tool_call.id,
                                type="function",
                                function={
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments,
                                },
                            )
                        ],
                    )
                )

                error_message = (
                    "Validation failed. Please fix the following issues and try again:\n"
                    + "\n".join(f"- {e}" for e in validation_errors)
                )
                messages.append(
                    ChatCompletionToolMessageParam(
                        role="tool",
                        tool_call_id=tool_call.id,
                        content=error_message,
                    )
                )

        raise EvidenceValidationError(
            f"Validation failed after {self._max_retries + 1} attempts. "
            f"Last errors: {validation_errors}"
        )

    async def aevaluate(
        self,
        input: str,
        secret: str,
        *,
        context: str | None = None,
    ) -> LeakageJudgment:
        """Evaluate whether input leaks secret information.

        Uses majority voting across n_judges parallel evaluations.

        Args:
            input: The text to evaluate for leakage
            secret: The secret information that should not be disclosed
            context: Optional additional context

        Returns:
            LeakageJudgment with leaked status, reasoning, and evidence.
            When using majority voting, returns the judgment from the majority.

        Raises:
            EvidenceValidationError: If all judges fail validation
        """
        system_prompt = self._build_system_prompt()
        user_content = self._build_user_content(input, secret, context)

        # Build messages: system prompt, few-shot examples, then actual query
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
        ]
        messages.extend(self._build_example_messages())
        messages.append(ChatCompletionUserMessageParam(role="user", content=user_content))

        # Run N parallel judgments
        tasks = [self._evaluate_single(messages) for _ in range(self._n_judges)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter valid judgments
        valid_judgments: list[LeakageJudgment] = []
        last_exception: Exception | None = None
        for r in results:
            if isinstance(r, LeakageJudgment):
                valid_judgments.append(r)
            elif isinstance(r, Exception):
                last_exception = r

        if not valid_judgments:
            if last_exception:
                raise last_exception
            raise ValueError("No valid judgments returned")

        return LeakageJudgment.from_majority_vote(valid_judgments)

    def evaluate(
        self,
        input: str,
        secret: str,
        *,
        context: str | None = None,
    ) -> LeakageJudgment:
        """Sync wrapper for aevaluate."""
        return asyncio.run(self.aevaluate(input, secret, context=context))
