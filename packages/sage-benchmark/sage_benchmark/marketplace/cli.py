"""CLI for minimal marketplace simulation benchmark."""

import argparse
import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path

from sage_llm import ModelClient

from sage_benchmark.shared.logging import create_benchmark_logger

from .loader import load_tasks
from .runner import run_and_evaluate_tasks
from .types import TaskExecutionResult

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal marketplace negotiation simulation")
    parser.add_argument(
        "--data",
        nargs="+",
        required=True,
        help="YAML file(s) or directories containing marketplace tasks",
    )
    parser.add_argument("--limit", type=int, default=None, help="Limit tasks to run")
    parser.add_argument(
        "--max-steps-per-turn",
        type=int,
        default=3,
        help="Maximum tool calls per agent turn (default: 3)",
    )
    parser.add_argument(
        "--model", default=None, help="Default model for buyer and seller (LLM mode)"
    )
    parser.add_argument("--buyer-model", default=None, help="Buyer model (overrides --model)")
    parser.add_argument("--seller-model", default=None, help="Seller model (overrides --model)")
    parser.add_argument(
        "--base-url",
        default=None,
        help="Default base URL for OpenAI-compatible API (LLM mode)",
    )
    parser.add_argument(
        "--buyer-base-url", default=None, help="Buyer base URL (overrides --base-url)"
    )
    parser.add_argument(
        "--seller-base-url", default=None, help="Seller base URL (overrides --base-url)"
    )
    parser.add_argument(
        "--judge-model",
        default=None,
        help="Model for privacy leakage judge (enables LLM-based leakage detection)",
    )
    parser.add_argument(
        "--judge-base-url",
        default=None,
        help="Base URL for privacy leakage judge API (defaults to --base-url)",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/marketplace",
        help="Directory to write execution results",
    )
    parser.add_argument(
        "--reasoning-effort",
        default=None,
        help="Reasoning effort for models (e.g. 'low', 'medium', 'high', or integer budget)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Number of tasks to run in parallel (default: 50)",
    )
    parser.add_argument(
        "--logger",
        default="progress",
        choices=["verbose", "progress", "quiet"],
        help="Logging style: verbose, progress (default, tqdm bar), quiet (minimal)",
    )
    return parser.parse_args()


def _compute_summary(results: list[TaskExecutionResult]) -> dict:
    deal_count = sum(1 for r in results if r.outcome.deal_reached)
    return {
        "task_count": len(results),
        "deals_reached": deal_count,
        "deal_rate": (deal_count / len(results)) if results else 0.0,
    }


async def _run_and_evaluate(args: argparse.Namespace) -> None:
    loaded = load_tasks(args.data, limit=args.limit)
    tasks = loaded.all_tasks
    if not tasks:
        raise ValueError("No tasks loaded")

    buyer_model = args.buyer_model or args.model
    seller_model = args.seller_model or args.model
    if not buyer_model or not seller_model:
        raise ValueError("Requires --model or both --buyer-model and --seller-model")

    benchmark_logger = create_benchmark_logger(args.logger)

    benchmark_logger.log_message(
        logging.INFO,
        "Starting marketplace experiment: "
        "tasks=%d buyer_model=%s seller_model=%s "
        "max_steps_per_turn=%d batch_size=%d",
        len(tasks),
        buyer_model,
        seller_model,
        args.max_steps_per_turn,
        args.batch_size,
    )

    reasoning_effort: str | int = "none"
    if args.reasoning_effort is not None:
        try:
            reasoning_effort = int(args.reasoning_effort)
        except ValueError:
            reasoning_effort = args.reasoning_effort

    buyer_client = ModelClient(
        base_url=args.buyer_base_url or args.base_url,
        reasoning_effort=reasoning_effort,
    )
    seller_client = ModelClient(
        base_url=args.seller_base_url or args.base_url,
        reasoning_effort=reasoning_effort,
    )

    # Set up judge client if --judge-model provided (enables LLM-based leakage evaluation)
    judge_model = args.judge_model
    judge_client = None
    if judge_model:
        judge_client = ModelClient(
            base_url=args.judge_base_url or args.base_url,
        )

    # Run execution + evaluation coupled together in a single TaskPoolExecutor
    # (no drain between phases — each task is executed then immediately evaluated)
    with benchmark_logger:
        paired_results = await run_and_evaluate_tasks(
            tasks,
            buyer_model=buyer_model,
            seller_model=seller_model,
            buyer_client=buyer_client,
            seller_client=seller_client,
            max_steps_per_turn=args.max_steps_per_turn,
            batch_size=args.batch_size,
            benchmark_logger=benchmark_logger,
            judge_model=judge_model,
            judge_client=judge_client,
        )

    results = [r for r, _ in paired_results]
    evaluations = [e for _, e in paired_results]

    run_dir = Path(args.output_dir) / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    out_path = run_dir / "results.json"
    summary = _compute_summary(results)

    payload = {
        "task_count": len(results),
        "summary": summary,
        "results": [
            {
                "execution": r.model_dump(mode="json"),
                "evaluation": e.model_dump(mode="json"),
            }
            for r, e in zip(results, evaluations)
        ],
    }
    out_path.write_text(json.dumps(payload, indent=2))

    print("Marketplace experiment finished.")
    print(f"Loaded {len(tasks)} task(s)")
    print(f"Saved results to {out_path}")
    print(f"Summary: deal_rate={summary['deal_rate']:.1%}")


def main() -> None:
    args = parse_args()
    asyncio.run(_run_and_evaluate(args))
