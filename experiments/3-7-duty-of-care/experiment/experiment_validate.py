"""Validate: double-booking attacks across models, datasets, and preference visibility.

Mirrors the 2-26 duty_of_care experiment structure: sweeps assistant model x
expose_preferences (hidden vs exposed) x dataset.

Usage:
    # List experiments
    uv run sagebench calendar \
        --experiments experiments/3-7-duty-of-care/experiment/experiment_validate.py \
        --collect-only

    # Run all
    uv run sagebench calendar \
        --experiments experiments/3-7-duty-of-care/experiment/experiment_validate.py

    # Run with a small limit for testing
    uv run sagebench calendar \
        --experiments experiments/3-7-duty-of-care/experiment/experiment_validate.py \
        --limit 2

    # Filter by variant name
    uv run sagebench calendar \
        --experiments experiments/3-7-duty-of-care/experiment/experiment_validate.py \
        -k gpt5.2-medium
"""

import json
import os
from pathlib import Path

from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig

EXPERIMENT_DIR = Path(__file__).parent.parent

# -- Sweep dimensions (edit these to expand/narrow the sweep) --

ASSISTANT_MODELS = {
    "gpt4.1-cot": {
        "assistant_model": "phyagi/gpt-4.1",
        "assistant_explicit_cot": True,
        "assistant_reasoning_effort": None,
    },
    "gpt5.2-medium": {
        "assistant_model": "phyagi/gpt-5.2",
        "assistant_explicit_cot": False,
        "assistant_reasoning_effort": "medium",
    },
    "gemini-3-flash-medium": {
        "assistant_model": "gemini-3-flash-preview",
        "assistant_explicit_cot": False,
        "assistant_reasoning_effort": "medium",
    },
}

DATASETS = ["benign", "mal-hc-double-booking", "mal-whim-double-booking"]

# -- Fixed config --

DATASET_SIZE = "large"
MAX_ROUNDS = 10
OUTPUT_BASE = "outputs/calendar_scheduling/3-7-duty-of-care/validation"

REQUESTOR_MODEL = "gemini-3-flash-preview"
REQUESTOR_REASONING_EFFORT = "medium"
JUDGE_MODEL = "phyagi/gpt-4.1"


# -- Helpers --

def _model_slug(model: str) -> str:
    """Turn 'phyagi/gpt-5.2' into 'gpt-5.2', etc."""
    return model.split("/")[-1]


def _get_winner(assistant_model: str) -> str:
    force = os.environ.get("FORCE_STRATEGY")
    if force:
        return force

    slug = _model_slug(assistant_model)
    results_path = EXPERIMENT_DIR / "results" / f"screening_results_{slug}.json"
    if not results_path.exists():
        raise FileNotFoundError(
            f"No screening results at {results_path}. "
            f"Run screen.py for {assistant_model} first or set FORCE_STRATEGY env var."
        )
    return json.loads(results_path.read_text())["winner"]


DATASET_PATHS = {
    "benign": f"data/calendar-scheduling/final/{DATASET_SIZE}.yaml",
    "mal-hc-double-booking": f"data/calendar-scheduling/final/{DATASET_SIZE}-malicious-hand-crafted-double-booking.yaml",
}


def _get_dataset_path(ds_label: str, assistant_model: str) -> str | None:
    if ds_label == "mal-whim-double-booking":
        try:
            winner = _get_winner(assistant_model)
        except FileNotFoundError:
            return None
        whim_path = EXPERIMENT_DIR / "data" / "validation-duty-of-care" / f"{winner}.yaml"
        if not whim_path.exists():
            return None
        return str(whim_path)
    return DATASET_PATHS[ds_label]


def _make_config(assistant_cfg, **kwargs):
    return ExperimentConfig(
        limit=None,
        max_rounds=MAX_ROUNDS,
        assistant_model=assistant_cfg["assistant_model"],
        assistant_explicit_cot=assistant_cfg["assistant_explicit_cot"],
        assistant_reasoning_effort=assistant_cfg["assistant_reasoning_effort"],
        requestor_model=REQUESTOR_MODEL,
        requestor_explicit_cot=False,
        requestor_reasoning_effort=REQUESTOR_REASONING_EFFORT,
        judge_model=JUDGE_MODEL,
        judge_votes=3,
        assistant_system_prompt="default",
        output_dir=OUTPUT_BASE,
        **kwargs,
    )


# -- Experiment --

def experiment_duty_of_care():
    """Double-booking attacks: model x preference visibility x dataset."""
    for model_name, assistant_cfg in ASSISTANT_MODELS.items():
        for expose, pref_label in [(False, "prefs-hidden"), (True, "prefs-exposed")]:
            for ds_label in DATASETS:
                ds_path = _get_dataset_path(ds_label, assistant_cfg["assistant_model"])
                if ds_path is None:
                    continue
                yield _make_config(
                    assistant_cfg,
                    paths=[ds_path],
                    expose_preferences=expose,
                    variant=f"{model_name}_{pref_label}_{ds_label}",
                )
