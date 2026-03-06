"""Plot 2×2 comparison from results_2x2.csv."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

CSV = Path(__file__).parent / "results_2x2.csv"


def main():
    rows = list(csv.DictReader(open(CSV)))

    models = []
    hc = []
    whim = []
    for r in rows:
        rate = float(r["leakage_rate"]) * 100
        if r["attack"] == "Hand-Crafted":
            models.append(f"{r['model']} (CI)")
            hc.append(rate)
        else:
            whim.append(rate)

    x = np.arange(len(models))
    width = 0.32

    fig, ax = plt.subplots(figsize=(6, 4))
    bars_hc = ax.bar(x - width / 2, hc, width, label="Hand-Crafted", color="#5B9BD5")
    bars_wh = ax.bar(x + width / 2, whim, width, label="WhimsyGen Top", color="#ED7D31")

    ax.set_ylabel("Leakage Rate (%)")
    ax.set_title("Privacy Leakage: WhimsyGen vs Hand-Crafted (140 tasks)")
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylim(0, 65)
    ax.legend()

    for bar in [*bars_hc, *bars_wh]:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{bar.get_height():.1f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    out = Path(__file__).parent / "2x2_comparison.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
