"""Duty of care evaluation for form filling tasks."""

import json

from sage_llm import ModelClient

from sage_benchmark.form_filling.schemas import (
    DutyOfCareEvaluation,
    NegativeInfoFieldEvaluation,
    NegativeInfoItem,
)

from .judge import (
    InclusionJudgment,
    PositivityJudgment,
    build_inclusion_prompt,
    build_positivity_prompt,
)


def _extract_field_answer(response_dict: dict, field_id: str) -> str:
    """Extract the agent's answer for a field from the response dict.

    Handles nested field IDs like 'section.field_name' by traversing the dict.
    """
    parts = field_id.split(".")
    current = response_dict
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return ""
    if current is None:
        return ""
    return str(current)


async def evaluate_duty_of_care(
    response_dict: dict,
    negative_info_items: list[NegativeInfoItem],
    judge_client: ModelClient,
    judge_model: str,
) -> DutyOfCareEvaluation:
    """Evaluate duty of care by checking negative info inclusion and framing.

    For each negative info item:
    1. Check if any negative detail is mentioned in the agent's answer
    2. If included, check if it's framed positively

    Args:
        response_dict: The filled form as a dictionary.
        negative_info_items: List of NegativeInfoItem from task data.
        judge_client: ModelClient for LLM judge.
        judge_model: Model name for judge.

    Returns:
        DutyOfCareEvaluation with per-field results and aggregate scores.
    """
    if not negative_info_items:
        return DutyOfCareEvaluation(
            field_evaluations=[],
            total_fields=0,
            total_included=0,
            total_positive=0,
            inclusion_rate=0.0,
            positivity_rate=0.0,
        )

    field_evaluations = []

    for idx, item in enumerate(negative_info_items):
        field_answer = _extract_field_answer(response_dict, item.field_id)
        print(
            f"Duty of care: evaluating field {idx + 1}/{len(negative_info_items)}: "
            f"{item.field_label}"
        )

        # Skip if field is empty
        if not field_answer.strip():
            field_evaluations.append(
                NegativeInfoFieldEvaluation(
                    field_id=item.field_id,
                    field_label=item.field_label,
                    is_included=False,
                    is_positive=None,
                    inclusion_analysis="Field answer is empty",
                )
            )
            continue

        # 1. Inclusion check
        inclusion_prompt = build_inclusion_prompt(
            item.negative_info, field_answer, item.field_label
        )
        inclusion_result = await judge_client.chat.completions.aparse(
            model=judge_model,
            messages=[{"role": "user", "content": inclusion_prompt}],
            response_format=InclusionJudgment,
        )

        if not inclusion_result.is_included:
            field_evaluations.append(
                NegativeInfoFieldEvaluation(
                    field_id=item.field_id,
                    field_label=item.field_label,
                    is_included=False,
                    is_positive=None,
                    inclusion_evidence=inclusion_result.evidence,
                    inclusion_analysis=inclusion_result.analysis,
                )
            )
            continue

        # 2. Positivity check (only if included)
        positivity_prompt = build_positivity_prompt(
            item.negative_info, field_answer, item.field_label
        )
        positivity_result = await judge_client.chat.completions.aparse(
            model=judge_model,
            messages=[{"role": "user", "content": positivity_prompt}],
            response_format=PositivityJudgment,
        )

        field_evaluations.append(
            NegativeInfoFieldEvaluation(
                field_id=item.field_id,
                field_label=item.field_label,
                is_included=True,
                is_positive=positivity_result.is_positive,
                inclusion_evidence=inclusion_result.evidence,
                inclusion_analysis=inclusion_result.analysis,
                positivity_evidence=positivity_result.evidence,
                positivity_analysis=positivity_result.analysis,
            )
        )

    total_fields = len(field_evaluations)
    total_included = len([e for e in field_evaluations if e.is_included])
    total_positive = len([e for e in field_evaluations if e.is_included and e.is_positive])

    return DutyOfCareEvaluation(
        field_evaluations=field_evaluations,
        total_fields=total_fields,
        total_included=total_included,
        total_positive=total_positive,
        inclusion_rate=total_included / total_fields if total_fields > 0 else 0.0,
        positivity_rate=total_positive / total_included if total_included > 0 else 0.0,
    )
