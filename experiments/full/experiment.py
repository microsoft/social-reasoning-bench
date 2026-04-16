"""Full experiment: benchmarks × attacks × privacy prompts × models.

Sweeps:
  - 3 benchmarks: calendar, marketplace, form_filling
  - 7 attack conditions: normal + hand_crafted × 3 + whimsical × 3
  - 4 privacy prompt levels: none, simple, strong, ci
  - 11 model configs (split by reasoning capability):
      Non-reasoning: gpt-4.1 × {no_cot, cot}  (2)
      Reasoning: {gpt-5.4, gemini-3.1-pro, claude-sonnet-4.6} × {think_off, think_med, think_high}  (9)

Counterparty agents (requestor, interviewer, seller) use a fixed strong
model: azure_pool/gpt-5.4 with medium reasoning effort across all sweeps.

Usage::

    sagebench experiment experiments/experiment_full.py
    sagebench experiment experiments/experiment_full.py -k calendar
    sagebench experiment experiments/experiment_full.py -k gpt-4.1
    sagebench experiment experiments/experiment_full.py --set model=gpt-5.4
"""

from typing import Any

from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig
from sage_benchmark.benchmarks.form_filling.config import FormFillingRunConfig
from sage_benchmark.benchmarks.marketplace.config import MarketplaceRunConfig

# ── Data paths ──────────────────────────────────────────────────────

CAL_DIR = "data/calendar-scheduling"
MKT_DIR = "data/marketplace"
FF_DIR = "data/form-filling"

# ── Sweep axes ──────────────────────────────────────────────────────

ATTACK_TYPES = ["privacy", "duty_of_care", "due_diligence"]
PRIVACY_LEVELS = ["none", "simple", "strong", "ci"]

NON_REASONING_MODELS = [
    "azure_pool/gpt-4.1",
]
REASONING_MODELS = [
    "azure_pool/gpt-5.4",
    "google/gemini-3.1-pro-preview",
    "anthropic/claude-sonnet-4.6",
]

REASONING_EFFORTS: dict[str, list[tuple[str | int, str]]] = {
    "azure_pool/gpt-5.4": [("none", "think_off"), ("medium", "think_med"), ("high", "think_high")],
    "google/gemini-3.1-pro-preview": [
        ("none", "think_off"),
        ("medium", "think_med"),
        ("high", "think_high"),
    ],
    # Claude Sonnet 4.6 requires integer budget tokens for extended thinking
    "anthropic/claude-sonnet-4.6": [
        ("none", "think_off"),
        (4096, "think_med"),
        (10000, "think_high"),
    ],
}

# ── Fixed values ──────────────────────────────────────────────────────

JUDGE_KWARGS: dict[str, Any] = {
    "judge_model": "azure_pool/gpt-5.4",
    "judge_reasoning_effort": "medium",
    "judge_votes": 1,
}

ROUNDS_KWARGS: dict[str, Any] = {
    "max_rounds": 20,
    "max_steps_per_turn": 10,
}

# Calendar: counterparty is the requestor
CAL_COUNTERPARTY_KWARGS: dict[str, Any] = {
    "requestor_model": "gemini/gemini-3-flash-preview",
    "requestor_reasoning_effort": "medium",
}

# Form filling: counterparty is the interviewer
FF_COUNTERPARTY_KWARGS: dict[str, Any] = {
    "interviewer_model": "gemini/gemini-3-flash-preview",
    "interviewer_reasoning_effort": "medium",
}

# Marketplace: counterparty is the seller
MKT_COUNTERPARTY_KWARGS: dict[str, Any] = {
    "seller_model": "gemini/gemini-3-flash-preview",
    "seller_reasoning_effort": "medium",
}


def _model_tag(model: str) -> str:
    """'gpt-4.1' -> 'gpt-4.1'

    Args:
        model: Fully-qualified or slash-separated model identifier.

    Returns:
        The last segment after splitting on '/'.
    """
    return model.split("/")[-1]


def _variant(benchmark: str, *parts: str) -> str:
    """Build variant name from non-empty parts.

    Args:
        benchmark: Benchmark prefix (e.g. 'calendar', 'marketplace').
        *parts: Additional name segments; empty strings are filtered out.

    Returns:
        Underscore-joined variant name.
    """
    return "_".join(p for p in (benchmark, *parts) if p)


# ── Calendar ────────────────────────────────────────────────────────
# Calendar uses privacy_prompt for privacy and assistant_explicit_cot
# for CoT (only the assistant agent, not the requestor).


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
        privacy_prompt=privacy,
        expose_preferences=True,
        reasoning_effort=reasoning_effort,
        assistant_explicit_cot=assistant_explicit_cot,
        attack_types=attack_types,
        **CAL_COUNTERPARTY_KWARGS,
        **ROUNDS_KWARGS,
        **JUDGE_KWARGS,
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
        # Handcrafted: runtime injection from benign data
        yield _cal(
            [f"{CAL_DIR}/small.yaml"],
            _variant("calendar", tag, privacy, f"hand_crafted_{attack}"),
            model,
            privacy,
            reasoning_effort,
            assistant_explicit_cot,
            attack_types=[attack],
        )
        # Whimsical: pre-generated data files
        yield _cal(
            [f"{CAL_DIR}/small-whimsical-{attack}.yaml"],
            _variant("calendar", tag, privacy, f"whimsical_{attack}"),
            model,
            privacy,
            reasoning_effort,
            assistant_explicit_cot,
        )


def experiment_calendar():
    for privacy in PRIVACY_LEVELS:
        # Reasoning models: sweep reasoning_effort levels
        for model in REASONING_MODELS:
            mtag = _model_tag(model)
            for effort, effort_tag in REASONING_EFFORTS[model]:
                yield from _cal_attacks(
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
                yield from _cal_attacks(
                    model,
                    privacy,
                    f"{mtag}_{cot_tag}",
                    assistant_explicit_cot=cot,
                )


# ── Marketplace ─────────────────────────────────────────────────────
# Marketplace uses privacy_prompt (base field) for privacy and explicit_cot
# (base field) which applies to both buyer and seller agents.


def _mkt(
    paths, variant, model, privacy, reasoning_effort=None, explicit_cot=None, attack_types=None
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
        **JUDGE_KWARGS,
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
        # Handcrafted: runtime injection from benign data
        yield _mkt(
            [f"{MKT_DIR}/small.yaml"],
            _variant("marketplace", tag, privacy, f"hand_crafted_{attack}"),
            model,
            privacy,
            reasoning_effort,
            explicit_cot,
            attack_types=[attack],
        )
        # Whimsical: pre-generated data files
        yield _mkt(
            [f"{MKT_DIR}/small-whimsical-{attack}.yaml"],
            _variant("marketplace", tag, privacy, f"whimsical_{attack}"),
            model,
            privacy,
            reasoning_effort,
            explicit_cot,
        )


def experiment_marketplace():
    for privacy in PRIVACY_LEVELS:
        # Reasoning models: sweep reasoning_effort levels
        for model in REASONING_MODELS:
            mtag = _model_tag(model)
            for effort, effort_tag in REASONING_EFFORTS[model]:
                yield from _mkt_attacks(
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
                yield from _mkt_attacks(
                    model,
                    privacy,
                    f"{mtag}_{cot_tag}",
                    explicit_cot=cot,
                )


# ── Form filling ────────────────────────────────────────────────────
# Form filling uses privacy_prompt for privacy and explicit_cot (base field).


def _ff(
    paths, variant, model, privacy, reasoning_effort=None, explicit_cot=None, attack_types=None
):
    return FormFillingRunConfig(
        paths=paths,
        variant=variant,
        model=model,
        privacy_prompt=privacy,
        reasoning_effort=reasoning_effort,
        explicit_cot=explicit_cot,
        attack_types=attack_types,
        **FF_COUNTERPARTY_KWARGS,
        **ROUNDS_KWARGS,
        **JUDGE_KWARGS,
    )


def _ff_attacks(model, privacy, tag, reasoning_effort=None, explicit_cot=None):
    """Yield normal + all attack variants for one form-filling config."""
    yield _ff(
        [f"{FF_DIR}/tasks.yaml"],
        _variant("form_filling", tag, privacy, "normal"),
        model,
        privacy,
        reasoning_effort,
        explicit_cot,
    )
    for attack in ATTACK_TYPES:
        # Handcrafted: runtime injection from benign data
        yield _ff(
            [f"{FF_DIR}/tasks.yaml"],
            _variant("form_filling", tag, privacy, f"hand_crafted_{attack}"),
            model,
            privacy,
            reasoning_effort,
            explicit_cot,
            attack_types=[attack],
        )
        # Whimsical: pre-generated data files
        yield _ff(
            [f"{FF_DIR}/tasks-whimsical-{attack}.yaml"],
            _variant("form_filling", tag, privacy, f"whimsical_{attack}"),
            model,
            privacy,
            reasoning_effort,
            explicit_cot,
        )


def experiment_form_filling():
    for privacy in PRIVACY_LEVELS:
        # Reasoning models: sweep reasoning_effort levels
        for model in REASONING_MODELS:
            mtag = _model_tag(model)
            for effort, effort_tag in REASONING_EFFORTS[model]:
                yield from _ff_attacks(
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
                yield from _ff_attacks(
                    model,
                    privacy,
                    f"{mtag}_{cot_tag}",
                    explicit_cot=cot,
                )
