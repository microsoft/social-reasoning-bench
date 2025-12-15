from typing import Literal

from pydantic import BaseModel


class ToolDefinition(BaseModel):
    """Defines a tool that can be called by the LLM."""

    name: str
    description: str
    parameters_schema: type[BaseModel]


class ToolCall(BaseModel):
    """Represents a tool call made by the LLM."""

    tool_name: str
    arguments: dict


class ToolCallResult(BaseModel):
    """Result of a tool-calling LLM request."""

    tool_call: ToolCall | None = None
    raw_response: str
    error: str | None = None


# --- Message Format ---


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
