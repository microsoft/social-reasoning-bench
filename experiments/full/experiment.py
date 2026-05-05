"""Full experiment: benchmarks × attacks × system prompts × models.

Sweeps:
  - 2 benchmarks: calendar, marketplace
  - 7 attack conditions: normal + hand_crafted × 3 + whimsical × 3
  - 5 system prompt presets: none, privacy, dd_info_gathering, dd_advocacy, oo
  - 11 model configs (split by reasoning capability):
      Non-reasoning: gpt-4.1 × {no_cot, cot}  (2)
      Reasoning: {gpt-5.4, gemini-3.1-pro, claude-sonnet-4.6} × {think_off, think_med, think_high}  (9)

Counterparty agents (requestor, seller) use a fixed strong
model: azure_pool/gpt-5.4 with medium reasoning effort across all sweeps.

Usage::

    sagebench experiment experiments/experiment_full.py
    sagebench experiment experiments/experiment_full.py -k calendar
    sagebench experiment experiments/experiment_full.py -k gpt-4.1
    sagebench experiment experiments/experiment_full.py --set model=gpt-5.4
"""

from typing import Any

from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig
from sage_benchmark.benchmarks.marketplace.config import MarketplaceRunConfig

# ── Data paths ──────────────────────────────────────────────────────

CAL_DIR = "data/calendar-scheduling"
MKT_DIR = "data/marketplace"

# ── Sweep axes ──────────────────────────────────────────────────────

ATTACK_TYPES = ["privacy", "outcome_optimality", "due_diligence"]
SYSTEM_PROMPT_PRESETS = ["none", "privacy", "dd_info_gathering", "dd_advocacy", "oo"]

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


def _cal(
    paths,
    variant,
    model,
    preset,
    reasoning_effort=None,
    assistant_explicit_cot=None,
    attack_types=None,
):
    return CalendarRunConfig(
        paths=paths,
        variant=variant,
        model=model,
        system_prompt=preset,
        expose_preferences=True,
        reasoning_effort=reasoning_effort,
        assistant_explicit_cot=assistant_explicit_cot,
        attack_types=attack_types,
        **CAL_COUNTERPARTY_KWARGS,
        **ROUNDS_KWARGS,
        **JUDGE_KWARGS,
    )


def _cal_attacks(model, preset, tag, reasoning_effort=None, assistant_explicit_cot=None):
    """Yield normal + all attack variants for one calendar config."""
    yield _cal(
        [f"{CAL_DIR}/small.yaml"],
        _variant("calendar", tag, preset, "normal"),
        model,
        preset,
        reasoning_effort,
        assistant_explicit_cot,
    )
    for attack in ATTACK_TYPES:
        # Handcrafted: runtime injection from benign data
        yield _cal(
            [f"{CAL_DIR}/small.yaml"],
            _variant("calendar", tag, preset, f"hand_crafted_{attack}"),
            model,
            preset,
            reasoning_effort,
            assistant_explicit_cot,
            attack_types=[attack],
        )
        # Whimsical: pre-generated data files
        yield _cal(
            [f"{CAL_DIR}/small-whimsical-{attack}.yaml"],
            _variant("calendar", tag, preset, f"whimsical_{attack}"),
            model,
            preset,
            reasoning_effort,
            assistant_explicit_cot,
        )


def experiment_calendar():
    for preset in SYSTEM_PROMPT_PRESETS:
        # Reasoning models: sweep reasoning_effort levels
        for model in REASONING_MODELS:
            mtag = _model_tag(model)
            for effort, effort_tag in REASONING_EFFORTS[model]:
                yield from _cal_attacks(
                    model,
                    preset,
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
                    preset,
                    f"{mtag}_{cot_tag}",
                    assistant_explicit_cot=cot,
                )


# ── Marketplace ─────────────────────────────────────────────────────


def _mkt(
    paths, variant, model, preset, reasoning_effort=None, explicit_cot=None, attack_types=None
):
    return MarketplaceRunConfig(
        paths=paths,
        variant=variant,
        model=model,
        system_prompt=preset,
        reasoning_effort=reasoning_effort,
        explicit_cot=explicit_cot,
        attack_types=attack_types,
        **MKT_COUNTERPARTY_KWARGS,
        **ROUNDS_KWARGS,
        **JUDGE_KWARGS,
    )


def _mkt_attacks(model, preset, tag, reasoning_effort=None, explicit_cot=None):
    """Yield normal + all attack variants for one marketplace config."""
    yield _mkt(
        [f"{MKT_DIR}/small.yaml"],
        _variant("marketplace", tag, preset, "normal"),
        model,
        preset,
        reasoning_effort,
        explicit_cot,
    )
    for attack in ATTACK_TYPES:
        # Handcrafted: runtime injection from benign data
        yield _mkt(
            [f"{MKT_DIR}/small.yaml"],
            _variant("marketplace", tag, preset, f"hand_crafted_{attack}"),
            model,
            preset,
            reasoning_effort,
            explicit_cot,
            attack_types=[attack],
        )
        # Whimsical: pre-generated data files
        yield _mkt(
            [f"{MKT_DIR}/small-whimsical-{attack}.yaml"],
            _variant("marketplace", tag, preset, f"whimsical_{attack}"),
            model,
            preset,
            reasoning_effort,
            explicit_cot,
        )


def experiment_marketplace():
    for preset in SYSTEM_PROMPT_PRESETS:
        if preset == "dd_info_gathering":
            # Info gathering doesn't apply to marketplace
            continue

        # Reasoning models: sweep reasoning_effort levels
        for model in REASONING_MODELS:
            mtag = _model_tag(model)
            for effort, effort_tag in REASONING_EFFORTS[model]:
                yield from _mkt_attacks(
                    model,
                    preset,
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
                    preset,
                    f"{mtag}_{cot_tag}",
                    explicit_cot=cot,
                )
