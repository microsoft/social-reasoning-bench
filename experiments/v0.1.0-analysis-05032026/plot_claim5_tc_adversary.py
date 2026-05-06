"""Claim 5: Task Completion under attack.

Generates two figures:
- graph8c_tc_by_adversary.png: benign vs hand-crafted vs whimsical
- graph8d_tc_adversary_merged.png: benign vs adversarial (merged)
"""
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUR_DIR = Path(__file__).resolve().parent
PLOTTING_DIR = Path(__file__).resolve().parents[1] / "v0.1.0" / "plotting"
sys.path.insert(0, str(OUR_DIR))
sys.path.insert(1, str(PLOTTING_DIR))

from common import FIGURES_DIR, get_model, load_results_dirs
from benign_oo import load_calendar_results, load_marketplace_results

MODELS = ["GPT-4.1", "GPT-5.4", "Gemini"]
DOMAINS = ["calendar", "marketplace"]
DOMAIN_TITLES = {"calendar": "Calendar", "marketplace": "Marketplace"}


def _get_attack_style(cfg: dict) -> str:
    paths = cfg.get("paths") or []
    path = paths[0] if paths else ""
    attack_types = cfg.get("attack_types") or []
    if "whimsical" in path:
        return "whimsical"
    elif attack_types:
        return "hand_crafted"
    return "normal"


def _load_tc_data():
    """Load task completion per (domain, model, attack_style)."""
    dirs = load_results_dirs(prompt_filter="all", include_malicious=True)
    data: dict[tuple[str, str, str], list[float]] = {}

    for d in dirs:
        results_data = json.loads((d / "results.json").read_text())
        cfg = results_data.get("config") or {}
        domain = "calendar" if "calendar" in d.name else "marketplace"
        model = get_model(d.name)
        attack_style = _get_attack_style(cfg)

        if domain == "marketplace":
            typed = load_marketplace_results(results_data)
        else:
            typed = load_calendar_results(results_data)

        for r in typed:
            data.setdefault((domain, model, attack_style), []).append(float(r.task_completed))

    return data


def _plot_bars(data, conditions, colors, labels, title, filename):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    n_conds = len(conditions)
    bar_width = 0.7 / n_conds
    pct_formatter = FuncFormatter(lambda x, _: f"{x:.0f}%")

    for ax, domain in zip(axes, DOMAINS):
        x = np.arange(len(MODELS))
        for i, cond in enumerate(conditions):
            vals = []
            for model in MODELS:
                scores = data.get((domain, model, cond), [])
                vals.append(np.mean(scores) * 100 if scores else 0)
            offset = (i - (n_conds - 1) / 2) * bar_width
            bars = ax.bar(x + offset, vals, bar_width, label=labels[cond], color=colors[cond])
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + 1, f"{h:.0f}%",
                        ha="center", va="bottom", fontsize=7, fontweight="bold")

        ax.set_xticks(x)
        ax.set_xticklabels(MODELS, fontsize=10)
        ax.set_title(DOMAIN_TITLES[domain], fontsize=12)
        ax.set_ylim(0, 115)
        ax.yaxis.set_major_formatter(pct_formatter)

    handles, labels_list = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels_list, loc="upper center", ncol=len(labels_list), fontsize=9,
               frameon=False, bbox_to_anchor=(0.5, 1.02))
    fig.suptitle(title, fontsize=12, fontweight="bold", y=1.06)
    plt.tight_layout()
    out_path = FIGURES_DIR / filename
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


def main():
    raw_data = _load_tc_data()

    # Version 1: three-way split
    _plot_bars(
        raw_data,
        conditions=["normal", "hand_crafted", "whimsical"],
        colors={"normal": "#66bb6a", "hand_crafted": "#ef5350", "whimsical": "#ffa726"},
        labels={"normal": "Benign", "hand_crafted": "Hand-Crafted", "whimsical": "Whimsical"},
        title="Task Completion Under Attack (Defensive Prompt)",
        filename="graph8c_tc_by_adversary.png",
    )

    # Version 2: merged adversarial
    merged_data = {}
    for (domain, model, style), vals in raw_data.items():
        cond = "benign" if style == "normal" else "adversarial"
        merged_data.setdefault((domain, model, cond), []).extend(vals)

    _plot_bars(
        merged_data,
        conditions=["benign", "adversarial"],
        colors={"benign": "#66bb6a", "adversarial": "#ef5350"},
        labels={"benign": "Benign Requestor", "adversarial": "Adversarial Requestor"},
        title="Task Completion: Benign vs Adversarial Requestors",
        filename="graph8d_tc_adversary_merged.png",
    )


if __name__ == "__main__":
    main()
