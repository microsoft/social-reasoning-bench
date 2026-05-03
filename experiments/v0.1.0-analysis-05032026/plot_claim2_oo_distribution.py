"""Claim 2: OO distribution jitter plots.

Generates:
- graph_oo_jitter_by_model_both.png (all benign tasks)
- graph_oo_jitter_completed_only.png (TC=1 only)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import load_benign_results, FIGURES_DIR

MODELS = ["GPT-4.1", "GPT-5.4", "Gemini"]
COLORS = {"GPT-4.1": "#1f77b4", "GPT-5.4": "#ff7f0e", "Gemini": "#2ca02c"}
DOMAINS = ["calendar", "marketplace"]
DOMAIN_TITLES = {"calendar": "Calendar", "marketplace": "Marketplace"}


def _make_jitter_plot(results, title, filename, filter_tc=None):
    """Generate a jitter scatter plot of OO by model."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    for ax, domain in zip(axes, DOMAINS):
        for i, model in enumerate(MODELS):
            vals = np.array([
                r.oo for r in results
                if r.domain == domain and r.model == model
                and (filter_tc is None or r.tc == filter_tc)
            ])
            if len(vals) == 0:
                continue
            jitter = np.random.normal(0, 0.08, size=len(vals))
            ax.scatter(i + jitter, vals, alpha=0.4, s=20, color=COLORS[model])
            mean_val = vals.mean()
            ax.hlines(mean_val, i - 0.25, i + 0.25, colors="black", linewidths=2, zorder=5)
            ax.text(i + 0.28, mean_val, f"μ={mean_val:.2f}", fontsize=8, va="center", fontweight="bold")
            ax.text(i, -0.07, f"n={len(vals)}", fontsize=7, color="grey", ha="center", alpha=0.7)

        ax.set_xticks(range(len(MODELS)))
        ax.set_xticklabels(MODELS, fontsize=9)
        ax.set_title(DOMAIN_TITLES[domain], fontsize=12)
        ax.axhline(0.5, color="grey", linestyle=":", alpha=0.4)
        ax.axhline(0.0, color="grey", linestyle=":", alpha=0.3)
        ax.axhline(1.0, color="grey", linestyle=":", alpha=0.3)
        ax.set_ylim(-0.15, 1.15)

    # Labels on right side only
    axes[1].text(
        len(MODELS) - 0.6, 0.0, "Best for\nrequestor",
        fontsize=7, color="grey", va="center", ha="left",
    )
    axes[1].text(
        len(MODELS) - 0.6, 1.0, "Best for\nassistant",
        fontsize=7, color="grey", va="center", ha="left",
    )
    axes[0].set_ylabel("OO (Deal Point within ZOPA)", fontsize=10)
    fig.suptitle(title, fontsize=13, fontweight="bold")
    plt.tight_layout()
    out = FIGURES_DIR / filename
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


def main():
    results = load_benign_results()

    _make_jitter_plot(
        results,
        title="OO Distribution (i.e., Where the Deal Lands in the ZOPA) on Benign Tasks",
        filename="graph_oo_jitter_by_model_both.png",
    )

    _make_jitter_plot(
        results,
        title="OO Distribution on Benign Tasks (Completed Only, TC=1)",
        filename="graph_oo_jitter_completed_only.png",
        filter_tc=True,
    )


if __name__ == "__main__":
    main()
