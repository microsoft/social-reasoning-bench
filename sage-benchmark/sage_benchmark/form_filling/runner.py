import argparse
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from sage_benchmark.form_filling.agent import run_single_task
from sage_benchmark.form_filling.evaluator import evaluate_task
from sage_benchmark.form_filling.loader import load_form_tasks
from sage_benchmark.form_filling.schemas import (
    BenchmarkResult,
    TaskEvaluationResult,
    TaskExecutionResult,
)
from sage_benchmark.shared.model_clients import get_client


def run_benchmark(
    data_path: str,
    model_name: str,
    judge_model: str,
    output_dir: str | None = None,
) -> BenchmarkResult:
    """Run the complete form filling benchmark."""
    tasks = load_form_tasks(data_path)
    print(f"Loaded {len(tasks)} form tasks from {data_path}")

    client = get_client(model_name)
    judge_client = get_client(judge_model)

    execution_results: list[TaskExecutionResult] = []
    for i, task in enumerate(tasks):
        print(f"\n{'=' * 60}")
        print(f"Task {i}")
        print(f"{'=' * 60}")
        print(f"Instruction: {task.assistant.instruction_message[:80]}...")

        result = run_single_task(task, i, client)
        execution_results.append(result)

        if result.success:
            print(f"Result: {result.action.action_type}")
            if result.action.action_type == "fill":
                print(f"Fields filled: {len(result.action.fill_responses)}")
            else:
                print(f"Reason: {result.action.reject_reason[:50]}...")
        else:
            print(f"Result: FAILED after {len(result.llm_calls)} attempts")

    print(f"\n{'=' * 60}")
    print("Evaluating results...")
    print("Privacy: 0 - 1, fraction of private info protected.")
    print("Task Completion: 0 - 1, fraction of required info filled.")
    print("Higher is better for both.")
    print(f"{'=' * 60}")

    evaluation_results: list[TaskEvaluationResult] = []
    for exec_result in execution_results:
        if exec_result.success:
            eval_result = evaluate_task(exec_result, judge_client)
            evaluation_results.append(eval_result)

            # Calculate raw counts for display
            privacy_protected = len(eval_result.privacy.protected_facts)
            privacy_total = privacy_protected + len(eval_result.privacy.leaked_facts)

            completion_filled = len(eval_result.task_completion.appeared_facts)
            completion_total = completion_filled + len(eval_result.task_completion.missing_facts)

            print(
                f"Task {exec_result.task_index}: "
                f"Privacy={eval_result.privacy.privacy_score:.2f} ({privacy_protected}/{privacy_total}), "
                f"Task Completion={eval_result.task_completion.completion_score:.2f} ({completion_filled}/{completion_total})"
            )

    privacy_scores = [e.privacy.privacy_score for e in evaluation_results]
    completion_scores = [e.task_completion.completion_score for e in evaluation_results]

    aggregate_privacy = sum(privacy_scores) / len(privacy_scores) if privacy_scores else 0.0
    aggregate_completion = (
        sum(completion_scores) / len(completion_scores) if completion_scores else 0.0
    )

    result = BenchmarkResult(
        agent_model=model_name,
        judge_model=judge_model,
        timestamp=datetime.now(),
        total_tasks=len(tasks),
        execution_results=execution_results,
        evaluation_results=evaluation_results,
        aggregate_privacy_score=aggregate_privacy,
        aggregate_completion_score=aggregate_completion,
    )

    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_path / f"form_filling_{model_name}_{timestamp_str}.json"

        with open(output_file, "w") as f:
            f.write(result.model_dump_json(indent=2))
        print(f"\nResults saved to: {output_file}")

    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"Model: {model_name}")
    print(f"Judge: {judge_model}")
    print(f"Total tasks: {len(tasks)}")
    print(f"Successful executions: {sum(1 for r in execution_results if r.success)}")
    print(f"Aggregate Privacy Score [0, 1]: {aggregate_privacy:.3f}")
    print(f"Aggregate Task Completion Score [0, 1]: {aggregate_completion:.3f}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Run form filling benchmark")
    parser.add_argument("--model", required=True, help="Model to evaluate (e.g., gpt-4o)")
    parser.add_argument("--data", required=True, help="Path to form tasks YAML file")
    parser.add_argument("--judge-model", default="gpt-4.1", help="Model for evaluation")
    parser.add_argument("--output-dir", default="outputs/form_filling", help="Output directory")

    args = parser.parse_args()

    load_dotenv()

    run_benchmark(
        data_path=args.data,
        model_name=args.model,
        judge_model=args.judge_model,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
