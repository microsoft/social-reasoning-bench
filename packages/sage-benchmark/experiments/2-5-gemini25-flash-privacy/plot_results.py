#!/usr/bin/env python3
"""Plot privacy leakage results for Gemini 2.5 Flash 3x2 experiment."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Results directory
RESULTS_DIR = Path(__file__).parent.parent.parent / "outputs" / "calendar_scheduling"


# Load results
def load_leakage(filename):
    with open(RESULTS_DIR / filename) as f:
        data = json.load(f)
    leaked = data["summary"]["privacy_tasks_with_leakage"]
    total = data["summary"]["valid_tasks"]
    return leaked, total, leaked / total * 100


# Load all results
results = {
    "Normal": {
        "default": load_leakage("gemini25-flash-high-normal-default.json"),
        "privacy-ci": load_leakage("gemini25-flash-high-normal-privacy-ci.json"),
    },
    "Malicious": {
        "default": load_leakage("gemini25-flash-high-malicious-default.json"),
        "privacy-ci": load_leakage("gemini25-flash-high-malicious-privacy-ci.json"),
    },
    "Strategies": {
        "default": load_leakage("gemini25-flash-high-strategies-default.json"),
        "privacy-ci": load_leakage("gemini25-flash-high-strategies-privacy-ci.json"),
    },
}

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(3)
width = 0.35

task_types = ["Normal", "Malicious", "Strategies"]
default_vals = [results[t]["default"][2] for t in task_types]
privacy_vals = [results[t]["privacy-ci"][2] for t in task_types]

bars1 = ax.bar(x - width / 2, default_vals, width, label="Default Prompt", color="#4285f4")
bars2 = ax.bar(x + width / 2, privacy_vals, width, label="Privacy-CI Prompt", color="#34a853")

ax.set_ylabel("Privacy Leakage (%)", fontsize=12)
ax.set_xlabel("Requester Type", fontsize=12)
ax.set_title("Gemini 2.5 Flash (Thinking=High): Privacy Leakage by Condition", fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(task_types, fontsize=11)
ax.legend(fontsize=10)
ax.set_ylim(0, 60)


# Add value labels on bars
def add_labels(bars, data):
    for bar, (leaked, total, pct) in zip(bars, data):
        height = bar.get_height()
        ax.annotate(
            f"{int(leaked)}/{total}\n({pct:.0f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )


add_labels(bars1, [results[t]["default"] for t in task_types])
add_labels(bars2, [results[t]["privacy-ci"] for t in task_types])

plt.tight_layout()
plt.savefig(Path(__file__).parent / "plot_leakage_3x2.png", dpi=150)
plt.savefig(Path(__file__).parent / "plot_leakage_3x2.pdf")
print("Saved plot_leakage_3x2.png and plot_leakage_3x2.pdf")
