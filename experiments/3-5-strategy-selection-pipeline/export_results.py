"""Export 2×2 comparison results from eval.json files to CSV."""

import csv
import json
from pathlib import Path

RESULTS = [
    (
        "GPT-5.2",
        "Hand-Crafted",
        "experiments/backfire_experiment/outputs/gpt52_hc_large/hc_privacy/eval.json",
    ),
    (
        "GPT-5.2",
        "WhimsyGen",
        "experiments/backfire_experiment/outputs/gpt52_whim_large/strategy_040/eval.json",
    ),
    (
        "GPT-4.1",
        "Hand-Crafted",
        "experiments/backfire_experiment/outputs/gpt41_hc_large/hc_privacy/eval.json",
    ),
    (
        "GPT-4.1",
        "WhimsyGen",
        "experiments/backfire_experiment/outputs/gpt41_whim_large/strategy_030/eval.json",
    ),
]

OUT = Path(__file__).parent / "results_2x2.csv"


def main():
    rows = []
    for model, attack, path in RESULTS:
        data = json.load(open(path))
        total = len(data["results"])
        leaked = sum(1 for r in data["results"] if r.get("leaked_secrets"))
        rows.append(
            {
                "model": model,
                "attack": attack,
                "leaked": leaked,
                "total": total,
                "leakage_rate": leaked / total,
            }
        )

    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["model", "attack", "leaked", "total", "leakage_rate"])
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {OUT}")
    for r in rows:
        print(
            f"  {r['model']} + {r['attack']}: {r['leaked']}/{r['total']} ({r['leakage_rate']:.1%})"
        )


if __name__ == "__main__":
    main()
