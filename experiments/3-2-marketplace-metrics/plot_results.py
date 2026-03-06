#!/usr/bin/env python3
"""Plot all per-task marketplace metrics from the new evaluation output.

Usage:
    uv run experiments/3-2-marketplace-metrics/plot_results.py
    uv run experiments/3-2-marketplace-metrics/plot_results.py --input-dir outputs/marketplace/3-2-marketplace-metrics
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR_DEFAULT = "experiments/3-2-marketplace-metrics"
INPUT_DIR_DEFAULT = "outputs/marketplace/3-2-marketplace-metrics"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot marketplace per-task metrics.")
    parser.add_argument("--input-dir", default=INPUT_DIR_DEFAULT)
    parser.add_argument("--output-dir", default=OUTPUT_DIR_DEFAULT)
    return parser.parse_args()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Data extraction helpers
# ---------------------------------------------------------------------------


def _extract_variant_data(summary: dict) -> list[dict]:
    """For each variant in summary.json, load the results and extract metrics."""
    variants = []
    for run in summary.get("runs", []):
        results_path = Path(run["results_path"])
        if not results_path.exists():
            print(f"WARNING: {results_path} not found, skipping {run['variant']}")
            continue
        payload = _load_json(results_path)
        evals = [item["evaluation"] for item in payload.get("results", [])]
        variants.append(
            {
                "name": run["variant"],
                "deal_rate": run.get("summary", {}).get("deal_rate", 0),
                "evals": evals,
            }
        )
    return variants


def _collect_metric(evals: list[dict], key: str) -> list[float]:
    """Collect non-None values for a top-level metric key."""
    return [e[key] for e in evals if e.get(key) is not None]


def _collect_role_metric(evals: list[dict], role: str, key: str) -> list[float]:
    """Collect non-None values for a nested role metric."""
    return [
        e[f"{role}_metrics"][key]
        for e in evals
        if e.get(f"{role}_metrics", {}).get(key) is not None
    ]


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

COLORS = ["#4c78a8", "#f58518", "#54a24b", "#e45756", "#72b7b2", "#eeca3b"]


def _boxplot_metric(
    ax: plt.Axes,
    data_per_variant: list[list[float]],
    labels: list[str],
    title: str,
    ylabel: str,
    *,
    hlines: dict[float, str] | None = None,
    ylim: tuple[float, float] | None = None,
) -> None:
    """Draw a boxplot with overlaid jittered scatter points."""
    if not data_per_variant or all(len(d) == 0 for d in data_per_variant):
        ax.set_title(f"{title}\n(no data)")
        return

    # Clip data for display if ylim is set; count outliers
    display_data = []
    n_clipped = 0
    for values in data_per_variant:
        if ylim is not None:
            clipped = [v for v in values if ylim[0] <= v <= ylim[1]]
            n_clipped += len(values) - len(clipped)
            display_data.append(clipped)
        else:
            display_data.append(values)

    positions = list(range(1, len(display_data) + 1))
    bp = ax.boxplot(
        display_data,
        positions=positions,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "black", "linewidth": 1.5},
        widths=0.5,
    )
    for i, patch in enumerate(bp["boxes"]):
        patch.set_facecolor(COLORS[i % len(COLORS)])
        patch.set_alpha(0.45)

    # Jittered scatter overlay
    for i, values in enumerate(display_data):
        if not values:
            continue
        jitter = np.random.default_rng(42).uniform(-0.12, 0.12, size=len(values))
        ax.scatter(
            np.full(len(values), positions[i]) + jitter,
            values,
            color=COLORS[i % len(COLORS)],
            alpha=0.5,
            s=18,
            zorder=3,
        )

    if hlines:
        for y, style in hlines.items():
            ax.axhline(y, color="gray", linestyle=style, linewidth=0.8, alpha=0.6)

    if ylim is not None:
        ax.set_ylim(ylim)

    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=9)
    suffix = f"\n({n_clipped} outlier(s) clipped)" if n_clipped else ""
    ax.set_title(f"{title}{suffix}", fontsize=11)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(axis="y", alpha=0.25)


def _paired_boxplot(
    ax: plt.Axes,
    buyer_data: list[list[float]],
    seller_data: list[list[float]],
    variant_labels: list[str],
    title: str,
    ylabel: str,
    *,
    hlines: dict[float, str] | None = None,
    ylim: tuple[float, float] | None = None,
) -> None:
    """Draw paired buyer/seller box plots for each variant."""
    n = len(variant_labels)
    if n == 0:
        return

    # Clip if needed
    def _clip(data: list[list[float]]) -> tuple[list[list[float]], int]:
        if ylim is None:
            return data, 0
        clipped_data, total = [], 0
        for vals in data:
            c = [v for v in vals if ylim[0] <= v <= ylim[1]]
            total += len(vals) - len(c)
            clipped_data.append(c)
        return clipped_data, total

    b_data, b_clip = _clip(buyer_data)
    s_data, s_clip = _clip(seller_data)
    n_clipped = b_clip + s_clip

    width = 0.3
    rng = np.random.default_rng(42)
    for i in range(n):
        pos_b, pos_s = i * 1.0 - 0.18, i * 1.0 + 0.18
        for data, pos, color, label in [
            (b_data[i], pos_b, COLORS[0], "Buyer" if i == 0 else None),
            (s_data[i], pos_s, COLORS[1], "Seller" if i == 0 else None),
        ]:
            if not data:
                continue
            bp = ax.boxplot(
                [data],
                positions=[pos],
                widths=width,
                patch_artist=True,
                showfliers=False,
                medianprops={"color": "black", "linewidth": 1.5},
            )
            bp["boxes"][0].set_facecolor(color)
            bp["boxes"][0].set_alpha(0.45)
            jitter = rng.uniform(-0.06, 0.06, size=len(data))
            ax.scatter(
                np.full(len(data), pos) + jitter,
                data,
                color=color,
                alpha=0.5,
                s=14,
                zorder=3,
                label=label,
            )

    if hlines:
        for y, style in hlines.items():
            ax.axhline(y, color="gray", linestyle=style, linewidth=0.8, alpha=0.6)
    if ylim is not None:
        ax.set_ylim(ylim)

    ax.set_xticks([i * 1.0 for i in range(n)])
    ax.set_xticklabels(variant_labels, fontsize=9)
    suffix = f"\n({n_clipped} clipped)" if n_clipped else ""
    ax.set_title(f"{title}{suffix}", fontsize=11)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(axis="y", alpha=0.25)


def plot_all(variants: list[dict], output_dir: Path) -> None:
    labels = [v["name"] for v in variants]
    deal_rates_str = ", ".join(f"{v['name']}: {v['deal_rate'] * 100:.1f}%" for v in variants)

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # ── Privacy: buyer vs seller inference error ──
    _paired_boxplot(
        axes[0][0],
        [_collect_metric(v["evals"], "buyer_inference_error") for v in variants],
        [_collect_metric(v["evals"], "seller_inference_error") for v in variants],
        labels,
        "Privacy: Inference Error\n(lower = more leakage)",
        "Error (|estimate - actual| / ZOPA)",
        hlines={1.0: "--"},
    )

    # ── Duty of care: deal ratio centered ──
    _boxplot_metric(
        axes[0][1],
        [_collect_metric(v["evals"], "deal_ratio_centered") for v in variants],
        labels,
        "Duty of Care: Deal Position\n(-1 = buyer favored, +1 = seller favored)",
        "Ratio [-1, +1]",
        hlines={0.0: "-", -1.0: "--", 1.0: "--"},
        ylim=(-2.0, 2.0),
    )

    # ── Due diligence: offer count ──
    _paired_boxplot(
        axes[1][0],
        [_collect_role_metric(v["evals"], "buyer", "offer_count") for v in variants],
        [_collect_role_metric(v["evals"], "seller", "offer_count") for v in variants],
        labels,
        "Due Diligence: Offer Count",
        "Count",
    )

    # ── Due diligence: price range explored ──
    _paired_boxplot(
        axes[1][1],
        [_collect_role_metric(v["evals"], "buyer", "price_range_explored") for v in variants],
        [_collect_role_metric(v["evals"], "seller", "price_range_explored") for v in variants],
        labels,
        "Due Diligence: Price Range Explored\n(max - min offer) / ZOPA",
        "Range / ZOPA",
        ylim=(0.0, 3.0),
    )

    fig.suptitle(f"Marketplace Metrics  |  Deal Rate: {deal_rates_str}", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_dir / "results.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {output_dir / 'results.png'}")


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = input_dir / "summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(
            f"No summary.json found at {summary_path}. Run the experiment first."
        )

    summary = _load_json(summary_path)
    variants = _extract_variant_data(summary)
    if not variants:
        raise ValueError("No variant data found")

    plot_all(variants, output_dir)


if __name__ == "__main__":
    main()
