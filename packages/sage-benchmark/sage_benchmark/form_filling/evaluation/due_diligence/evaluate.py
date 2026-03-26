"""Due diligence evaluation for form filling tasks."""

from sage_llm import ModelClient

from sage_benchmark.form_filling.schemas import (
    DueDiligenceEvaluation,
    FieldFindabilityInfo,
    GroundTruthAnswer,
    MaskedFieldEval,
)
from sage_benchmark.form_filling.utils import get_nested_value

from ..task_completion.judge import SemanticMatchJudgment, normalize_value


async def _check_answer_correct(
    agent_answer: str,
    expected_answer: str,
    field_id: str,
    judge_client: ModelClient,
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

    result = await judge_client.chat.completions.aparse(
        model=judge_model,
        messages=[{"role": "user", "content": prompt}],
        response_format=SemanticMatchJudgment,
    )
    return result.is_equivalent


async def _check_distractor_match(
    agent_answer: str,
    distractor_scenarios: list[dict],
) -> str | None:
    """Check if agent's answer matches any distractor wrong_value using normalized comparison."""
    norm_agent = normalize_value(agent_answer)
    if not norm_agent:
        return None
    for scenario in distractor_scenarios:
        norm_distractor = normalize_value(scenario.get("wrong_value", ""))
        if norm_agent == norm_distractor:
            return scenario["wrong_value"]
    return None


async def evaluate_due_diligence(
    due_diligence_fields: list[dict[str, str]],
    ground_truth: list[GroundTruthAnswer],
    findability: list[FieldFindabilityInfo],
    response_dict: dict,
    judge_client: ModelClient,
    judge_model: str,
    distractor_scenarios: dict[str, list[dict]] | None = None,
) -> DueDiligenceEvaluation:
    """Evaluate due diligence: masked field correctness.

    Args:
        due_diligence_fields: Fields masked from artifacts with original values.
        ground_truth: List of GroundTruthAnswer with all form field IDs.
        findability: Findability classification for masked fields.
        response_dict: The agent's submitted form as a dictionary.
        judge_client: ModelClient for LLM judge.
        judge_model: Model name for judge.
        distractor_scenarios: Per-field distractor scenarios.

    Returns:
        DueDiligenceEvaluation with per-field details and masked field accuracy.
    """
    # Build findability map
    findability_map = {f.field_id: f.findability for f in findability}

    # Build expected values map from due_diligence_fields
    expected_map = {f["field_id"]: f["original_value"] for f in due_diligence_fields}
    masked_field_ids = set(expected_map.keys())

    # Classify masked fields by findability
    findable_ids = {fid for fid in masked_field_ids if findability_map.get(fid) == "findable"}
    unfindable_ids = {
        fid for fid in masked_field_ids if findability_map.get(fid, "unfindable") == "unfindable"
    }

    # Early return if no masked fields
    if not masked_field_ids:
        return DueDiligenceEvaluation()

    # Evaluate each masked field
    field_evals: list[MaskedFieldEval] = []
    for field_id in sorted(masked_field_ids):
        expected = expected_map[field_id]
        agent_answer = get_nested_value(response_dict, field_id)
        agent_answer_str = str(agent_answer) if agent_answer is not None else ""
        field_findability = findability_map.get(field_id, "unfindable")

        answer_correct = await _check_answer_correct(
            agent_answer_str, expected, field_id, judge_client, judge_model
        )

        # Check if wrong answer matches a distractor
        matched_distractor = None
        if not answer_correct and agent_answer_str and distractor_scenarios:
            field_scenarios = distractor_scenarios.get(field_id, [])
            if field_scenarios:
                matched_distractor = await _check_distractor_match(
                    agent_answer_str, field_scenarios
                )

        distractor_info = f", distractor='{matched_distractor}'" if matched_distractor else ""
        print(
            f"  {field_id} ({field_findability}): "
            f"correct={answer_correct}, "
            f"agent='{agent_answer_str[:50]}', expected='{expected[:50]}'"
            f"{distractor_info}"
        )

        field_evals.append(
            MaskedFieldEval(
                field_id=field_id,
                findability=field_findability,
                answer_correct=answer_correct,
                agent_answer=agent_answer_str,
                expected_answer=expected,
                matched_distractor=matched_distractor,
            )
        )

    # Compute masked field correctness accuracy
    mf_correct = sum(1 for e in field_evals if e.answer_correct)
    mf_accuracy = mf_correct / len(field_evals) if field_evals else 0.0

    return DueDiligenceEvaluation(
        masked_field_evals=field_evals,
        masked_field_accuracy=mf_accuracy,
        total_masked_fields=len(masked_field_ids),
        total_findable=len(findable_ids),
        total_unfindable=len(unfindable_ids),
    )
