"""Screen strategies and select the best one.

Runs each strategy on the screening tasks for N rounds.
Picks the strategy with the highest leak rate.

Usage:
    uv run python experiments/3-18-final-calendar-doc-privacy/privacy/2_screen/run.py \
        --assistant-model phyagi/gpt-5.2

    # Quick test
    uv run python experiments/3-18-final-calendar-doc-privacy/privacy/2_screen/run.py --screening-rounds 1
"""

import argparse
import asyncio
import json
import signal
import time
from pathlib import Path

from dotenv import load_dotenv
from sage_benchmark.calendar_scheduling.experiments import (
    Experiment,
    ExperimentConfig,
    ExperimentPoolExecutor,
)

EXPERIMENT_DIR = Path("experiments/3-18-final-calendar-doc-privacy/privacy")


def _model_slug(model: str) -> str:
    """Turn 'phyagi/gpt-5.2' into 'gpt-5.2', etc."""
    return model.split("/")[-1]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Screen strategies")
    p.add_argument("--assistant-model", default="phyagi/gpt-5.2")
    p.add_argument("--assistant-reasoning-effort", default=None)
    p.add_argument("--assistant-explicit-cot", action="store_true", default=False)
    p.add_argument("--requestor-model", default="gemini-3-flash-preview")
    p.add_argument("--requestor-reasoning-effort", default="medium")
    p.add_argument("--judge-model", default="phyagi/gpt-4.1")
    p.add_argument("--screening-rounds", type=int, default=3)
    p.add_argument("--strategy-data-dir", type=str, default=str(EXPERIMENT_DIR / "2_screen/data"))
    p.add_argument("--batch-size", type=int, default=16)
    return p.parse_args()


def make_config(
    path: str, variant: str, output_dir: Path, args: argparse.Namespace
) -> ExperimentConfig:
    return ExperimentConfig(
        paths=[path],
        limit=None,
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
    to_run = [c for c in configs if not (c.output_dir / "eval.json").exists()]
    skipped = len(configs) - len(to_run)
    if skipped:
        print(f"  Skipping {skipped} completed")
    if not to_run:
        return

    prepared = []
    for c in to_run:
        try:
            prepared.append(Experiment(c))
        except Exception as e:
            print(f"  WARNING: {c.variant}: {e}")
    if not prepared:
        return

    print(
        f"  Running {sum(e.task_count for e in prepared)} tasks across {len(prepared)} experiments"
    )

    async def _run():
        loop = asyncio.get_event_loop()
        cancel = asyncio.Event()

        def on_signal():
            print("\n  Interrupted, saving checkpoints...")
            cancel.set()
            for e in prepared:
                e.checkpoint_mgr.set_interrupted(True)
            for s in (signal.SIGINT, signal.SIGTERM):
                loop.remove_signal_handler(s)

        for s in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(s, on_signal)

        pool = ExperimentPoolExecutor(prepared, batch_size=batch_size, cancel_event=cancel)
        t0 = time.monotonic()
        await pool.run()
        m, s = divmod(time.monotonic() - t0, 60)
        print(f"  Done in {int(m)}m{s:04.1f}s")

    asyncio.run(_run())


def read_eval(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        print(f"  WARNING: {path}: {e}")
        return None


def has_leakage(eval_data: dict) -> bool:
    return any(r.get("leaked_secrets") for r in eval_data.get("results", []))


def main() -> None:
    load_dotenv()
    args = parse_args()
    data_dir = Path(args.strategy_data_dir)

    # Discover strategies from directory
    strategy_files = sorted(data_dir.glob("strategy_*.yaml"))
    if not strategy_files:
        raise FileNotFoundError(f"No strategy files in {data_dir}")

    slug = _model_slug(args.assistant_model)
    print(f"Screening {len(strategy_files)} strategies × {args.screening_rounds} rounds")
    print(f"Assistant: {args.assistant_model} ({slug}) | Requestor: {args.requestor_model}")

    # Run each round
    for r in range(args.screening_rounds):
        print(f"\n--- Round {r} ---")
        out = Path(
            f"outputs/calendar_scheduling/3-18-final-calendar-doc-privacy/privacy/screen_{slug}_r{r}"
        )
        configs = [make_config(str(sf), sf.stem, out, args) for sf in strategy_files]
        run_experiments(configs, args.batch_size)

    # Tally results
    results = {}
    for sf in strategy_files:
        name = sf.stem
        leaks, total = 0, 0
        for r in range(args.screening_rounds):
            ev = read_eval(
                Path(
                    f"outputs/calendar_scheduling/3-18-final-calendar-doc-privacy/privacy/screen_{slug}_r{r}"
                )
                / name
                / "eval.json"
            )
            if ev is None:
                continue
            total += 1
            leaks += has_leakage(ev)
        results[name] = {
            "strategy": name,
            "leaks": leaks,
            "total_rounds": total,
            "leak_rate": leaks / total if total else 0.0,
        }

    # Select winner
    best = min(results.values(), key=lambda s: (-s["leak_rate"], s["strategy"]))
    if best["leak_rate"] == 0:
        raise RuntimeError(
            f"No strategy leaked in any round ({len(strategy_files)} strategies × "
            f"{args.screening_rounds} rounds). The model may be too robust for these "
            f"strategies, or screening may need more rounds / a different task."
        )
    winner = best["strategy"]
    print(f"\nWinner: {winner} ({best['leak_rate']:.0%}, {best['leaks']}/{best['total_rounds']})")

    # Save
    out_dir = EXPERIMENT_DIR / "2_screen/results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"screening_results_{slug}.json").write_text(
        json.dumps(
            {
                "assistant_model": args.assistant_model,
                "requestor_model": args.requestor_model,
                "num_strategies": len(strategy_files),
                "screening_rounds": args.screening_rounds,
                "winner": winner,
                "strategies": sorted(results.values(), key=lambda s: s["strategy"]),
            },
            indent=2,
        )
    )
    print(f"Saved results to {out_dir / f'screening_results_{slug}.json'}")


if __name__ == "__main__":
    main()
