"""CLI for interviewer benchmark."""

import argparse
import asyncio

from dotenv import load_dotenv

from .runner import run_tasks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Interviewer benchmark")
    parser.add_argument(
        "--interviewer-model", required=True, help="Model for interviewer agent (e.g., gpt-4o)"
    )
    parser.add_argument(
        "--assistant-model", required=True, help="Model for assistant agent (e.g., gpt-4o)"
    )
    parser.add_argument("--data", required=True, help="Path to tasks.yaml file")
    parser.add_argument("--judge-model", default="gpt-4.1", help="Model for evaluation")
    parser.add_argument("--output-dir", default="outputs/interviewer", help="Output directory")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of tasks to run")
    parser.add_argument(
        "--mode",
        choices=["all", "tasks", "eval"],
        default="all",
        help="Run mode: 'all' (tasks + eval), 'tasks' (skip eval), 'eval' (load tasks and eval)",
    )
    parser.add_argument(
        "--task-results-path",
        help="Path to task_results.json file (required for eval mode)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=75,
        help="Number of tasks/evals to run in parallel (default: 75)",
    )
    parser.add_argument(
        "--max-concurrent-requests",
        type=int,
        default=100,
        help="Maximum concurrent API requests per client (default: 100)",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=50,
        help="Maximum conversation rounds per task (default: 50)",
    )

    return parser.parse_args()


def main():
    """Main runner for interviewer tasks."""
    args = parse_args()

    load_dotenv()

    # Validate arguments
    if args.mode == "eval" and not args.task_results_path:
        raise ValueError("--task-results-path is required when using --mode eval")

    asyncio.run(
        run_tasks(
            data_path=args.data,
            interviewer_model=args.interviewer_model,
            assistant_model=args.assistant_model,
            judge_model=args.judge_model,
            output_dir=args.output_dir,
            limit=args.limit,
            mode=args.mode,
            task_results_path=args.task_results_path,
            batch_size=args.batch_size,
            max_concurrent_requests=args.max_concurrent_requests,
            max_rounds=args.max_rounds,
        )
    )


if __name__ == "__main__":
    main()
