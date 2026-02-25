from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig

LIMIT = 50
MAX_ROUNDS = 10

BENIGN_PATHS = [f"data/calendar-scheduling/archive/generated/generated-tasks.yaml"]
MALICIOUS_HC_PATHS = [
    f"data/calendar-scheduling/archive/generated/generated-tasks-malicious-extraction.yaml"
]
MALICIOUS_WHIM_PATHS = [
    f"data/calendar-scheduling/archive/generated/generated-tasks-malicious-with-strategies-50.yaml"
]

REQUESTOR_TYPES = {
    "benign": BENIGN_PATHS,
    "malicious-hc": MALICIOUS_HC_PATHS,
    "malicious-whimsical": MALICIOUS_WHIM_PATHS,
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
}

REQUESTOR_MODEL = "phyagi/gpt-5.2"
REQUESTOR_EXPLICIT_COT = False
REQUESTOR_REASONING = "medium"

JUDGE_MODEL = "phyagi/gpt-4.1"

OUTPUT_BASE = "outputs/calendar_scheduling/2-23-calendar-sweep"

PRIVACY_PROMPTS = {
    "base": "default",
    "privacy-aware": "privacy-simple",
    "privacy-strong": "privacy-strong",
    "privacy-ci": "privacy-ci",
}


def _make_config(assistant_cfg, req_paths, output_subdir, **kwargs):
    return ExperimentConfig(
        paths=req_paths,
        limit=LIMIT,
        max_rounds=MAX_ROUNDS,
        # Assistant
        assistant_model=assistant_cfg["assistant_model"],
        assistant_explicit_cot=assistant_cfg["assistant_explicit_cot"],
        assistant_reasoning_effort=assistant_cfg["assistant_reasoning_effort"],
        # Requestor
        requestor_model=REQUESTOR_MODEL,
        requestor_explicit_cot=REQUESTOR_EXPLICIT_COT,
        requestor_reasoning_effort=REQUESTOR_REASONING,
        # Judge
        judge_model=JUDGE_MODEL,
        # Output
        output_dir=f"{OUTPUT_BASE}/{output_subdir}",
        **kwargs,
    )


def experiment_duty_of_care():
    """Duty of care: model x preference visibility x requestor type.

    prefs-hidden + default prompt overlaps with privacy base — those runs
    are emitted only here (under duty_of_care) to avoid duplicates.
    """
    for model_name, assistant_cfg in ASSISTANT_MODELS.items():
        for expose, pref_label in [(False, "prefs-hidden"), (True, "prefs-exposed")]:
            for req_label, req_paths in REQUESTOR_TYPES.items():
                yield _make_config(
                    assistant_cfg,
                    req_paths,
                    output_subdir="duty_of_care",
                    assistant_system_prompt="default",
                    expose_preferences=expose,
                    variant=f"{model_name}_{pref_label}_{req_label}",
                )


def experiment_privacy():
    """Privacy: model x prompt strategy x requestor type.

    Skips the 'base' (default) prompt since those runs are covered by
    duty_of_care prefs-hidden experiments (same default prompt + prefs hidden).
    """
    prompts_without_base = {k: v for k, v in PRIVACY_PROMPTS.items() if k != "base"}
    for model_name, assistant_cfg in ASSISTANT_MODELS.items():
        for prompt_label, prompt_key in prompts_without_base.items():
            for req_label, req_paths in REQUESTOR_TYPES.items():
                yield _make_config(
                    assistant_cfg,
                    req_paths,
                    output_subdir="privacy",
                    assistant_system_prompt=prompt_key,
                    expose_preferences=False,
                    variant=f"{model_name}_{prompt_label}_{req_label}",
                )
