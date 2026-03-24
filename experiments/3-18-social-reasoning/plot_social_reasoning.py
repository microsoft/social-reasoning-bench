#!/usr/bin/env python3
"""Plot social reasoning comparison across models and scenarios.

Generates a 3-row x N-model grid of grouped bar charts comparing
base vs. social reasoning on F1, Privacy (violation rate), Due Diligence,
and Duty of Care.

Usage:
    python -m sage_benchmark.form_filling.plot_social_reasoning
"""

import glob
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = Path("outputs/form_filling/social-reasoning-comparison")

# Map directory model names to display names
MODEL_DISPLAY = {
    "phyagi_gpt_5_1": "GPT 5.1",
    "phyagi_gpt_5_2": "GPT 5.2",
    "openai_Qwen_Qwen3_5_9B": "Qwen 3.5-9B",
}

METRICS = ["F1", "Privacy\n(violation rate)", "Due\nDiligence", "Duty of\nCare"]

# Row definitions: (row_label, scenario, mode)
ROWS = [
    ("Form Filling (One-Shot)", "base", "oneshot"),
    ("Interview (Base)", "base", "interactive"),
    ("Interview (Malicious)", "malicious", "interactive"),
]


def parse_dir_name(name: str) -> dict | None:
    """Parse experiment directory name into components."""
    # Pattern: {scenario}_{social}_{provider}_{model}_{mode}_{n}
    # Examples:
    #   base_nosocial_phyagi_gpt_5_2_oneshot_n1
    #   malicious_social_openai_Qwen_Qwen3_5_9B_interactive_n2
    # Check for suffixes
    has_examples = False
    has_privacyci = False
    has_privacyexplained = False
    if name.endswith("_useexamples"):
        has_examples = True
        name = name[: -len("_useexamples")]
    elif name.endswith("_privacyci"):
        has_privacyci = True
        name = name[: -len("_privacyci")]
    elif name.endswith("_privacyexplained"):
        has_privacyexplained = True
        name = name[: -len("_privacyexplained")]

    parts = name.rsplit("_", 1)
    if len(parts) != 2 or not parts[1].startswith("n"):
        return None
    repeat = parts[1]
    rest = parts[0]

    # Extract mode (last segment before repeat)
    for mode in ("oneshot", "interactive"):
        if rest.endswith(f"_{mode}"):
            rest = rest[: -len(f"_{mode}")]
            break
    else:
        return None

    # Extract scenario
    for scenario in ("base", "malicious"):
        if rest.startswith(f"{scenario}_"):
            rest = rest[len(f"{scenario}_") :]
            break
    else:
        return None

    # Extract social
    for social in ("social", "nosocial"):
        if rest.startswith(f"{social}_"):
            rest = rest[len(f"{social}_") :]
            break
    else:
        return None

    model_key = rest  # e.g. "phyagi_gpt_5_2" or "openai_Qwen_Qwen3_5_9B"

    # Override social label for suffix directories
    if has_examples:
        social = "social_example"
    elif has_privacyci:
        social = "privacy_ci"
    elif has_privacyexplained:
        social = "privacy_explained"

    return {
        "scenario": scenario,
        "social": social,
        "model_key": model_key,
        "mode": mode,
        "repeat": repeat,
    }


def extract_metrics(summary: dict, mode: str) -> dict:
    """Extract the 4 metrics from a summary dict."""
    s = summary.get("summary", {})
    successful = s.get("successful_executions", 1) or 1

    f1 = s.get("avg_f1_score")

    if mode == "oneshot":
        privacy_violations = s.get("leakage_count", 0)
    else:
        privacy_violations = s.get("conversation_leakage_count", 0)
    privacy_rate = privacy_violations / successful

    dd = s.get("avg_masked_field_accuracy")
    doc = s.get("avg_duty_of_care_score")

    return {"f1": f1, "privacy": privacy_rate, "dd": dd, "doc": doc}


def load_all_data() -> dict:
    """Load and organize all experiment data.

    Returns: {(scenario, mode, model_key, social): [metrics_dict, ...]}
    """
    data = defaultdict(list)

    for exp_dir in sorted(DATA_DIR.iterdir()):
        if not exp_dir.is_dir():
            continue
        parsed = parse_dir_name(exp_dir.name)
        if not parsed:
            continue

        # Find summary.json
        summaries = list(exp_dir.glob("run_*/summary.json"))
        if not summaries:
            continue

        with open(summaries[0]) as f:
            summary = json.load(f)

        metrics = extract_metrics(summary, parsed["mode"])
        key = (parsed["scenario"], parsed["mode"], parsed["model_key"], parsed["social"])
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

    # Determine which models have data for any row
    all_models = sorted(
        {k[2] for k in data.keys() if k[2] in MODEL_DISPLAY},
        key=lambda m: list(MODEL_DISPLAY.keys()).index(m),
    )

    if not all_models:
        print("No data found!")
        return

    n_models = len(all_models)
    metric_keys = ["f1", "privacy", "dd", "doc"]

    fig, axes = plt.subplots(
        len(ROWS),
        n_models,
        figsize=(4.5 * n_models, 3.5 * len(ROWS)),
        squeeze=False,
    )

    bar_width = 0.15
    x = np.arange(len(METRICS))
    colors_base = "#6baed6"
    colors_social = "#fd8d3c"
    colors_example = "#74c476"
    colors_privacyci = "#e377c2"
    colors_privacyexplained = "#bcbd22"

    for row_idx, (row_label, scenario, mode) in enumerate(ROWS):
        for col_idx, model_key in enumerate(all_models):
            ax = axes[row_idx][col_idx]

            key_nosocial = (scenario, mode, model_key, "nosocial")
            key_social = (scenario, mode, model_key, "social")
            key_example = (scenario, mode, model_key, "social_example")
            key_privacyci = (scenario, mode, model_key, "privacy_ci")
            key_privacyexplained = (scenario, mode, model_key, "privacy_explained")

            nosocial_data = data.get(key_nosocial, [])
            social_data = data.get(key_social, [])
            example_data = data.get(key_example, [])
            privacyci_data = data.get(key_privacyci, [])
            privacyexplained_data = data.get(key_privacyexplained, [])

            has_data = (
                bool(nosocial_data)
                or bool(social_data)
                or bool(example_data)
                or bool(privacyci_data)
                or bool(privacyexplained_data)
            )

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
                nosocial_means, nosocial_stds = [], []
                social_means, social_stds = [], []
                example_means, example_stds = [], []
                privacyci_means, privacyci_stds = [], []
                privacyexplained_means, privacyexplained_stds = [], []

                for mk in metric_keys:
                    nm, ns = compute_stats([d[mk] for d in nosocial_data])
                    sm, ss = compute_stats([d[mk] for d in social_data])
                    em, es = compute_stats([d[mk] for d in example_data])
                    pm, ps = compute_stats([d[mk] for d in privacyci_data])
                    pem, pes = compute_stats([d[mk] for d in privacyexplained_data])
                    nosocial_means.append(nm)
                    nosocial_stds.append(ns)
                    social_means.append(sm)
                    social_stds.append(ss)
                    example_means.append(em)
                    example_stds.append(es)
                    privacyci_means.append(pm)
                    privacyci_stds.append(ps)
                    privacyexplained_means.append(pem)
                    privacyexplained_stds.append(pes)

                if nosocial_data:
                    bars1 = ax.bar(
                        x - 2 * bar_width,
                        nosocial_means,
                        bar_width,
                        yerr=nosocial_stds,
                        label="Base",
                        color=colors_base,
                        capsize=3,
                        edgecolor="white",
                        linewidth=0.5,
                    )
                    for bar, val in zip(bars1, nosocial_means):
                        if not np.isnan(val):
                            ax.text(
                                bar.get_x() + bar.get_width() / 2,
                                bar.get_height() + 0.02,
                                f"{val:.2f}",
                                ha="center",
                                va="bottom",
                                fontsize=6,
                            )

                if social_data:
                    bars2 = ax.bar(
                        x - 1 * bar_width,
                        social_means,
                        bar_width,
                        yerr=social_stds,
                        label="ToM",
                        color=colors_social,
                        capsize=3,
                        edgecolor="white",
                        linewidth=0.5,
                    )
                    for bar, val in zip(bars2, social_means):
                        if not np.isnan(val):
                            ax.text(
                                bar.get_x() + bar.get_width() / 2,
                                bar.get_height() + 0.02,
                                f"{val:.2f}",
                                ha="center",
                                va="bottom",
                                fontsize=6,
                            )

                if example_data:
                    bars3 = ax.bar(
                        x,
                        example_means,
                        bar_width,
                        yerr=example_stds,
                        label="ToM + Examples",
                        color=colors_example,
                        capsize=3,
                        edgecolor="white",
                        linewidth=0.5,
                    )
                    for bar, val in zip(bars3, example_means):
                        if not np.isnan(val):
                            ax.text(
                                bar.get_x() + bar.get_width() / 2,
                                bar.get_height() + 0.02,
                                f"{val:.2f}",
                                ha="center",
                                va="bottom",
                                fontsize=6,
                            )

                if privacyci_data:
                    bars4 = ax.bar(
                        x + 1 * bar_width,
                        privacyci_means,
                        bar_width,
                        yerr=privacyci_stds,
                        label="Privacy CI",
                        color=colors_privacyci,
                        capsize=3,
                        edgecolor="white",
                        linewidth=0.5,
                    )
                    for bar, val in zip(bars4, privacyci_means):
                        if not np.isnan(val):
                            ax.text(
                                bar.get_x() + bar.get_width() / 2,
                                bar.get_height() + 0.02,
                                f"{val:.2f}",
                                ha="center",
                                va="bottom",
                                fontsize=6,
                            )

                if privacyexplained_data:
                    bars5 = ax.bar(
                        x + 2 * bar_width,
                        privacyexplained_means,
                        bar_width,
                        yerr=privacyexplained_stds,
                        label="Privacy Explained",
                        color=colors_privacyexplained,
                        capsize=3,
                        edgecolor="white",
                        linewidth=0.5,
                    )
                    for bar, val in zip(bars5, privacyexplained_means):
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

            # Row label on leftmost column
            if col_idx == 0:
                ax.set_ylabel(row_label, fontsize=10, fontweight="bold")

            # Model name on top row
            if row_idx == 0:
                ax.set_title(
                    MODEL_DISPLAY.get(model_key, model_key), fontsize=11, fontweight="bold"
                )

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.tick_params(axis="y", labelsize=8)

            # Show repeat counts as annotation
            n_base = len(nosocial_data)
            n_social = len(social_data)
            n_example = len(example_data)
            n_privacyci = len(privacyci_data)
            n_privacyexplained = len(privacyexplained_data)
            ax.text(
                0.98,
                0.98,
                f"n={n_base}/{n_social}/{n_example}/{n_privacyci}/{n_privacyexplained}",
                ha="right",
                va="top",
                transform=ax.transAxes,
                fontsize=7,
                color="gray",
            )

    # Shared legend
    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=colors_base, label="Base"),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors_social, label="ToM"),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors_example, label="ToM + Examples"),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors_privacyci, label="Privacy CI"),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors_privacyexplained, label="Privacy Explained"),
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
        "Social Reasoning Comparison",
        fontsize=14,
        fontweight="bold",
        y=1.03,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    out_path = Path(__file__).parent / "social_reasoning_comparison.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved: {out_path}")
    plt.close(fig)


if __name__ == "__main__":
    main()
