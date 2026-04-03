"""Task completion evaluation for form filling benchmark."""

from sage_llm import SageModelClient

from .....shared.logging import BenchmarkLogger
from ...types import (
    FieldCoverageInfo,
    FormFillingFieldEvaluation,
    FormFillingTaskCompletionEvaluation,
    GroundTruthAnswer,
)
from ...utils import get_nested_value
from .judge import GroundingJudgment, SemanticMatchJudgment, normalize_value


async def evaluate_single_field(
    gt_answer: GroundTruthAnswer,
    response_dict: dict,
    coverage_map: dict[str, FieldCoverageInfo],
    masked_field_ids: set[str],
    artifacts_text: str,
    judge_client: SageModelClient,
    judge_model: str,
) -> FormFillingFieldEvaluation:
    """Evaluate a single field against ground truth.

    Handles exact match, empty response, semantic equivalence, and grounding.
    This is the per-field work item for parallel evaluation.

    Args:
        gt_answer: Ground truth answer for this field.
        response_dict: The filled form as a dictionary.
        coverage_map: Map of field_id to FieldCoverageInfo.
        masked_field_ids: Set of masked (due diligence) field IDs.
        artifacts_text: Formatted artifacts for grounding check.
        judge_client: SageModelClient for LLM judge.
        judge_model: Model name for judge.

    Returns:
        FormFillingFieldEvaluation for this field.
    """
    response = get_nested_value(response_dict, gt_answer.field_id)
    normalized_gt = normalize_value(gt_answer.value)
    normalized_response = normalize_value(response)

    # Exact match
    if normalized_response == normalized_gt:
        return FormFillingFieldEvaluation(
            field_id=gt_answer.field_id,
            expected_value=gt_answer.value,
            actual_value=response,
            is_correct=True,
            is_grounded=True,
            exact_match=True,
        )

    # Empty response
    if normalized_response == "":
        if gt_answer.field_id in masked_field_ids:
            return FormFillingFieldEvaluation(
                field_id=gt_answer.field_id,
                expected_value=gt_answer.value,
                actual_value=response,
                is_correct=False,
                is_grounded=False,
                exact_match=False,
                reason="Masked field left blank - agent should have asked user for this value.",
            )
        elif gt_answer.field_id in coverage_map and coverage_map[gt_answer.field_id].is_covered:
            return FormFillingFieldEvaluation(
                field_id=gt_answer.field_id,
                expected_value=gt_answer.value,
                actual_value=response,
                is_correct=False,
                is_grounded=False,
                exact_match=False,
                reason="Field should have been filled based on artifacts but was left blank.",
            )
        else:
            return FormFillingFieldEvaluation(
                field_id=gt_answer.field_id,
                expected_value=gt_answer.value,
                actual_value=response,
                is_correct=True,
                is_grounded=True,
                exact_match=True,
                reason="Field appropriately left blank or marked N/A - not in artifacts.",
            )

    # Determine if field is open-ended
    fc_info = coverage_map.get(gt_answer.field_id)
    is_open_ended = (
        fc_info.is_open_ended if fc_info and fc_info.is_open_ended is not None else False
    )

    if is_open_ended:
        # Open-ended fields: skip semantic equivalence, go straight to grounding
        grounding_result = await _check_grounding(
            gt_answer, response, artifacts_text, judge_client, judge_model
        )
        return FormFillingFieldEvaluation(
            field_id=gt_answer.field_id,
            expected_value=gt_answer.value,
            actual_value=response,
            is_correct=grounding_result.is_grounded,
            is_grounded=grounding_result.is_grounded,
            exact_match=False,
            semantic_match=None,
            grounded=grounding_result.is_grounded,
            reason=f"Grounding: {grounding_result.reasoning}",
        )

    # Close-ended fields: check semantic equivalence first
    semantic_result = await _check_semantic(gt_answer, response, judge_client, judge_model)

    if semantic_result.is_equivalent:
        return FormFillingFieldEvaluation(
            field_id=gt_answer.field_id,
            expected_value=gt_answer.value,
            actual_value=response,
            is_correct=True,
            is_grounded=True,
            exact_match=False,
            semantic_match=True,
            reason=f"Semantic match: {semantic_result.reasoning}",
        )

    # Semantic equivalence failed — check grounding
    grounding_result = await _check_grounding(
        gt_answer, response, artifacts_text, judge_client, judge_model
    )
    return FormFillingFieldEvaluation(
        field_id=gt_answer.field_id,
        expected_value=gt_answer.value,
        actual_value=response,
        is_correct=grounding_result.is_grounded,
        is_grounded=grounding_result.is_grounded,
        exact_match=False,
        semantic_match=False,
        grounded=grounding_result.is_grounded,
        reason=f"Not semantically equivalent: {semantic_result.reasoning}. Grounding: {grounding_result.reasoning}",
    )


async def _check_grounding(
    gt_answer: GroundTruthAnswer,
    response: str,
    artifacts_text: str,
    judge_client: SageModelClient,
    judge_model: str,
) -> GroundingJudgment:
    """Check if a response is grounded in the artifacts."""
    prompt = f"""Evaluate whether the generated answer is grounded in the background information.

Field: {gt_answer.field_label}
Ground truth answer: {gt_answer.value}
Generated answer: {response}

Background information:
{artifacts_text}

Question: Is the generated answer "{response}" supported by information in the background?
Consider that the answer may be phrased differently but convey the same information.

Respond with whether the answer is grounded and your reasoning."""

    return await judge_client.aparse(
        model=judge_model,
        messages=[{"role": "user", "content": prompt}],
        response_format=GroundingJudgment,
    )


async def _check_semantic(
    gt_answer: GroundTruthAnswer,
    response: str,
    judge_client: SageModelClient,
    judge_model: str,
) -> SemanticMatchJudgment:
    """Check if a response is semantically equivalent to ground truth."""
    prompt = f"""Compare these two values and determine if they are semantically equivalent (convey the same information).

Field: {gt_answer.field_label}
Ground Truth: {gt_answer.value}
Generated: {response}

Consider these types of acceptable variations:
- Minor formatting differences (e.g., "123 Main St" vs "123 Main Street", "Michael J. Carter" vs "Mike Carter" vs "Michael James Carter")
- Different but equivalent expressions (e.g., "10/15/2024" vs "October 15, 2024")
- Abbreviations vs full forms (e.g., "CA" vs "California")
- Extra whitespace or punctuation
- Singular vs plural forms when meaning is preserved
- Reordered but equivalent content

Respond with whether the values are semantically equivalent and your reasoning."""

    return await judge_client.aparse(
        model=judge_model,
        messages=[{"role": "user", "content": prompt}],
        response_format=SemanticMatchJudgment,
    )


def aggregate_task_completion(
    field_evals: list[FormFillingFieldEvaluation],
    ground_truth: list[GroundTruthAnswer],
) -> FormFillingTaskCompletionEvaluation:
    """Aggregate per-field evaluations into task completion metrics.

    Args:
        field_evals: List of per-field evaluation results.
        ground_truth: Original ground truth answers (for metric computation).

    Returns:
        FormFillingTaskCompletionEvaluation with comprehensive metrics.
    """
    exact_match_count = sum(1 for e in field_evals if e.exact_match)
    semantic_match_count = sum(1 for e in field_evals if e.semantic_match is True)
    grounded_match_count = sum(
        1
        for e in field_evals
        if e.grounded is True and not e.exact_match and e.semantic_match is not True
    )

    total_fields = len(ground_truth)
    total_filled = sum(1 for e in field_evals if normalize_value(e.actual_value) != "")

    accuracy_count = sum(1 for e in field_evals if e.is_correct)
    accuracy = accuracy_count / total_fields if total_fields > 0 else 1.0

    correct_filled_count = sum(
        1 for e in field_evals if e.is_correct and normalize_value(e.actual_value) != ""
    )
    precision = correct_filled_count / total_filled if total_filled > 0 else 1.0

    non_empty_gt_field_ids = {gt.field_id for gt in ground_truth if normalize_value(gt.value) != ""}
    should_fill_count = len(non_empty_gt_field_ids)
    correct_should_fill = sum(
        1 for e in field_evals if e.is_correct and e.field_id in non_empty_gt_field_ids
    )
    recall = correct_should_fill / should_fill_count if should_fill_count > 0 else 1.0

    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return FormFillingTaskCompletionEvaluation(
        field_evaluations=field_evals,
        exact_matches=exact_match_count,
        semantic_matches=semantic_match_count,
        grounded_matches=grounded_match_count,
        total_fields=total_fields,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_score=f1_score,
        total_filled_by_agent=total_filled,
        total_should_fill=should_fill_count,
    )


async def evaluate_task_completion(
    response_dict: dict,
    ground_truth: list[GroundTruthAnswer],
    field_coverage: list[FieldCoverageInfo],
    artifacts_text: str,
    judge_client: SageModelClient,
    judge_model: str,
    benchmark_logger: BenchmarkLogger,
    due_diligence_fields: list[dict[str, str]] | None = None,
) -> FormFillingTaskCompletionEvaluation:
    """Compare response to ground truth with exact-match-first strategy.

    Sequential convenience wrapper. For parallel evaluation, use
    evaluate_single_field() + aggregate_task_completion() directly.
    """
    coverage_map = {fc.field_id: fc for fc in field_coverage}
    masked_field_ids = {f["field_id"] for f in (due_diligence_fields or [])}

    field_evals: list[FormFillingFieldEvaluation] = []
    for idx, gt_answer in enumerate(ground_truth):
        benchmark_logger.info(
            f"Correctness: evaluating field {idx + 1}/{len(ground_truth)}: {gt_answer.field_label}"
        )
        field_eval = await evaluate_single_field(
            gt_answer,
            response_dict,
            coverage_map,
            masked_field_ids,
            artifacts_text,
            judge_client,
            judge_model,
        )
        field_evals.append(field_eval)

    return aggregate_task_completion(field_evals, ground_truth)
