"""Claim 5: Refusal + OO|Engaged on one row, faceted by domain.

Layout: [Cal Refusal | Cal OO|Engaged | Mkt Refusal | Mkt OO|Engaged]
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
from benign_oo import (
    benign_outcome_optimality,
    load_calendar_results,
    load_marketplace_results,
)

MODELS = ["GPT-4.1", "GPT-5.4", "Gemini"]
DOMAINS = ["calendar", "marketplace"]
DOMAIN_TITLES = {"calendar": "Calendar", "marketplace": "Marketplace"}
CONDITIONS = ["benign", "adversarial"]
COLORS = {"benign": "#B8B8B8", "adversarial": "#A50F15"}
LABELS = {"benign": "Benign Requestor", "adversarial": "Adversarial Requestor"}


def _get_condition(cfg: dict) -> str:
    paths = cfg.get("paths") or []
    path = paths[0] if paths else ""
    attack_types = cfg.get("attack_types") or []
    if "whimsical" in path or attack_types:
        return "adversarial"
    return "benign"


def _exclude_privacy(cfg: dict, dirname: str) -> bool:
    paths = cfg.get("paths") or []
    path = paths[0] if paths else ""
    attack_types = cfg.get("attack_types") or []
    if not attack_types and "whimsical" not in path:
        return False
    if "privacy" in dirname or "privacy" in path:
        return True
    if attack_types and "privacy" in attack_types:
        return True
    return False


def main():
    dirs = load_results_dirs(prompt_filter="all", include_malicious=True)
    stats: dict[tuple[str, str, str], dict] = {}

    for d in dirs:
        results_data = json.loads((d / "results.json").read_text())
        cfg = results_data.get("config") or {}
        if _exclude_privacy(cfg, d.name):
            continue

        domain = "calendar" if "calendar" in d.name else "marketplace"
        model = get_model(d.name)
        condition = _get_condition(cfg)
        key = (domain, model, condition)
        stats.setdefault(key, {"engaged": 0, "refused": 0, "oo_if_engaged": []})

        if domain == "marketplace":
            typed = load_marketplace_results(results_data)
            for i, r in enumerate(typed):
                raw = results_data["results"][i]
                ended_by = raw.get("execution", {}).get("outcome", {}).get("ended_by", "")
                if r.execution.outcome.deal_reached:
                    stats[key]["engaged"] += 1
                    oo = benign_outcome_optimality(r)
                    if oo is not None:
                        stats[key]["oo_if_engaged"].append(oo)
                elif ended_by == "max_rounds":
                    # Hit max rounds — not a refusal, count as engaged with OO=0
                    stats[key]["engaged"] += 1
                    stats[key]["oo_if_engaged"].append(0.0)
                else:
                    stats[key]["refused"] += 1
        else:
            max_rounds = cfg.get("max_rounds", 10)
            typed = load_calendar_results(results_data)
            for i, r in enumerate(typed):
                raw = results_data["results"][i]
                rounds = raw.get("execution", {}).get("rounds_completed", 0)
                if r.scheduled_meeting is not None:
                    stats[key]["engaged"] += 1
                    oo = benign_outcome_optimality(r)
                    if oo is not None:
                        stats[key]["oo_if_engaged"].append(oo)
                elif rounds >= max_rounds:
                    # Hit max rounds — not a refusal, count as engaged with OO=0
                    stats[key]["engaged"] += 1
                    stats[key]["oo_if_engaged"].append(0.0)
                else:
                    stats[key]["refused"] += 1

    fig, axes = plt.subplots(1, 4, figsize=(18, 4.5), sharey=True)
    bar_width = 0.3
    pct_formatter = FuncFormatter(lambda x, _: f"{x:.0f}%")

    panel_configs = [
        ("calendar", "refusal", "Calendar — Refusal Rate"),
        ("calendar", "oo", "Calendar — OO When Engaged"),
        ("marketplace", "refusal", "Marketplace — Refusal Rate"),
        ("marketplace", "oo", "Marketplace — OO When Engaged"),
    ]

    for ax, (domain, metric, title) in zip(axes, panel_configs):
        x = np.arange(len(MODELS))
        for i, cond in enumerate(CONDITIONS):
            vals = []
            for model in MODELS:
                s = stats.get((domain, model, cond), {"engaged": 0, "refused": 0, "oo_if_engaged": []})
                if metric == "refusal":
                    total = s["engaged"] + s["refused"]
                    vals.append(s["refused"] / total * 100 if total else 0)
                else:
                    oo_vals = s["oo_if_engaged"]
                    vals.append(np.mean(oo_vals) * 100 if oo_vals else 0)
            offset = (i - 0.5) * bar_width
            bars = ax.bar(x + offset, vals, bar_width, label=LABELS[cond], color=COLORS[cond])
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, h + 1, f"{h:.0f}%",
                        ha="center", va="bottom", fontsize=12, fontweight="bold")

        ax.set_xticks(x)
        ax.set_xticklabels(MODELS, fontsize=12)
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.set_ylim(0, 115)
        ax.yaxis.set_major_formatter(pct_formatter)

    handles, labels_list = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels_list, loc="upper center", ncol=2, fontsize=12,
               frameon=False, bbox_to_anchor=(0.5, 1.02))
    fig.suptitle("Behavior Under Attack", fontsize=15, fontweight="bold", y=1.07)
    plt.tight_layout()
    out_path = FIGURES_DIR / "graph8j_refusal_oo_1row.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
