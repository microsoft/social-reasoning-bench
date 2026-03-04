"""Malicious duty-of-care strategy isolation experiment.

Tests each of the top 5 duty-of-care strategies individually alongside the
5 existing small dataset variants (benign + 4 malicious), across 3 assistant
models with hidden/exposed preferences.

60 variants total: 10 datasets x 3 assistants x 2 pref settings.

Usage:
    # List all experiments
    uv run sagebench calendar --experiments experiments/3-03-malicious-cal-more/experiment.py --collect

    # Run all
    uv run sagebench calendar --experiments experiments/3-03-malicious-cal-more/experiment.py
"""

from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig

LIMIT = None
MAX_ROUNDS = 10

DATA_DIR = "data/calendar-scheduling/final"
VARIANTS_DIR = f"{DATA_DIR}/malicious-whim-variants"

DATASETS = {
    # Existing variants
    "benign": f"{DATA_DIR}/small.yaml",
    "mal-hc-privacy": f"{DATA_DIR}/small-malicious-hand-crafted-privacy.yaml",
    "mal-hc-doc": f"{DATA_DIR}/small-malicious-hand-crafted-duty-of-care.yaml",
    "mal-whim-privacy": f"{DATA_DIR}/small-malicious-whimsical-privacy.yaml",
    "mal-whim-doc": f"{DATA_DIR}/small-malicious-whimsical-duty-of-care.yaml",
    # Per-strategy duty-of-care variants
    "doc-strat-1": f"{VARIANTS_DIR}/small-malicious-whimsical-duty-of-care-strat-1.yaml",
    "doc-strat-5": f"{VARIANTS_DIR}/small-malicious-whimsical-duty-of-care-strat-5.yaml",
    "doc-strat-6": f"{VARIANTS_DIR}/small-malicious-whimsical-duty-of-care-strat-6.yaml",
    "doc-strat-7": f"{VARIANTS_DIR}/small-malicious-whimsical-duty-of-care-strat-7.yaml",
    "doc-strat-8": f"{VARIANTS_DIR}/small-malicious-whimsical-duty-of-care-strat-8.yaml",
}

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

REQUESTOR_CFG = {
    "requestor_model": "phyagi/gpt-4.1",
    "requestor_explicit_cot": False,
    "requestor_reasoning_effort": None,
}

JUDGE_MODEL = "phyagi/gpt-4.1"
OUTPUT_BASE = "outputs/calendar_scheduling/3-03-malicious-cal-more"


def _make_config(assistant_cfg, **kwargs):
    return ExperimentConfig(
        limit=LIMIT,
        max_rounds=MAX_ROUNDS,
        assistant_model=assistant_cfg["assistant_model"],
        assistant_explicit_cot=assistant_cfg["assistant_explicit_cot"],
        assistant_reasoning_effort=assistant_cfg["assistant_reasoning_effort"],
        requestor_model=REQUESTOR_CFG["requestor_model"],
        requestor_explicit_cot=REQUESTOR_CFG["requestor_explicit_cot"],
        requestor_reasoning_effort=REQUESTOR_CFG["requestor_reasoning_effort"],
        judge_model=JUDGE_MODEL,
        output_dir=f"{OUTPUT_BASE}",
        **kwargs,
    )


def experiment_duty_of_care():
    """Duty of care: assistant model x preference visibility x dataset."""
    for model_name, assistant_cfg in ASSISTANT_MODELS.items():
        for expose, pref_label in [(False, "prefs-hidden"), (True, "prefs-exposed")]:
            for ds_label, ds_path in DATASETS.items():
                yield _make_config(
                    assistant_cfg,
                    paths=[ds_path],
                    assistant_system_prompt="default",
                    expose_preferences=expose,
                    variant=f"{model_name}_{pref_label}_{ds_label}",
                )
