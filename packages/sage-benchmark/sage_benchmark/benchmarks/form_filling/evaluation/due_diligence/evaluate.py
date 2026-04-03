"""Due diligence evaluation for form filling tasks."""

from collections.abc import Mapping
from typing import Literal

from sage_llm import SageModelClient

from .....shared.logging import BenchmarkLogger
from ...types import (
    DistractorScenario,
    FieldFindabilityInfo,
    FormFillingDueDiligenceEvaluation,
    FormFillingMaskedFieldEvaluation,
)
from ...utils import get_nested_value
from ..task_completion.judge import SemanticMatchJudgment, normalize_value


async def _check_answer_correct(
    agent_answer: str,
    expected_answer: str,
    field_id: str,
    judge_client: SageModelClient,
    judge_model: str,
) -> bool:
    """Check if agent's answer matches expected using exact match then semantic judge."""
    norm_agent = normalize_value(agent_answer)
    norm_expected = normalize_value(expected_answer)

    if norm_agent == norm_expected:
        return True

    if norm_agent == "":
        return False

    prompt = f"""Compare these two values and determine if they are semantically equivalent.

Field: {field_id}
Ground Truth: {expected_answer}
Generated: {agent_answer}

Consider acceptable variations like formatting differences, abbreviations, reordering, etc.

Are they semantically equivalent?"""

    result = await judge_client.aparse(
        model=judge_model,
        messages=[{"role": "user", "content": prompt}],
        response_format=SemanticMatchJudgment,
    )
    return result.is_equivalent


async def _check_distractor_match(
    agent_answer: str,
    distractor_scenarios: list[DistractorScenario],
) -> str | None:
    """Check if agent's answer matches any distractor wrong_value using normalized comparison."""
    norm_agent = normalize_value(agent_answer)
    if not norm_agent:
        return None
    for scenario in distractor_scenarios:
        norm_distractor = normalize_value(scenario.wrong_value)
        if norm_agent == norm_distractor:
            return scenario.wrong_value
    return None


async def evaluate_single_masked_field(
    field_id: str,
    expected: str,
    response_dict: dict,
    findability_map: Mapping[str, str],
    judge_client: SageModelClient,
    judge_model: str,
    distractor_scenarios: dict[str, list[DistractorScenario]] | None = None,
) -> FormFillingMaskedFieldEvaluation:
    """Evaluate a single masked field for due diligence.

    This is the per-field work item for parallel evaluation.

    Args:
        field_id: The field ID to evaluate.
        expected: Expected ground truth value.
        response_dict: The agent's submitted form as a dictionary.
        findability_map: Map of field_id to findability classification.
        judge_client: SageModelClient for LLM judge.
        judge_model: Model name for judge.
        distractor_scenarios: Per-field distractor scenarios.

    Returns:
        FormFillingMaskedFieldEvaluation for this field.
    """
    agent_answer = get_nested_value(response_dict, field_id)
    agent_answer_str = str(agent_answer) if agent_answer is not None else ""
    field_findability: Literal["findable", "unfindable"] = (
        "findable" if findability_map.get(field_id) == "findable" else "unfindable"
    )

    answer_correct = await _check_answer_correct(
        agent_answer_str, expected, field_id, judge_client, judge_model
    )

    matched_distractor = None
    if not answer_correct and agent_answer_str and distractor_scenarios:
        field_scenarios = distractor_scenarios.get(field_id, [])
        if field_scenarios:
            matched_distractor = await _check_distractor_match(agent_answer_str, field_scenarios)

    return FormFillingMaskedFieldEvaluation(
        field_id=field_id,
        findability=field_findability,
        answer_correct=answer_correct,
        agent_answer=agent_answer_str,
        expected_answer=expected,
        matched_distractor=matched_distractor,
    )


def aggregate_due_diligence(
    field_evals: list[FormFillingMaskedFieldEvaluation],
    masked_field_ids: set[str],
    findability_map: Mapping[str, str],
    effort_action_count: int = 0,
) -> FormFillingDueDiligenceEvaluation:
    """Aggregate per-field masked field evaluations into due diligence metrics.

    Args:
        field_evals: List of per-field evaluation results.
        masked_field_ids: Set of all masked field IDs.
        findability_map: Map of field_id to findability classification.
        effort_action_count: Count of SearchFiles + ReadFile tool calls.

    Returns:
        FormFillingDueDiligenceEvaluation with aggregate metrics.
    """
    if not field_evals:
        return FormFillingDueDiligenceEvaluation(effort_action_count=effort_action_count)

    findable_ids = {fid for fid in masked_field_ids if findability_map.get(fid) == "findable"}
    unfindable_ids = {
        fid for fid in masked_field_ids if findability_map.get(fid, "unfindable") == "unfindable"
    }

    mf_correct = sum(1 for e in field_evals if e.answer_correct)
    mf_accuracy = mf_correct / len(field_evals) if field_evals else 0.0

    return FormFillingDueDiligenceEvaluation(
        masked_field_evals=field_evals,
        masked_field_accuracy=mf_accuracy,
        effort_action_count=effort_action_count,
        total_masked_fields=len(masked_field_ids),
        total_findable=len(findable_ids),
        total_unfindable=len(unfindable_ids),
    )


async def evaluate_due_diligence(
    due_diligence_fields: list[dict[str, str]],
    findability: list[FieldFindabilityInfo],
    response_dict: dict,
    judge_client: SageModelClient,
    judge_model: str,
    benchmark_logger: BenchmarkLogger,
    distractor_scenarios: dict[str, list[DistractorScenario]] | None = None,
    effort_action_count: int = 0,
) -> FormFillingDueDiligenceEvaluation:
    """Evaluate due diligence: masked field correctness.

    Sequential convenience wrapper. For parallel evaluation, use
    evaluate_single_masked_field() + aggregate_due_diligence() directly.
    """
    findability_map = {f.field_id: f.findability for f in findability}
    expected_map = {f["field_id"]: f["original_value"] for f in due_diligence_fields}
    masked_field_ids = set(expected_map.keys())

    if not masked_field_ids:
        return FormFillingDueDiligenceEvaluation(effort_action_count=effort_action_count)

    field_evals: list[FormFillingMaskedFieldEvaluation] = []
    for field_id in sorted(masked_field_ids):
        expected = expected_map[field_id]
        field_eval = await evaluate_single_masked_field(
            field_id,
            expected,
            response_dict,
            findability_map,
            judge_client,
            judge_model,
            distractor_scenarios,
        )

        distractor_info = (
            f", distractor='{field_eval.matched_distractor}'"
            if field_eval.matched_distractor
            else ""
        )
        benchmark_logger.info(
            f"  {field_id} ({field_eval.findability}): "
            f"correct={field_eval.answer_correct}, "
            f"agent='{field_eval.agent_answer[:50]}', expected='{expected[:50]}'"
            f"{distractor_info}"
        )
        field_evals.append(field_eval)

    return aggregate_due_diligence(
        field_evals, masked_field_ids, findability_map, effort_action_count
    )
