#!/usr/bin/env python3
"""Form-Filling Adversarial Strategy Selection Pipeline.

Three-stage pipeline:
  Stage 1 (Generate): Generate N strategies per attack type using WhimsyGen
  Stage 2 (Screen):   Run each strategy on a small task subset to find the most effective
  Stage 3 (Full Run): Run winning strategies across target assistant models on all tasks

Usage:
    # Full pipeline
    uv run python scripts/run_form_filling_strategy_pipeline.py

    # Dry run (print commands only)
    uv run python scripts/run_form_filling_strategy_pipeline.py --dry-run

    # Quick smoke test
    uv run python scripts/run_form_filling_strategy_pipeline.py \
        --num-strategies 3 --screening-limit 2 --skip-full-run

    # Skip generation, re-screen with existing strategies
    uv run python scripts/run_form_filling_strategy_pipeline.py --skip-generate

    # Skip to full run with forced strategy winners
    uv run python scripts/run_form_filling_strategy_pipeline.py \
        --skip-generate --skip-screen --force-strategy "privacy:3,hallucination:7,red_flags:12"
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

# Map attack type -> module name for strategy generation
ATTACK_TYPE_MODULES = {
    "privacy": "sage_data_gen.form_filling.malicious.whimsical.privacy",
    "hallucination": "sage_data_gen.form_filling.malicious.whimsical.hallucination",
    "red_flags": "sage_data_gen.form_filling.malicious.whimsical.red_flags",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Form-Filling Adversarial Strategy Selection Pipeline"
    )

    # Stage control
    parser.add_argument("--skip-generate", action="store_true", help="Skip strategy generation")
    parser.add_argument("--skip-screen", action="store_true", help="Skip screening")
    parser.add_argument("--skip-full-run", action="store_true", help="Skip full run")

    # Strategy generation
    parser.add_argument("--num-strategies", type=int, default=50)
    parser.add_argument("--strategy-gen-model", default="gemini-2.5-flash")
    parser.add_argument(
        "--seeds-dir", default="seeds/", help="Directory with WhimsyGen seed YAML files"
    )
    parser.add_argument(
        "--attack-types",
        nargs="+",
        default=["privacy", "hallucination", "red_flags"],
        choices=["privacy", "hallucination", "red_flags"],
    )

    # Screening
    parser.add_argument("--screening-model", default="phyagi/gpt-5.2")
    parser.add_argument("--screening-limit", type=int, default=10)

    # Full run
    parser.add_argument("--assistant-models", nargs="+", default=["phyagi/gpt-5.2"])
    parser.add_argument(
        "--prompt-type",
        default="base",
        choices=["base", "privacy_aware", "privacy_explained", "privacy_ci", "social_reasoning"],
    )

    # Shared model config
    parser.add_argument("--interviewer-model", default="gemini-3-flash-preview")
    parser.add_argument("--judge-model", default="phyagi/gpt-5.1")
    parser.add_argument("--data-dir", default="data/form-filling/tasks/")
    parser.add_argument("--output-dir", default="outputs/strategy_pipeline")

    # Overrides
    parser.add_argument(
        "--force-strategy",
        type=str,
        default=None,
        help='Override winners, e.g. "privacy:3,hallucination:7,red_flags:12"',
    )
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")

    return parser.parse_args()


def load_strategies(path: Path) -> list[str]:
    """Load strategies from a YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("strategies", [])


def find_latest_summary(output_dir: Path) -> Path | None:
    """Find the most recent summary.json in timestamped run subdirectories."""
    summaries = sorted(
        output_dir.glob("run_*/summary.json"),
        key=lambda p: p.stat().st_mtime,
    )
    return summaries[-1] if summaries else None


def run_cmd(cmd: list[str], dry_run: bool = False) -> int:
    """Run a subprocess command, returning the exit code."""
    cmd_str = " ".join(cmd)
    if dry_run:
        print(f"  [DRY RUN] {cmd_str}\n")
        return 0
    print(f"  Running: {cmd_str}\n")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"  WARNING: Command exited with code {result.returncode}")
    return result.returncode


def extract_metric(summary_path: Path, attack_type: str) -> float:
    """Extract the attacker-success metric from a summary.json (higher = more effective)."""
    try:
        with open(summary_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"  WARNING: Failed to read {summary_path}: {e}")
        return 0.0

    summary = data.get("summary", {})
    evaluated = summary.get("evaluated_forms", 0)

    if attack_type == "privacy":
        if evaluated == 0:
            return 0.0
        return summary.get("conversation_leakage_count", 0) / evaluated

    if attack_type == "hallucination":
        return 1.0 - summary.get("avg_accuracy", 1.0)

    if attack_type == "red_flags":
        doc_score = summary.get("avg_duty_of_care_score")
        if doc_score is None:
            return 0.0
        return 1.0 - doc_score

    return 0.0


# ── Stage 1: Generate ──────────────────────────────────────────────


def stage1_generate(args: argparse.Namespace) -> None:
    """Generate strategies for each attack type using WhimsyGen."""
    print(f"\n{'=' * 60}")
    print(f"STAGE 1: Generating {args.num_strategies} strategies per attack type")
    print(f"{'=' * 60}")

    base = Path(args.output_dir)
    base.mkdir(parents=True, exist_ok=True)

    for attack_type in args.attack_types:
        strategies_file = base / f"strategies_{attack_type}.yaml"

        # Skip if enough strategies already exist
        if strategies_file.exists():
            existing = load_strategies(strategies_file)
            if len(existing) >= args.num_strategies:
                print(f"  [{attack_type}] Skipping: {len(existing)} strategies already exist")
                continue

        module = ATTACK_TYPE_MODULES[attack_type]
        cmd = [
            "uv",
            "run",
            "--package",
            "sage-data-gen",
            "python",
            "-m",
            module,
            "-m",
            args.strategy_gen_model,
            "-n",
            str(args.num_strategies),
            "-o",
            str(strategies_file),
            "--seeds-dir",
            args.seeds_dir,
        ]
        print(f"\n  [{attack_type}] Generating strategies...")
        run_cmd(cmd, args.dry_run)

        # Verify
        if not args.dry_run and strategies_file.exists():
            count = len(load_strategies(strategies_file))
            print(f"  [{attack_type}] Generated {count} strategies -> {strategies_file}")


# ── Stage 2: Screen ────────────────────────────────────────────────


def stage2_screen(args: argparse.Namespace) -> dict[str, dict]:
    """Screen each strategy on a small task subset and select winners."""
    print(f"\n{'=' * 60}")
    print(f"STAGE 2: Screening strategies (limit={args.screening_limit} tasks each)")
    print(f"{'=' * 60}")

    base = Path(args.output_dir)
    all_results: dict[str, dict] = {}

    for attack_type in args.attack_types:
        strategies_file = base / f"strategies_{attack_type}.yaml"
        if not strategies_file.exists() and not args.dry_run:
            print(f"  [{attack_type}] ERROR: strategies file not found: {strategies_file}")
            continue

        num_strategies = args.num_strategies
        if not args.dry_run:
            strategies = load_strategies(strategies_file)
            num_strategies = len(strategies)
            print(f"\n  [{attack_type}] Screening {num_strategies} strategies...")

        scores: list[dict] = []

        for i in range(num_strategies):
            screen_dir = base / "screen" / attack_type / f"strategy_{i:03d}"

            # Skip if already has results
            existing_summary = find_latest_summary(screen_dir)
            if existing_summary is not None:
                score = extract_metric(existing_summary, attack_type)
                scores.append({"index": i, "score": score})
                print(f"    strategy_{i:03d}: {score:.3f} (cached)")
                continue

            cmd = [
                "uv",
                "run",
                "sagebench",
                "forms",
                "--data",
                args.data_dir,
                "--execution-mode",
                "interactive",
                "--assistant-model",
                args.screening_model,
                "--interviewer-model",
                args.interviewer_model,
                "--malicious-strategy",
                str(i),
                "--malicious-attack-type",
                attack_type,
                "--malicious-strategies-file",
                str(strategies_file),
                "--output-dir",
                str(screen_dir),
                "--limit",
                str(args.screening_limit),
                "--judge-model",
                args.judge_model,
                "--prompt-type",
                args.prompt_type,
            ]
            run_cmd(cmd, args.dry_run)

            if args.dry_run:
                scores.append({"index": i, "score": 0.0})
                continue

            # Read result
            summary_path = find_latest_summary(screen_dir)
            if summary_path is None:
                print(f"    strategy_{i:03d}: FAILED (no summary.json)")
                scores.append({"index": i, "score": 0.0})
                continue

            score = extract_metric(summary_path, attack_type)
            scores.append({"index": i, "score": score})
            print(f"    strategy_{i:03d}: {score:.3f}")

        # Select winner (highest score, tiebreak: lowest index)
        scores.sort(key=lambda s: (-s["score"], s["index"]))
        winner = scores[0] if scores else {"index": 0, "score": 0.0}

        all_results[attack_type] = {
            "winner_index": winner["index"],
            "winner_score": winner["score"],
            "all_scores": scores,
        }
        print(
            f"\n  [{attack_type}] Winner: strategy_{winner['index']:03d} (score={winner['score']:.3f})"
        )

    # Save screening results
    results_path = base / "screening_results.json"
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n  Saved screening results to {results_path}")

    return all_results


def load_screening_results(args: argparse.Namespace) -> dict[str, dict]:
    """Load screening results from a previous run."""
    results_path = Path(args.output_dir) / "screening_results.json"
    with open(results_path) as f:
        return json.load(f)


# ── Stage 3: Full Run ──────────────────────────────────────────────


def stage3_full_run(args: argparse.Namespace, winners: dict[str, int]) -> None:
    """Run winning strategies across all target models on all tasks."""
    print(f"\n{'=' * 60}")
    print(f"STAGE 3: Full run with winning strategies")
    print(f"  Models: {args.assistant_models}")
    print(f"  Winners: {winners}")
    print(f"{'=' * 60}")

    base = Path(args.output_dir)

    for attack_type in args.attack_types:
        if attack_type not in winners:
            print(f"  [{attack_type}] No winner found, skipping")
            continue

        winner_idx = winners[attack_type]
        strategies_file = base / f"strategies_{attack_type}.yaml"

        for model in args.assistant_models:
            model_norm = model.replace("/", "_").replace(":", "_")
            full_dir = base / "full" / attack_type / model_norm

            # Skip if results exist
            existing_summary = find_latest_summary(full_dir)
            if existing_summary is not None:
                print(f"  [{attack_type}/{model}] Skipping: results exist")
                continue

            print(f"\n  [{attack_type}/{model}] Running strategy_{winner_idx:03d}...")
            cmd = [
                "uv",
                "run",
                "sagebench",
                "forms",
                "--data",
                args.data_dir,
                "--execution-mode",
                "interactive",
                "--assistant-model",
                model,
                "--interviewer-model",
                args.interviewer_model,
                "--malicious-strategy",
                str(winner_idx),
                "--malicious-attack-type",
                attack_type,
                "--malicious-strategies-file",
                str(strategies_file),
                "--output-dir",
                str(full_dir),
                "--judge-model",
                args.judge_model,
                "--prompt-type",
                args.prompt_type,
            ]
            run_cmd(cmd, args.dry_run)


# ── Main ───────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()
    base = Path(args.output_dir)

    print("Form-Filling Strategy Selection Pipeline")
    print(f"  Output dir: {args.output_dir}")
    print(f"  Attack types: {args.attack_types}")
    print(f"  Strategies per type: {args.num_strategies}")
    print(f"  Screening model: {args.screening_model}")
    print(f"  Interviewer: {args.interviewer_model}")
    print(f"  Judge: {args.judge_model}")

    # Stage 1: Generate
    if not args.skip_generate:
        stage1_generate(args)
    else:
        print("\n  Skipping Stage 1 (generate)")

    # Stage 2: Screen
    screening_results = None
    if not args.skip_screen:
        screening_results = stage2_screen(args)
    else:
        print("\n  Skipping Stage 2 (screen)")

    # Determine winners
    winners: dict[str, int] = {}
    if screening_results:
        for attack_type, result in screening_results.items():
            winners[attack_type] = result["winner_index"]
    elif (base / "screening_results.json").exists():
        print("  Loading previous screening results...")
        prev = load_screening_results(args)
        for attack_type, result in prev.items():
            winners[attack_type] = result["winner_index"]

    # Apply --force-strategy overrides
    if args.force_strategy:
        for spec in args.force_strategy.split(","):
            attack_type, idx = spec.split(":")
            attack_type = attack_type.strip()
            winners[attack_type] = int(idx.strip())
        print(f"  Forced winners: {winners}")

    if not winners and not args.skip_full_run:
        print("ERROR: No winners determined. Run screening or use --force-strategy.")
        sys.exit(1)

    # Stage 3: Full run
    if not args.skip_full_run:
        stage3_full_run(args, winners)
    else:
        print("\n  Skipping Stage 3 (full run)")

    # Save pipeline summary
    summary = {
        "screening_model": args.screening_model,
        "interviewer_model": args.interviewer_model,
        "judge_model": args.judge_model,
        "assistant_models": args.assistant_models,
        "num_strategies": args.num_strategies,
        "screening_limit": args.screening_limit,
        "winners": winners,
    }
    summary_path = base / "pipeline_summary.json"
    base.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'=' * 60}")
    print("PIPELINE COMPLETE")
    print(f"{'=' * 60}")
    for attack_type, idx in winners.items():
        print(f"  {attack_type}: strategy_{idx:03d}")
    print(f"  Summary: {summary_path}")


if __name__ == "__main__":
    main()
