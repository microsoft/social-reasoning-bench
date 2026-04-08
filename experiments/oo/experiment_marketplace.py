"""Marketplace OO experiment: privacy prompt × duty-of-care attack × model sweep.

Sweeps:
  - 2 privacy prompt levels: none, strong
  - 3 attack conditions: normal, hand_crafted duty_of_care, whimsical duty_of_care
  - 11 model configs (same as experiment_full):
      Non-reasoning: gpt-4.1 × {no_cot, cot}  (2)
      Reasoning: {gpt-5.4, gemini-3.1-pro, claude-sonnet-4.6} × {think_off, think_med, think_high}  (9)

Total configs: 2 × 3 × 11 = 66

Usage::

    sagebench experiment experiments/experiment_marketplace_oo.py
    sagebench experiment experiments/experiment_marketplace_oo.py -k gpt-5.4
    sagebench experiment experiments/experiment_marketplace_oo.py -k strong
"""

from typing import Any

from sage_benchmark.benchmarks.marketplace.config import MarketplaceRunConfig

# ── Data paths ──────────────────────────────────────────────────────

MKT_DIR = "data/marketplace"

# ── Sweep axes ──────────────────────────────────────────────────────

PRIVACY_LEVELS = ["none", "strong"]
ATTACK_TYPES = ["duty_of_care"]

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

COUNTERPARTY_KWARGS: dict[str, Any] = {
    "seller_model": "azure_pool/gpt-5.4",
    "seller_reasoning_effort": "medium",
}

JUDGE_KWARGS: dict[str, Any] = {
    "judge_votes": 1,
}

ROUNDS_KWARGS: dict[str, Any] = {
    "max_rounds": 20,
    "max_steps_per_turn": 10,
}


def _model_tag(model: str) -> str:
    return model.split("/")[-1]


def _variant(*parts: str) -> str:
    return "_".join(p for p in parts if p)


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
        **COUNTERPARTY_KWARGS,
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
        # Hand-crafted (runtime injection)
        yield _mkt(
            [f"{MKT_DIR}/small.yaml"],
            _variant("marketplace", tag, privacy, f"hand_crafted_{attack}"),
            model,
            privacy,
            reasoning_effort,
            explicit_cot,
            attack_types=[attack],
        )
        # Whimsical (pre-generated data)
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
