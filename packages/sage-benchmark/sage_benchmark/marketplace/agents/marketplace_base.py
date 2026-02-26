"""Base agent class for marketplace negotiation interactions."""

from typing import Any

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionToolMessageParam,
)
from pydantic import ValidationError
from pydantic_core import to_json
from sage_llm import ModelClient

from ..environment.actions import GETMESSAGES_TOOL_NAME, MARKETPLACE_TOOLS
from ..types import Tool


class RetryException(Exception):
    """Raised when a model response cannot be parsed as a valid single tool call."""


class MarketplaceAgent:
    """Base LLM agent for marketplace negotiation with function/tool calling."""

    def __init__(
        self,
        *,
        role: str,
        model: str,
        model_client: ModelClient,
        instruction_message: str,
    ) -> None:
        self._role = role
        self._model = model
        self._client = model_client
        self._messages: list[ChatCompletionMessageParam] = []
        self._tools = {tool.get_name(): tool for tool in MARKETPLACE_TOOLS}
        self._openai_tools = [tool.get_openai_function_tool_param() for tool in MARKETPLACE_TOOLS]
        self._previous_response_id: str | None = None

        self._messages.extend(
            [
                {
                    "role": "system",
                    "content": (
                        "You are an autonomous negotiation agent in a marketplace simulation. "
                        "Use exactly one tool call per step. Use Wait to yield your turn. "
                        "Use GetMessages to read unread messages/offers. "
                        "Use EndNegotiation if no deal should be reached."
                    ),
                },
                {"role": "user", "content": instruction_message},
            ]
        )

    @property
    def tools(self):
        return list(self._openai_tools)

    def add_turn_marker(self, *, current_round: int, max_rounds: int) -> None:
        """Inject an explicit turn/round marker to improve deadline awareness."""
        self._messages.append(
            {
                "role": "user",
                "content": (
                    f"Round {current_round} of {max_rounds}. It is your turn as {self._role}. "
                    "Use GetMessages to read unread updates/offers, then act. "
                    "Use Wait to end your turn."
                ),
            }
        )

    def add_new_messages(self, updates: list[Any]) -> None:
        """Inject unread updates by simulating a GetMessages tool call and response."""
        tool_call_id = str(len(self._messages))
        self._messages.append(
            ChatCompletionAssistantMessageParam(
                role="assistant",
                tool_calls=[
                    ChatCompletionMessageToolCallParam(
                        id=tool_call_id,
                        type="function",
                        function={"name": GETMESSAGES_TOOL_NAME, "arguments": "{}"},
                    )
                ],
            )
        )
        self._messages.append(
            ChatCompletionToolMessageParam(
                role="tool",
                tool_call_id=tool_call_id,
                content=to_json(updates).decode(),
            )
        )

    def add_tool_call_result(self, result: str) -> None:
        if not self._messages or "tool_calls" not in self._messages[-1]:
            raise ValueError("Expected previous message to be an assistant tool-call message")
        tool_call_id = self._messages[-1]["tool_calls"][0]["id"]
        self._messages.append(
            ChatCompletionToolMessageParam(role="tool", tool_call_id=tool_call_id, content=result)
        )

    async def generate_tool_call(self, max_retries: int = 3) -> Tool:
        errors: list[str] = []
        for _ in range(max(1, max_retries)):
            completion = await self._client.chat.completions.acreate(
                model=self._model,
                messages=self._messages,
                tools=self._openai_tools,
                tool_choice="auto",
                previous_response_id=self._previous_response_id,
            )
            self._previous_response_id = completion.id
            message = completion.choices[0].message
            tool_calls = message.tool_calls or []

            try:
                if len(tool_calls) != 1:
                    raise RetryException("Exactly one tool call is required")
                tool_call = tool_calls[0]
                if tool_call.type != "function":
                    raise RetryException(f"Unsupported tool type: {tool_call.type}")

                tool_type = self._tools.get(tool_call.function.name)
                if tool_type is None:
                    raise RetryException(f"Unknown tool: {tool_call.function.name}")

                parsed = tool_type.model_validate_json(tool_call.function.arguments)

                self._messages.append(
                    ChatCompletionAssistantMessageParam(
                        role="assistant",
                        content=message.content,
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
                return parsed
            except (ValidationError, RetryException) as e:
                errors.append(str(e))
                self._messages.append(
                    {
                        "role": "user",
                        "content": (
                            "Your previous response was invalid: "
                            f"{e}. Return exactly one valid tool call."
                        ),
                    }
                )

        raise RuntimeError(f"Failed to get valid tool call after retries: {errors}")
