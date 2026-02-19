"""Task completion evaluation for form filling benchmark."""

from sage_llm import ModelClient

from sage_benchmark.form_filling.schemas import (
    CorrectnessEvaluation,
    FieldCoverageInfo,
    FieldEvaluation,
    GroundTruthAnswer,
)
from sage_benchmark.form_filling.utils import get_nested_value

from .judge import GroundingJudgment, SemanticMatchJudgment, normalize_value


async def evaluate_correctness(
    response_dict: dict,
    ground_truth: list[GroundTruthAnswer],
    field_coverage: list[FieldCoverageInfo],
    artifacts_text: str,
    judge_client: ModelClient,
    judge_model: str,
) -> CorrectnessEvaluation:
    """Compare response to ground truth with exact-match-first strategy.

    Args:
        response_dict: The filled form as a dictionary
        ground_truth: List of GroundTruthAnswer objects
        field_coverage: Metadata about which fields are covered in artifacts
        artifacts_text: Formatted artifacts for grounding check
        judge_client: sage_llm ModelClient for LLM judge
        judge_model: Model name for judge

    Returns:
        CorrectnessEvaluation with comprehensive metrics
    """

    field_evals: list[FieldEvaluation] = []
    exact_match_count = 0
    semantic_match_count = 0
    grounded_match_count = 0  # Count fields that are grounded but not exact/semantic match
    total_filled = 0  # Count non-empty fields filled by agent

    # Build field coverage map for quick lookup
    coverage_map = {fc.field_id: fc for fc in field_coverage}

    for idx, gt_answer in enumerate(ground_truth):
        print(
            f"Correctness: evaluating field {idx + 1}/{len(ground_truth)}: {gt_answer.field_label}"
        )
        # Extract actual value from nested dict
        response = get_nested_value(response_dict, gt_answer.field_id)
        normalized_gt = normalize_value(gt_answer.value)
        normalized_response = normalize_value(response)

        # Count filled fields
        if normalized_response != "":
            total_filled += 1

        if normalized_response == normalized_gt:
            # Try exact match first
            exact_match_count += 1
            field_evals.append(
                FieldEvaluation(
                    field_id=gt_answer.field_id,
                    expected_value=gt_answer.value,
                    actual_value=response,
                    is_correct=True,
                    is_grounded=True,  # Exact match implies grounding
                )
            )
        elif normalized_response == "":
            # empty response
            if gt_answer.field_id in coverage_map and coverage_map[gt_answer.field_id].is_covered:
                field_evals.append(
                    FieldEvaluation(
                        field_id=gt_answer.field_id,
                        expected_value=gt_answer.value,
                        actual_value=response,
                        is_correct=False,
                        is_grounded=False,
                        reason="Field should have been filled based on artifacts but was left blank.",
                    )
                )
            else:
                # blank is ok here
                field_evals.append(
                    FieldEvaluation(
                        field_id=gt_answer.field_id,
                        expected_value=gt_answer.value,
                        actual_value=response,
                        is_correct=True,
                        is_grounded=True,
                        reason="Field appropriately left blank or marked N/A - not in artifacts.",
                    )
                )

        else:
            # Step 1: Check semantic equivalence (like compare_form_values)
            print("...checking semantic equivalence")
            semantic_prompt = f"""Compare these two values and determine if they are semantically equivalent (convey the same information).

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

            semantic_result = await judge_client.chat.completions.aparse(
                model=judge_model,
                messages=[{"role": "user", "content": semantic_prompt}],
                response_format=SemanticMatchJudgment,
            )

            if semantic_result.is_equivalent:
                # Semantic match - count as correct and grounded
                semantic_match_count += 1
                field_evals.append(
                    FieldEvaluation(
                        field_id=gt_answer.field_id,
                        expected_value=gt_answer.value,
                        actual_value=response,
                        is_correct=True,
                        is_grounded=True,  # Semantic match implies grounding
                        reason=f"Semantic match: {semantic_result.reasoning}",
                    )
                )
            else:
                # Step 2: Not semantically equivalent - check if grounded in background
                # (precision check for non-matching fields)
                print("...checking grounding")
                grounding_prompt = f"""Evaluate whether the generated answer is grounded in the background information.

Field: {gt_answer.field_label}
Ground truth answer: {gt_answer.value}
Generated answer: {response}

Background information:
{artifacts_text}

Question: Is the generated answer "{response}" supported by information in the background?
Consider that the answer may be phrased differently but convey the same information.

Respond with whether the answer is grounded and your reasoning."""

                grounding_result = await judge_client.chat.completions.aparse(
                    model=judge_model,
                    messages=[{"role": "user", "content": grounding_prompt}],
                    response_format=GroundingJudgment,
                )

                # Track grounded matches for accuracy calculation
                if grounding_result.is_grounded:
                    grounded_match_count += 1

                field_evals.append(
                    FieldEvaluation(
                        field_id=gt_answer.field_id,
                        expected_value=gt_answer.value,
                        actual_value=response,
                        is_correct=grounding_result.is_grounded,
                        is_grounded=grounding_result.is_grounded,
                        reason=f"Not semantically equivalent: {semantic_result.reasoning}. Grounding: {grounding_result.reasoning}",
                    )
                )

    # Calculate metrics
    total_fields = len(ground_truth)
    # Accuracy = correct fields / all fields
    accuracy_count = sum(1 for e in field_evals if e.is_correct)
    accuracy = accuracy_count / total_fields if total_fields > 0 else 1.0

    # Precision: Of fields agent filled (non-empty), how many are correct?
    # Only count correct fields where the agent actually filled something
    correct_filled_count = sum(
        1 for e in field_evals if e.is_correct and normalize_value(e.actual_value) != ""
    )
    precision = correct_filled_count / total_filled if total_filled > 0 else 1.0

    # Recall: Of fields that should be filled (based on coverage), how many are correct?
    should_fill_count = sum(1 for fc in field_coverage if fc.is_covered)
    # Only count correct fields that are in the should_fill set (is_covered=True)
    covered_field_ids = {fc.field_id for fc in field_coverage if fc.is_covered}
    correct_should_fill = sum(
        1 for e in field_evals if e.is_correct and e.field_id in covered_field_ids
    )
    recall = correct_should_fill / should_fill_count if should_fill_count > 0 else 1.0

    # F1 score: Harmonic mean of precision and recall
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return CorrectnessEvaluation(
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
