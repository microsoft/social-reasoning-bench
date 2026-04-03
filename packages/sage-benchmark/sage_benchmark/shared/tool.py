"""Shared Tool base class for all SAGE benchmarks.

Unifies the identical Tool and ToolError definitions from:
- calendar_scheduling/types.py
- form_filling/environment/actions.py
- marketplace/types.py

Each benchmark can subclass Tool to define its own tool actions.
"""

from typing import Any

from openai.types.chat import ChatCompletionFunctionToolParam
from openai.types.shared_params import FunctionDefinition
from pydantic import BaseModel


class ToolError(Exception):
    """Raised when a tool execution fails due to invalid input or state."""

    pass


class Tool(BaseModel):
    """Base class for LLM tool calling.

    Subclass this to define a tool action. The class name becomes the tool name,
    the class docstring becomes the description, and Pydantic fields become the
    parameter schema.

    Example::

        class SendEmail(Tool):
            \"\"\"Send an email to the specified recipient.\"\"\"
            to: str = Field(description="Recipient email address")
            subject: str = Field(description="Email subject")
            body: str = Field(description="Email body")

        # Get OpenAI-compatible tool definition
        tool_param = SendEmail.get_openai_function_tool_param()

        # Parse a tool call from the LLM
        action = SendEmail.model_validate_json(function.arguments)
    """

    model_config = {"extra": "forbid"}

    @classmethod
    def get_name(cls) -> str:
        """Return the tool name (defaults to the class name)."""
        return cls.__name__

    @classmethod
    def get_description(cls) -> str:
        """Return the tool description (defaults to the class docstring)."""
        return cls.__doc__ or ""

    @classmethod
    def get_parameters_schema(cls) -> dict[str, Any]:
        """Return the JSON Schema for the tool's parameters.

        Cleans up the Pydantic-generated schema by removing ``$defs`` and
        ``title`` keys that are not expected by LLM tool-calling APIs.

        For tools with no parameters, returns a minimal ``{"type": "object",
        "properties": {}}`` schema that satisfies both Gemini and Anthropic
        API requirements.
        """
        schema = cls.model_json_schema()
        # Remove $defs from top level and inline if needed
        schema.pop("$defs", None)
        schema.pop("title", None)

        # Gemini requires non-empty properties for type: object
        # If there are no properties, return minimal valid schema
        # (Anthropic API requires "type" field in input_schema)
        if schema.get("properties") == {}:
            return {"type": "object", "properties": {}}

        return schema

    @classmethod
    def get_openai_function_tool_param(cls) -> ChatCompletionFunctionToolParam:
        """Return an OpenAI-compatible function tool parameter definition.

        This produces a ``ChatCompletionFunctionToolParam`` TypedDict suitable
        for passing directly to the ``tools`` argument of the OpenAI chat
        completions API (or compatible wrappers like ``SageModelClient``).
        """
        return ChatCompletionFunctionToolParam(
            type="function",
            function=FunctionDefinition(
                name=cls.get_name(),
                description=cls.get_description(),
                parameters=cls.get_parameters_schema(),
            ),
        )
