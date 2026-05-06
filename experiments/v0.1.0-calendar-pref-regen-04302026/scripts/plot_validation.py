"""Validation plots for the production geometric-pref PR.

Produces two PNGs:
  comparison.png       — 10 (model x attack) groups, 2 bars each (baseline vs new)
                         with per-condition theoretical random-baseline lines.
  condition_averages.png — 2 bars (baseline vs new) averaged across all 10
                           (model x attack) variants.

Reads results.json from outputs/v0.1.0-calendar-pref-regen/{baselines,new}/
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
from sage_benchmark.benchmarks.calendar_scheduling.evaluation.outcome_optimality.evaluate import (
    _find_mutually_free_start_times,
)
from sage_benchmark.benchmarks.calendar_scheduling.loader import load_tasks

REPO_ROOT = Path(__file__).resolve().parents[3]
EXP_DIR = REPO_ROOT / "experiments" / "v0.1.0-calendar-pref-regen-04302026"
RESULTS_BASE = REPO_ROOT / "outputs" / "v0.1.0-calendar-pref-regen-04302026"
CONDITION_SUBDIR = {"baseline": "baselines", "new": "new"}
FIG_DIR = EXP_DIR / "figures"

CONDITIONS = ["baseline", "new"]
MODELS = ["gpt-4.1", "gpt-5.4-med"]
ATTACKS = [
    "benign",
    "hc_oo",
    "whimsical_due_diligence",
    "whimsical_outcome_optimality",
    "whimsical_privacy",
]
ATTACK_LABELS = {
    "benign": "Benign",
    "hc_oo": "Malicious-hc-oo",
    "whimsical_due_diligence": "Whimsical-DD",
    "whimsical_outcome_optimality": "Whimsical-OO",
    "whimsical_privacy": "Whimsical-Privacy",
}
COND_COLOR = {"baseline": "#b07a3a", "new": "#2f6f9f"}
COND_LABEL = {"baseline": "Baseline (current)", "new": "New (geometric)"}


def variant_dir(condition: str, model: str, attack: str) -> Path:
    return RESULTS_BASE / CONDITION_SUBDIR[condition] / f"calendar_{condition}_{model}_{attack}"


def load_oos(condition: str, model: str, attack: str) -> list[float]:
    path = variant_dir(condition, model, attack) / "results.json"
    if not path.exists():
        return []
    j = json.loads(path.read_text())
    return [
        r["outcome_optimality_score"]
        for r in j["results"]
        if r.get("outcome_optimality_score") is not None
    ]


def theoretical_random_baseline(yaml_path: Path) -> float:
    """E[OO] under uniform-random ZOPA pick = mean(zopa_prefs) / max(zopa_prefs), per task."""
    loaded = load_tasks([str(yaml_path)])
    per_task = []
    for t in loaded.all_tasks:
        zopa = _find_mutually_free_start_times(
            t.assistant.preferences, t.assistant.calendar, t.requestor.calendar
        )
        score_by_start = {p.start_time: p.score for p in t.assistant.preferences}
        zopa_scores = [score_by_start[s] for s in zopa]
        if not zopa_scores or max(zopa_scores) == 0:
            continue
        per_task.append(mean(zopa_scores) / max(zopa_scores))
    return mean(per_task) if per_task else float("nan")


def baselines_per_condition() -> dict[str, float]:
    """Per-condition theoretical random baseline (averaged across the small + whimsical-oo yamls)."""
    out = {}
    for cond in CONDITIONS:
        if cond == "baseline":
            data_dir = EXP_DIR / "data" / "baseline"
        else:
            data_dir = REPO_ROOT / "data" / "calendar-scheduling"
        smalls = [
            data_dir / "small.yaml",
            data_dir / "small-whimsical-due_diligence.yaml",
            data_dir / "small-whimsical-outcome_optimality.yaml",
            data_dir / "small-whimsical-privacy.yaml",
        ]
        vals = [theoretical_random_baseline(p) for p in smalls if p.exists()]
        out[cond] = mean(vals) if vals else float("nan")
    return out


def plot_comparison(means: dict[tuple[str, str, str], float], baselines: dict[str, float]) -> None:
    groups = [(m, a) for m in MODELS for a in ATTACKS]
    n = len(groups)
    width = 0.4
    x = np.arange(n)

    fig, ax = plt.subplots(figsize=(15, 5))
    for i, cond in enumerate(CONDITIONS):
        vals = [means.get((cond, m, a), 0.0) for m, a in groups]
        ax.bar(
            x + (i - 0.5) * width,
            vals,
            width=width,
            color=COND_COLOR[cond],
            label=COND_LABEL[cond],
        )
        ax.axhline(
            baselines[cond],
            color=COND_COLOR[cond],
            linestyle="--",
            linewidth=1,
            alpha=0.5,
            label=f"{COND_LABEL[cond]} random baseline = {baselines[cond]:.2f}",
        )

    ax.set_xticks(x)
    ax.set_xticklabels([f"{m}\n{ATTACK_LABELS[a]}" for m, a in groups], fontsize=9)
    ax.set_ylabel("Mean Outcome Optimality")
    ax.set_ylim(0, 1)
    ax.set_title("Validation: baseline vs new geometric scoring (small dataset, N=21)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "comparison.png"
    fig.savefig(out, dpi=150)
    print(f"  Wrote {out}")


def plot_condition_averages(
    means: dict[tuple[str, str, str], float], baselines: dict[str, float]
) -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    cond_means = {
        cond: mean([means[(cond, m, a)] for m in MODELS for a in ATTACKS if (cond, m, a) in means])
        for cond in CONDITIONS
    }
    x = np.arange(len(CONDITIONS))
    bars = ax.bar(
        x,
        [cond_means[c] for c in CONDITIONS],
        color=[COND_COLOR[c] for c in CONDITIONS],
        width=0.55,
    )
    for cond, b in zip(CONDITIONS, bars):
        ax.hlines(
            baselines[cond],
            b.get_x(),
            b.get_x() + b.get_width(),
            color=COND_COLOR[cond],
            linestyle="--",
            linewidth=1.5,
            label=f"{COND_LABEL[cond]} random baseline = {baselines[cond]:.2f}",
        )
        ax.text(
            b.get_x() + b.get_width() / 2,
            cond_means[cond] + 0.02,
            f"{cond_means[cond]:.2f}",
            ha="center",
            fontsize=10,
        )
    ax.legend(loc="upper right", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([COND_LABEL[c] for c in CONDITIONS])
    ax.set_ylabel("Mean OO (averaged over 2 models x 5 attacks)")
    ax.set_ylim(0, 1)
    ax.set_title("Aggregate validation: baseline vs new\n(dashed = theoretical random baseline)")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "condition_averages.png"
    fig.savefig(out, dpi=150)
    print(f"  Wrote {out}")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    means: dict[tuple[str, str, str], float] = {}
    for cond in CONDITIONS:
        for m in MODELS:
            for a in ATTACKS:
                oos = load_oos(cond, m, a)
                if oos:
                    means[(cond, m, a)] = mean(oos)
    baselines = baselines_per_condition()
    print(f"Loaded {len(means)}/12 variants. Baselines: {baselines}")
    plot_comparison(means, baselines)
    plot_condition_averages(means, baselines)


if __name__ == "__main__":
    main()
