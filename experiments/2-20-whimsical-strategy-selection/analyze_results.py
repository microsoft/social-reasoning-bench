#!/usr/bin/env python3
"""Analyze whimsical strategy experiment results and rank by impact."""

import json
from pathlib import Path

import yaml


def load_result(output_dir: Path) -> dict | None:
    """Load the benchmark output JSON from a directory."""
    eval_file = output_dir / "eval.json"
    if not eval_file.exists():
        return None
    with open(eval_file) as f:
        return json.load(f)


def load_strategy(strategy_dir: Path) -> str | None:
    """Load the strategy text from strategies.yaml."""
    strategies_file = strategy_dir / "strategies.yaml"
    if not strategies_file.exists():
        return None
    with open(strategies_file) as f:
        data = yaml.safe_load(f)
    # Extract the game_strategies text from the first strategy
    if data and "strategies" in data and len(data["strategies"]) > 0:
        return data["strategies"][0].get("game_strategies", "")
    return None


def main():
    experiment_dir = Path(__file__).parent
    outputs_dir = experiment_dir / "outputs"
    strategies_dir = experiment_dir / "strategies"

    # Load baseline
    baseline_result = load_result(outputs_dir / "baseline")
    if not baseline_result:
        print("ERROR: Baseline results not found")
        return

    baseline_leakage = baseline_result["summary"].get("privacy_avg_leakage_rate", 0)
    baseline_doc = baseline_result["summary"].get("fiduciary_avg_assistant_duty_of_care_score", 1)
    baseline_impact = baseline_leakage + (1 - baseline_doc)

    print("=" * 60)
    print("BASELINE RESULTS")
    print("=" * 60)
    print(f"  Leakage Rate:    {baseline_leakage:.3f}")
    print(f"  Duty of Care:    {baseline_doc:.3f}")
    print(f"  Impact Score:    {baseline_impact:.3f}")
    print()

    # Load strategy results
    results = []
    for i in range(10):
        strategy_output_dir = outputs_dir / f"strategy_{i}"
        strategy_dir = strategies_dir / f"strategy_{i}"

        result = load_result(strategy_output_dir)
        if not result:
            print(f"WARNING: Strategy {i} results not found")
            continue

        leakage = result["summary"].get("privacy_avg_leakage_rate", 0)
        doc = result["summary"].get("fiduciary_avg_assistant_duty_of_care_score", 1)
        impact = leakage + (1 - doc)
        delta = impact - baseline_impact

        strategy_text = load_strategy(strategy_dir)

        results.append(
            {
                "index": i,
                "leakage": leakage,
                "duty_of_care": doc,
                "impact": impact,
                "delta": delta,
                "strategy_text": strategy_text,
            }
        )

    # Sort by impact (descending)
    results.sort(key=lambda x: x["impact"], reverse=True)

    # Print rankings
    print("=" * 60)
    print("STRATEGY RANKINGS (by impact score)")
    print("=" * 60)
    print(f"{'Rank':<5} {'Strategy':<10} {'Leakage':<10} {'DoC':<10} {'Impact':<10} {'Delta':<10}")
    print("-" * 60)

    for rank, r in enumerate(results, 1):
        delta_str = f"+{r['delta']:.3f}" if r["delta"] >= 0 else f"{r['delta']:.3f}"
        print(
            f"{rank:<5} {r['index']:<10} {r['leakage']:<10.3f} {r['duty_of_care']:<10.3f} {r['impact']:<10.3f} {delta_str:<10}"
        )

    print()

    # Show the most impactful strategy
    if results:
        winner = results[0]
        print("=" * 60)
        print(f"MOST IMPACTFUL STRATEGY (#{winner['index']})")
        print("=" * 60)
        print(f"  Impact Score: {winner['impact']:.3f} (delta: +{winner['delta']:.3f})")
        print(f"  Leakage Rate: {winner['leakage']:.3f} (baseline: {baseline_leakage:.3f})")
        print(f"  Duty of Care: {winner['duty_of_care']:.3f} (baseline: {baseline_doc:.3f})")
        print()
        print("Strategy Text:")
        print("-" * 60)
        if winner["strategy_text"]:
            # Print first 500 chars of strategy
            text = winner["strategy_text"]
            if len(text) > 500:
                text = text[:500] + "..."
            print(text)
        else:
            print("(Strategy text not found)")
        print()
        print(f"Full strategy file: strategies/strategy_{winner['index']}/strategies.yaml")


if __name__ == "__main__":
    main()
