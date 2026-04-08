"""Calendar v2 experiment: privacy prompt × duty-of-care attack × model sweep.

Sweeps:
  - 2 privacy prompt levels: none, strong
  - 3 attack conditions: normal, hand_crafted duty_of_care, whimsical duty_of_care
  - 11 model configs (same as experiment_full):
      Non-reasoning: gpt-4.1 × {no_cot, cot}  (2)
      Reasoning: {gpt-5.4, gemini-3.1-pro, claude-sonnet-4.6} × {think_off, think_med, think_high}  (9)

Total configs: 2 × 3 × 11 = 66

Usage::

    sagebench experiment experiments/experiment_calendar_v2.py
    sagebench experiment experiments/experiment_calendar_v2.py -k gpt-5.4
    sagebench experiment experiments/experiment_calendar_v2.py -k strong
"""

from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig

# ── Data paths ──────────────────────────────────────────────────────

CAL_DIR = "data/calendar-scheduling-v2"

# ── Sweep axes ──────────────────────────────────────────────────────

PRIVACY_LEVELS = ["none", "strong"]
ATTACK_TYPE = "duty_of_care"

# Fixed strong counterparty model
COUNTERPARTY_MODEL = "azure_pool/gpt-5.4"
COUNTERPARTY_REASONING_EFFORT = "medium"

# ── Run parameters ─────────────────────────────────────────────────

MAX_ROUNDS = 20
MAX_STEPS_PER_TURN = 10
JUDGE_VOTES = 1

# Same model sweep as experiment_full
NON_REASONING_MODELS = [
    "azure_pool/gpt-4.1",
]
REASONING_MODELS = [
    "azure_pool/gpt-5.4",
    # "google/gemini-3.1-pro-preview",
    # "anthropic/claude-sonnet-4.6",
]

REASONING_EFFORTS: dict[str, list[tuple[str | int, str]]] = {
    "azure_pool/gpt-5.4": [("none", "think_off"), ("medium", "think_med"), ("high", "think_high")],
    # "google/gemini-3.1-pro-preview": [
    #     ("none", "think_off"),
    #     ("medium", "think_med"),
    #     ("high", "think_high"),
    # ],
    # "anthropic/claude-sonnet-4.6": [
    #     ("none", "think_off"),
    #     (4096, "think_med"),
    #     (10000, "think_high"),
    # ],
}


def _model_tag(model: str) -> str:
    return model.split("/")[-1]


def _variant(*parts: str) -> str:
    return "_".join(p for p in parts if p)


def _cal(
    paths,
    variant,
    model,
    privacy,
    reasoning_effort=None,
    assistant_explicit_cot=None,
    attack_types=None,
):
    return CalendarRunConfig(
        paths=paths,
        variant=variant,
        model=model,
        requestor_model=COUNTERPARTY_MODEL,
        requestor_reasoning_effort=COUNTERPARTY_REASONING_EFFORT,
        privacy_prompt=privacy,
        expose_preferences=True,
        reasoning_effort=reasoning_effort,
        assistant_explicit_cot=assistant_explicit_cot,
        attack_types=attack_types,
        max_rounds=MAX_ROUNDS,
        max_steps_per_turn=MAX_STEPS_PER_TURN,
        judge_votes=JUDGE_VOTES,
    )


def _cal_duty_of_care(model, privacy, tag, reasoning_effort=None, assistant_explicit_cot=None):
    """Yield normal + duty_of_care attack variants (hand-crafted + whimsical).

    Args:
        model: Model identifier to use for the assistant agent.
        privacy: Privacy prompt level for the calendar scenario.
        tag: Human-readable tag included in the variant name.
        reasoning_effort: Optional reasoning effort budget for reasoning models.
        assistant_explicit_cot: Optional flag enabling explicit chain-of-thought
            for the assistant agent.
    """
    # Normal (no attack)
    yield _cal(
        [f"{CAL_DIR}/small.yaml"],
        _variant("calendar", tag, privacy, "normal"),
        model,
        privacy,
        reasoning_effort,
        assistant_explicit_cot,
    )
    # Hand-crafted duty_of_care (runtime injection)
    yield _cal(
        [f"{CAL_DIR}/small.yaml"],
        _variant("calendar", tag, privacy, f"hand_crafted_{ATTACK_TYPE}"),
        model,
        privacy,
        reasoning_effort,
        assistant_explicit_cot,
        attack_types=[ATTACK_TYPE],
    )
    # Whimsical duty_of_care (pre-generated data)
    yield _cal(
        [f"{CAL_DIR}/small-whimsical-{ATTACK_TYPE}.yaml"],
        _variant("calendar", tag, privacy, f"whimsical_{ATTACK_TYPE}"),
        model,
        privacy,
        reasoning_effort,
        assistant_explicit_cot,
    )


def experiment_calendar_v2():
    for privacy in PRIVACY_LEVELS:
        # Reasoning models: sweep reasoning_effort levels
        for model in REASONING_MODELS:
            mtag = _model_tag(model)
            for effort, effort_tag in REASONING_EFFORTS[model]:
                yield from _cal_duty_of_care(
                    model,
                    privacy,
                    f"{mtag}_{effort_tag}",
                    reasoning_effort=effort,
                )

        # Non-reasoning models: sweep explicit_cot True/False
        for model in NON_REASONING_MODELS:
            mtag = _model_tag(model)
            for cot in (False, True):
                cot_tag = "cot" if cot else "no_cot"
                yield from _cal_duty_of_care(
                    model,
                    privacy,
                    f"{mtag}_{cot_tag}",
                    assistant_explicit_cot=cot,
                )
