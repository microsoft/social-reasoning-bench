"""Claim 5 variant: OO benign vs adversarial (merged hand-crafted + whimsical).

Uses continuous benign OO formula. Combines all malicious conditions into one
"Adversarial Requestor" bar.
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

from common import RESULTS_DIR, FIGURES_DIR, get_model, load_results_dirs
from benign_oo import (
    benign_outcome_optimality,
    load_calendar_results,
    load_marketplace_results,
)

MODELS = ["GPT-4.1", "GPT-5.4", "Gemini"]
DOMAINS = ["calendar", "marketplace"]
DOMAIN_TITLES = {"calendar": "Calendar", "marketplace": "Marketplace"}
CONDITIONS = ["benign", "adversarial"]
COLORS = {"benign": "#66bb6a", "adversarial": "#ef5350"}
LABELS = {"benign": "Benign Requestor", "adversarial": "Adversarial Requestor"}


def _get_attack_style(cfg: dict) -> str:
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
    
    # Collect per-task OO keyed by (domain, model, condition)
    data: dict[tuple[str, str, str], list[float]] = {}
    
    for d in dirs:
        results_data = json.loads((d / "results.json").read_text())
        cfg = results_data.get("config") or {}
        domain = "calendar" if "calendar" in d.name else "marketplace"
        model = get_model(d.name)
        attack_style = _get_attack_style(cfg)
        condition = "benign" if attack_style == "normal" else "adversarial"
        
        if domain == "marketplace":
            typed_results = load_marketplace_results(results_data)
        elif domain == "calendar":
            typed_results = load_calendar_results(results_data)
        else:
            continue
        
        for r in typed_results:
            oo = benign_outcome_optimality(r)
            if oo is not None:
                data.setdefault((domain, model, condition), []).append(oo)

    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    bar_width = 0.3
    pct_formatter = FuncFormatter(lambda x, _: f"{x:.0f}%")

    for ax, domain in zip(axes, DOMAINS):
        x = np.arange(len(MODELS))
        for i, cond in enumerate(CONDITIONS):
            vals = []
            for model in MODELS:
                scores = data.get((domain, model, cond), [])
                vals.append(np.mean(scores) * 100 if scores else 0)
            offset = (i - 0.5) * bar_width
            bars = ax.bar(x + offset, vals, bar_width, label=LABELS[cond], color=COLORS[cond])
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + 1, f"{h:.0f}%",
                        ha="center", va="bottom", fontsize=8, fontweight="bold")

        ax.set_xticks(x)
        ax.set_xticklabels(MODELS, fontsize=10)
        ax.set_title(DOMAIN_TITLES[domain], fontsize=12)
        ax.set_ylim(0, 115)
        ax.yaxis.set_major_formatter(pct_formatter)

    handles, labels_list = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels_list, loc="upper center", ncol=len(labels_list), fontsize=10,
               frameon=False, bbox_to_anchor=(0.5, 1.02))
    fig.suptitle("Outcome Optimality: Benign vs Adversarial Requestors",
                 fontsize=12, fontweight="bold", y=1.06)
    plt.tight_layout()
    out_path = FIGURES_DIR / "graph8b_oo_adversary_merged.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
