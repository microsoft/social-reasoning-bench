"""Claim 1: TC vs OO bar chart with prompting breakdown.

Generates graph1_tc_oo_by_model.png showing TC (grey), OO no-prompt (light green),
and OO with-prompt (dark green) per model, faceted by domain.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from common import load_benign_results, FIGURES_DIR

MODELS = ["GPT-4.1", "GPT-5.4", "Gemini"]
DOMAINS = ["calendar", "marketplace"]
DOMAIN_TITLES = {"calendar": "Calendar", "marketplace": "Marketplace"}


def main():
    results = load_benign_results()

    # Group data
    data = {}
    for r in results:
        data.setdefault((r.domain, r.model, r.prompt), {"tc": [], "oo": []})
        data[(r.domain, r.model, r.prompt)]["tc"].append(r.tc)
        data[(r.domain, r.model, r.prompt)]["oo"].append(r.oo)

    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    bar_width = 0.25
    pct_formatter = FuncFormatter(lambda x, _: f"{x:.0f}%")

    for ax, domain in zip(axes, DOMAINS):
        x = np.arange(len(MODELS))
        tc_vals, oo_none_vals, oo_all_vals = [], [], []

        for model in MODELS:
            all_tc = (
                data.get((domain, model, "none"), {"tc": []})["tc"]
                + data.get((domain, model, "all"), {"tc": []})["tc"]
            )
            tc_vals.append(np.mean(all_tc) * 100 if all_tc else 0)

            d = data.get((domain, model, "none"), {"oo": []})
            oo_none_vals.append(np.mean(d["oo"]) * 100 if d["oo"] else 0)

            d = data.get((domain, model, "all"), {"oo": []})
            oo_all_vals.append(np.mean(d["oo"]) * 100 if d["oo"] else 0)

        bars1 = ax.bar(x - bar_width, tc_vals, bar_width, label="TC", color="#9e9e9e")
        bars2 = ax.bar(x, oo_none_vals, bar_width, label="OO (no prompt)", color="#a5d6a7")
        bars3 = ax.bar(x + bar_width, oo_all_vals, bar_width, label="OO (with prompt)", color="#2e7d32")

        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                h = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2, h + 1, f"{h:.0f}%",
                    ha="center", va="bottom", fontsize=8, fontweight="bold",
                )

        ax.set_xticks(x)
        ax.set_xticklabels(MODELS, fontsize=10)
        ax.set_title(DOMAIN_TITLES[domain], fontsize=12)
        ax.set_ylim(0, 115)
        ax.yaxis.set_major_formatter(pct_formatter)

    handles, labels = axes[0].get_legend_handles_labels()
    axes[1].legend(handles, labels, loc="upper right", fontsize=9)

    fig.suptitle(
        "Task Completion vs Outcome Optimality by Prompting Strategy (Benign Tasks)",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout()
    out = FIGURES_DIR / "graph1_tc_oo_by_model.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
