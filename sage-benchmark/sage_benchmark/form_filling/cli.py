import argparse
import asyncio

from dotenv import load_dotenv

from sage_benchmark.form_filling.runner import run_tasks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Form filling benchmark")
    parser.add_argument("--model", required=True, help="Model to evaluate (e.g., gpt-4o)")
    parser.add_argument(
        "--data", required=True, help="Path to task directory (e.g., data/form-filling/tasks)"
    )
    parser.add_argument("--judge-model", default="gpt-4.1", help="Model for evaluation")
    parser.add_argument(
        "--base-url",
        type=str,
        default=None,
        help="Base URL for OpenAI-compatible API (e.g., http://localhost:8001/v1 for vLLM)",
    )
    parser.add_argument("--output-dir", default="outputs/form_filling", help="Output directory")
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
    # Note: if you increase this beyond 256, might hit OS limits on open file descriptors
    parser.add_argument(
        "--max-concurrent-requests",
        type=int,
        default=100,
        help="Maximum concurrent API requests per client (default: 100)",
    )
    parser.add_argument(
        "--prompt-type",
        type=str,
        default="base",
        choices=["base", "privacy_aware", "privacy_explained"],
        help='Type of prompt to use for the agent (default: "base")',
    )

    return parser.parse_args()


def main():
    """Main runner for form filling tasks."""
    args = parse_args()

    load_dotenv()

    # Validate arguments
    if args.mode == "eval" and not args.task_results_path:
        raise ValueError("--task-results-path is required when using --mode eval")

    asyncio.run(
        run_tasks(
            data_path=args.data,
            model_name=args.model,
            judge_model=args.judge_model,
            base_url=args.base_url,
            output_dir=args.output_dir,
            limit=args.limit,
            mode=args.mode,
            task_results_path=args.task_results_path,
            batch_size=args.batch_size,
            max_concurrent_requests=args.max_concurrent_requests,
            prompt_type=args.prompt_type,
        )
    )


if __name__ == "__main__":
    main()
