"""Claim 5: OO by adversary type (benign vs handcrafted vs whimsical).

Uses the *continuous* benign OO formula for malicious tasks (same as rq2_plot.py).
This shows how bad outcomes are when agents DO engage, excluding refusals.
"""

import json
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUR_DIR = Path(__file__).resolve().parent
PLOTTING_DIR = Path(__file__).resolve().parents[1] / "v0.1.0" / "plotting"
sys.path.insert(0, str(OUR_DIR))
sys.path.insert(1, str(PLOTTING_DIR))

from benign_oo import (
    benign_outcome_optimality,
    load_calendar_results,
    load_marketplace_results,
)
from common import FIGURES_DIR, RESULTS_DIR, get_model, load_results_dirs

MODELS = ["GPT-4.1", "GPT-5.4", "Gemini"]
DOMAINS = ["calendar", "marketplace"]
DOMAIN_TITLES = {"calendar": "Calendar", "marketplace": "Marketplace"}
STYLE_ORDER = ["normal", "hand_crafted", "whimsical"]
COLORS = {"normal": "#66bb6a", "hand_crafted": "#ef5350", "whimsical": "#ffa726"}
LABELS = {"normal": "Benign", "hand_crafted": "Hand-Crafted", "whimsical": "Whimsical"}


def _get_attack_style(cfg: dict) -> str:
    """Determine attack style from config (mirrors canonical _parse_config logic)."""
    paths = cfg.get("paths") or []
    path = paths[0] if paths else ""
    attack_types = cfg.get("attack_types") or []
    if "whimsical" in path:
        return "whimsical"
    elif attack_types:
        return "hand_crafted"
    return "normal"


def main():
    dirs = load_results_dirs(prompt_filter="all", include_malicious=True)

    # Collect per-task continuous OO scores keyed by (domain, model, attack_style)
    data: dict[tuple[str, str, str], list[float]] = {}

    for d in dirs:
        results_file = d / "results.json"
        results_data = json.loads(results_file.read_text())
        cfg = results_data.get("config") or {}

        domain = "calendar" if "calendar" in d.name else "marketplace"
        model = get_model(d.name)
        attack_style = _get_attack_style(cfg)

        # Load typed results and compute benign OO
        if domain == "marketplace":
            typed_results = load_marketplace_results(results_data)
        elif domain == "calendar":
            typed_results = load_calendar_results(results_data)
        else:
            continue

        for r in typed_results:
            oo = benign_outcome_optimality(r)
            if oo is not None:
                data.setdefault((domain, model, attack_style), []).append(oo)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    bar_width = 0.25
    pct_formatter = FuncFormatter(lambda x, _: f"{x:.0f}%")

    for ax, domain in zip(axes, DOMAINS):
        x = np.arange(len(MODELS))
        for i, style in enumerate(STYLE_ORDER):
            vals = []
            for model in MODELS:
                scores = data.get((domain, model, style), [])
                vals.append(np.mean(scores) * 100 if scores else 0)
            offset = (i - 1) * bar_width
            bars = ax.bar(x + offset, vals, bar_width, label=LABELS[style], color=COLORS[style])
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

    handles, labels_list = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels_list,
        loc="upper center",
        ncol=len(labels_list),
        fontsize=9,
        frameon=False,
        bbox_to_anchor=(0.5, 1.02),
    )
    fig.suptitle(
        "Outcome Optimality Under Attack (Continuous Benign OO)",
        fontsize=12,
        fontweight="bold",
        y=1.06,
    )
    plt.tight_layout()
    out_path = FIGURES_DIR / "graph8_oo_by_adversary.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
