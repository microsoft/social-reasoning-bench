"""Claim 5: Refusal Rate + OO|Engaged side-by-side.

Left panel: Refusal rate (how often agent declines) — higher = better under attack.
Right panel: OO conditional on engagement — how good is the deal when they do engage.
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
from common import FIGURES_DIR, get_model, load_results_dirs

MODELS = ["GPT-4.1", "GPT-5.4", "Gemini"]
DOMAINS = ["calendar", "marketplace"]
DOMAIN_TITLES = {"calendar": "Calendar", "marketplace": "Marketplace"}
CONDITIONS = ["benign", "adversarial"]
COLORS = {"benign": "#66bb6a", "adversarial": "#ef5350"}
LABELS = {"benign": "Benign", "adversarial": "Adversarial"}


def _get_condition(cfg: dict) -> str:
    paths = cfg.get("paths") or []
    path = paths[0] if paths else ""
    attack_types = cfg.get("attack_types") or []
    if "whimsical" in path or attack_types:
        return "adversarial"
    return "benign"


def main():
    dirs = load_results_dirs(prompt_filter="all", include_malicious=True)

    # Collect per-task: engaged/refused + OO if engaged
    stats: dict[tuple[str, str, str], dict] = {}

    for d in dirs:
        results_data = json.loads((d / "results.json").read_text())
        cfg = results_data.get("config") or {}
        domain = "calendar" if "calendar" in d.name else "marketplace"
        model = get_model(d.name)
        condition = _get_condition(cfg)
        key = (domain, model, condition)
        stats.setdefault(key, {"engaged": 0, "refused": 0, "oo_if_engaged": []})

        if domain == "marketplace":
            typed = load_marketplace_results(results_data)
            for r in typed:
                if r.execution.outcome.deal_reached:
                    stats[key]["engaged"] += 1
                    oo = benign_outcome_optimality(r)
                    if oo is not None:
                        stats[key]["oo_if_engaged"].append(oo)
                else:
                    stats[key]["refused"] += 1
        else:
            typed = load_calendar_results(results_data)
            for r in typed:
                if r.scheduled_meeting is not None:
                    stats[key]["engaged"] += 1
                    oo = benign_outcome_optimality(r)
                    if oo is not None:
                        stats[key]["oo_if_engaged"].append(oo)
                else:
                    stats[key]["refused"] += 1

    # Build 2x2 grid: rows=domain, cols=[Refusal Rate, OO|Engaged]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    bar_width = 0.3
    pct_formatter = FuncFormatter(lambda x, _: f"{x:.0f}%")

    for row, domain in enumerate(DOMAINS):
        # Left: Refusal Rate
        ax_ref = axes[row, 0]
        x = np.arange(len(MODELS))
        for i, cond in enumerate(CONDITIONS):
            vals = []
            for model in MODELS:
                s = stats.get((domain, model, cond), {"engaged": 0, "refused": 0})
                total = s["engaged"] + s["refused"]
                vals.append(s["refused"] / total * 100 if total else 0)
            offset = (i - 0.5) * bar_width
            bars = ax_ref.bar(x + offset, vals, bar_width, label=LABELS[cond], color=COLORS[cond])
            for bar in bars:
                h = bar.get_height()
                ax_ref.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 1,
                    f"{h:.0f}%",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    fontweight="bold",
                )

        ax_ref.set_xticks(x)
        ax_ref.set_xticklabels(MODELS, fontsize=10)
        ax_ref.set_title(f"{DOMAIN_TITLES[domain]} — Refusal Rate", fontsize=11, fontweight="bold")
        ax_ref.set_ylim(0, 115)
        ax_ref.yaxis.set_major_formatter(pct_formatter)
        ax_ref.set_ylabel("% tasks refused")

        # Right: OO | Engaged
        ax_oo = axes[row, 1]
        for i, cond in enumerate(CONDITIONS):
            vals = []
            for model in MODELS:
                s = stats.get((domain, model, cond), {"oo_if_engaged": []})
                oo_vals = s["oo_if_engaged"]
                vals.append(np.mean(oo_vals) * 100 if oo_vals else 0)
            offset = (i - 0.5) * bar_width
            bars = ax_oo.bar(x + offset, vals, bar_width, label=LABELS[cond], color=COLORS[cond])
            for bar in bars:
                h = bar.get_height()
                ax_oo.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 1,
                    f"{h:.0f}%",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    fontweight="bold",
                )

        ax_oo.set_xticks(x)
        ax_oo.set_xticklabels(MODELS, fontsize=10)
        ax_oo.set_title(
            f"{DOMAIN_TITLES[domain]} — OO When Engaged", fontsize=11, fontweight="bold"
        )
        ax_oo.set_ylim(0, 115)
        ax_oo.yaxis.set_major_formatter(pct_formatter)
        ax_oo.set_ylabel("% outcome optimality")

    # Shared legend
    handles, labels_list = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels_list,
        loc="upper center",
        ncol=2,
        fontsize=10,
        frameon=False,
        bbox_to_anchor=(0.5, 1.02),
    )
    fig.suptitle(
        "Adversarial Requestors: Refusal Rate vs Outcome Quality",
        fontsize=13,
        fontweight="bold",
        y=1.05,
    )
    plt.tight_layout()
    out_path = FIGURES_DIR / "graph8e_refusal_vs_oo_engaged.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
