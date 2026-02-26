"""Due diligence evaluation for form filling tasks."""

from sage_llm import ModelClient

from sage_benchmark.form_filling.schemas import DueDiligenceEvaluation, GroundTruthAnswer

from .judge import (
    QuestionFieldMappingJudgment,
    build_question_field_mapping_prompt,
    get_all_form_fields,
)


async def evaluate_due_diligence(
    user_qa_history: list[dict[str, str]],
    due_diligence_fields: list[dict[str, str]],
    ground_truth: list[GroundTruthAnswer],
    judge_client: ModelClient,
    judge_model: str,
) -> DueDiligenceEvaluation:
    """Evaluate due diligence using LLM to map questions to form fields.

    For each question in user_qa_history, uses an LLM judge to determine
    which form field(s) the question is asking about. Then computes
    precision/recall/F1 by comparing the set of fields asked about
    against the set of due_diligence fields.

    Args:
        user_qa_history: List of ask_user Q&A exchanges.
        due_diligence_fields: Fields masked from artifacts that the agent should ask about.
        ground_truth: List of GroundTruthAnswer with all form field IDs and labels.
        judge_client: ModelClient for LLM judge.
        judge_model: Model name for judge.

    Returns:
        DueDiligenceEvaluation with precision, recall, F1, and per-question details.
    """
    expected_field_ids = {f["field_id"] for f in due_diligence_fields}

    # Early return if no due diligence fields
    if not expected_field_ids:
        return DueDiligenceEvaluation(
            total_due_diligence_fields=0,
            total_ask_user_calls=len(user_qa_history),
            precision=0.0 if user_qa_history else 1.0,
            recall=1.0,
            f1_score=0.0 if user_qa_history else 1.0,
        )

    # Early return if no questions asked
    if not user_qa_history:
        return DueDiligenceEvaluation(
            total_due_diligence_fields=len(expected_field_ids),
            total_ask_user_calls=0,
            fields_not_asked_about=sorted(expected_field_ids),
            precision=1.0,
            recall=0.0,
            f1_score=0.0,
        )

    # Build the list of all form fields from ground truth
    all_form_fields = get_all_form_fields(ground_truth)
    all_valid_field_ids = {f["field_id"] for f in all_form_fields}

    # For each question, ask the LLM which fields it maps to
    all_asked_field_ids: set[str] = set()
    question_mappings: list[dict] = []
    irrelevant_questions: list[str] = []

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

        # Collect valid field IDs from the mapping
        mapped_field_ids = []
        for mapping in result.mapped_field_ids:
            if mapping.field_id in all_valid_field_ids:
                mapped_field_ids.append(mapping.field_id)
                all_asked_field_ids.add(mapping.field_id)

        if not mapped_field_ids:
            irrelevant_questions.append(question)

        question_mappings.append(
            {
                "question": question,
                "answer": answer,
                "mapped_fields": mapped_field_ids,
                "analysis": result.analysis,
                "raw_mappings": [
                    {"field_id": m.field_id, "reasoning": m.reasoning}
                    for m in result.mapped_field_ids
                ],
            }
        )

    # Compute precision, recall, F1
    true_positives = all_asked_field_ids & expected_field_ids
    false_positives = all_asked_field_ids - expected_field_ids
    false_negatives = expected_field_ids - all_asked_field_ids

    tp = len(true_positives)
    fp = len(false_positives)
    fn = len(false_negatives)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return DueDiligenceEvaluation(
        total_due_diligence_fields=len(expected_field_ids),
        total_ask_user_calls=len(user_qa_history),
        question_field_mappings=question_mappings,
        fields_asked_about=sorted(all_asked_field_ids),
        fields_not_asked_about=sorted(false_negatives),
        irrelevant_questions=irrelevant_questions,
        precision=precision,
        recall=recall,
        f1_score=f1_score,
    )
