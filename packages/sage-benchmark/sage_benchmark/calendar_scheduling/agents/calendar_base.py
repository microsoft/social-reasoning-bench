"""Base agent class for calendar scheduling interactions."""

from typing import Any

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageToolCallParam,
    ChatCompletionToolMessageParam,
)
from pydantic_core import to_json
from sage_llm import ModelClient

from sage_benchmark.shared.agent import BaseAgent, RetryException

from ..environment.actions import (
    CALENDAR_TOOLS,
    GetEmails,
    SendEmail,
)
from ..types import Tool


class CalendarAgent(BaseAgent):
    """Base agent class for calendar scheduling.

    This agent supports multi-step turns where it can call multiple tools
    before yielding with Wait or ending with EndConversation.

    Extends :class:`BaseAgent` with:
    - Default tool set (``CALENDAR_TOOLS``)
    - ``SendEmail`` recipient validation via :meth:`validate_tool_call`
    - ``add_new_messages`` for injecting emails via simulated ``GetEmails``
    """

    def __init__(
        self,
        model: str,
        model_client: ModelClient,
        allowed_contacts: list[str],
        tools: list[type[Tool]] | None = None,
        explicit_cot: bool = False,
    ):
        # Default to all calendar tools if none specified
        tool_list: list[type[Tool]] = list(tools) if tools is not None else list(CALENDAR_TOOLS)

        super().__init__(
            model=model,
            model_client=model_client,
            tools=tool_list,
            explicit_cot=explicit_cot,
        )

        self._allowed_contacts = list(allowed_contacts)

    # ------------------------------------------------------------------ #
    # Validation hook
    # ------------------------------------------------------------------ #

    def validate_tool_call(self, tool_call: Tool) -> None:
        """Reject SendEmail calls to recipients not in the allowed contacts list."""
        if isinstance(tool_call, SendEmail) and tool_call.to not in self._allowed_contacts:
            raise RetryException(
                f"Cannot SendEmail to {tool_call.to}. "
                f"Supported recipients are: {self._allowed_contacts}"
            )

    # ------------------------------------------------------------------ #
    # Calendar-specific message helpers
    # ------------------------------------------------------------------ #

    def add_new_messages(self, new_messages: list[Any]) -> None:
        """Inject new messages by simulating a GetEmails tool call and response."""
        tool_call_id = str(len(self._messages))
        tool_call_message = ChatCompletionAssistantMessageParam(
            role="assistant",
            tool_calls=[
                ChatCompletionMessageToolCallParam(
                    id=tool_call_id,
                    type="function",
                    function={"name": GetEmails.get_name(), "arguments": "{}"},
                )
            ],
        )

        tool_message = ChatCompletionToolMessageParam(
            role="tool",
            tool_call_id=tool_call_id,
            content=to_json(new_messages).decode(),
        )

        self._messages.append(tool_call_message)
        self._messages.append(tool_message)
