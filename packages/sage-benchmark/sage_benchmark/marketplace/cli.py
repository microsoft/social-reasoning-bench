"""CLI for minimal marketplace simulation benchmark."""

import argparse
import asyncio
import json
from datetime import datetime
from pathlib import Path
from statistics import mean

from sage_llm import ModelClient

from .loader import load_tasks
from .runner import run_tasks
from .types import TaskExecutionResult


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
        "--output-dir",
        default="outputs/marketplace",
        help="Directory to write execution results",
    )
    return parser.parse_args()


def _compute_summary(results: list[TaskExecutionResult]) -> dict:
    deal_results = [
        r for r in results if r.outcome.deal_reached and r.outcome.deal_price is not None
    ]
    midpoint_abs_deltas: list[float] = []
    for r in results:
        if r.outcome.deal_reached and r.outcome.deal_price is not None:
            midpoint = (r.task.buyer.reservation_price + r.task.seller.reservation_price) / 2.0
            midpoint_abs_deltas.append(abs(r.outcome.deal_price - midpoint))

    return {
        "task_count": len(results),
        "deals_reached": len(deal_results),
        "deal_rate": (len(deal_results) / len(results)) if results else 0.0,
        # MVP fairness/duty-of-care proxy: closeness to midpoint of reservation prices.
        "avg_abs_midpoint_price_delta": mean(midpoint_abs_deltas) if midpoint_abs_deltas else None,
    }


def main() -> None:
    args = parse_args()
    loaded = load_tasks(args.data, limit=args.limit)
    tasks = loaded.all_tasks
    if not tasks:
        raise ValueError("No tasks loaded")

    buyer_model = args.buyer_model or args.model
    seller_model = args.seller_model or args.model
    if not buyer_model or not seller_model:
        raise ValueError("Requires --model or both --buyer-model and --seller-model")
    print(
        "Starting marketplace experiment: "
        f"tasks={len(tasks)} buyer_model={buyer_model} seller_model={seller_model} "
        f"max_steps_per_turn={args.max_steps_per_turn}"
    )
    buyer_client = ModelClient(base_url=args.buyer_base_url or args.base_url)
    seller_client = ModelClient(base_url=args.seller_base_url or args.base_url)

    def _print_task_done(r: TaskExecutionResult) -> None:
        print(
            f"Finished task {r.task.id}: deal={r.outcome.deal_reached} "
            f"price={r.outcome.deal_price} invalid_actions={r.invalid_actions}"
        )

    results = asyncio.run(
        run_tasks(
            tasks,
            buyer_model=buyer_model,
            seller_model=seller_model,
            buyer_client=buyer_client,
            seller_client=seller_client,
            max_steps_per_turn=args.max_steps_per_turn,
            on_task_complete=_print_task_done,
        )
    )

    run_dir = Path(args.output_dir) / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    out_path = run_dir / "executions.json"
    summary = _compute_summary(results)

    payload = {
        "task_count": len(results),
        "summary": summary,
        "results": [r.model_dump(mode="json") for r in results],
    }
    out_path.write_text(json.dumps(payload, indent=2))

    print("Marketplace experiment finished.")
    print(f"Loaded {len(tasks)} task(s)")
    print(f"Saved results to {out_path}")
    print(
        "Summary: "
        f"deal_rate={summary['deal_rate']:.1%} "
        f"avg_abs_midpoint_price_delta={summary['avg_abs_midpoint_price_delta']}"
    )
