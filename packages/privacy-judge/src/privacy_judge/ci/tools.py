"""Tools for CI flow analysis judge."""

from typing import Literal

from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition
from pydantic import BaseModel, Field

from .models import CIFlowAnalysis


class ReportCIFlow(CIFlowAnalysis):
    """Report a single information flow analysis.

    Call this tool once for each distinct information flow identified.
    Use parallel calls for multiple independent flows.
    """

    @classmethod
    def get_tool_param(cls) -> ChatCompletionToolParam:
        """Return OpenAI function tool parameter."""
        schema = cls.model_json_schema()
        schema.pop("title", None)
        schema.pop("$defs", None)
        return ChatCompletionToolParam(
            type="function",
            function=FunctionDefinition(
                name=cls.__name__,
                description=cls.__doc__ or "",
                parameters=schema,
            ),
        )


class NoMoreFlows(BaseModel):
    """Signal that all information flows have been identified and analyzed.

    Call this tool when you have exhaustively analyzed all information flows
    in the input and no new flows remain to identify.
    """

    confirmation: Literal["complete"] = Field(
        default="complete",
        description="Confirm that no additional information flows remain to analyze",
    )

    @classmethod
    def get_tool_param(cls) -> ChatCompletionToolParam:
        """Return OpenAI function tool parameter."""
        schema = cls.model_json_schema()
        schema.pop("title", None)
        return ChatCompletionToolParam(
            type="function",
            function=FunctionDefinition(
                name=cls.__name__,
                description=cls.__doc__ or "",
                parameters=schema,
            ),
        )
