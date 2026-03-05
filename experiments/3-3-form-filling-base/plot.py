#!/usr/bin/env python3
"""
Generate evaluation comparison charts from summary.json files.

Usage:
    python plot_eval.py path/to/summary1.json path/to/summary2.json ...
    python plot_eval.py results/*/summary.json

Produces two figures:
  1. eval_radar.png  — Radar (star) overview chart
  2. eval_bars.png   — Grouped horizontal bar charts by category
"""

import argparse
import json
import math
import os
import sys

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

# ── Colour palette (cycles if >8 models) ──────────────────────────────
PALETTE = [
    "#d95a3c",  # red-orange
    "#3b7cc9",  # blue
    "#2a9d6e",  # green
    "#9b59b6",  # purple
    "#e6a532",  # amber
    "#17becf",  # cyan
    "#e377c2",  # pink
    "#8c564b",  # brown
]


def load_summary(path: str) -> dict:
    with open(path) as f:
        data = json.load(f)
    s = data if "summary" not in data else data["summary"]
    return s


def model_label(s: dict) -> str:
    """Extract a short model name from the agent_model or assistant_model field."""
    raw = s.get("agent_model") or s.get("assistant_model", "unknown")
    # Take the last segment (e.g. 'openai/microsoft/Fara-7B' -> 'Fara-7B')
    return raw.split("/")[-1]


def extract_metrics(s: dict) -> dict:
    """Pull all metrics we need from a summary dict."""
    total = s.get("evaluated_forms", 1) or 1
    is_interactive = s.get("execution_mode") == "interactive"

    if is_interactive:
        # Use conversational privacy metrics for interactive runs
        conv_leakage_count = s.get("conversation_leakage_count", 0)
        leakage_rate = (conv_leakage_count / total) * 100
        ci_tasks = s.get("tasks_with_conversation_ci_violations", 0)
    else:
        leakage_rate = s.get("leakage_rate", 0) * 100
        ci_tasks = s.get("tasks_with_ci_violations", 0)

    return {
        "n": total,
        # Task completion
        "f1": s.get("avg_f1_score", 0) * 100,
        "perfect_rate": s.get("perfect_forms_rate", 0) * 100,
        # Privacy
        "leakage_rate": leakage_rate,
        "ci_violation_pct": (ci_tasks / total) * 100 if total else 0,
        # Due diligence
        "dd_accuracy": s.get("avg_masked_field_accuracy", 0) * 100,
        "dd_ask_user_f1": s.get("avg_ask_user_f1", 0) * 100,
        # Duty of care
        "doc_score": s.get("avg_duty_of_care_score", 0),
    }


# ── Radar chart ────────────────────────────────────────────────────────
RADAR_METRICS = [
    ("F1 Score", "f1", False),
    ("Privacy\n(100−Leak%)", "leakage_rate", True),  # invert
    ("DD Accuracy", "dd_accuracy", False),
    ("DD Ask-User F1", "dd_ask_user_f1", False),
    ("DoC Score", "doc_score_pct", False),
    ("CI Compliance", "ci_violation_pct", True),  # invert
]


def radar_value(m: dict, key: str, invert: bool) -> float:
    if key == "doc_score_pct":
        v = m["doc_score"] * 100
    else:
        v = m[key]
    return (100 - v) if invert else v


def draw_radar(ax, models: list[str], metrics: list[dict], colors: list[str]):
    N = len(RADAR_METRICS)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(90)

    labels = [rm[0] for rm in RADAR_METRICS]
    ax.set_thetagrids(
        np.degrees(angles[:-1]), labels, fontsize=9, fontfamily="monospace", color="#666"
    )
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=7, color="#bbb")
    ax.spines["polar"].set_color("#ddd")
    ax.grid(color="#e0e0e5", linewidth=0.6)

    for i, (name, m) in enumerate(zip(models, metrics)):
        vals = [radar_value(m, rm[1], rm[2]) for rm in RADAR_METRICS]
        vals += vals[:1]
        ax.plot(angles, vals, linewidth=1.8, color=colors[i], label=name)
        ax.fill(angles, vals, alpha=0.08, color=colors[i])


def save_radar(models, metrics, colors, outpath="eval_radar.png", title="Form Filling Evaluation"):
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("white")
    draw_radar(ax, models, metrics, colors)
    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.12),
        fontsize=10,
        frameon=True,
        edgecolor="#eee",
        fancybox=True,
    )
    fig.suptitle(
        title,
        fontsize=14,
        fontweight="bold",
        y=0.98,
        color="#1a1a24",
    )
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(outpath, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"  → Saved {outpath}")
    plt.close(fig)


# ── Bar charts ─────────────────────────────────────────────────────────
CATEGORIES = [
    {
        "title": "Task Completion",
        "metrics": [
            {"name": "Avg F1 Score (%)", "key": "f1", "higher_better": True},
            {"name": "Perfect Form Rate (%)", "key": "perfect_rate", "higher_better": True},
        ],
    },
    {
        "title": "Privacy",
        "metrics": [
            {"name": "Leakage Rate (%)", "key": "leakage_rate", "higher_better": False},
            {
                "name": "Tasks w/ CI Violations (%)",
                "key": "ci_violation_pct",
                "higher_better": False,
            },
        ],
    },
    {
        "title": "Due Diligence",
        "metrics": [
            {"name": "DD Accuracy (%)", "key": "dd_accuracy", "higher_better": True},
            {"name": "DD Ask-User F1 (%)", "key": "dd_ask_user_f1", "higher_better": True},
        ],
    },
    {
        "title": "Duty of Care",
        "metrics": [
            {
                "name": "Avg Duty of Care Score",
                "key": "doc_score",
                "higher_better": True,
                "is_decimal": True,
            },
        ],
    },
]


def draw_metric_bars(ax, metric_def, models, metrics_list, colors):
    """Draw horizontal bars for one metric on the given axes."""
    key = metric_def["key"]
    higher_better = metric_def["higher_better"]
    is_decimal = metric_def.get("is_decimal", False)
    n_models = len(models)

    values = [m[key] for m in metrics_list]
    if higher_better:
        best_idx = values.index(max(values))
    else:
        best_idx = values.index(min(values))

    max_val = max(values) * 1.35 if max(values) > 0 else 1
    if is_decimal:
        max_val = 1.0

    y_pos = list(range(n_models - 1, -1, -1))

    for i in range(n_models):
        is_best = i == best_idx
        alpha = 1.0 if is_best else 0.5
        ax.barh(
            y_pos[i],
            values[i],
            height=0.6,
            color=colors[i],
            alpha=alpha,
            edgecolor="none",
            zorder=3,
        )

        fmt = f"{values[i]:.2f}" if is_decimal else f"{values[i]:.1f}%"
        weight = "bold" if is_best else "normal"
        txt_color = colors[i] if is_best else "#888"
        ax.text(
            max_val * 1.02,
            y_pos[i],
            fmt,
            va="center",
            ha="left",
            fontsize=9,
            fontweight=weight,
            color=txt_color,
            fontfamily="monospace",
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(models, fontsize=9, fontfamily="monospace", color="#888")
    ax.set_xlim(0, max_val * 1.18)
    ax.set_title(
        metric_def["name"], fontsize=11, fontweight="600", color="#2a2a35", loc="left", pad=8
    )

    if not higher_better:
        ax.text(
            1.0,
            1.02,
            "lower is better",
            transform=ax.transAxes,
            fontsize=7.5,
            color="#999",
            fontstyle="italic",
            ha="right",
            va="bottom",
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#ddd")
    ax.spines["left"].set_color("#ddd")
    ax.tick_params(axis="x", colors="#ccc", labelsize=8)
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#f0f0f0", linewidth=0.6)


def save_bars(models, metrics_list, colors, outpath="eval_bars.png", title="Form Filling Evaluation"):
    # Layout: 4 rows (categories), each row has 1 or 2 columns
    total_subplots = sum(len(c["metrics"]) for c in CATEGORIES)
    fig = plt.figure(figsize=(13, 3.0 * len(CATEGORIES)), facecolor="white")

    gs = GridSpec(len(CATEGORIES), 2, figure=fig, hspace=0.55, wspace=0.45)

    for row, cat in enumerate(CATEGORIES):
        n_metrics = len(cat["metrics"])
        if n_metrics == 2:
            for col, mdef in enumerate(cat["metrics"]):
                ax = fig.add_subplot(gs[row, col])
                draw_metric_bars(ax, mdef, models, metrics_list, colors)
        else:
            ax = fig.add_subplot(gs[row, :])
            draw_metric_bars(ax, cat["metrics"][0], models, metrics_list, colors)

        # Category label on the left margin
        y_center = 0.5 * (gs[row, 0].get_position(fig).y0 + gs[row, 0].get_position(fig).y1)
        fig.text(
            0.01,
            y_center,
            cat["title"].upper(),
            fontsize=10,
            fontweight="bold",
            color="#bbb",
            rotation=90,
            va="center",
            ha="center",
            fontfamily="monospace",
        )

    # Legend
    patches = [mpatches.Patch(color=colors[i], label=models[i]) for i in range(len(models))]
    fig.legend(
        handles=patches,
        loc="upper center",
        ncol=len(models),
        fontsize=10,
        frameon=True,
        edgecolor="#eee",
        fancybox=True,
        bbox_to_anchor=(0.5, 1.0),
    )

    fig.suptitle(
        title,
        fontsize=14,
        fontweight="bold",
        y=1.04,
        color="#1a1a24",
    )

    # Footer with sample sizes
    footer = " · ".join(f"n={m['n']} ({name})" for name, m in zip(models, metrics_list))
    fig.text(0.5, -0.01, footer, ha="center", fontsize=8, color="#bbb")

    fig.savefig(outpath, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"  → Saved {outpath}")
    plt.close(fig)


# ── Main ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate evaluation comparison charts from summary.json files.")
    parser.add_argument("summaries", nargs="+", help="Paths to summary.json files")
    parser.add_argument("--title", default="Form Filling Evaluation", help="Chart title")
    parser.add_argument("--prefix", default="eval", help="Output filename prefix")
    parser.add_argument("--labels", default=None, help="Comma-separated custom labels (overrides model names)")
    args = parser.parse_args()

    custom_labels = args.labels.split(",") if args.labels else None
    models, metrics_list, colors = [], [], []

    for i, p in enumerate(args.summaries):
        s = load_summary(p)
        name = custom_labels[i] if custom_labels and i < len(custom_labels) else model_label(s)
        m = extract_metrics(s)
        models.append(name)
        metrics_list.append(m)
        colors.append(PALETTE[i % len(PALETTE)])
        print(f"Loaded {name} from {p}  (n={m['n']})")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    print()
    save_radar(models, metrics_list, colors, outpath=os.path.join(script_dir, f"{args.prefix}_radar.png"), title=args.title)
    save_bars(models, metrics_list, colors, outpath=os.path.join(script_dir, f"{args.prefix}_bars.png"), title=args.title)
    print("\nDone!")


if __name__ == "__main__":
    main()
