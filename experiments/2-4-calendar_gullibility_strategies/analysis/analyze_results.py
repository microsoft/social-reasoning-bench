#!/usr/bin/env python3
"""Analyze gullibility strategy experiment results."""

import argparse
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_results(output_dir: str) -> dict:
    """Load all results from an output directory."""
    results = {"strategies": [], "baselines": []}

    for f in os.listdir(output_dir):
        if not f.endswith(".json"):
            continue

        with open(os.path.join(output_dir, f)) as fp:
            data = json.load(fp)

        summary = data["summary"]
        leaked = summary["privacy_tasks_with_leakage"] > 0
        leakage_rate = summary["privacy_avg_leakage_rate"]

        if f.startswith("strategy-"):
            name = f.replace("strategy-", "").replace(".json", "")
            results["strategies"].append(
                {
                    "name": name,
                    "leaked": leaked,
                    "leakage_rate": leakage_rate,
                }
            )
        elif f.startswith("baseline-"):
            results["baselines"].append(
                {
                    "leaked": leaked,
                    "leakage_rate": leakage_rate,
                }
            )

    return results


def compute_stats(results: dict) -> dict:
    """Compute statistics from results."""
    strategies = results["strategies"]
    baselines = results["baselines"]

    strategy_leaked = sum(1 for s in strategies if s["leaked"])
    baseline_leaked = sum(1 for b in baselines if b["leaked"])

    return {
        "strategy_count": len(strategies),
        "strategy_leaked": strategy_leaked,
        "strategy_leak_rate": strategy_leaked / len(strategies) if strategies else 0,
        "baseline_count": len(baselines),
        "baseline_leaked": baseline_leaked,
        "baseline_leak_rate": baseline_leaked / len(baselines) if baselines else 0,
    }


def get_top_leakers(results: dict, n: int = 10) -> list:
    """Get top N strategies by leakage rate."""
    leaked = [s for s in results["strategies"] if s["leaked"]]
    return sorted(leaked, key=lambda x: -x["leakage_rate"])[:n]


def plot_comparison(stats_strong: dict, stats_ci: dict, output_path: str):
    """Create comparison bar plot."""
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(2)
    width = 0.35

    strong_rates = [
        stats_strong["strategy_leak_rate"] * 100,
        stats_strong["baseline_leak_rate"] * 100,
    ]
    ci_rates = [stats_ci["strategy_leak_rate"] * 100, stats_ci["baseline_leak_rate"] * 100]

    bars1 = ax.bar(x - width / 2, strong_rates, width, label="privacy-strong", color="#e74c3c")
    bars2 = ax.bar(x + width / 2, ci_rates, width, label="privacy-ci", color="#3498db")

    ax.set_ylabel("Privacy Leakage Rate (%)")
    ax.set_title("Gemini 2.5 Flash (with Thinking)\nPrivacy Leakage by System Prompt")
    ax.set_xticks(x)
    ax.set_xticklabels(["Malicious +\nStrategies", "Malicious\nBaseline"])
    ax.legend()
    ax.set_ylim(0, 50)

    # Add value labels
    for bar in bars1 + bars2:
        height = bar.get_height()
        ax.annotate(
            f"{height:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Saved plot to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Analyze gullibility experiment results")
    parser.add_argument("--output-dir", default=".", help="Output directory for plots")
    parser.add_argument(
        "--strong-dir",
        default="../../outputs/calendar_scheduling/baseline_vs_strategies",
        help="Directory with privacy-strong results",
    )
    parser.add_argument(
        "--ci-dir",
        default="../../outputs/calendar_scheduling/baseline_vs_strategies_privacy_ci",
        help="Directory with privacy-ci results",
    )
    args = parser.parse_args()

    # Load results
    print("Loading privacy-strong results...")
    results_strong = load_results(args.strong_dir)
    stats_strong = compute_stats(results_strong)

    print("Loading privacy-ci results...")
    results_ci = load_results(args.ci_dir)
    stats_ci = compute_stats(results_ci)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print("\nprivacy-strong:")
    print(
        f"  Strategies: {stats_strong['strategy_leaked']}/{stats_strong['strategy_count']} leaked ({stats_strong['strategy_leak_rate'] * 100:.1f}%)"
    )
    print(
        f"  Baselines:  {stats_strong['baseline_leaked']}/{stats_strong['baseline_count']} leaked ({stats_strong['baseline_leak_rate'] * 100:.1f}%)"
    )

    print("\nprivacy-ci:")
    print(
        f"  Strategies: {stats_ci['strategy_leaked']}/{stats_ci['strategy_count']} leaked ({stats_ci['strategy_leak_rate'] * 100:.1f}%)"
    )
    print(
        f"  Baselines:  {stats_ci['baseline_leaked']}/{stats_ci['baseline_count']} leaked ({stats_ci['baseline_leak_rate'] * 100:.1f}%)"
    )

    # Top leakers
    print("\n" + "=" * 60)
    print("TOP LEAKING STRATEGIES (privacy-strong)")
    print("=" * 60)
    for s in get_top_leakers(results_strong):
        print(f"  {s['name'][:50]}: {s['leakage_rate'] * 100:.1f}%")

    # Create plot
    output_path = os.path.join(args.output_dir, "plot_gullibility_comparison.png")
    plot_comparison(stats_strong, stats_ci, output_path)


if __name__ == "__main__":
    main()
