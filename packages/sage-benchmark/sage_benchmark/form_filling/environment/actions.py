"""Tool definitions for the file system environment.

Provides unified search and read tools across all artifact types.
k=3 is fixed internally -- the agent cannot control how many results are returned.
"""

from typing import Any

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


class SearchFiles(Tool):
    """Search the user's files by keyword query. Returns top results with snippets."""

    query: str = Field(description="Search query (keywords)")


class ReadFile(Tool):
    """Read the full content of a file by its ID."""

    id: str = Field(description="File ID to read")


FILE_SYSTEM_TOOLS = [SearchFiles, ReadFile]
