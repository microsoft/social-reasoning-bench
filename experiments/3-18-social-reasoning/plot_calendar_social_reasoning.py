#!/usr/bin/env python3
"""Plot calendar scheduling social reasoning comparison across models and scenarios.

Generates a 3-row x N-model grid of grouped bar charts comparing
Base, ToM, ToM + Examples, Privacy CI, and Privacy Strong on
Task Success Rate, Privacy (leakage rate), Due Diligence, and Duty of Care.

Usage:
    python experiments/3-18-social-reasoning/plot_calendar_social_reasoning.py
"""

import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = Path("outputs/calendar_scheduling/social-reasoning-comparison")

# Map directory model names to display names
MODEL_DISPLAY = {
    "phyagi_gpt_5_1": "GPT 5.1",
    "phyagi_gpt_5_2": "GPT 5.2",
    "openai_Qwen_Qwen3_5_9B": "Qwen 3.5-9B",
}

METRICS = ["Task Success\nRate", "Privacy\n(leakage rate)", "Due\nDiligence", "Duty of\nCare"]

# Row definitions: (row_label, scenario_prefix)
ROWS = [
    ("Benign", "benign"),
    ("Malicious (Hard-Coded)", "malicious_hc"),
    ("Malicious (Whim)", "malicious_whim"),
]


def parse_dir_name(name: str) -> dict | None:
    """Parse experiment directory name into components.

    Patterns:
        benign_nosocial_phyagi_gpt_5_1_n1
        benign_social_phyagi_gpt_5_1_n1
        benign_social_phyagi_gpt_5_1_n1_useexamples
        benign_nosocial_phyagi_gpt_5_1_n1_privacyci
        malicious_hc_nosocial_openai_Qwen_Qwen3_5_9B_n2_privacystrong
    """
    # Check for suffixes
    has_examples = False
    has_privacyci = False
    has_privacystrong = False
    if name.endswith("_useexamples"):
        has_examples = True
        name = name[: -len("_useexamples")]
    elif name.endswith("_privacyci"):
        has_privacyci = True
        name = name[: -len("_privacyci")]
    elif name.endswith("_privacystrong"):
        has_privacystrong = True
        name = name[: -len("_privacystrong")]

    # Extract repeat (last segment)
    parts = name.rsplit("_", 1)
    if len(parts) != 2 or not parts[1].startswith("n"):
        return None
    repeat = parts[1]
    rest = parts[0]

    # Extract scenario
    for scenario in ("malicious_hc", "malicious_whim", "benign"):
        if rest.startswith(f"{scenario}_"):
            rest = rest[len(f"{scenario}_") :]
            break
    else:
        return None

    # Extract social tag
    for social in ("social", "nosocial"):
        if rest.startswith(f"{social}_"):
            rest = rest[len(f"{social}_") :]
            break
    else:
        return None

    model_key = rest

    # Determine condition
    if has_examples:
        condition = "social_example"
    elif has_privacyci:
        condition = "privacy_ci"
    elif has_privacystrong:
        condition = "privacy_strong"
    elif social == "social":
        condition = "social"
    else:
        condition = "nosocial"

    return {
        "scenario": scenario,
        "model_key": model_key,
        "repeat": repeat,
        "condition": condition,
    }


def extract_metrics(data: dict) -> dict:
    """Extract the 4 metrics from an eval.json dict."""
    s = data.get("summary", {})

    success_rate = s.get("task_success_rate", 0.0)
    privacy_leakage = s.get("privacy_leakage_rate", 0.0)
    due_diligence = s.get("due_diligence_avg_preference_mention_count", 0.0)
    duty_of_care = s.get("fiduciary_avg_assistant_duty_of_care_score", 0.0)

    return {
        "success_rate": success_rate,
        "privacy": privacy_leakage,
        "dd": due_diligence,
        "doc": duty_of_care,
    }


def load_all_data() -> dict:
    """Load and organize all experiment data.

    Returns: {(scenario, model_key, condition): [metrics_dict, ...]}
    """
    data = defaultdict(list)

    for exp_dir in sorted(DATA_DIR.iterdir()):
        if not exp_dir.is_dir():
            continue
        parsed = parse_dir_name(exp_dir.name)
        if not parsed:
            continue

        eval_path = exp_dir / "eval.json"
        if not eval_path.exists():
            continue

        with open(eval_path) as f:
            eval_data = json.load(f)

        metrics = extract_metrics(eval_data)
        key = (parsed["scenario"], parsed["model_key"], parsed["condition"])
        data[key].append(metrics)

    return dict(data)


def compute_stats(values: list[float | None]) -> tuple[float, float]:
    """Compute mean and std, ignoring None values."""
    clean = [v for v in values if v is not None]
    if not clean:
        return float("nan"), 0.0
    mean = np.mean(clean)
    std = np.std(clean) if len(clean) > 1 else 0.0
    return float(mean), float(std)


def main():
    data = load_all_data()

    all_models = sorted(
        {k[1] for k in data.keys() if k[1] in MODEL_DISPLAY},
        key=lambda m: list(MODEL_DISPLAY.keys()).index(m),
    )

    if not all_models:
        print("No data found!")
        return

    n_models = len(all_models)
    metric_keys = ["success_rate", "privacy", "dd", "doc"]

    # 5 conditions
    CONDITIONS = [
        ("nosocial", "Base", "#6baed6"),
        ("social", "ToM", "#fd8d3c"),
        ("social_example", "ToM + Examples", "#74c476"),
        ("privacy_ci", "Privacy CI", "#e377c2"),
        ("privacy_strong", "Privacy Strong", "#bcbd22"),
    ]

    fig, axes = plt.subplots(
        len(ROWS),
        n_models,
        figsize=(4.5 * n_models, 3.5 * len(ROWS)),
        squeeze=False,
    )

    bar_width = 0.15
    x = np.arange(len(METRICS))

    for row_idx, (row_label, scenario) in enumerate(ROWS):
        for col_idx, model_key in enumerate(all_models):
            ax = axes[row_idx][col_idx]

            # Gather data for all conditions
            cond_data = {}
            for cond_key, _, _ in CONDITIONS:
                cond_data[cond_key] = data.get((scenario, model_key, cond_key), [])

            has_data = any(bool(v) for v in cond_data.values())

            if not has_data:
                ax.text(
                    0.5,
                    0.5,
                    "No data",
                    ha="center",
                    va="center",
                    transform=ax.transAxes,
                    fontsize=11,
                    color="gray",
                )
                ax.set_xticks(x)
                ax.set_xticklabels(METRICS, fontsize=8)
                ax.set_ylim(0, 1.1)
            else:
                for i, (cond_key, cond_label, cond_color) in enumerate(CONDITIONS):
                    cd = cond_data[cond_key]
                    if not cd:
                        continue

                    means, stds = [], []
                    for mk in metric_keys:
                        m, s = compute_stats([d[mk] for d in cd])
                        means.append(m)
                        stds.append(s)

                    offset = (i - 2) * bar_width
                    bars = ax.bar(
                        x + offset,
                        means,
                        bar_width,
                        yerr=stds,
                        label=cond_label,
                        color=cond_color,
                        capsize=3,
                        edgecolor="white",
                        linewidth=0.5,
                    )
                    for bar, val in zip(bars, means):
                        if not np.isnan(val):
                            ax.text(
                                bar.get_x() + bar.get_width() / 2,
                                bar.get_height() + 0.02,
                                f"{val:.2f}",
                                ha="center",
                                va="bottom",
                                fontsize=6,
                            )

                ax.set_xticks(x)
                ax.set_xticklabels(METRICS, fontsize=8)
                ax.set_ylim(0, 1.1)

            if col_idx == 0:
                ax.set_ylabel(row_label, fontsize=10, fontweight="bold")

            if row_idx == 0:
                ax.set_title(
                    MODEL_DISPLAY.get(model_key, model_key), fontsize=11, fontweight="bold"
                )

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.tick_params(axis="y", labelsize=8)

            counts = "/".join(str(len(cond_data[ck])) for ck, _, _ in CONDITIONS)
            ax.text(
                0.98,
                0.98,
                f"n={counts}",
                ha="right",
                va="top",
                transform=ax.transAxes,
                fontsize=7,
                color="gray",
            )

    # Shared legend
    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=color, label=label) for _, label, color in CONDITIONS
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        ncol=5,
        fontsize=10,
        frameon=False,
        bbox_to_anchor=(0.5, 1.0),
    )

    fig.suptitle(
        "Calendar Scheduling: Social Reasoning Comparison",
        fontsize=14,
        fontweight="bold",
        y=1.03,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    out_path = Path(__file__).parent / "calendar_social_reasoning_comparison.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
