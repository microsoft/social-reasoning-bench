#!/usr/bin/env python3
"""Generate final adversarial data using top-ranked whimsical strategies.

Analyzes experiment results to identify top N strategies per task type,
merges them into a single combined strategies file, then generates one
adversarial dataset per (task_type, size) with the top strategies applied
uniformly (round-robin) across tasks.

Output files mirror the source dataset name with a malicious suffix:
  data/calendar-scheduling/final/small-malicious-whimsical-privacy.yaml
  data/calendar-scheduling/final/medium-malicious-whimsical-privacy.yaml
  data/calendar-scheduling/final/large-malicious-whimsical-duty-of-care.yaml
  ...

Usage:
    python experiments/2-25-split-whimsical/generate_final_data.py
    python experiments/2-25-split-whimsical/generate_final_data.py -n 5
    python experiments/2-25-split-whimsical/generate_final_data.py --task privacy
    python experiments/2-25-split-whimsical/generate_final_data.py --dry-run
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

# Dataset sizes to generate
SIZES = ["small", "medium", "large"]
INPUT_TEMPLATE = "data/calendar-scheduling/final/{size}.yaml"
DEFAULT_MODEL = "gemini-3-flash-preview"
NUM_STRATEGIES = 10
TASK_TYPES = ["privacy", "duty_of_care"]


def discover_models(outputs_dir: Path) -> list[str]:
    """Discover requestor model labels from completed baseline runs."""
    models = []
    for path in sorted(outputs_dir.glob("baseline_*")):
        if (path / "eval.json").exists():
            models.append(re.sub(r"^baseline_", "", path.name))
    return models


def load_result(output_dir: Path) -> dict | None:
    """Load the benchmark output JSON from a directory."""
    eval_file = output_dir / "eval.json"
    if not eval_file.exists():
        return None
    with open(eval_file) as f:
        return json.load(f)


def get_top_strategies(
    task_type: str,
    outputs_dir: Path,
    requestor_models: list[str],
    top_n: int,
) -> list[tuple[int, float]]:
    """Return (strategy_idx, avg_metric) for top N strategies, ranked by avg metric across models.

    For privacy: higher leakage rate = more effective (ranked descending).
    For duty_of_care: lower DoC score = more effective (ranked ascending).
    """
    if task_type == "privacy":
        metric_key = "privacy_avg_leakage_rate"
        reverse = True  # higher = worse for assistant = better attack
    else:
        metric_key = "fiduciary_avg_assistant_duty_of_care_score"
        reverse = False  # lower = worse for assistant = better attack

    strategy_scores: list[tuple[int, float]] = []
    for i in range(NUM_STRATEGIES):
        metrics = []
        for model in requestor_models:
            result = load_result(outputs_dir / f"{task_type}_{i}_{model}")
            if result:
                val = result["summary"].get(metric_key)
                if val is not None:
                    metrics.append(val)
        if metrics:
            strategy_scores.append((i, sum(metrics) / len(metrics)))

    strategy_scores.sort(key=lambda x: x[1], reverse=reverse)
    return strategy_scores[:top_n]


def merge_strategy_files(strategy_files: list[Path]) -> dict:
    """Merge multiple single-strategy YAML files into a StrategyCollection dict."""
    strategies = []
    for f in strategy_files:
        with open(f) as fh:
            data = yaml.safe_load(fh)
        strategies.extend(data["strategies"])
    return {"strategies": strategies}


def generate_adversarial_data(
    repo_root: Path,
    combined_strategies_file: Path,
    num_strategies: int,
    input_yaml: Path,
    output_path: Path,
    model: str,
    task_type: str,
    dry_run: bool = False,
) -> bool:
    """Run whimsical.py to generate adversarial data with top-N strategies applied round-robin."""
    assignment_args = [
        "--strategy-assignment",
        "sequential",
        "--max-strategies",
        str(num_strategies),
    ]
    module = f"sage_data_gen.calendar_scheduling.malicious.whimsical.{task_type}"
    cmd = [
        "uv",
        "run",
        "--package",
        "sage-data-gen",
        "python",
        "-m",
        module,
        str(input_yaml),
        "-m",
        model,
        *assignment_args,
        "--strategies-file",
        str(combined_strategies_file),
        "-o",
        str(output_path),
    ]

    if dry_run:
        print(f"  [DRY RUN] {' '.join(str(c) for c in cmd)}")
        return True

    result = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR generating {output_path.name}:\n{result.stderr[-500:]}", file=sys.stderr)
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate final adversarial data from top-ranked whimsical strategies"
    )
    parser.add_argument(
        "-n",
        "--top-n",
        type=int,
        default=5,
        help="Number of top strategies per task type (default: 5)",
    )
    parser.add_argument(
        "--task",
        choices=["privacy", "duty_of_care", "both"],
        default="both",
        help="Which task type to process (default: both)",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model for whimsical injection (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        choices=SIZES,
        default=SIZES,
        help="Dataset sizes to generate (default: small medium large)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without running them",
    )
    args = parser.parse_args()

    experiment_dir = Path(__file__).parent
    repo_root = experiment_dir.parent.parent
    outputs_dir = experiment_dir / "outputs"
    strategies_dir = experiment_dir / "strategies"
    final_data_dir = repo_root / "data/calendar-scheduling/final"

    requestor_models = discover_models(outputs_dir)
    if not requestor_models:
        print(
            "ERROR: No completed baseline runs found in outputs/. Run the experiment first.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Discovered models: {requestor_models}")

    tasks_to_run = list(TASK_TYPES) if args.task == "both" else [args.task]
    selection_summary: dict = {"top_n": args.top_n, "selected": {}}

    with tempfile.TemporaryDirectory() as tmpdir:
        for task_type in tasks_to_run:
            print(f"\n=== {task_type.upper()} ===")

            top_strategies = get_top_strategies(
                task_type, outputs_dir, requestor_models, args.top_n
            )
            if not top_strategies:
                print(f"  No completed results found for {task_type}. Skipping.")
                continue

            print(f"  Top {len(top_strategies)} strategies (index: avg_metric):")
            for rank, (idx, score) in enumerate(top_strategies, 1):
                print(f"    #{rank}: strategy_{idx}  avg={score:.3f}")

            selection_summary["selected"][task_type] = [
                {"rank": rank, "strategy_index": idx, "avg_metric": score}
                for rank, (idx, score) in enumerate(top_strategies, 1)
            ]

            # Collect and validate strategy files
            strategy_files = []
            for rank, (strategy_idx, _) in enumerate(top_strategies, 1):
                f = strategies_dir / task_type / f"strategy_{strategy_idx}.yaml"
                if not f.exists():
                    print(f"  WARNING: Strategy file not found: {f}")
                else:
                    strategy_files.append(f)

            if not strategy_files:
                print(f"  No strategy files found for {task_type}. Skipping.")
                continue

            # Merge into a single combined file for sequential assignment
            combined = merge_strategy_files(strategy_files)
            combined_path = Path(tmpdir) / f"{task_type}_combined.yaml"
            if not args.dry_run:
                with open(combined_path, "w") as f:
                    yaml.dump(combined, f, default_flow_style=False, allow_unicode=True, width=120)
            print(f"  Merged {len(strategy_files)} strategies")

            task_slug = task_type.replace("_", "-")
            for size in args.sizes:
                input_yaml = repo_root / INPUT_TEMPLATE.format(size=size)
                if not input_yaml.exists():
                    print(f"  WARNING: Input file not found: {input_yaml}")
                    continue

                output_path = final_data_dir / f"{size}-malicious-whimsical-{task_slug}.yaml"
                if output_path.exists() and not args.dry_run:
                    print(f"  Skipping {output_path.name} (already exists)")
                    continue
                print(f"  [{task_type}] combined/{size}", end=" ", flush=True)
                ok = generate_adversarial_data(
                    repo_root=repo_root,
                    combined_strategies_file=combined_path,
                    num_strategies=len(strategy_files),
                    input_yaml=input_yaml,
                    output_path=output_path,
                    model=args.model,
                    task_type=task_type,
                    dry_run=args.dry_run,
                )
                if ok and not args.dry_run:
                    print("✓")

    if not args.dry_run:
        summary_path = experiment_dir / "final_data_summary.json"
        with open(summary_path, "w") as f:
            json.dump(selection_summary, f, indent=2)
        print(f"\nSaved strategy selection summary to: {summary_path}")
        print(f"Output directory: {final_data_dir}/")


if __name__ == "__main__":
    main()
