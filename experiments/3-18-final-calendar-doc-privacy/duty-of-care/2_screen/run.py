"""Screen strategies and select the best one for double-booking attacks.

Runs each strategy on the screening tasks for N rounds.
Picks the strategy with the lowest sum of duty-of-care score (most harmful).

Usage:
    uv run python experiments/3-18-final-calendar-doc-privacy/duty-of-care/2_screen/run.py \
        --assistant-model phyagi/gpt-5.2

    # Quick test
    uv run python experiments/3-18-final-calendar-doc-privacy/duty-of-care/2_screen/run.py --screening-rounds 1
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

EXPERIMENT_DIR = Path("experiments/3-18-final-calendar-doc-privacy/duty-of-care")


def _model_slug(model: str) -> str:
    """Turn 'phyagi/gpt-5.2' into 'gpt-5.2', etc."""
    return model.split("/")[-1]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Screen double-booking strategies")
    p.add_argument("--assistant-model", default="phyagi/gpt-5.2")
    p.add_argument("--assistant-reasoning-effort", default=None)
    p.add_argument("--assistant-explicit-cot", action="store_true", default=False)
    p.add_argument("--requestor-model", default="gemini-3-flash-preview")
    p.add_argument("--requestor-reasoning-effort", default="medium")
    p.add_argument("--judge-model", default="phyagi/gpt-4.1")
    p.add_argument("--assistant-system-prompt", default="default")
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
        assistant_system_prompt=args.assistant_system_prompt,
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


def get_doc_score(eval_data: dict) -> float:
    """Get the average duty-of-care score from eval data. Lower = more harmful."""
    score = eval_data.get("summary", {}).get("fiduciary_avg_assistant_duty_of_care_score")
    return score if score is not None else 1.0


def count_conflicts(eval_data: dict) -> int:
    """Count tasks with has_conflicts=True."""
    return sum(1 for r in eval_data.get("results", []) if r.get("has_conflicts"))


def main() -> None:
    load_dotenv()
    args = parse_args()
    data_dir = Path(args.strategy_data_dir)

    # Discover strategies from directory
    strategy_files = sorted(data_dir.glob("strategy_*.yaml"))
    if not strategy_files:
        raise FileNotFoundError(f"No strategy files in {data_dir}")

    slug = _model_slug(args.assistant_model)
    prompt = args.assistant_system_prompt
    tag = f"{slug}_{prompt}" if prompt != "default" else slug
    print(f"Screening {len(strategy_files)} strategies x {args.screening_rounds} rounds")
    print(
        f"Assistant: {args.assistant_model} ({slug}) | Prompt: {prompt} | Requestor: {args.requestor_model}"
    )

    # Run each round
    for r in range(args.screening_rounds):
        print(f"\n--- Round {r} ---")
        out = Path(
            f"outputs/calendar_scheduling/3-18-final-calendar-doc-privacy/duty-of-care/screen_{tag}_r{r}"
        )
        configs = [make_config(str(sf), sf.stem, out, args) for sf in strategy_files]
        run_experiments(configs, args.batch_size)

    # Tally results: sum duty-of-care scores across rounds (lower = more harmful)
    results = {}
    for sf in strategy_files:
        name = sf.stem
        doc_sum, total, conflict_count = 0.0, 0, 0
        for r in range(args.screening_rounds):
            ev = read_eval(
                Path(
                    f"outputs/calendar_scheduling/3-18-final-calendar-doc-privacy/duty-of-care/screen_{tag}_r{r}"
                )
                / name
                / "eval.json"
            )
            if ev is None:
                continue
            total += 1
            doc_sum += get_doc_score(ev)
            conflict_count += count_conflicts(ev)
        results[name] = {
            "strategy": name,
            "doc_sum": doc_sum,
            "doc_avg": doc_sum / total if total else 1.0,
            "conflicts": conflict_count,
            "total_rounds": total,
        }

    # Select winner: lowest doc_sum (most harmful)
    best = min(results.values(), key=lambda s: (s["doc_avg"], s["strategy"]))
    winner = best["strategy"]
    print(
        f"\nWinner: {winner} (avg DoC: {best['doc_avg']:.2f}, conflicts: {best['conflicts']}/{best['total_rounds']})"
    )

    # Save
    out_dir = EXPERIMENT_DIR / "2_screen/results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"screening_results_{tag}.json").write_text(
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
    print(f"Saved results to {out_dir / f'screening_results_{tag}.json'}")


if __name__ == "__main__":
    main()
