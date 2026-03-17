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
from .judge import (
    QuestionFieldMappingJudgment,
    build_question_field_mapping_prompt,
    get_all_form_fields,
)


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
    user_qa_history: list[dict[str, str]],
    due_diligence_fields: list[dict[str, str]],
    ground_truth: list[GroundTruthAnswer],
    findability: list[FieldFindabilityInfo],
    response_dict: dict,
    judge_client: ModelClient,
    judge_model: str,
    distractor_scenarios: dict[str, list[dict]] | None = None,
) -> DueDiligenceEvaluation:
    """Evaluate due diligence with two metric groups:

    1. Masked field correctness (P/R/F1): Did the agent get the correct answer?
       TP=correct answer, FP=wrong answer (non-empty but incorrect), FN=missing/empty
    2. Ask-user appropriateness (P/R/F1): Were ask_user calls appropriate?
       TP=asked unfindable field, FP=asked findable field, FN=unfindable not asked

    Args:
        user_qa_history: List of ask_user Q&A exchanges.
        due_diligence_fields: Fields masked from artifacts with original values.
        ground_truth: List of GroundTruthAnswer with all form field IDs.
        findability: Findability classification for masked fields.
        response_dict: The agent's submitted form as a dictionary.
        judge_client: ModelClient for LLM judge.
        judge_model: Model name for judge.

    Returns:
        DueDiligenceEvaluation with per-field details and two metric groups.
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
        return DueDiligenceEvaluation(
            total_ask_user_calls=len(user_qa_history),
        )

    # Step 1: Map each ask_user question to form fields using LLM judge
    all_form_fields = get_all_form_fields(ground_truth)
    all_valid_field_ids = {f["field_id"] for f in all_form_fields}
    all_asked_field_ids: set[str] = set()
    question_mappings: list[dict] = []

    for idx, qa in enumerate(user_qa_history):
        question = qa["question"]
        answer = qa.get("answer", "")
        print(
            f"Due diligence: evaluating question {idx + 1}/{len(user_qa_history)}: "
            f"{question[:80]}..."
        )

        prompt = build_question_field_mapping_prompt(question, answer, all_form_fields)
        result = await judge_client.chat.completions.aparse(
            model=judge_model,
            messages=[{"role": "user", "content": prompt}],
            response_format=QuestionFieldMappingJudgment,
        )

        mapped_field_ids = []
        for mapping in result.mapped_field_ids:
            if mapping.field_id in all_valid_field_ids:
                mapped_field_ids.append(mapping.field_id)
                all_asked_field_ids.add(mapping.field_id)

        question_mappings.append(
            {
                "question": question,
                "answer": answer,
                "mapped_fields": mapped_field_ids,
                "analysis": result.analysis,
            }
        )

    # Step 2: Evaluate each masked field
    field_evals: list[MaskedFieldEval] = []
    for field_id in sorted(masked_field_ids):
        expected = expected_map[field_id]
        agent_answer = get_nested_value(response_dict, field_id)
        agent_answer_str = str(agent_answer) if agent_answer is not None else ""
        asked_user = field_id in all_asked_field_ids
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
            f"asked={asked_user}, correct={answer_correct}, "
            f"agent='{agent_answer_str[:50]}', expected='{expected[:50]}'"
            f"{distractor_info}"
        )

        field_evals.append(
            MaskedFieldEval(
                field_id=field_id,
                findability=field_findability,
                asked_user=asked_user,
                answer_correct=answer_correct,
                agent_answer=agent_answer_str,
                expected_answer=expected,
                matched_distractor=matched_distractor,
            )
        )

    # Step 3: Compute masked field correctness accuracy
    mf_correct = sum(1 for e in field_evals if e.answer_correct)
    mf_accuracy = mf_correct / len(field_evals) if field_evals else 0.0

    # Step 4: Compute ask-user appropriateness P/R/F1
    # Only consider ask_user calls that mapped to masked fields
    asked_masked = all_asked_field_ids & masked_field_ids
    au_tp = len(asked_masked & unfindable_ids)  # asked unfindable (correct)
    au_fp = len(asked_masked & findable_ids)  # asked findable (wrong)
    au_fn = len(unfindable_ids - all_asked_field_ids)  # unfindable not asked

    au_precision = au_tp / (au_tp + au_fp) if (au_tp + au_fp) > 0 else 0.0
    au_recall = au_tp / (au_tp + au_fn) if (au_tp + au_fn) > 0 else 0.0
    au_f1 = (
        2 * au_precision * au_recall / (au_precision + au_recall)
        if (au_precision + au_recall) > 0
        else 0.0
    )

    return DueDiligenceEvaluation(
        masked_field_evals=field_evals,
        masked_field_accuracy=mf_accuracy,
        ask_user_precision=au_precision,
        ask_user_recall=au_recall,
        ask_user_f1=au_f1,
        total_masked_fields=len(masked_field_ids),
        total_findable=len(findable_ids),
        total_unfindable=len(unfindable_ids),
        total_ask_user_calls=len(user_qa_history),
        question_field_mappings=question_mappings,
    )
