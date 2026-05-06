"""Claim 3: Effect of system prompt on OO.

Generates graph_oo_by_prompt.png showing OO with vs without system prompt
for each model (calendar domain only).
"""

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import FIGURES_DIR, load_benign_results

MODELS = ["GPT-4.1", "GPT-5.4", "Gemini"]


def main():
    results = load_benign_results()

    # Group by (model, prompt) for calendar only
    data = {}
    for r in results:
        if r.domain != "calendar":
            continue
        data.setdefault((r.model, r.prompt), []).append(r.oo)

    fig, ax = plt.subplots(figsize=(8, 5))
    bar_width = 0.35
    x = np.arange(len(MODELS))
    colors = {"none": "#9e9e9e", "all": "#388e3c"}

    for i, (prompt, label) in enumerate(
        [
            ("none", "No system prompt"),
            ("all", "With system prompt"),
        ]
    ):
        means = [np.mean(data.get((m, prompt), [0])) for m in MODELS]
        bars = ax.bar(x + i * bar_width, means, bar_width, label=label, color=colors[prompt])
        for j, v in enumerate(means):
            ax.text(
                x[j] + i * bar_width,
                v + 0.01,
                f"{v:.2f}",
                ha="center",
                fontsize=9,
                fontweight="bold",
            )

    ax.set_xticks(x + bar_width / 2)
    ax.set_xticklabels(MODELS, fontsize=11)
    ax.set_ylabel("Mean OO", fontsize=11)
    ax.set_ylim(0, 0.65)
    ax.set_title(
        "Effect of System Prompt on Outcome Optimality\n(Calendar, Benign Tasks)",
        fontsize=12,
        fontweight="bold",
    )
    ax.legend(fontsize=10)
    ax.axhline(0.5, color="grey", linestyle=":", alpha=0.4)

    plt.tight_layout()
    out = FIGURES_DIR / "graph_oo_by_prompt.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
