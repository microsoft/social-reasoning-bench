"""Evaluation orchestration for form filling tasks."""

from pathlib import Path

from sage_llm import ModelClient

from sage_benchmark.form_filling.schemas import (
    FormTask,
    FormTaskEvaluationResult,
    InteractiveTaskEvaluationResult,
    InteractiveTaskExecutionResult,
    TaskExecutionResult,
)
from sage_benchmark.form_filling.utils import import_form_model_from_file

from .due_diligence import evaluate_due_diligence
from .duty_of_care import evaluate_duty_of_care
from .privacy import evaluate_conversation_privacy, evaluate_privacy
from .task_completion import evaluate_correctness, validate_with_pydantic


async def evaluate_task(
    exec_result: TaskExecutionResult,
    task_data: FormTask,
    judge_client: ModelClient,
    judge_model: str,
) -> FormTaskEvaluationResult:
    """Complete evaluation.

    Args:
        exec_result: Task execution result
        task_data: FormTask with ground truth and secrets
        judge_client: sage_llm ModelClient for LLM judge
        judge_model: Model name for judge

    Returns:
        FormTaskEvaluationResult with correctness, privacy, and validation scores
    """
    if not exec_result.success or exec_result.action is None:
        raise ValueError("Cannot evaluate failed task")

    response_dict = exec_result.action.fill_responses

    # Load form class for validation
    _, form_class = import_form_model_from_file(Path(task_data.form_model_path))

    # 1. Pydantic validation
    valid, errors = validate_with_pydantic(response_dict, form_class)

    # 2. Prepare artifacts text for grounding evaluation
    artifacts_text = "\n\n".join(
        f"=== {art.artifact_type.upper()} ===\n{art.content}" for art in task_data.artifacts
    )

    # 3. Correctness evaluation
    correctness = await evaluate_correctness(
        response_dict,
        task_data.ground_truth,
        task_data.field_coverage,
        artifacts_text,
        judge_client,
        judge_model,
        due_diligence_fields=task_data.due_diligence_fields,
    )

    # 4. Privacy evaluation
    privacy = await evaluate_privacy(response_dict, task_data.secrets, judge_client, judge_model)

    # 5. Due diligence evaluation
    due_diligence = await evaluate_due_diligence(
        exec_result.user_qa_history,
        task_data.due_diligence_fields,
        task_data.ground_truth,
        judge_client,
        judge_model,
    )

    # 6. Duty of care evaluation
    duty_of_care = await evaluate_duty_of_care(
        response_dict, task_data.negative_info, judge_client, judge_model
    )

    return FormTaskEvaluationResult(
        task_index=exec_result.task_index,
        task=task_data,
        correctness=correctness,
        privacy=privacy,
        due_diligence=due_diligence,
        duty_of_care=duty_of_care,
        pydantic_validation_passed=valid,
        pydantic_validation_errors=errors,
    )


async def evaluate_interactive_task(
    exec_result: InteractiveTaskExecutionResult,
    judge_client: ModelClient,
    judge_model: str,
) -> InteractiveTaskEvaluationResult:
    """Evaluate an interactive interview task.

    Combines:
    1. Correctness evaluation (reused from one-shot)
    2. Form privacy evaluation (reused from one-shot)
    3. Conversation privacy evaluation (interactive-specific)
    4. Pydantic validation

    Args:
        exec_result: Interactive task execution result
        judge_client: sage_llm ModelClient for LLM judge
        judge_model: Model name for judge

    Returns:
        InteractiveTaskEvaluationResult

    Raises:
        ValueError: If task failed
    """
    if not exec_result.success:
        raise ValueError("Cannot evaluate failed task")

    form_task: FormTask = exec_result.task

    # Use the structured dict directly (already in correct format from LLM)
    if not isinstance(exec_result.form_submission, dict):
        raise ValueError(
            f"Expected dict for form submission, got {type(exec_result.form_submission)}"
        )

    form_dict = exec_result.form_submission

    # 1. Evaluate correctness
    artifacts_text = "\n\n".join(
        f"=== {art.artifact_type.upper()} ===\n{art.content}" for art in form_task.artifacts
    )

    correctness_eval = await evaluate_correctness(
        form_dict,
        form_task.ground_truth,
        form_task.field_coverage,
        artifacts_text,
        judge_client,
        judge_model,
        due_diligence_fields=form_task.due_diligence_fields,
    )

    # 2. Evaluate form privacy (secrets in form submission)
    form_privacy_eval = await evaluate_privacy(
        form_dict,
        form_task.secrets,
        judge_client,
        judge_model,
    )

    # 3. Evaluate conversation privacy (secrets in conversation)
    conversation_privacy_eval = await evaluate_conversation_privacy(
        exec_result.conversation,
        form_task.secrets,
        judge_client,
        judge_model,
    )

    # 4. Validate with Pydantic
    valid, errors = validate_with_pydantic(form_dict, form_task.form_class)

    # 5. Due diligence evaluation
    due_diligence_eval = await evaluate_due_diligence(
        exec_result.user_qa_history,
        form_task.due_diligence_fields,
        form_task.ground_truth,
        judge_client,
        judge_model,
    )

    # 6. Duty of care evaluation
    duty_of_care_eval = await evaluate_duty_of_care(
        form_dict, form_task.negative_info, judge_client, judge_model
    )

    return InteractiveTaskEvaluationResult(
        task_index=exec_result.task_index,
        form_id=exec_result.form_id,
        correctness=correctness_eval,
        form_privacy=form_privacy_eval,
        conversation_privacy=conversation_privacy_eval,
        due_diligence=due_diligence_eval,
        duty_of_care=duty_of_care_eval,
        pydantic_validation_passed=valid,
        pydantic_validation_errors=errors,
    )
