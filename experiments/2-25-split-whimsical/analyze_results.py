#!/usr/bin/env python3
"""Analyze split whimsical strategy experiment results.

Analyzes privacy and duty-of-care strategies separately, ranking each by
their targeted metric.
"""

import json
import re
from pathlib import Path

import yaml

# Experiment configuration (must match experiment_whimsical_strategy.py)
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


def load_strategy_text(strategies_dir: Path, task_type: str, strategy_idx: int) -> str | None:
    """Load the strategy text from the strategies directory."""
    strategy_file = strategies_dir / task_type / f"strategy_{strategy_idx}.yaml"
    if not strategy_file.exists():
        return None

    with open(strategy_file) as f:
        data = yaml.safe_load(f)

    if data and "strategies" in data and len(data["strategies"]) > 0:
        return data["strategies"][0].get("game_strategies", "")
    return None


def analyze_task_type(
    task_type: str,
    outputs_dir: Path,
    strategies_dir: Path,
    baselines: dict,
    requestor_models: list[str],
) -> list[dict]:
    """Analyze strategies for a single task type."""
    # Choose the primary metric based on task type
    if task_type == "privacy":
        metric_key = "privacy_avg_leakage_rate"
        metric_label = "Leakage"
        higher_is_worse = True
    else:
        metric_key = "fiduciary_avg_assistant_duty_of_care_score"
        metric_label = "Duty of Care"
        higher_is_worse = False

    strategy_results = []

    for i in range(NUM_STRATEGIES):
        strategy_data = {
            "index": i,
            "task_type": task_type,
            "by_model": {},
            "avg_metric": 0,
            "avg_delta": 0,
        }

        metrics = []
        deltas = []

        for model in requestor_models:
            variant = f"{task_type}_{i}_{model}"
            result = load_result(outputs_dir / variant)

            if result:
                metric_val = result["summary"].get(metric_key, 0 if higher_is_worse else 1)
                leakage = result["summary"].get("privacy_avg_leakage_rate", 0)
                doc = result["summary"].get("fiduciary_avg_assistant_duty_of_care_score", 1)

                baseline = baselines.get(model, {})
                base_metric = baseline.get(metric_key, 0 if higher_is_worse else 1)
                delta = metric_val - base_metric

                strategy_data["by_model"][model] = {
                    "metric": metric_val,
                    "leakage": leakage,
                    "doc": doc,
                    "delta": delta,
                }

                metrics.append(metric_val)
                deltas.append(delta)

        if metrics:
            strategy_data["avg_metric"] = sum(metrics) / len(metrics)
            strategy_data["avg_delta"] = sum(deltas) / len(deltas)

        strategy_data["strategy_text"] = load_strategy_text(strategies_dir, task_type, i)
        strategy_results.append(strategy_data)

    # Sort: for privacy (leakage), higher is more effective attack;
    # for duty_of_care, lower score means more effective attack
    strategy_results.sort(
        key=lambda x: x["avg_metric"],
        reverse=higher_is_worse,
    )

    # Print results
    print(f"\n{'=' * 80}")
    print(f"{task_type.upper()} STRATEGY RANKINGS (by {metric_label})")
    print(f"{'=' * 80}")

    for model in requestor_models:
        print(f"\n  {model}:")
        print(f"  {'Rank':<6} {'Strategy':<12} {metric_label:<12} {'Delta':<10}")
        print(f"  {'-' * 45}")

        model_results = [
            (s["index"], s["by_model"].get(model, {}))
            for s in strategy_results
            if model in s["by_model"]
        ]
        model_results.sort(
            key=lambda x: x[1].get("metric", 0),
            reverse=higher_is_worse,
        )

        for rank, (idx, data) in enumerate(model_results[:10], 1):
            delta = data.get("delta", 0)
            delta_str = f"+{delta:.3f}" if delta >= 0 else f"{delta:.3f}"
            print(f"  {rank:<6} {idx:<12} {data.get('metric', 0):<12.3f} {delta_str:<10}")

    print(f"\n  Overall (averaged across models):")
    print(f"  {'Rank':<6} {'Strategy':<12} {'Avg ' + metric_label:<15} {'Avg Delta':<12}")
    print(f"  {'-' * 50}")

    for rank, s in enumerate(strategy_results, 1):
        delta_str = f"+{s['avg_delta']:.3f}" if s["avg_delta"] >= 0 else f"{s['avg_delta']:.3f}"
        print(f"  {rank:<6} {s['index']:<12} {s['avg_metric']:<15.3f} {delta_str:<12}")

    return strategy_results


def main():
    experiment_dir = Path(__file__).parent
    outputs_dir = experiment_dir / "outputs"
    strategies_dir = experiment_dir / "strategies"

    requestor_models = discover_models(outputs_dir)

    # Load baselines
    baselines = {}
    print("=" * 80)
    print("BASELINE RESULTS")
    print("=" * 80)
    print(f"{'Model':<25} {'Leakage':<12} {'Duty of Care':<15}")
    print("-" * 55)

    for model in requestor_models:
        variant = f"baseline_{model}"
        result = load_result(outputs_dir / variant)
        if result:
            leakage = result["summary"].get("privacy_avg_leakage_rate", 0)
            doc = result["summary"].get("fiduciary_avg_assistant_duty_of_care_score", 1)
            baselines[model] = {
                "privacy_avg_leakage_rate": leakage,
                "fiduciary_avg_assistant_duty_of_care_score": doc,
            }
            print(f"{model:<25} {leakage:<12.3f} {doc:<15.3f}")
        else:
            print(f"{model:<25} {'N/A':<12} {'N/A':<15}")

    # Analyze each task type
    all_results = {}
    for task_type in TASK_TYPES:
        all_results[task_type] = analyze_task_type(
            task_type, outputs_dir, strategies_dir, baselines, requestor_models
        )

    # Export summary
    summary = {
        "baselines": baselines,
        "task_types": {
            task_type: [
                {
                    "index": s["index"],
                    "avg_metric": s["avg_metric"],
                    "avg_delta": s["avg_delta"],
                    "by_model": s["by_model"],
                }
                for s in results
            ]
            for task_type, results in all_results.items()
        },
    }

    summary_path = experiment_dir / "analysis_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nExported summary to: {summary_path}")


if __name__ == "__main__":
    main()
