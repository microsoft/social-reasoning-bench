"""Tool definitions for the file system environment.

Provides search and read tools for emails and calendar events.
k=3 is fixed internally -- the agent cannot control how many results are returned.
"""

from typing import Any

from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition
from pydantic import BaseModel, Field


class Tool(BaseModel):
    """Base class for file system tools."""

    model_config = {"extra": "forbid"}

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_description(cls) -> str:
        return cls.__doc__ or ""

    @classmethod
    def get_parameters_schema(cls) -> dict[str, Any]:
        schema = cls.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        if schema.get("properties") == {}:
            return {"type": "object", "properties": {}}
        return schema

    @classmethod
    def get_openai_function_tool_param(cls) -> dict:
        return {
            "type": "function",
            "function": {
                "name": cls.get_name(),
                "description": cls.get_description(),
                "parameters": cls.get_parameters_schema(),
            },
        }


class SearchEmail(Tool):
    """Search emails by keyword query. Returns top 3 results with snippets."""

    query: str = Field(description="Search query (keywords)")


class ReadEmail(Tool):
    """Read the full content of an email by its ID."""

    id: str = Field(description="Email ID to read")


class SearchCalendar(Tool):
    """Search calendar events by keyword query. Returns top 3 results with snippets."""

    query: str = Field(description="Search query (keywords)")


class ReadCalendar(Tool):
    """Read the full content of a calendar event by its ID."""

    id: str = Field(description="Calendar event ID to read")


FILE_SYSTEM_TOOLS = [SearchEmail, ReadEmail, SearchCalendar, ReadCalendar]
