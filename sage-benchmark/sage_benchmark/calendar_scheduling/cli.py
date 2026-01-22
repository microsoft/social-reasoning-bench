import argparse
import asyncio
import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from pydantic_core import to_json

from .evaluator import evaluate_tasks, print_evaluation_summary, print_per_task_summary
from .loader import load_artifacts, load_calendar_tasks
from .model_client import ModelClient, ModelClientConfig
from .runner import run_tasks
from .types import CalendarTask

logger = logging.getLogger(__name__)


def default_output_filename(model_name: str) -> str:
    """Generate default output filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"outputs/calendar_scheduling/calendar_scheduling_{model_name}_{timestamp}.json"


def load_tasks_from_paths(paths: list[str | Path], limit: int | None = None) -> list[CalendarTask]:
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
    if limit is not None:
        tasks = tasks[:limit]
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

    # Default model options (can be overridden by agent-specific options)
    parser.add_argument(
        "--model",
        default="gpt-4.1",
        help="Default model for all agents (default: gpt-4.1)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Default API key for all agents (defaults to OPENAI_API_KEY env var)",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Default base URL for OpenAI-compatible API",
    )
    parser.add_argument(
        "--api-version",
        default=None,
        help="Default API version for all agents",
    )

    # Assistant agent options
    parser.add_argument(
        "--assistant-model",
        default=None,
        help="Model for assistant agent (overrides --model)",
    )
    parser.add_argument(
        "--assistant-base-url",
        default=None,
        help="Base URL for assistant agent's OpenAI-compatible API (overrides --base-url)",
    )
    parser.add_argument(
        "--assistant-api-key",
        default=None,
        help="API key for assistant agent (overrides --api-key)",
    )
    parser.add_argument(
        "--assistant-api-version",
        default=None,
        help="API version for assistant agent (overrides --api-version)",
    )

    # Requestor agent options
    parser.add_argument(
        "--requestor-model",
        default=None,
        help="Model for requestor agent (overrides --model)",
    )
    parser.add_argument(
        "--requestor-base-url",
        default=None,
        help="Base URL for requestor agent's OpenAI-compatible API (overrides --base-url)",
    )
    parser.add_argument(
        "--requestor-api-key",
        default=None,
        help="API key for requestor agent (overrides --api-key)",
    )
    parser.add_argument(
        "--requestor-api-version",
        default=None,
        help="API version for requestor agent (overrides --api-version)",
    )

    # Logging options
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Logging level (default: info)",
    )

    # Judge (evaluation) options
    parser.add_argument(
        "--judge-model",
        default=None,
        help="Model for LLM-as-judge evaluation (overrides --model)",
    )
    parser.add_argument(
        "--judge-base-url",
        default=None,
        help="Base URL for judge's OpenAI-compatible API (overrides --base-url)",
    )
    parser.add_argument(
        "--judge-api-key",
        default=None,
        help="API key for judge (overrides --api-key)",
    )
    parser.add_argument(
        "--judge-api-version",
        default=None,
        help="API version for judge (overrides --api-version)",
    )

    # Artifacts option
    parser.add_argument(
        "--artifacts",
        default=None,
        help="Path to artifacts JSON file to inject into assistant context",
    )

    # Task limiting option
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of tasks to load (default: None, loads all tasks)",
    )

    # Batch size for parallelization
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Number of tasks/evals to run in parallel (default: 50)",
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
    # Meeting should have been scheduled but wasn't
    missing_meetings = sum(
        1 for r in eval_results if r.task_satisfiable and not r.scheduled_meeting_found
    )
    # Meeting shouldn't have been scheduled but was
    unwanted_meetings = sum(
        1 for r in eval_results if not r.task_satisfiable and r.scheduled_meeting_found
    )

    print(f"\n{'=' * 40}")
    print("EVALUATION SUMMARY")
    print(f"{'=' * 40}")
    print(f"Total tasks:          {len(eval_results)}")
    print(f"Met expectations:     {completed}/{len(eval_results)} ({avg_completion:.1%})")
    print(f"  - Conflicts:        {conflicts}")
    print(f"  - Illegal moves:    {illegal_moves}")
    print(f"  - Missing meetings: {missing_meetings}")
    print(f"  - Unwanted meetings:{unwanted_meetings}")
    print(f"Avg leakage rate:     {avg_leakage:.1%}")
    print(f"{'=' * 40}")


async def run():
    args = parse_args()

    # Configure logging
    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
    )

    load_dotenv()

    # Resolve model names with fallback to defaults
    assistant_model = args.assistant_model or args.model
    requestor_model = args.requestor_model or args.model
    judge_model = args.judge_model or args.model

    assistant_client = ModelClient(
        config=ModelClientConfig(
            base_url=args.assistant_base_url or args.base_url,
            api_key=args.assistant_api_key or args.api_key,
            api_version=args.assistant_api_version or args.api_version,
        )
    )
    requestor_client = ModelClient(
        config=ModelClientConfig(
            base_url=args.requestor_base_url or args.base_url,
            api_key=args.requestor_api_key or args.api_key,
            api_version=args.requestor_api_version or args.api_version,
        )
    )
    judge_client = ModelClient(
        config=ModelClientConfig(
            base_url=args.judge_base_url or args.base_url,
            api_key=args.judge_api_key or args.api_key,
            api_version=args.judge_api_version or args.api_version,
        )
    )

    tasks = load_tasks_from_paths(args.paths, limit=args.limit)

    # Load artifacts if provided
    artifacts_by_task = None
    if args.artifacts:
        logger.info(f"Loading artifacts from {args.artifacts}...")
        artifacts_by_task = load_artifacts(args.artifacts)

    logger.info("Running %d task(s)...", len(tasks))
    execution_results = await run_tasks(
        tasks=tasks,
        assistant_model=assistant_model,
        assistant_client=assistant_client,
        requestor_model=requestor_model,
        requestor_client=requestor_client,
        max_rounds=args.max_rounds,
        batch_size=args.batch_size,
        artifacts_by_task=artifacts_by_task,
    )

    logger.info("Evaluating %d execution results...", len(execution_results))
    eval_results = await evaluate_tasks(
        execution_results=execution_results,
        model=judge_model,
        model_client=judge_client,
        batch_size=args.batch_size,
    )

    output_path = Path(args.output or default_output_filename(assistant_model))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(to_json(eval_results, indent=2))
    logger.info("Saved %d evaluation results to %s", len(eval_results), output_path)

    print_per_task_summary(eval_results)
    print_evaluation_summary(eval_results)


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
