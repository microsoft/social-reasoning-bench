"""Tool definitions for the file system environment.

Provides unified search and read tools across all artifact types.
k=3 is fixed internally -- the agent cannot control how many results are returned.
"""

from pydantic import Field

from sage_benchmark.shared.tool import Tool


class SearchFiles(Tool):
    """Search the user's files by keyword query. Returns top results with snippets."""

    query: str = Field(description="Search query (keywords)")


class ReadFile(Tool):
    """Read the full content of a file by its ID."""

    id: str = Field(description="File ID to read")


FILE_SYSTEM_TOOLS = [SearchFiles, ReadFile]
