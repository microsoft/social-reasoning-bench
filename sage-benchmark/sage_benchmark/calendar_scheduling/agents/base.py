import traceback
from typing import Any

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionFunctionToolParam,
    ChatCompletionMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionToolMessageParam,
)
from openai.types.shared_params import FunctionDefinition
from pydantic import ValidationError
from pydantic_core import to_json

from ..environments.messenger.actions import GetUnreadMessages, SendMessage
from ..types import Tool


class RetryException(Exception): ...


class MessengerAgent:
    def __init__(
        self,
        model: str,
        model_client: OpenAI,
        allowed_contacts: list[str],
        tools: list[type[Tool]] | None = None,
    ):
        self._model = model
        self._model_client = model_client
        self._messages: list[ChatCompletionMessageParam] = []
        self._allowed_contacts = list(allowed_contacts)

        self._tools: dict[str, type[Tool]] = {SendMessage.get_name(): SendMessage}
        if tools:
            for tool in tools:
                self._tools[tool.get_name()] = tool

        self._openai_tools = [
            ChatCompletionFunctionToolParam(
                type="function",
                function=FunctionDefinition(
                    name=tool.get_name(),
                    description=tool.get_description(),
                    parameters=tool.get_parameters_schema(),
                ),
            )
            for tool in self._tools.values()
        ]

    def add_new_messages(self, new_messages: list[Any]):
        # Inject the new messages into the context by simulating a tool call and response for GetUnreadMessages
        tool_call_id = str(len(self._messages))
        tool_call_message = ChatCompletionAssistantMessageParam(
            role="assistant",
            tool_calls=[
                ChatCompletionMessageToolCallParam(
                    id=tool_call_id,
                    type="function",
                    function={"name": GetUnreadMessages.get_name(), "arguments": "{}"},
                )
            ],
        )

        tool_message = ChatCompletionToolMessageParam(
            role="tool", tool_call_id=tool_call_id, content=to_json(new_messages).decode()
        )

        self._messages.append(tool_call_message)
        self._messages.append(tool_message)

    def add_tool_call_result(self, result: str):
        if self._messages and "tool_calls" in self._messages[-1]:
            tool_calls = list(self._messages[-1]["tool_calls"])
            if len(tool_calls) != 1:
                raise ValueError("Can only call add_tool_call_result after exactly one tool call")
            tool_call_id = tool_calls[0]["id"]

            self._messages.append(
                ChatCompletionToolMessageParam(
                    role="tool",
                    tool_call_id=tool_call_id,
                    content=result,
                )
            )

        else:
            raise ValueError("Can only call add_tool_call_result after a successful step")

    def generate_tool_call(self, max_retries: int = 3) -> Tool:
        # Make local copy that we can modify on retry
        messages = list(self._messages)
        for _ in range(max(1, max_retries)):
            # Generate the next action
            completion = self._model_client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=self._openai_tools,
                tool_choice="required",
            )

            message = completion.choices[0].message
            tool_calls = message.tool_calls

            if tool_calls is None:
                raise ValueError(
                    "OpenAI client returned None tool_calls despite tool_choice=required"
                )

            try:
                if len(tool_calls) != 1:
                    raise RetryException("Exactly 1 tool must be called.")
                else:
                    tool_call = tool_calls[0]
                    if tool_call.type != "function":
                        raise RetryException(f"Unsupported tool type '{tool_call.type}'")

                    function = tool_call.function
                    tool_type = self._tools.get(function.name, None)
                    if tool_type is None:
                        raise RetryException(f"Unrecognized function name '{function.name}'")

                    parsed_tool_call = tool_type.model_validate_json(function.arguments)

                    if (
                        isinstance(parsed_tool_call, SendMessage)
                        and parsed_tool_call.to not in self._allowed_contacts
                    ):
                        raise RetryException(
                            f"Cannot SendMessage to {parsed_tool_call.to}. Supported recipients are: {self._allowed_contacts}"
                        )

                    # Successfully parsed the tool call, append it to the context
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

                    return parsed_tool_call
            except (ValidationError, RetryException):
                # Append the failed tool call to local messages
                messages.append(
                    ChatCompletionAssistantMessageParam(
                        role="assistant",
                        content=message.content,
                        tool_calls=[
                            ChatCompletionMessageToolCallParam(
                                **tool_call.model_dump(include={"id", "type", "function"})
                            )
                            for tool_call in tool_calls
                        ],
                    )
                )

                # We don't know which tool_call caused the error,
                # but they all need a tool message, so just repeat the error for each tool
                for tool_call in tool_calls:
                    messages.append(
                        ChatCompletionToolMessageParam(
                            role="tool", tool_call_id=tool_call.id, content=traceback.format_exc()
                        )
                    )

        raise ValueError("Exceeded maximum retries generating tool call")
