"""Claim 1: TC vs OO bar chart with prompting breakdown.

Generates graph1_tc_oo_by_model.png showing TC (grey), OO no-prompt (light green),
and OO with-prompt (dark green) per model, faceted by domain.
"""

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common import FIGURES_DIR, load_benign_results
from matplotlib.ticker import FuncFormatter

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

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    bar_width = 0.19
    pct_formatter = FuncFormatter(lambda x, _: f"{x:.0f}%")

    for ax, domain in zip(axes, DOMAINS):
        x = np.arange(len(MODELS))
        tc_vals, oo_none_vals, oo_all_vals, oo_overall_vals = [], [], [], []

        for model in MODELS:
            all_tc = (
                data.get((domain, model, "none"), {"tc": []})["tc"]
                + data.get((domain, model, "all"), {"tc": []})["tc"]
            )
            tc_vals.append(np.mean(all_tc) * 100 if all_tc else 0)

            d_none = data.get((domain, model, "none"), {"oo": []})
            oo_none_vals.append(np.mean(d_none["oo"]) * 100 if d_none["oo"] else 0)

            d_all = data.get((domain, model, "all"), {"oo": []})
            oo_all_vals.append(np.mean(d_all["oo"]) * 100 if d_all["oo"] else 0)

            all_oo = d_none["oo"] + d_all["oo"]
            oo_overall_vals.append(np.mean(all_oo) * 100 if all_oo else 0)

        offset = bar_width * 1.5
        bars1 = ax.bar(x - offset, tc_vals, bar_width, label="Task Completion", color="#9e9e9e")
        bars2 = ax.bar(
            x - bar_width / 2,
            oo_overall_vals,
            bar_width,
            label="Outcome Optimality (Overall)",
            color="#c8e6c9",
        )
        bars3 = ax.bar(
            x + bar_width / 2,
            oo_none_vals,
            bar_width,
            label="Outcome Optimality (Basic Prompt)",
            color="#66bb6a",
        )
        bars4 = ax.bar(
            x + offset,
            oo_all_vals,
            bar_width,
            label="Outcome Optimality (Defensive Prompt)",
            color="#1b5e20",
        )

        for bars in [bars1, bars2, bars3, bars4]:
            for bar in bars:
                h = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 1,
                    f"{h:.0f}%",
                    ha="center",
                    va="bottom",
                    fontsize=7,
                    fontweight="bold",
                )

        ax.set_xticks(x)
        ax.set_xticklabels(MODELS, fontsize=10)
        ax.set_title(DOMAIN_TITLES[domain], fontsize=12)
        ax.set_ylim(0, 115)
        ax.yaxis.set_major_formatter(pct_formatter)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=len(labels),
        fontsize=9,
        frameon=False,
        bbox_to_anchor=(0.5, 1.02),
    )

    fig.suptitle(
        "Task Completion vs Outcome Optimality (Benign Tasks)",
        fontsize=12,
        fontweight="bold",
        y=1.06,
    )
    plt.tight_layout()
    out = FIGURES_DIR / "graph1_tc_oo_by_model.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
