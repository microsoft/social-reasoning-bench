"""CLI for form filling benchmark supporting one-shot, interactive, and GUI modes."""

import argparse
import asyncio

from dotenv import load_dotenv

from sage_benchmark.form_filling.runner import run_tasks
from sage_benchmark.shared.cli_utils import parse_reasoning_effort


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Form filling benchmark")

    # Execution mode
    parser.add_argument(
        "--execution-mode",
        type=str,
        choices=["one-shot", "interactive", "gui"],
        default="one-shot",
        help="Execution mode: 'one-shot' (structured output), 'interactive' (interview Q&A), or 'gui' (browser automation)",
    )

    # Model configuration - different depending on mode
    parser.add_argument(
        "--assistant-model",
        help="Model for form filling (one-shot/gui mode) or assistant agent (interactive mode)",
    )
    parser.add_argument(
        "--interviewer-model",
        help="Model for interviewer agent (interactive mode only)",
    )

    # Common arguments
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
        "--id",
        type=int,
        default=None,
        help="Run only the task at this index (0-based). Must be less than total number of tasks.",
    )
    parser.add_argument(
        "--run-mode",
        choices=["all", "tasks", "eval"],
        default="all",
        help="Run mode: 'all' (tasks + eval), 'tasks' (skip eval), 'eval' (load tasks and eval)",
    )
    parser.add_argument(
        "--task-results-path",
        help="Path to task_results.json file (required for eval run-mode)",
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

    # One-shot mode specific arguments
    parser.add_argument(
        "--prompt-type",
        type=str,
        default="base",
        choices=["base", "privacy_aware", "privacy_explained", "privacy_ci"],
        help='Type of prompt to use for the agent (default: "base")',
    )

    # Interactive mode specific arguments
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=50,
        help="Maximum conversation rounds per task in interactive mode (default: 50)",
    )
    parser.add_argument(
        "--interviewer-reasoning-effort",
        type=parse_reasoning_effort,
        default=None,
        help="Reasoning effort for interviewer agent (interactive mode): none/minimal/low/medium/high/xhigh/default, or integer budget tokens",
    )
    parser.add_argument(
        "--assistant-reasoning-effort",
        type=parse_reasoning_effort,
        default=None,
        help="Reasoning effort for assistant agent (interactive mode) or form filler (one-shot mode): none/minimal/low/medium/high/xhigh/default, or integer budget tokens",
    )
    parser.add_argument(
        "--judge-reasoning-effort",
        type=parse_reasoning_effort,
        default=None,
        help="Reasoning effort for judge: none/minimal/low/medium/high/xhigh/default, or integer budget tokens",
    )
    parser.add_argument(
        "--interviewer-type",
        type=str,
        default="base",
        choices=["base", "detail"],
        help="Type of interviewer prompt in interactive mode: 'base' or 'detail' (default: 'base')",
    )
    parser.add_argument(
        "--single-field-mode",
        action="store_true",
        help="If set, interviewer asks only one question per turn (interactive mode only)",
    )
    parser.add_argument(
        "--malicious-strategy",
        type=int,
        default=None,
        help="Use malicious interviewer with the n-th strategy (0-indexed) from strategies.yaml. "
        "When set, overrides --interviewer-type.",
    )
    parser.add_argument(
        "--assistant-temperature",
        type=float,
        default=None,
        help="Sampling temperature for assistant/form-filler generation",
    )

    # File system mode (orthogonal to execution mode)
    parser.add_argument(
        "--file-system",
        action="store_true",
        help="Enable file-system mode: agent uses search/read tools instead of receiving artifacts in context",
    )

    # GUI mode specific arguments
    parser.add_argument(
        "--http-port",
        type=int,
        default=8080,
        help="HTTP port for serving GUI forms (default: 8080)",
    )
    parser.add_argument(
        "--max-gui-steps",
        type=int,
        default=30,
        help="Maximum interaction steps per form in GUI mode (default: 30)",
    )
    parser.add_argument(
        "--restructure-model",
        type=str,
        default="trapi/msraif/shared/gpt-4.1",
        help="Model for restructuring flat HTML values to Pydantic schema in GUI mode (default: trapi/msraif/shared/gpt-4.1)",
    )

    return parser.parse_args()


def main():
    """Main runner for form filling tasks."""
    args = parse_args()

    load_dotenv()

    # Validate arguments based on execution mode
    if args.execution_mode == "one-shot":
        if not args.assistant_model:
            raise ValueError("--assistant-model is required for one-shot mode")
    elif args.execution_mode == "interactive":
        if not args.assistant_model:
            raise ValueError("--assistant-model is required for interactive mode")
        if not args.interviewer_model:
            raise ValueError("--interviewer-model is required for interactive mode")
    elif args.execution_mode == "gui":
        if not args.assistant_model:
            args.assistant_model = "microsoft/Fara-7B"

    if args.run_mode == "eval" and not args.task_results_path:
        raise ValueError("--task-results-path is required when using --run-mode eval")

    asyncio.run(
        run_tasks(
            data_path=args.data,
            execution_mode=args.execution_mode,
            model_name=args.assistant_model,
            interviewer_model=args.interviewer_model,
            judge_model=args.judge_model,
            base_url=args.base_url,
            output_dir=args.output_dir,
            limit=args.limit,
            task_id=args.id,
            run_mode=args.run_mode,
            task_results_path=args.task_results_path,
            batch_size=args.batch_size,
            max_concurrent_requests=args.max_concurrent_requests,
            prompt_type=args.prompt_type,
            interviewer_reasoning_effort=args.interviewer_reasoning_effort,
            assistant_reasoning_effort=args.assistant_reasoning_effort,
            judge_reasoning_effort=args.judge_reasoning_effort,
            max_rounds=args.max_rounds,
            interviewer_type=args.interviewer_type,
            single_field_mode=args.single_field_mode,
            malicious_strategy=args.malicious_strategy,
            http_port=args.http_port,
            max_steps=args.max_gui_steps,
            restructure_model=args.restructure_model,
            temperature=args.assistant_temperature,
            file_system=args.file_system,
        )
    )


if __name__ == "__main__":
    main()
