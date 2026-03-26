"""CLI for form filling benchmark (interactive mode)."""

import argparse
import asyncio

from dotenv import load_dotenv

from sage_benchmark.form_filling.runner import run_tasks
from sage_benchmark.shared.cli_utils import parse_reasoning_effort


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Form filling benchmark")

    # Model configuration
    parser.add_argument(
        "--assistant-model",
        required=True,
        help="Model for assistant agent (interactive mode)",
    )
    parser.add_argument(
        "--interviewer-model",
        required=True,
        help="Model for interviewer agent (interactive mode)",
    )
    parser.add_argument(
        "--interviewer-form-fill-model",
        default=None,
        help="Separate model for the form-filling step after the interview (defaults to --interviewer-model). "
        "Useful when the interviewer model doesn't support constrained decoding.",
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

    # Prompt type
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
        help="Reasoning effort for interviewer agent: none/minimal/low/medium/high/xhigh/default, or integer budget tokens",
    )
    parser.add_argument(
        "--assistant-reasoning-effort",
        type=parse_reasoning_effort,
        default=None,
        help="Reasoning effort for assistant agent: none/minimal/low/medium/high/xhigh/default, or integer budget tokens",
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
        help="If set, interviewer asks only one question per turn",
    )
    parser.add_argument(
        "--malicious-strategy",
        type=int,
        default=None,
        help="Use malicious interviewer with the n-th strategy (0-indexed) from strategies file. "
        "When set, overrides --interviewer-type.",
    )
    parser.add_argument(
        "--malicious-attack-type",
        choices=["privacy", "hallucination", "red_flags"],
        default="privacy",
        help="Type of malicious attack (only used with --malicious-strategy)",
    )
    parser.add_argument(
        "--malicious-strategies-file",
        type=str,
        default=None,
        help="Path to strategies YAML file for malicious mode. Required when --malicious-strategy is set.",
    )

    parser.add_argument(
        "--social-reasoning",
        action="store_true",
        help="Enable social reasoning for assistant agent (ToM-augmented)",
    )
    parser.add_argument(
        "--use-privacy-example",
        action="store_true",
        help="Append privacy/sensitive information examples to the social reasoning prompt (requires --social-reasoning)",
    )

    return parser.parse_args()


def main():
    """Main runner for form filling tasks."""
    args = parse_args()

    load_dotenv()

    if args.run_mode == "eval" and not args.task_results_path:
        raise ValueError("--task-results-path is required when using --run-mode eval")

    if args.malicious_strategy is not None and not args.malicious_strategies_file:
        raise ValueError(
            "--malicious-strategies-file is required when --malicious-strategy is set. "
            "Generate strategies first using: uv run --package sage-data-gen python -m "
            f"sage_data_gen.form_filling.malicious.whimsical.{args.malicious_attack_type} "
            "-m <model> -o <output.yaml>"
        )

    asyncio.run(
        run_tasks(
            data_path=args.data,
            model_name=args.assistant_model,
            interviewer_model=args.interviewer_model,
            interviewer_form_fill_model=args.interviewer_form_fill_model,
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
            malicious_attack_type=args.malicious_attack_type,
            malicious_strategies_file=args.malicious_strategies_file,
            social_reasoning=args.social_reasoning,
            use_privacy_example=args.use_privacy_example,
        )
    )


if __name__ == "__main__":
    main()
