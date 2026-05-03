"""Argument 2: DoC quadrant bubble charts by model.

Generates graph6_heatmap_by_model.png showing 2×3 grid of DoC quadrant
bubble charts (Calendar + Marketplace rows × 3 model columns).
Uses LLM judge DD scores.
"""

import json
import glob
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import get_model, get_prompt_type, is_benign, RESULTS_DIR, FIGURES_DIR

MODELS = ["GPT-4.1", "GPT-5.4", "Gemini"]
DOMAINS = ["calendar", "marketplace"]
DOMAIN_TITLES = {"calendar": "Calendar", "marketplace": "Marketplace"}

# Quadrant thresholds
OO_THRESHOLD = 0.5
DD_THRESHOLD = 0.5

QUADRANT_COLORS = {
    "RC": "#4CAF50",
    "LF": "#FFC107",
    "CG": "#FF9800",
    "Neg": "#F44336",
}
QUADRANT_POSITIONS = {
    "RC": (1, 1),
    "LF": (0, 1),
    "CG": (1, 0),
    "Neg": (0, 0),
}


def _classify_quadrant(oo: float, dd: float) -> str:
    if oo >= OO_THRESHOLD and dd >= DD_THRESHOLD:
        return "RC"  # Responsible Care
    elif oo >= OO_THRESHOLD and dd < DD_THRESHOLD:
        return "LF"  # Lucked-out Fragility
    elif oo < OO_THRESHOLD and dd >= DD_THRESHOLD:
        return "CG"  # Careful but Gave-away
    else:
        return "Neg"  # Negligence


def main():
    # Collect per (domain, model) quadrant counts
    quadrant_counts = {}  # (domain, model) -> {"RC": n, "LF": n, "CG": n, "Neg": n}

    for domain in DOMAINS:
        for rpath in sorted(glob.glob(str(RESULTS_DIR / f"{domain}_*" / "results.json"))):
            model_dir = Path(rpath).parent.name
            model = get_model(model_dir)
            if not model:
                continue
            prompt = get_prompt_type(model_dir)
            if not prompt:
                continue

            with open(rpath) as f:
                results = json.load(f)["results"]

            for r in results:
                oo = r.get("outcome_optimality")
                dd = r.get("due_diligence")
                if oo is None or dd is None:
                    continue
                if not is_benign(r, domain):
                    continue

                key = (domain, model)
                quadrant_counts.setdefault(key, {"RC": 0, "LF": 0, "CG": 0, "Neg": 0})
                q = _classify_quadrant(oo, dd)
                quadrant_counts[key][q] += 1

    # Plot 2×3 bubble charts
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    for row, domain in enumerate(DOMAINS):
        for col, model in enumerate(MODELS):
            ax = axes[row, col]
            counts = quadrant_counts.get((domain, model), {"RC": 0, "LF": 0, "CG": 0, "Neg": 0})
            total = sum(counts.values())

            ax.set_xlim(-0.5, 1.5)
            ax.set_ylim(-0.5, 1.5)
            ax.set_xticks([0, 1])
            ax.set_xticklabels(["Low DD", "High DD"], fontsize=9)
            ax.set_yticks([0, 1])
            ax.set_yticklabels(["Low OO", "High OO"], fontsize=9)
            ax.grid(True, alpha=0.3)
            ax.set_aspect('equal')

            for quad, (x, y) in QUADRANT_POSITIONS.items():
                pct = 100 * counts[quad] / total if total > 0 else 0
                size = pct * 40
                if pct > 0:
                    ax.scatter(x, y, s=size, c=QUADRANT_COLORS[quad], alpha=0.7,
                               edgecolors='black', linewidth=0.5)
                    ax.annotate(f"{pct:.0f}%", (x, y), ha='center', va='center',
                                fontsize=9, fontweight='bold')
                else:
                    ax.annotate("0%", (x, y), ha='center', va='center',
                                fontsize=8, color='gray', alpha=0.5)

            if row == 0:
                ax.set_title(f"{model}", fontsize=12, fontweight='bold')
            if col == 0:
                ax.set_ylabel(f"{DOMAIN_TITLES[domain]}\n\nOutcome Optimality",
                              fontsize=10, fontweight='bold')
            if row == 1:
                ax.set_xlabel("Due Diligence", fontsize=10)

    fig.suptitle("Duty of Care Quadrants by Model and Domain — LLM Judge DD\n(Reasoning-Only Runs, Benign Tasks)",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    out = FIGURES_DIR / "graph6_heatmap_by_model.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
