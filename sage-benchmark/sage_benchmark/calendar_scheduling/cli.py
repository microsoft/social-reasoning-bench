import argparse
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic_core import to_json

from .evaluator import evaluate_tasks
from .loader import load_calendar_tasks
from .runner import run_tasks
from .types import CalendarTask


def default_output_filename(model_name: str) -> str:
    """Generate default output filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"outputs/calendar_scheduling/calendar_scheduling_{model_name}_{timestamp}.json"


def load_tasks_from_paths(paths: list[str | Path]) -> list[CalendarTask]:
    """Load tasks from YAML files or directories."""
    tasks: list[CalendarTask] = []
    for path in paths:
        path = Path(path)
        if path.is_dir():
            for yaml_file in path.glob("*.yaml"):
                tasks.extend(load_calendar_tasks(yaml_file))
            for yaml_file in path.glob("*.yml"):
                tasks.extend(load_calendar_tasks(yaml_file))
        else:
            tasks.extend(load_calendar_tasks(path))
    return tasks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calendar scheduling benchmark - runs tasks and evaluates results",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="YAML files or directories containing task definitions",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file for evaluation results (default: calendar_scheduling_MODELNAME_YYYYMMDD_HHMMSS.json)",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=20,
        help="Maximum conversation rounds per task (default: 20)",
    )
    # Assistant agent options
    parser.add_argument(
        "--assistant-model",
        default="gpt-4.1",
        help="Model for assistant agent (default: gpt-4.1)",
    )
    parser.add_argument(
        "--assistant-base-url",
        default=None,
        help="Base URL for assistant agent's OpenAI-compatible API",
    )
    parser.add_argument(
        "--assistant-api-key",
        default=None,
        help="API key for assistant agent (defaults to OPENAI_API_KEY env var)",
    )

    # Requestor agent options
    parser.add_argument(
        "--requestor-model",
        default="gpt-4.1",
        help="Model for requestor agent (default: gpt-4.1)",
    )
    parser.add_argument(
        "--requestor-base-url",
        default=None,
        help="Base URL for requestor agent's OpenAI-compatible API",
    )
    parser.add_argument(
        "--requestor-api-key",
        default=None,
        help="API key for requestor agent (defaults to OPENAI_API_KEY env var)",
    )

    # Judge (evaluation) options
    parser.add_argument(
        "--judge-model",
        default="gpt-4.1",
        help="Model for LLM-as-judge evaluation (default: gpt-4.1)",
    )
    parser.add_argument(
        "--judge-base-url",
        default=None,
        help="Base URL for judge's OpenAI-compatible API",
    )
    parser.add_argument(
        "--judge-api-key",
        default=None,
        help="API key for judge (defaults to OPENAI_API_KEY env var)",
    )

    return parser.parse_args()


def print_evaluation_summary(eval_results: list) -> None:
    """Print summary statistics for evaluation results."""
    if not eval_results:
        print("No results to summarize.")
        return

    completed = sum(1 for r in eval_results if r.met_expectations)
    avg_completion = completed / len(eval_results)
    avg_leakage = sum(r.leakage_rate for r in eval_results) / len(eval_results)

    # Count error types
    conflicts = sum(1 for r in eval_results if r.has_conflicts)
    illegal_moves = sum(1 for r in eval_results if r.illegal_moves)
    # Event should have been scheduled but wasn't
    missing_events = sum(
        1 for r in eval_results if r.task_satisfiable and not r.scheduled_event_found
    )
    # Event shouldn't have been scheduled but was
    unwanted_events = sum(
        1 for r in eval_results if not r.task_satisfiable and r.scheduled_event_found
    )

    print(f"\n{'=' * 40}")
    print("EVALUATION SUMMARY")
    print(f"{'=' * 40}")
    print(f"Total tasks:          {len(eval_results)}")
    print(f"Met expectations:     {completed}/{len(eval_results)} ({avg_completion:.1%})")
    print(f"  - Conflicts:        {conflicts}")
    print(f"  - Illegal moves:    {illegal_moves}")
    print(f"  - Missing events:   {missing_events}")
    print(f"  - Unwanted events:  {unwanted_events}")
    print(f"Avg leakage rate:     {avg_leakage:.1%}")
    print(f"{'=' * 40}")


def main():
    args = parse_args()

    load_dotenv()

    assistant_client = OpenAI(
        base_url=args.assistant_base_url,
        api_key=args.assistant_api_key,
    )
    requestor_client = OpenAI(
        base_url=args.requestor_base_url,
        api_key=args.requestor_api_key,
    )
    judge_client = OpenAI(
        base_url=args.judge_base_url,
        api_key=args.judge_api_key,
    )

    tasks = load_tasks_from_paths(args.paths)
    print(f"Running {len(tasks)} task(s)...")
    execution_results = run_tasks(
        tasks=tasks,
        assistant_model=args.assistant_model,
        assistant_client=assistant_client,
        requestor_model=args.requestor_model,
        requestor_client=requestor_client,
        max_rounds=args.max_rounds,
    )

    print(f"Evaluating {len(execution_results)} execution results...")
    eval_results = evaluate_tasks(
        execution_results=execution_results,
        model=args.judge_model,
        model_client=judge_client,
    )

    output_path = Path(args.output or default_output_filename(args.assistant_model))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(to_json(eval_results, indent=2))
    print(f"Saved {len(eval_results)} evaluation results to {output_path}")

    print_evaluation_summary(eval_results)


if __name__ == "__main__":
    main()
