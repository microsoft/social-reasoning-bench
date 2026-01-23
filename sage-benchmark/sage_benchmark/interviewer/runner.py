"""Async runner for interviewer benchmark with batching and parallelization."""

import asyncio
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Literal

from sage_benchmark.shared.model_clients import AsyncModelClient, get_async_client

from .agents.assistant import AssistantAgent
from .agents.interviewer import InterviewerAgent
from .evaluation import evaluate_task
from .loader import load_tasks_unified
from .schemas import (
    ConversationMessage,
    FormSubmission,
    TaskEvaluationResult,
    TaskExecutionResult,
)
from .task import InterviewTaskInterface
from .utils import append_batch_to_json_list, load_json_list, load_prior_results

logger = logging.getLogger(__name__)


def _initialize_agents(
    task_adapter: InterviewTaskInterface,
    interviewer_client: AsyncModelClient,
    assistant_client: AsyncModelClient,
) -> tuple[str, InterviewerAgent, AssistantAgent, any]:
    """Initialize agents based on task format."""
    task_format = task_adapter.get_task_format()
    raw_task = task_adapter.get_raw_task()

    assistant_context = task_adapter.get_assistant_context()
    assistant = AssistantAgent(assistant_client, assistant_context)

    form_info = task_adapter.get_form_as_string()
    interviewer = InterviewerAgent(interviewer_client, form_info)

    return task_format, interviewer, assistant, raw_task


async def _run_conversation_loop(
    interviewer: InterviewerAgent,
    assistant: AssistantAgent,
    conversation: list[ConversationMessage],
    max_rounds: int,
    task_id: int | str,
) -> str:
    """Run the interview conversation loop.

    Returns:
        Termination reason: "interviewer_ended", "assistant_ended", or "max_rounds"
    """
    for round_num in range(max_rounds):
        print(f"[Task {task_id}] Round {round_num}")

        # 1. Interviewer's turn
        interviewer_action = await interviewer.generate_action()

        if interviewer_action.tool_name == "EndInterview":
            return "interviewer_ended"
        elif interviewer_action.tool_name == "SendMessage":
            msg = interviewer_action.arguments["message"]
            conversation.append(
                ConversationMessage(
                    from_agent="interviewer",
                    content=msg,
                    timestamp=datetime.now(),
                    round=round_num,
                )
            )
            interviewer.add_tool_result("Message sent")
            assistant.add_new_message("interviewer", msg)

        # 2. Assistant's turn
        assistant_action = await assistant.generate_action()

        if assistant_action.tool_name == "EndConversation":
            return "assistant_ended"
        elif assistant_action.tool_name == "SendMessage":
            msg = assistant_action.arguments["message"]
            conversation.append(
                ConversationMessage(
                    from_agent="assistant",
                    content=msg,
                    timestamp=datetime.now(),
                    round=round_num,
                )
            )
            assistant.add_tool_result("Message sent")
            interviewer.add_new_message("assistant", msg)

    return "max_rounds"


async def run_single_task(
    task_adapter: InterviewTaskInterface,
    task_index: int,
    interviewer_client: AsyncModelClient,
    assistant_client: AsyncModelClient,
    max_rounds: int,
) -> TaskExecutionResult:
    """Execute a single interview task."""
    conversation: list[ConversationMessage] = []
    interviewer = None
    assistant = None

    # 1. INITIALIZATION
    task_format, interviewer, assistant, raw_task = _initialize_agents(
        task_adapter, interviewer_client, assistant_client
    )
    try:
        # 2. CONVERSATION
        termination_reason = await _run_conversation_loop(
            interviewer, assistant, conversation, max_rounds, task_adapter.task_id
        )

        # 3. FORM FILLING
        form_class = raw_task.form_class if task_format == "form_filling" else FormSubmission

        form_submission = await interviewer.fill_form(
            form_context=task_adapter.get_form_as_string(), form_class=form_class
        )

        # 4. RETURN SUCCESS RESULT
        return TaskExecutionResult(
            task_index=task_index,
            task_format=task_format,
            task=raw_task if task_format == "yaml" else None,
            task_adapter=task_adapter,
            conversation=conversation,
            form_submission=form_submission,
            termination_reason=termination_reason,
            total_rounds=len([m for m in conversation if m.from_agent == "interviewer"]),
            success=True,
            interviewer_context=interviewer.messages,
            assistant_context=assistant.messages,
        )

    except Exception as e:
        logger.error(f"Task {task_index} failed: {e}")
        logger.error(traceback.format_exc())

        return TaskExecutionResult(
            task_index=task_index,
            task_format=task_format,
            task=raw_task if task_format == "yaml" else None,
            task_adapter=task_adapter,
            conversation=conversation,
            form_submission=None,
            termination_reason="error",
            total_rounds=len([m for m in conversation if m.from_agent == "interviewer"]),
            success=False,
            error_message=str(e),
            interviewer_context=getattr(interviewer, "messages", []) if interviewer else [],
            assistant_context=getattr(assistant, "messages", []) if assistant else [],
        )


async def run_tasks(
    data_path: str,
    interviewer_model: str,
    assistant_model: str,
    judge_model: str,
    output_dir: str | None = None,
    limit: int | None = None,
    mode: Literal["all", "tasks", "eval"] = "all",
    task_results_path: str | None = None,
    batch_size: int = 25,
    max_concurrent_requests: int = 100,
    max_rounds: int = 30,
    interviewer_reasoning_effort: str | None = None,
    assistant_reasoning_effort: str | None = None,
    judge_reasoning_effort: str | None = None,
):
    """Run the complete interviewer benchmark with async parallelization.

    Args:
        data_path: Path to tasks.yaml OR directory of form_filling tasks
        interviewer_model: Model for interviewer agent
        assistant_model: Model for assistant agent
        judge_model: Model for evaluation
        output_dir: Optional directory to save results
        limit: Optional limit on number of tasks
        mode: Run mode - 'all', 'tasks', or 'eval'
        task_results_path: Path to task_results.json (for eval mode)
        batch_size: Number of tasks to run in parallel
        max_concurrent_requests: Max concurrent API requests per client
        max_rounds: Maximum conversation rounds per task
        interviewer_reasoning_effort: Reasoning effort for interviewer agent (gpt-5.x, gemini)
        assistant_reasoning_effort: Reasoning effort for assistant agent (gpt-5.x, gemini)
        judge_reasoning_effort: Reasoning effort for judge (gpt-5.x, gemini)

    Returns:
        Dictionary with benchmark results
    """
    # Create run directory
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = (
            output_path
            / f"run_{timestamp_str}_interviewer_{interviewer_model}_assistant_{assistant_model}"
        )
        run_dir.mkdir(parents=True, exist_ok=True)

        task_results_file = run_dir / "task_results.json"
        eval_results_file = run_dir / "eval_results.json"
        summary_file = run_dir / "summary.json"
        print(f"Run directory: {run_dir}")
    else:
        run_dir = None
        task_results_file = None
        eval_results_file = None
        summary_file = None

    # Execute tasks (or load from file)
    execution_results: list[TaskExecutionResult] = []
    tasks = load_tasks_unified(data_path)

    if mode == "eval":
        # eval only - load prior results
        execution_results = load_prior_results(task_results_path, tasks)

    else:
        ### ---- RUN TASKS ---- ###
        print(f"Loaded {len(tasks)} interview tasks from {data_path}")
        print(f"Task format: {tasks[0].get_task_format() if tasks else 'unknown'}")

        if limit:
            tasks = tasks[:limit]
            print(f"Running first {limit} tasks")

        # Create async clients
        interviewer_client = get_async_client(
            interviewer_model,
            max_concurrent_requests=max_concurrent_requests,
            reasoning_effort=interviewer_reasoning_effort,
        )
        assistant_client = get_async_client(
            assistant_model,
            max_concurrent_requests=max_concurrent_requests,
            reasoning_effort=assistant_reasoning_effort,
        )

        print(f"\n{'=' * 60}")
        print(f"Running {len(tasks)} tasks in batches of {batch_size}")
        print(f"Max rounds per task: {max_rounds}")
        print(f"{'=' * 60}\n")

        # Process tasks in batches
        for batch_start in range(0, len(tasks), batch_size):
            batch_end = min(batch_start + batch_size, len(tasks))
            batch = tasks[batch_start:batch_end]

            print(
                f"Processing batch {batch_start // batch_size + 1} (tasks {batch_start}-{batch_end - 1})..."
            )

            # Run batch in parallel
            batch_tasks = [
                run_single_task(task, idx, interviewer_client, assistant_client, max_rounds)
                for idx, task in enumerate(batch, start=batch_start)
            ]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            # Process results
            batch_data_to_save = []
            for task_idx, result in zip(range(batch_start, batch_end), batch_results):
                if isinstance(result, Exception):
                    logger.error(f"Task {task_idx} failed: {result}")
                    print(f"Task {task_idx}: FAILED - {result}")
                else:
                    execution_results.append(result)
                    print(
                        f"Task {task_idx}: {result.termination_reason} - "
                        f"{result.total_rounds} rounds"
                    )

                    if task_results_file:
                        # Use task_adapter to get task_id for both formats
                        task_id = (
                            result.task_adapter.task_id if result.task_adapter else result.task.id
                        )
                        batch_data_to_save.append(
                            {
                                "task_index": result.task_index,
                                "task_id": task_id,
                                "task_format": result.task_format,
                                "execution": result.model_dump(mode="json"),
                            }
                        )

            # Batch-level file write
            if task_results_file and batch_data_to_save:
                append_batch_to_json_list(task_results_file, batch_data_to_save)
                print(f"Saved batch {batch_start // batch_size + 1} results\n")

    ### ---- RUN EVALUATION ---- ###
    evaluation_results = []
    if mode != "tasks":
        print(f"\n{'=' * 60}")
        print("Evaluating results...")
        print(f"{'=' * 60}\n")

        judge_client = get_async_client(
            judge_model,
            max_concurrent_requests=max_concurrent_requests,
            reasoning_effort=judge_reasoning_effort,
        )

        successful_results = [r for r in execution_results if r.success]
        print(f"Evaluating {len(successful_results)} successful tasks in batches of {batch_size}\n")

        # Process evaluations in batches
        for batch_start in range(0, len(successful_results), batch_size):
            batch_end = min(batch_start + batch_size, len(successful_results))
            batch = successful_results[batch_start:batch_end]

            print(f"Evaluating batch {batch_start // batch_size + 1}...")

            eval_tasks = [evaluate_task(exec_result, judge_client) for exec_result in batch]

            batch_eval_results = await asyncio.gather(*eval_tasks, return_exceptions=True)

            batch_eval_data_to_save = []
            for eval_result in batch_eval_results:
                if isinstance(eval_result, Exception):
                    logger.error(f"Evaluation failed: {eval_result}")
                else:
                    evaluation_results.append(eval_result)

                    if eval_result.task_format == "yaml":
                        # yaml task result
                        print(
                            f"Task {eval_result.task_index}: "
                            f"Completion={eval_result.task_completion.completion_score:.2%} ({eval_result.task_completion.correct_answers}/{eval_result.task_completion.total_questions}), "
                            f"Privacy={eval_result.conversation_privacy.privacy_score:.2%} ({len(eval_result.conversation_privacy.secrets_leaked_in_conversation)}/{len(eval_result.conversation_privacy.secrets_checked)})"
                        )

                    else:
                        # Form filling task result
                        print(
                            f"Task {eval_result.task_index}: "
                            f"Accuracy={eval_result.correctness.accuracy:.2%}, "
                            f"FormPrivacy={eval_result.form_privacy.privacy_score:.2%}, "
                            f"ConvPrivacy={eval_result.conversation_privacy.privacy_score:.2%}, "
                            f"Valid={eval_result.pydantic_validation_passed}"
                        )

                    batch_eval_data_to_save.append(
                        {
                            "task_index": eval_result.task_index,
                            "task_format": eval_result.task_format,
                            "task_id": eval_result.task.id if eval_result.task else None,
                            "evaluation": eval_result.model_dump(mode="json"),
                        }
                    )

            if eval_results_file and batch_eval_data_to_save:
                append_batch_to_json_list(eval_results_file, batch_eval_data_to_save)
                print("Saved batch eval results\n")

    # Aggregate metrics (handle both YAML and form_filling results)
    yaml_results = [r for r in evaluation_results if r.task_completion is not None]
    ff_results = [r for r in evaluation_results if r.correctness is not None]

    # Calculate YAML metrics
    if yaml_results:
        avg_completion = sum(e.task_completion.completion_score for e in yaml_results) / len(
            yaml_results
        )
        avg_conv_privacy = sum(e.conversation_privacy.privacy_score for e in yaml_results) / len(
            yaml_results
        )
    else:
        avg_completion = 0.0
        avg_conv_privacy = 0.0

    # Calculate form_filling metrics
    if ff_results:
        avg_accuracy = sum(e.correctness.accuracy for e in ff_results) / len(ff_results)
        avg_form_privacy = sum(e.form_privacy.privacy_score for e in ff_results) / len(ff_results)
        avg_ff_conv_privacy = sum(e.conversation_privacy.privacy_score for e in ff_results) / len(
            ff_results
        )
        avg_validation = sum(1 for e in ff_results if e.pydantic_validation_passed) / len(
            ff_results
        )
        perfect_accuracy_count = sum(1 for e in ff_results if e.correctness.accuracy == 1.0)
        perfect_privacy_count = sum(
            1
            for e in ff_results
            if e.form_privacy.privacy_score == 1.0 and e.conversation_privacy.privacy_score == 1.0
        )
    else:
        avg_accuracy = 0.0
        avg_form_privacy = 0.0
        avg_ff_conv_privacy = 0.0
        avg_validation = 0.0
        perfect_accuracy_count = 0
        perfect_privacy_count = 0

    # Build detailed task-level evaluation data
    task_evaluations = []
    for eval_result in evaluation_results:
        if eval_result.task_completion is not None:
            # YAML task
            task_evaluations.append(
                {
                    "task_index": eval_result.task_index,
                    "task_format": "yaml",
                    "task_id": eval_result.task.id,
                    "task_completion": eval_result.task_completion.model_dump(mode="json"),
                    "conversation_privacy": eval_result.conversation_privacy.model_dump(
                        mode="json"
                    ),
                }
            )
        elif eval_result.correctness is not None:
            # Form filling task
            task_evaluations.append(
                {
                    "task_index": eval_result.task_index,
                    "task_format": "form_filling",
                    "correctness": eval_result.correctness.model_dump(mode="json"),
                    "form_privacy": eval_result.form_privacy.model_dump(mode="json"),
                    "conversation_privacy": eval_result.conversation_privacy.model_dump(
                        mode="json"
                    ),
                    "pydantic_validation_passed": eval_result.pydantic_validation_passed,
                }
            )

    # Build summary
    summary_dict = {
        "interviewer_model": interviewer_model,
        "assistant_model": assistant_model,
        "judge_model": judge_model,
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "total_tasks": len(execution_results),
        "successful_executions": sum(1 for r in execution_results if r.success),
        "batch_size": batch_size,
        "max_rounds": max_rounds,
    }

    # Add YAML metrics if present
    if yaml_results:
        summary_dict["yaml_tasks"] = {
            "count": len(yaml_results),
            "avg_completion_score": avg_completion,
            "avg_conversation_privacy_score": avg_conv_privacy,
        }

    # Add form_filling metrics if present
    if ff_results:
        summary_dict["form_filling_tasks"] = {
            "count": len(ff_results),
            "avg_accuracy": avg_accuracy,
            "avg_form_privacy_score": avg_form_privacy,
            "avg_conversation_privacy_score": avg_ff_conv_privacy,
            "avg_validation_rate": avg_validation,
            "perfect_accuracy_rate": perfect_accuracy_count / len(ff_results),
            "perfect_privacy_rate": perfect_privacy_count / len(ff_results),
        }

    result = {
        "summary": summary_dict,
        "task_evaluations": task_evaluations,
    }

    # Save summary
    if summary_file:
        with open(summary_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nSummary saved to: {summary_file}")

    # Print summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"Interviewer Model: {interviewer_model}")
    print(f"Assistant Model: {assistant_model}")
    print(f"Judge Model: {judge_model}")
    print(f"Total tasks: {len(execution_results)}")
    print(f"Successful: {result['summary']['successful_executions']}")

    if mode != "tasks":
        if yaml_results:
            print(f"\nYAML Tasks ({len(yaml_results)}):")
            print(f"  Avg Completion Score: {avg_completion:.3f} ({avg_completion:.1%})")
            print(f"  Avg Conv Privacy Score: {avg_conv_privacy:.3f} ({avg_conv_privacy:.1%})")

        if ff_results:
            print(f"\nForm Filling Tasks ({len(ff_results)}):")
            print(f"  Avg Accuracy: {avg_accuracy:.3f} ({avg_accuracy:.1%})")
            print(
                f"  Perfect Accuracy Rate: {perfect_accuracy_count}/{len(ff_results)} ({perfect_accuracy_count / len(ff_results):.1%})"
            )
            print(f"  Avg Form Privacy Score: {avg_form_privacy:.3f} ({avg_form_privacy:.1%})")
            print(
                f"  Avg Conv Privacy Score: {avg_ff_conv_privacy:.3f} ({avg_ff_conv_privacy:.1%})"
            )
            print(
                f"  Perfect Privacy Rate: {perfect_privacy_count}/{len(ff_results)} ({perfect_privacy_count / len(ff_results):.1%})"
            )
            print(f"  Avg Validation Rate: {avg_validation:.3f} ({avg_validation:.1%})")

    return result
