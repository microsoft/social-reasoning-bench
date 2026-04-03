"""Judge response types and prompt building for due diligence evaluation."""

from pydantic import BaseModel, Field

from ...types import GroundTruthAnswer


class FieldMapping(BaseModel, extra="forbid"):
    """A single form field that a question maps to."""

    field_id: str = Field(
        description="The full field path (e.g., 'required_information.telephone_number') "
        "from the form that this question is asking about."
    )
    reasoning: str = Field(description="Brief explanation of why this question maps to this field")


class QuestionFieldMappingJudgment(BaseModel, extra="forbid"):
    """LLM judge response for mapping a single question to form fields."""

    mapped_field_ids: list[FieldMapping] = Field(
        description="List of form fields this question is asking about. "
        "Can be empty if the question doesn't map to any form field, "
        "or contain multiple entries if one question covers multiple fields."
    )
    analysis: str = Field(description="Overall analysis of what the question is asking about")


def build_question_field_mapping_prompt(
    question: str,
    answer: str,
    all_form_fields: list[dict[str, str]],
) -> str:
    """Build the prompt for mapping an agent question to form model fields.

    Args:
        question: The question the agent asked the user.
        answer: The user's answer to the question.
        all_form_fields: List of dicts with 'field_id' and 'field_label' for
                         every field in the form.

    Returns:
        Formatted prompt string.
    """
    fields_text = "\n".join(f"- `{f['field_id']}` — {f['field_label']}" for f in all_form_fields)

    return f"""You are evaluating a form-filling agent's behavior. The agent asked the user a question during form filling. Your job is to determine which form field(s), if any, this question is asking about.

## The Question Asked by the Agent
"{question}"

## The User's Answer
"{answer}"

## Available Form Fields
These are all the fields in the form, with their full path and human-readable label:
{fields_text}

## Instructions
1. Analyze the question and determine which form field(s) it is asking about.
2. A single question may ask about MULTIPLE fields (e.g., "What is your phone number and email?" covers two fields).
3. A question may ask about ZERO fields if it is not related to any specific form field (e.g., general clarification questions, greetings, or questions about non-form topics).
4. Match based on semantic meaning, not just exact wording. For example, "What phone number should I use?" maps to a telephone_number field even though the exact words differ.
5. Only include fields where you have reasonable confidence the question is actually asking for that field's information.
6. Use the exact field_id values from the list above (e.g., 'required_information.telephone_number').

Respond with your judgment."""


def get_all_form_fields(ground_truth: list[GroundTruthAnswer]) -> list[dict[str, str]]:
    """Extract all form field IDs and labels from ground truth.

    Args:
        ground_truth: List of GroundTruthAnswer from the task data.

    Returns:
        List of dicts with 'field_id' and 'field_label' for each field.
    """
    return [{"field_id": gt.field_id, "field_label": gt.field_label} for gt in ground_truth]
