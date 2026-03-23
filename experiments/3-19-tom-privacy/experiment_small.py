"""ToM privacy prompt experiment on small dataset.

Compare privacy-tom against privacy-ci and base prompts.

Usage:
    # List experiments
    uv run sagebench calendar \
        --experiments experiments/3-19-tom-privacy/experiment_small.py \
        --collect-only

    # Run all (27 = 3 models × 3 prompts × 3 datasets)
    uv run sagebench calendar \
        --experiments experiments/3-19-tom-privacy/experiment_small.py

    # Run single model
    uv run sagebench calendar \
        --experiments experiments/3-19-tom-privacy/experiment_small.py \
        -k gpt5.2-medium
"""

import json
import os
from pathlib import Path

from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig

# Reuse screening results from 3-18-final-calendar-doc-privacy
SCREENING_DIR = Path("experiments/3-18-final-calendar-doc-privacy/privacy/2_screen/results")
WHIM_DATA_DIR = Path("experiments/3-18-final-calendar-doc-privacy/privacy/3_experiment/data")

# ── Sweep dimensions ────────────────────────────────────────────────────

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
    "privacy-tom": "privacy-tom",
    "privacy-tom-dual": "privacy-tom-dual",
}

DATASETS = ["benign", "mal-hc-privacy", "mal-whim-privacy"]

# ── Fixed config ────────────────────────────────────────────────────────

DATASET_SIZE = "small"
MAX_ROUNDS = 10
OUTPUT_BASE = "outputs/calendar_scheduling/3-19-tom-privacy/validation"

REQUESTOR_MODEL = "gemini-3-flash-preview"
REQUESTOR_REASONING_EFFORT = "medium"
JUDGE_MODEL = "phyagi/gpt-4.1"


# ── Helpers ─────────────────────────────────────────────────────────────


def _model_slug(model: str) -> str:
    return model.split("/")[-1]


def _get_winner(assistant_model: str) -> str:
    force = os.environ.get("FORCE_STRATEGY")
    if force:
        return force
    slug = _model_slug(assistant_model)
    results_path = SCREENING_DIR / f"screening_results_{slug}.json"
    if not results_path.exists():
        raise FileNotFoundError(f"No screening results at {results_path}.")
    return json.loads(results_path.read_text())["winner"]


DATASET_PATHS = {
    "benign": f"data/calendar-scheduling/final/{DATASET_SIZE}.yaml",
    "mal-hc-privacy": f"data/calendar-scheduling/final/{DATASET_SIZE}-malicious-hand-crafted-privacy.yaml",
}


def _get_dataset_path(ds_label: str, assistant_model: str) -> str:
    if ds_label == "mal-whim-privacy":
        winner = _get_winner(assistant_model)
        whim_path = WHIM_DATA_DIR / f"{winner}.yaml"
        if not whim_path.exists():
            raise FileNotFoundError(f"{whim_path} not found.")
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


# ── Experiment ──────────────────────────────────────────────────────────


def experiment_tom_privacy():
    """ToM privacy: model × dataset × prompt (base, ci, tom)."""
    for model_name, assistant_cfg in ASSISTANT_MODELS.items():
        for prompt_label, prompt_key in PROMPTS.items():
            for ds_label in DATASETS:
                yield _make_config(
                    assistant_cfg,
                    paths=[_get_dataset_path(ds_label, assistant_cfg["assistant_model"])],
                    assistant_system_prompt=prompt_key,
                    variant=f"{model_name}_{prompt_label}_{ds_label}",
                )
