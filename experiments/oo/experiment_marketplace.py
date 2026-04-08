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

from sage_benchmark.benchmarks.marketplace.config import MarketplaceRunConfig

# ── Data paths ──────────────────────────────────────────────────────

MKT_DIR = "data/marketplace"

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
        seller_model=COUNTERPARTY_MODEL,
        seller_reasoning_effort=COUNTERPARTY_REASONING_EFFORT,
        privacy_prompt=privacy,
        reasoning_effort=reasoning_effort,
        explicit_cot=explicit_cot,
        attack_types=attack_types,
        max_rounds=MAX_ROUNDS,
        max_steps_per_turn=MAX_STEPS_PER_TURN,
        judge_votes=JUDGE_VOTES,
    )


def _mkt_duty_of_care(model, privacy, tag, reasoning_effort=None, explicit_cot=None):
    """Yield normal + duty_of_care attack variants (hand-crafted + whimsical)."""
    # Normal (no attack)
    yield _mkt(
        [f"{MKT_DIR}/small.yaml"],
        _variant("marketplace", tag, privacy, "normal"),
        model,
        privacy,
        reasoning_effort,
        explicit_cot,
    )
    # Hand-crafted duty_of_care (runtime injection)
    yield _mkt(
        [f"{MKT_DIR}/small.yaml"],
        _variant("marketplace", tag, privacy, f"hand_crafted_{ATTACK_TYPE}"),
        model,
        privacy,
        reasoning_effort,
        explicit_cot,
        attack_types=[ATTACK_TYPE],
    )
    # Whimsical duty_of_care (pre-generated data)
    yield _mkt(
        [f"{MKT_DIR}/small-whimsical-{ATTACK_TYPE}.yaml"],
        _variant("marketplace", tag, privacy, f"whimsical_{ATTACK_TYPE}"),
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
                yield from _mkt_duty_of_care(
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
                yield from _mkt_duty_of_care(
                    model,
                    privacy,
                    f"{mtag}_{cot_tag}",
                    explicit_cot=cot,
                )
