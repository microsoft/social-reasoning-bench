"""OO experiment: calendar + marketplace — outcome-optimality attack × model sweep.

Sweeps (per benchmark):
  - 2 privacy prompt levels: none, strong
  - 3 attack conditions: normal, hand_crafted outcome_optimality, whimsical outcome_optimality
  - 5 model configs (active):
      Non-reasoning: gpt-4.1 × {no_cot, cot}  (2)
      Reasoning: gpt-5.4 × {think_off, think_med, think_high}  (3)

Usage::

    sagebench experiment experiments/oo/experiment.py
    sagebench experiment experiments/oo/experiment.py -k calendar
    sagebench experiment experiments/oo/experiment.py -k marketplace
    sagebench experiment experiments/oo/experiment.py -k gpt-5.4
"""

from typing import Any

from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig
from sage_benchmark.benchmarks.marketplace.config import MarketplaceRunConfig

# ── Data paths ──────────────────────────────────────────────────────

CAL_DIR = "data/calendar-scheduling-oo"
MKT_DIR = "data/marketplace"

# ── Sweep axes ──────────────────────────────────────────────────────

PRIVACY_LEVELS = ["none", "strong"]
ATTACK_TYPES = ["outcome_optimality"]

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

# ── Fixed values ──────────────────────────────────────────────────────

CAL_COUNTERPARTY_KWARGS = {
    "requestor_model": "gemini/gemini-3-flash-preview",
    "requestor_reasoning_effort": "medium",
}

CAL_JUDGE_KWARGS = {
    "judge_model": "azure_pool/gpt-5.4",
    "judge_reasoning_effort": "medium",
    "judge_votes": 1,
}

MKT_COUNTERPARTY_KWARGS: dict[str, Any] = {
    "seller_model": "gemini/gemini-3-flash-preview",
    "seller_reasoning_effort": "medium",
}

MKT_JUDGE_KWARGS: dict[str, Any] = {
    "judge_votes": 1,
}

ROUNDS_KWARGS: dict[str, Any] = {"max_rounds": 20, "max_steps_per_turn": 10}


def _model_tag(model: str) -> str:
    return model.split("/")[-1]


def _variant(*parts: str) -> str:
    return "_".join(p for p in parts if p)


# ── Calendar ────────────────────────────────────────────────────────


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
        privacy_prompt=privacy,
        expose_preferences=True,
        assistant_model=model,
        assistant_reasoning_effort=reasoning_effort,
        assistant_explicit_cot=assistant_explicit_cot,
        attack_types=attack_types,
        **ROUNDS_KWARGS,
        **CAL_COUNTERPARTY_KWARGS,
        **CAL_JUDGE_KWARGS,
    )


def _cal_attacks(model, privacy, tag, reasoning_effort=None, assistant_explicit_cot=None):
    """Yield normal + all attack variants for one calendar config."""
    yield _cal(
        [f"{CAL_DIR}/small.yaml"],
        _variant("calendar", tag, privacy, "normal"),
        model,
        privacy,
        reasoning_effort,
        assistant_explicit_cot,
    )
    for attack in ATTACK_TYPES:
        yield _cal(
            [f"{CAL_DIR}/small.yaml"],
            _variant("calendar", tag, privacy, f"hand_crafted_{attack}"),
            model,
            privacy,
            reasoning_effort,
            assistant_explicit_cot,
            attack_types=[attack],
        )
        yield _cal(
            [f"{CAL_DIR}/small-whimsical-{attack}.yaml"],
            _variant("calendar", tag, privacy, f"whimsical_{attack}"),
            model,
            privacy,
            reasoning_effort,
            assistant_explicit_cot,
        )


def experiment_calendar_oo():
    for privacy in PRIVACY_LEVELS:
        for model in REASONING_MODELS:
            mtag = _model_tag(model)
            for effort, effort_tag in REASONING_EFFORTS[model]:
                yield from _cal_attacks(
                    model, privacy, f"{mtag}_{effort_tag}", reasoning_effort=effort
                )
        for model in NON_REASONING_MODELS:
            mtag = _model_tag(model)
            for cot in (False, True):
                cot_tag = "cot" if cot else "no_cot"
                yield from _cal_attacks(
                    model, privacy, f"{mtag}_{cot_tag}", assistant_explicit_cot=cot
                )


# ── Marketplace ─────────────────────────────────────────────────────


def _mkt(
    paths,
    variant,
    model,
    privacy,
    reasoning_effort=None,
    explicit_cot=None,
    attack_types=None,
):
    return MarketplaceRunConfig(
        paths=paths,
        variant=variant,
        model=model,
        privacy_prompt=privacy,
        reasoning_effort=reasoning_effort,
        explicit_cot=explicit_cot,
        attack_types=attack_types,
        **MKT_COUNTERPARTY_KWARGS,
        **ROUNDS_KWARGS,
        **MKT_JUDGE_KWARGS,
    )


def _mkt_attacks(model, privacy, tag, reasoning_effort=None, explicit_cot=None):
    """Yield normal + all attack variants for one marketplace config."""
    yield _mkt(
        [f"{MKT_DIR}/small.yaml"],
        _variant("marketplace", tag, privacy, "normal"),
        model,
        privacy,
        reasoning_effort,
        explicit_cot,
    )
    for attack in ATTACK_TYPES:
        yield _mkt(
            [f"{MKT_DIR}/small.yaml"],
            _variant("marketplace", tag, privacy, f"hand_crafted_{attack}"),
            model,
            privacy,
            reasoning_effort,
            explicit_cot,
            attack_types=[attack],
        )
        yield _mkt(
            [f"{MKT_DIR}/small-whimsical-{attack}.yaml"],
            _variant("marketplace", tag, privacy, f"whimsical_{attack}"),
            model,
            privacy,
            reasoning_effort,
            explicit_cot,
        )


def experiment_marketplace_oo():
    for privacy in PRIVACY_LEVELS:
        for model in REASONING_MODELS:
            mtag = _model_tag(model)
            for effort, effort_tag in REASONING_EFFORTS[model]:
                yield from _mkt_attacks(
                    model, privacy, f"{mtag}_{effort_tag}", reasoning_effort=effort
                )
        for model in NON_REASONING_MODELS:
            mtag = _model_tag(model)
            for cot in (False, True):
                cot_tag = "cot" if cot else "no_cot"
                yield from _mkt_attacks(model, privacy, f"{mtag}_{cot_tag}", explicit_cot=cot)
