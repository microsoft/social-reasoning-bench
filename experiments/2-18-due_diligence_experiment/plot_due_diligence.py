#!/usr/bin/env python3
"""Plot due diligence vs optimality scatter plot.

Computes due diligence metrics (message count, preference mentions, proposals)
from raw execution data and plots against optimality (duty of care score).

Download Data:
    uv run sync.py download 2-2-calendar_duty_of_care outputs/calendar_scheduling/2-2-calendar_duty_of_care
    uv run sync.py download 2-4-simexple-prefs outputs/calendar_scheduling/2-4-simple-prefs/ 
    uv run sync.py download 2-10-negotiation outputs/calendar_scheduling/2-10-negotiation/

Usage:
    uv run experiments/2-18-due_diligence_experiment/plot_due_diligence.py \
        <input_dirs...> --judge-model <model> [--output <path>]

Example:
    uv run experiments/2-18-due_diligence_experiment/plot_due_diligence.py \
        outputs/calendar_scheduling/2-2-calendar_duty_of_care \
        outputs/calendar_scheduling/2-4-simple-prefs \
        outputs/calendar_scheduling/2-10-negotiation \
        --judge-model gpt-4.1
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from sage_benchmark.calendar_scheduling.evaluation.due_diligence.judge import (
    DueDiligenceJudge,
)
from sage_benchmark.calendar_scheduling.types import TimeSlotPreference
from sage_llm import ModelClient

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------


def discover_eval_files(input_dirs: list[Path]) -> list[Path]:
    """Find all eval JSON files across input directories.

    Handles two layouts:
    - Direct JSON files in directory (e.g. 2-2 pattern)
    - Subdirectories each containing eval.json (e.g. 2-4/2-10 pattern)
    """
    seen: set[Path] = set()
    files: list[Path] = []
    for d in input_dirs:
        # Pattern 1: JSON files directly in directory
        for f in sorted(d.glob("*.json")):
            resolved = f.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(f)
        # Pattern 2: eval.json in subdirectories
        for f in sorted(d.glob("*/eval.json")):
            resolved = f.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(f)
    return files


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_eval_file(filepath: Path) -> Optional[dict]:
    """Load an eval JSON file and extract label, metadata, and results."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Warning: Failed to load {filepath}: {e}", file=sys.stderr)
        return None

    if not isinstance(data, dict) or "results" not in data or "metadata" not in data:
        print(f"Warning: Unexpected format in {filepath}", file=sys.stderr)
        return None

    metadata = data["metadata"]
    summary = data.get("summary", {})

    # Derive label and dataset from path
    if filepath.name == "eval.json":
        short_label = filepath.parent.name
        dataset = filepath.parent.parent.name
    else:
        short_label = filepath.stem
        dataset = filepath.parent.name

    # Extract model short name
    model_full = metadata.get("assistant_model", "unknown")
    model = model_full.split("/")[-1]

    return {
        "filepath": str(filepath),
        "label": f"{dataset}/{short_label}",
        "short_label": short_label,
        "dataset": dataset,
        "model": model,
        "expose_preferences": metadata.get("expose_preferences"),
        "results": data["results"],
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Deterministic metric computation (no LLM needed)
# ---------------------------------------------------------------------------


def count_messages(result: dict) -> int:
    """Count emails sent by the assistant."""
    exec_data = result["execution"]
    assistant_email = exec_data["task"]["assistant"]["email"]
    return sum(1 for e in exec_data.get("emails", []) if e.get("from_") == assistant_email)


def count_formal_proposals(result: dict) -> int:
    """Count RequestMeeting and ReplyMeeting(COUNTER) tool calls from assistant."""
    count = 0
    for message in result["execution"].get("assistant_context", []):
        if message.get("role") != "assistant":
            continue
        for tc in message.get("tool_calls", []):
            name = tc["function"]["name"]
            if name == "RequestMeeting":
                count += 1
            elif name == "ReplyMeeting":
                try:
                    args = json.loads(tc["function"]["arguments"])
                    if args.get("status") == "COUNTER":
                        count += 1
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning("Failed to parse ReplyMeeting arguments: %s", e)
    return count


def extract_send_email_bodies(result: dict) -> list[str]:
    """Extract message bodies from SendEmail tool calls in assistant context."""
    bodies = []
    for message in result["execution"].get("assistant_context", []):
        if message.get("role") != "assistant":
            continue
        for tc in message.get("tool_calls", []):
            if tc["function"]["name"] == "SendEmail":
                try:
                    args = json.loads(tc["function"]["arguments"])
                    body = args.get("message", "")
                    if body and body.strip():
                        bodies.append(body)
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning("Failed to parse SendEmail arguments: %s", e)
    return bodies


def get_assistant_email_bodies(result: dict) -> list[str]:
    """Extract non-empty email bodies sent by the assistant."""
    exec_data = result["execution"]
    assistant_email = exec_data["task"]["assistant"]["email"]
    bodies = []
    for email in exec_data.get("emails", []):
        if email.get("from_") == assistant_email:
            body = email.get("body") or ""
            if body.strip():
                bodies.append(body)
    return bodies


def get_preferences(result: dict) -> list[TimeSlotPreference]:
    """Extract assistant's time slot preferences from a task result."""
    prefs_raw = result["execution"]["task"]["assistant"].get("preferences", [])
    return [TimeSlotPreference(**p) for p in prefs_raw]


# ---------------------------------------------------------------------------
# LLM-based metric computation
# ---------------------------------------------------------------------------


async def compute_preference_mentions(
    result: dict,
    judge: DueDiligenceJudge,
) -> int:
    """Count assistant emails that mention time preferences (LLM judge)."""
    preferences = get_preferences(result)
    if not preferences:
        return 0

    bodies = get_assistant_email_bodies(result)
    count = 0
    for body in bodies:
        judgement = await judge.evaluate_preference_mention(
            email_body=body,
            preferences=preferences,
        )
        if judgement.mentions_preference:
            count += 1
    return count


async def compute_text_proposals(
    result: dict,
    judge: DueDiligenceJudge,
) -> int:
    """Count text-based proposals in SendEmail bodies (LLM judge)."""
    bodies = extract_send_email_bodies(result)
    count = 0
    for body in bodies:
        judgement = await judge.evaluate_text_proposal(email_body=body)
        if judgement.contains_proposal:
            count += 1
    return count


# ---------------------------------------------------------------------------
# Per-eval-file metric aggregation
# ---------------------------------------------------------------------------


async def compute_metrics_for_eval(
    eval_data: dict,
    judge: DueDiligenceJudge,
    batch_size: int,
) -> dict:
    """Compute all due diligence metrics for one eval file."""
    results = eval_data["results"]
    summary = eval_data["summary"]

    # Optimality from pre-computed summary
    optimality = summary.get("fiduciary_avg_assistant_duty_of_care_score")
    if optimality is None:
        scores = [
            r["assistant_duty_of_care_score"]
            for r in results
            if r.get("assistant_duty_of_care_score") is not None
        ]
        optimality = float(np.mean(scores)) if scores else None

    # Compute deterministic metrics for all tasks
    msg_counts = [count_messages(r) for r in results]
    formal_proposals = [count_formal_proposals(r) for r in results]

    # Compute LLM-based metrics in batches
    pref_mention_counts = []
    text_proposal_counts = []

    for i in range(0, len(results), batch_size):
        batch = results[i : i + batch_size]
        pref_tasks = [compute_preference_mentions(r, judge) for r in batch]
        text_tasks = [compute_text_proposals(r, judge) for r in batch]

        pref_results = await asyncio.gather(*pref_tasks)
        text_results = await asyncio.gather(*text_tasks)

        pref_mention_counts.extend(pref_results)
        text_proposal_counts.extend(text_results)

    # Total proposal counts = formal + text
    proposal_counts = [fp + tp for fp, tp in zip(formal_proposals, text_proposal_counts)]

    avg_msg = float(np.mean(msg_counts))
    avg_pref_mentions = float(np.mean(pref_mention_counts))
    avg_proposals = float(np.mean(proposal_counts))
    composite = avg_msg + avg_pref_mentions + avg_proposals

    return {
        "label": eval_data["label"],
        "short_label": eval_data["short_label"],
        "dataset": eval_data["dataset"],
        "model": eval_data["model"],
        "expose_preferences": eval_data["expose_preferences"],
        "avg_message_count": avg_msg,
        "avg_preference_mentions": avg_pref_mentions,
        "avg_proposals": avg_proposals,
        "composite_due_diligence": composite,
        "optimality": optimality,
        "n_tasks": len(results),
    }


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

COLOR_POOL = [
    "#1f77b4",  # blue
    "#2ca02c",  # green
    "#d62728",  # red
    "#ff7f0e",  # orange
    "#9467bd",  # purple
    "#8c564b",  # brown
    "#e377c2",  # pink
    "#17becf",  # cyan
    "#bcbd22",  # olive
    "#7f7f7f",  # gray
]

MARKER_POOL = ["o", "s", "^", "D", "v", "<", ">", "p", "h", "*", "X", "P"]


def plot_due_diligence(data_points: list[dict], output_path: Path):
    """Create three due diligence scatter plots (one per metric) vs duty of care."""
    subplot_configs = [
        ("avg_message_count", "Avg Number of Messages"),
        ("avg_preference_mentions", "Avg Preference Mentions"),
        ("avg_proposals", "Avg Number of Proposals"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Dynamically assign colors to datasets and markers to models
    unique_datasets = sorted(set(dp["dataset"] for dp in data_points))
    unique_models = sorted(set(dp["model"] for dp in data_points))

    dataset_colors = {ds: COLOR_POOL[i % len(COLOR_POOL)] for i, ds in enumerate(unique_datasets)}
    model_markers = {m: MARKER_POOL[i % len(MARKER_POOL)] for i, m in enumerate(unique_models)}

    for ax, (x_key, x_label) in zip(axes, subplot_configs):
        for dp in data_points:
            if dp["optimality"] is None:
                continue

            dataset = dp["dataset"]
            model = dp["model"]

            color = dataset_colors[dataset]
            marker = model_markers[model]

            # Filled for exposed prefs, hollow for hidden
            exposed = dp["expose_preferences"]
            facecolor = color if exposed else "none"

            ax.scatter(
                dp[x_key],
                dp["optimality"],
                marker=marker,
                c=facecolor,
                edgecolors=color,
                s=90,
                linewidths=1.5,
                zorder=5,
            )

            # Text annotation
            ax.annotate(
                dp["short_label"],
                (dp[x_key], dp["optimality"]),
                textcoords="offset points",
                xytext=(6, 4),
                fontsize=6.5,
                color="#444444",
            )

        ax.set_xlabel(x_label, fontsize=11)
        ax.set_ylabel("Duty of Care", fontsize=11)
        ax.set_ylim(0, 1.05)

        # Tufte style
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_axisbelow(True)
        ax.grid(True, linestyle=":", alpha=0.5, color="#cccccc")

    # Build legend on the last subplot
    last_ax = axes[-1]
    legend_handles = []
    legend_labels = []

    # Dataset colors
    for dataset in unique_datasets:
        color = dataset_colors[dataset]
        handle = last_ax.scatter([], [], marker="o", c=color, edgecolors=color, s=64)
        legend_handles.append(handle)
        legend_labels.append(dataset)

    # Model markers
    for model in unique_models:
        marker = model_markers[model]
        handle = last_ax.scatter([], [], marker=marker, c="#666666", edgecolors="#666666", s=64)
        legend_handles.append(handle)
        legend_labels.append(model)

    # Filled vs hollow for prefs
    filled = last_ax.scatter([], [], marker="o", c="#1a1a1a", edgecolors="#1a1a1a", s=64)
    unfilled = last_ax.scatter(
        [], [], marker="o", c="none", edgecolors="#1a1a1a", s=64, linewidths=1.5
    )
    legend_handles.extend([filled, unfilled])
    legend_labels.extend(["exposed prefs", "hidden prefs"])

    last_ax.legend(
        legend_handles,
        legend_labels,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        frameon=True,
        fancybox=False,
        edgecolor="#cccccc",
        fontsize=8,
        borderaxespad=0,
    )

    # Annotation for total data points
    total_tasks = sum(dp["n_tasks"] for dp in data_points)
    last_ax.text(
        0.98,
        0.02,
        f"{len(data_points)} configs, {total_tasks} tasks",
        transform=last_ax.transAxes,
        fontsize=8,
        ha="right",
        va="bottom",
        color="#666666",
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved plot to: {output_path}")


# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------


def print_summary(data_points: list[dict]):
    """Print summary statistics to console."""
    print(f"\n{'=' * 100}")
    print("DUE DILIGENCE vs OPTIMALITY SUMMARY")
    print(f"{'=' * 100}")
    print(
        f"{'Label':<40} {'Model':<8} {'Prefs':<6} {'AvgMsg':>7} {'AvgPrM':>7} "
        f"{'AvgProp':>8} {'DD':>7} {'Opt':>7} {'Tasks':>5}"
    )
    print("-" * 100)

    for dp in sorted(data_points, key=lambda x: x["label"]):
        prefs_str = "exp" if dp["expose_preferences"] else "hid"
        opt_str = f"{dp['optimality']:.3f}" if dp["optimality"] is not None else "N/A"
        print(
            f"{dp['label']:<40} {dp['model']:<8} {prefs_str:<6} "
            f"{dp['avg_message_count']:>7.2f} {dp['avg_preference_mentions']:>7.2f} "
            f"{dp['avg_proposals']:>8.2f} {dp['composite_due_diligence']:>7.2f} "
            f"{opt_str:>7} {dp['n_tasks']:>5}"
        )

    print(f"{'=' * 100}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


async def async_main(args: argparse.Namespace):
    """Async entry point."""
    input_dirs = [Path(d) for d in args.input_dirs]
    for d in input_dirs:
        if not d.exists():
            print(f"Error: Directory {d} does not exist", file=sys.stderr)
            sys.exit(1)

    output_path = (
        Path(args.output) if args.output else input_dirs[0] / "due_diligence_vs_optimality.png"
    )

    # Discover eval files
    eval_files = discover_eval_files(input_dirs)
    if not eval_files:
        print("Error: No eval JSON files found", file=sys.stderr)
        sys.exit(1)
    print(f"Found {len(eval_files)} eval file(s)")

    # Load eval data
    eval_data_list = []
    for f in eval_files:
        data = load_eval_file(f)
        if data is not None:
            eval_data_list.append(data)
    print(f"Loaded {len(eval_data_list)} valid eval file(s)")

    # Initialize LLM judge
    model_client = ModelClient()
    judge = DueDiligenceJudge(model=args.judge_model, model_client=model_client)

    # Compute metrics for each eval file
    data_points = []
    for i, eval_data in enumerate(eval_data_list):
        label = eval_data["label"]
        n_tasks = len(eval_data["results"])
        print(
            f"  [{i + 1}/{len(eval_data_list)}] Computing metrics for {label} ({n_tasks} tasks)..."
        )
        metrics = await compute_metrics_for_eval(eval_data, judge, args.batch_size)
        data_points.append(metrics)

    # Filter out points without optimality
    valid_points = [dp for dp in data_points if dp["optimality"] is not None]
    if not valid_points:
        print("Error: No data points with valid optimality scores", file=sys.stderr)
        sys.exit(1)

    # Plot and summarize
    plot_due_diligence(valid_points, output_path)
    print_summary(data_points)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Plot due diligence vs optimality scatter plot")
    parser.add_argument(
        "input_dirs",
        nargs="+",
        help="Directories containing eval JSON files",
    )
    parser.add_argument(
        "--judge-model",
        required=True,
        help="Model for LLM judge calls (e.g. gpt-4.1)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="Concurrent LLM judge calls per batch (default: 20)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output plot path (default: due_diligence_vs_optimality.png in first input dir)",
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
