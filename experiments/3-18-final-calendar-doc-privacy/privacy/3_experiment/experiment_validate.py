"""Validate: privacy leakage across models, datasets, and prompt strategies.

Configure the sweep dimensions below. Already-completed experiments are
automatically skipped by the sagebench runner.

Usage:
    # List experiments
    uv run sagebench calendar \
        --experiments experiments/3-18-final-calendar-doc-privacy/privacy/3_experiment/experiment_validate.py \
        --collect-only

    # Run all
    uv run sagebench calendar \
        --experiments experiments/3-18-final-calendar-doc-privacy/privacy/3_experiment/experiment_validate.py

    # Run with a small limit for testing
    uv run sagebench calendar \
        --experiments experiments/3-18-final-calendar-doc-privacy/privacy/3_experiment/experiment_validate.py \
        --limit 2

    # Filter by variant name
    uv run sagebench calendar \
        --experiments experiments/3-18-final-calendar-doc-privacy/privacy/3_experiment/experiment_validate.py \
        -k gpt5.2-medium
"""

import json
import os
from pathlib import Path

from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig

EXPERIMENT_DIR = Path(__file__).parent.parent

# ── Sweep dimensions (edit these to expand/narrow the sweep) ─────────────

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

PROMPTS = {
    "base": "default",
    "privacy-aware": "privacy-simple",
    "privacy-strong": "privacy-strong",
    "privacy-ci": "privacy-ci",
}

DATASETS = ["benign", "mal-hc-privacy", "mal-whim-privacy"]

# ── Fixed config ─────────────────────────────────────────────────────────

DATASET_SIZE = "large"
MAX_ROUNDS = 10
OUTPUT_BASE = "outputs/calendar_scheduling/3-18-final-calendar-doc-privacy/privacy/validation"

REQUESTOR_MODEL = "gemini-3-flash-preview"
REQUESTOR_REASONING_EFFORT = "medium"
JUDGE_MODEL = "phyagi/gpt-4.1"


# ── Helpers ──────────────────────────────────────────────────────────────


def _model_slug(model: str) -> str:
    """Turn 'phyagi/gpt-5.2' into 'gpt-5.2', etc."""
    return model.split("/")[-1]


def _get_winner(assistant_model: str) -> str:
    force = os.environ.get("FORCE_STRATEGY")
    if force:
        return force

    slug = _model_slug(assistant_model)
    results_path = EXPERIMENT_DIR / "2_screen/results" / f"screening_results_{slug}.json"
    if not results_path.exists():
        raise FileNotFoundError(
            f"No screening results at {results_path}. "
            f"Run screen.py for {assistant_model} first or set FORCE_STRATEGY env var."
        )
    return json.loads(results_path.read_text())["winner"]


DATASET_PATHS = {
    "benign": f"data/calendar-scheduling/final/{DATASET_SIZE}.yaml",
    "mal-hc-privacy": f"data/calendar-scheduling/final/{DATASET_SIZE}-malicious-hand-crafted-privacy.yaml",
}


def _get_dataset_path(ds_label: str, assistant_model: str) -> str:
    if ds_label == "mal-whim-privacy":
        winner = _get_winner(assistant_model)
        whim_path = EXPERIMENT_DIR / "3_experiment" / "data" / f"{winner}.yaml"
        if not whim_path.exists():
            raise FileNotFoundError(f"{whim_path} not found. Run data_gen.py first.")
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
        expose_preferences=False,
        output_dir=OUTPUT_BASE,
        **kwargs,
    )


# ── Experiment ───────────────────────────────────────────────────────────


def experiment_privacy():
    """Privacy leakage: model × dataset × prompt strategy."""
    for model_name, assistant_cfg in ASSISTANT_MODELS.items():
        for prompt_label, prompt_key in PROMPTS.items():
            for ds_label in DATASETS:
                yield _make_config(
                    assistant_cfg,
                    paths=[_get_dataset_path(ds_label, assistant_cfg["assistant_model"])],
                    assistant_system_prompt=prompt_key,
                    variant=f"{model_name}_{prompt_label}_{ds_label}",
                )
