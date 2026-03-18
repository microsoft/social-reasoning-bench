"""Strategy Selection Pipeline: Screen → Select → Generalization Test.

Stage 1 (Screen): Run each strategy on 1 task, repeat N rounds to find
    the strategy with the highest leak rate.
Stage 2 (Generalization): Run the winning strategy on ALL tasks (no limit)
    to test if it generalizes across different task contexts.

Usage:
    uv run python experiments/3-5-strategy-selection-pipeline/run_pipeline.py \
        --assistant-model phyagi/gpt-5.2

Quick smoke test:
    uv run python experiments/3-5-strategy-selection-pipeline/run_pipeline.py \
        --screening-rounds 1 --num-strategies 5
"""

import argparse
import asyncio
import json
import signal
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from sage_benchmark.calendar_scheduling.experiments import (
    Experiment,
    ExperimentConfig,
    ExperimentPoolExecutor,
)

EXPERIMENT_DIR = Path("experiments/3-5-strategy-selection-pipeline")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Strategy Selection Pipeline")
    parser.add_argument("--assistant-model", default="phyagi/gpt-5.2")
    parser.add_argument("--assistant-reasoning-effort", default="medium")
    parser.add_argument("--assistant-explicit-cot", action="store_true", default=False)
    parser.add_argument("--requestor-model", default="gemini-3-flash-preview")
    parser.add_argument("--requestor-reasoning-effort", default="medium")
    parser.add_argument("--judge-model", default="phyagi/gpt-4.1")
    parser.add_argument("--screening-rounds", type=int, default=3)
    parser.add_argument(
        "--strategy-data-dir",
        type=str,
        default="experiments/3-5-strategy-selection-pipeline/data/privacy",
    )
    parser.add_argument("--num-strategies", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--skip-screen", action="store_true")
    parser.add_argument("--skip-generalization", action="store_true")
    parser.add_argument("--force-strategy", type=int, default=None)
    return parser.parse_args()


def make_config(
    paths: list[str],
    variant: str,
    output_dir: Path,
    args: argparse.Namespace,
    limit: int | None = 1,
) -> ExperimentConfig:
    """Create an ExperimentConfig with the shared model settings."""
    return ExperimentConfig(
        paths=paths,
        limit=limit,
        max_rounds=10,
        batch_size=args.batch_size,
        assistant_model=args.assistant_model,
        assistant_system_prompt="privacy-ci",
        expose_preferences=False,
        assistant_explicit_cot=args.assistant_explicit_cot,
        assistant_reasoning_effort=args.assistant_reasoning_effort,
        requestor_model=args.requestor_model,
        requestor_explicit_cot=False,
        requestor_reasoning_effort=args.requestor_reasoning_effort,
        judge_model=args.judge_model,
        judge_votes=3,
        output_dir=output_dir / variant,
        variant=variant,
    )


def run_experiments(configs: list[ExperimentConfig], batch_size: int) -> None:
    """Prepare and run a list of ExperimentConfigs via the pool executor."""
    # Skip already-completed experiments
    to_run = []
    skipped = 0
    for config in configs:
        eval_path = config.output_dir / "eval.json"
        if eval_path.exists():
            skipped += 1
            continue
        to_run.append(config)

    if skipped:
        print(f"  Skipping {skipped} already-completed experiments")
    if not to_run:
        print("  All experiments already completed")
        return

    # Prepare experiments
    prepared = []
    for config in to_run:
        try:
            exp = Experiment(config)
            prepared.append(exp)
        except Exception as e:
            print(f"  WARNING: Failed to prepare {config.variant}: {e}")

    if not prepared:
        print("  No experiments could be prepared")
        return

    total_tasks = sum(exp.task_count for exp in prepared)
    print(
        f"  Running {total_tasks} tasks across {len(prepared)} experiments (batch_size={batch_size})"
    )

    # Run with pool executor
    async def _run():
        loop = asyncio.get_event_loop()
        cancel_event = asyncio.Event()

        def signal_handler():
            print("\n  Interrupt received, saving checkpoints...")
            cancel_event.set()
            for exp in prepared:
                exp.checkpoint_mgr.set_interrupted(True)
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.remove_signal_handler(sig)

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, signal_handler)

        pool = ExperimentPoolExecutor(
            prepared,
            batch_size=batch_size,
            cancel_event=cancel_event,
        )
        start = time.monotonic()
        await pool.run()
        elapsed = time.monotonic() - start
        mins, secs = divmod(elapsed, 60)
        print(f"  Completed in {int(mins)}m{secs:04.1f}s")

    asyncio.run(_run())


def read_eval_json(eval_path: Path) -> dict | None:
    """Read an eval.json file, returning None if missing or invalid."""
    if not eval_path.exists():
        return None
    try:
        with open(eval_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  WARNING: Failed to read {eval_path}: {e}")
        return None


def has_leakage(eval_data: dict) -> bool:
    """Check if any task in the eval has leaked secrets."""
    for result in eval_data.get("results", []):
        if len(result.get("leaked_secrets", [])) > 0:
            return True
    return False


def stage1_screen(args: argparse.Namespace) -> dict[int, dict]:
    """Stage 1: Screen all strategies across multiple rounds."""
    print(f"\n{'=' * 60}")
    print(f"STAGE 1: Screening {args.num_strategies} strategies x {args.screening_rounds} rounds")
    print(f"{'=' * 60}")

    strategy_data_dir = Path(args.strategy_data_dir)

    # Run each round separately (separate pool invocations avoid dedup)
    for r in range(args.screening_rounds):
        print(f"\n--- Round {r} ---")
        output_dir = EXPERIMENT_DIR / f"outputs_screen_r{r}"
        configs = []
        for i in range(args.num_strategies):
            strategy_file = strategy_data_dir / f"strategy_{i}.yaml"
            if not strategy_file.exists():
                continue
            configs.append(
                make_config(
                    paths=[str(strategy_file)],
                    variant=f"strategy_{i:03d}",
                    output_dir=output_dir,
                    args=args,
                )
            )
        run_experiments(configs, args.batch_size)

    # Analyze results
    print(f"\n--- Analyzing screening results ---")
    strategy_results: dict[int, dict] = {}

    for i in range(args.num_strategies):
        leaks = 0
        total = 0
        for r in range(args.screening_rounds):
            eval_path = EXPERIMENT_DIR / f"outputs_screen_r{r}" / f"strategy_{i:03d}" / "eval.json"
            eval_data = read_eval_json(eval_path)
            if eval_data is None:
                print(f"  WARNING: Missing eval.json for strategy {i}, round {r}")
                continue
            total += 1
            if has_leakage(eval_data):
                leaks += 1

        strategy_results[i] = {
            "strategy_index": i,
            "leaks": leaks,
            "total_rounds": total,
            "leak_rate": leaks / total if total > 0 else 0.0,
        }

    # Save screening results
    results_dir = EXPERIMENT_DIR / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    screening_output = {
        "num_strategies": args.num_strategies,
        "screening_rounds": args.screening_rounds,
        "strategies": [strategy_results[i] for i in sorted(strategy_results.keys())],
    }
    screening_path = results_dir / "screening_results.json"
    with open(screening_path, "w") as f:
        json.dump(screening_output, f, indent=2)
    print(f"  Saved screening results to {screening_path}")

    return strategy_results


def select_winner(
    strategy_results: dict[int, dict],
    force_strategy: int | None = None,
) -> int:
    """Select the winning strategy (highest leak rate, tiebreak: lowest index)."""
    if force_strategy is not None:
        print(f"  Using forced strategy: {force_strategy}")
        return force_strategy

    best = min(
        strategy_results.values(),
        key=lambda s: (-s["leak_rate"], s["strategy_index"]),
    )
    winner = best["strategy_index"]
    print(
        f"  Selected strategy {winner} (leak rate: {best['leak_rate']:.1%}, "
        f"{best['leaks']}/{best['total_rounds']} rounds)"
    )
    return winner


def stage2_generalization(winner: int, args: argparse.Namespace) -> dict:
    """Stage 2: Run winning strategy on all tasks to test generalizability."""
    strategy_file = Path(args.strategy_data_dir) / f"strategy_{winner}.yaml"

    print(f"\n{'=' * 60}")
    print(f"STAGE 2: Generalization test for strategy {winner} on all tasks")
    print(f"  Strategy file: {strategy_file}")
    print(f"{'=' * 60}")

    output_dir = EXPERIMENT_DIR / "outputs_generalization"
    config = make_config(
        paths=[str(strategy_file)],
        variant=f"strategy_{winner:03d}",
        output_dir=output_dir,
        args=args,
        limit=None,  # run ALL tasks
    )
    run_experiments([config], args.batch_size)

    # Analyze results
    print(f"\n--- Analyzing generalization results ---")
    eval_path = output_dir / f"strategy_{winner:03d}" / "eval.json"
    eval_data = read_eval_json(eval_path)
    if eval_data is None:
        print("  WARNING: Missing eval.json")
        return {"strategy_index": winner, "status": "missing"}

    results = eval_data.get("results", [])
    total_tasks = len(results)
    tasks_with_leakage = sum(1 for r in results if len(r.get("leaked_secrets", [])) > 0)
    task_details = []
    for r in results:
        leaked = len(r.get("leaked_secrets", [])) > 0
        task_details.append(
            {
                "task_id": r.get("execution", {}).get("task", {}).get("id"),
                "leaked": leaked,
                "leakage_rate": r.get("leakage_rate", 0.0),
            }
        )

    summary = eval_data.get("summary", {})
    return {
        "strategy_index": winner,
        "total_tasks": total_tasks,
        "tasks_with_leakage": tasks_with_leakage,
        "leak_rate": tasks_with_leakage / total_tasks if total_tasks > 0 else 0.0,
        "avg_leakage_rate": summary.get("privacy_avg_leakage_rate", 0.0),
        "tasks": task_details,
    }


def save_final_results(
    winner: int,
    strategy_results: dict[int, dict] | None,
    generalization_results: dict | None,
    args: argparse.Namespace,
) -> None:
    """Save final pipeline results."""
    results_dir = EXPERIMENT_DIR / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Save selected strategy metadata
    selected = {
        "strategy_index": winner,
        "source_file": f"strategy_{winner}.yaml",
        "strategy_data_dir": args.strategy_data_dir,
        "screening_leak_rate": (
            strategy_results[winner]["leak_rate"]
            if strategy_results and winner in strategy_results
            else None
        ),
    }
    selected_path = results_dir / "selected_strategy.yaml"
    with open(selected_path, "w") as f:
        for k, v in selected.items():
            f.write(f"{k}: {v}\n")
    print(f"  Saved selected strategy to {selected_path}")

    # Save pipeline summary
    summary = {
        "assistant_model": args.assistant_model,
        "assistant_reasoning_effort": args.assistant_reasoning_effort,
        "requestor_model": args.requestor_model,
        "judge_model": args.judge_model,
        "strategy_data_dir": args.strategy_data_dir,
        "num_strategies": args.num_strategies,
        "screening_rounds": args.screening_rounds,
        "selected_strategy": winner,
        "screening": (
            strategy_results[winner] if strategy_results and winner in strategy_results else None
        ),
        "generalization": generalization_results,
    }
    summary_path = results_dir / "pipeline_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved pipeline summary to {summary_path}")


def load_screening_results(args: argparse.Namespace) -> dict[int, dict]:
    """Load screening results from a previous run."""
    screening_path = EXPERIMENT_DIR / "results" / "screening_results.json"
    with open(screening_path) as f:
        data = json.load(f)
    return {s["strategy_index"]: s for s in data["strategies"]}


def main() -> None:
    load_dotenv()
    args = parse_args()

    print("Strategy Selection Pipeline")
    print(f"  Assistant: {args.assistant_model} (reasoning: {args.assistant_reasoning_effort})")
    print(f"  Requestor: {args.requestor_model}")
    print(f"  Judge: {args.judge_model}")
    print(f"  Strategy data: {args.strategy_data_dir}")

    strategy_results = None
    winner = args.force_strategy

    # Stage 1: Screen
    if not args.skip_screen:
        strategy_results = stage1_screen(args)
        winner = select_winner(strategy_results, args.force_strategy)
    elif args.force_strategy is None:
        print("\n--- Loading previous screening results ---")
        strategy_results = load_screening_results(args)
        winner = select_winner(strategy_results, args.force_strategy)

    if winner is None:
        print("ERROR: No strategy selected. Run screening or use --force-strategy.")
        sys.exit(1)

    # Stage 2: Generalization test
    generalization_results = None
    if not args.skip_generalization:
        generalization_results = stage2_generalization(winner, args)

    # Save final results
    save_final_results(winner, strategy_results, generalization_results, args)

    # Print summary
    print(f"\n{'=' * 60}")
    print("PIPELINE COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Selected strategy: {winner}")
    if strategy_results and winner in strategy_results:
        sr = strategy_results[winner]
        print(f"  Screening leak rate: {sr['leak_rate']:.1%} ({sr['leaks']}/{sr['total_rounds']})")
    if generalization_results and "total_tasks" in generalization_results:
        gr = generalization_results
        print(
            f"  Generalization: {gr['tasks_with_leakage']}/{gr['total_tasks']} tasks leaked "
            f"({gr['leak_rate']:.1%})"
        )


if __name__ == "__main__":
    main()
