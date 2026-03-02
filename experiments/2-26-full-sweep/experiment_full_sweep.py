"""Full sweep over 5 calendar-scheduling datasets (duty of care + privacy).

Sweeps all final datasets at a configurable size with:
- Requestor: GPT-4.1 (no thinking, no COT)
- Assistants: GPT-4.1 (CoT) and GPT-5.2 (medium thinking) and gemini 3

Usage:
    # List all experiments
    uv run sagebench calendar --experiments experiments/2-26-full-sweep/experiment_full_sweep.py --collect

    # Run all
    uv run sagebench calendar --experiments experiments/2-26-full-sweep/experiment_full_sweep.py
"""

from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig

DATASET_SIZE = "large"
LIMIT = None
MAX_ROUNDS = 10

DATASETS = {
    "benign": f"data/calendar-scheduling/final/{DATASET_SIZE}.yaml",
    "mal-hc-privacy": f"data/calendar-scheduling/final/{DATASET_SIZE}-malicious-hand-crafted-privacy.yaml",
    "mal-hc-doc": f"data/calendar-scheduling/final/{DATASET_SIZE}-malicious-hand-crafted-duty-of-care.yaml",
    "mal-whim-privacy": f"data/calendar-scheduling/final/{DATASET_SIZE}-malicious-whimsical-privacy.yaml",
    "mal-whim-doc": f"data/calendar-scheduling/final/{DATASET_SIZE}-malicious-whimsical-duty-of-care.yaml",
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

OUTPUT_BASE = "outputs/calendar_scheduling/2-26-full-sweep"

PRIVACY_PROMPTS = {
    "base": "default",
    "privacy-aware": "privacy-simple",
    "privacy-strong": "privacy-strong",
    "privacy-ci": "privacy-ci",
}


def _make_config(assistant_cfg, output_subdir, **kwargs):
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
        output_dir=f"{OUTPUT_BASE}/{output_subdir}",
        **kwargs,
    )


def experiment_duty_of_care():
    """Duty of care: assistant model x preference visibility x dataset.

    prefs-hidden + default prompt overlaps with privacy base -- those runs
    are emitted only here to avoid duplicates.
    """
    for model_name, assistant_cfg in ASSISTANT_MODELS.items():
        for expose, pref_label in [(False, "prefs-hidden"), (True, "prefs-exposed")]:
            for ds_label, ds_path in DATASETS.items():
                yield _make_config(
                    assistant_cfg,
                    output_subdir="duty_of_care",
                    paths=[ds_path],
                    assistant_system_prompt="default",
                    expose_preferences=expose,
                    variant=f"{model_name}_{pref_label}_{ds_label}",
                )


def experiment_privacy():
    """Privacy: assistant model x prompt strategy x dataset.

    Skips the 'base' (default) prompt since those runs are covered by
    duty_of_care prefs-hidden experiments.
    """
    prompts_without_base = {k: v for k, v in PRIVACY_PROMPTS.items() if k != "base"}
    for model_name, assistant_cfg in ASSISTANT_MODELS.items():
        for prompt_label, prompt_key in prompts_without_base.items():
            for ds_label, ds_path in DATASETS.items():
                yield _make_config(
                    assistant_cfg,
                    output_subdir="privacy",
                    paths=[ds_path],
                    assistant_system_prompt=prompt_key,
                    expose_preferences=False,
                    variant=f"{model_name}_{prompt_label}_{ds_label}",
                )
