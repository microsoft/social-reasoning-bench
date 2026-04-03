"""Judge response types and utilities for task completion evaluation."""

from typing import Any

from pydantic import BaseModel, Field


def normalize_value(value: Any) -> str:
    """Normalize a value for exact matching."""
    if value is None or value == "" or str(value).strip().lower() in ["n/a", "none"]:
        return ""
    return str(value).strip().lower()


def validate_with_pydantic(response_dict: dict, form_class: type) -> tuple[bool, list[str]]:
    """Validate response against pydantic model.

    Args:
        response_dict: The filled form as a dictionary
        form_class: The pydantic model class to validate against

    Returns:
        Tuple of (is_valid, error_messages)
    """
    try:
        if not issubclass(form_class, BaseModel):
            return False, [f"{form_class.__name__} is not a BaseModel subclass"]

        form_class.model_validate(response_dict)
        return True, []
    except Exception as e:
        return False, [str(e)]


class SemanticMatchJudgment(BaseModel, extra="forbid"):
    """LLM judge response for semantic equivalence check."""

    is_equivalent: bool = Field(description="Whether values are semantically equivalent")
    reasoning: str = Field(description="Explanation of the judgment")


class GroundingJudgment(BaseModel, extra="forbid"):
    """LLM judge response for grounding evaluation."""

    is_grounded: bool = Field(
        description="Whether answer is grounded in the background information"
    )
    reasoning: str = Field(description="Explanation of the judgment")
