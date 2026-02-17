"""Tools formatter using the tool calling API."""

import json
from typing import Any

from .base import ConversationFormatter


class ToolsFormatter(ConversationFormatter):
    """Format conversations using tool calling API (GetUnreadMessages tool)."""

    def format(self, messages: list[dict[str, str]]) -> list[dict[str, Any]]:
        """Format messages as tool call/response pairs.

        Args:
            messages: List of message dicts with user/content fields

        Returns:
            List of assistant tool calls and tool responses
        """
        formatted = []
        call_id_counter = 0

        for msg in messages:
            call_id_counter += 1
            call_id = f"call_{call_id_counter}"

            # Assistant message with tool call
            formatted.append(
                {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": call_id,
                            "type": "function",
                            "function": {
                                "name": "GetUnreadMessages",
                                "arguments": "{}",
                            },
                        }
                    ],
                }
            )

            # Tool response with message content
            tool_content = json.dumps(
                {"messages": [{"user": msg["user"], "content": msg["content"]}]}
            )

            formatted.append({"role": "tool", "tool_call_id": call_id, "content": tool_content})

        return formatted
