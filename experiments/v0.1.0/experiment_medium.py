"""
Experiments for SocialReasoning-Bench v0.1.0

To reproduce:
    sagebench experiment experiments/v0.1.0
"""

from pathlib import Path
from typing import Any, Literal, get_args

from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig
from sage_benchmark.benchmarks.marketplace.config import MarketplaceRunConfig
from sage_benchmark.shared.prompts.assistant_system_prompts import SystemPromptPreset

DATA_SIZE: Literal["small", "medium", "large"] = "medium"

JUDGE: dict[str, Any] = {
    "model": "gemini-2.5-flash",
    "reasoning_effort": "medium",
    "explicit_cot": False,
}

COUNTERPARTY: dict[str, Any] = {
    "model": "gemini-3-flash-preview",
    "reasoning_effort": "medium",
    "explicit_cot": False,
}

CONCURRENCY: dict[str, Any] = {"batch_size": 200, "task_concurrency": 5, "llm_concurrency": 64}

ROUNDS: dict[str, Any] = {"max_rounds": 10, "max_steps_per_turn": 3}

def assistants():
    # Non-reasoning models
    for model in ["azure_pool/gpt-4.1"]:
        for explicit_cot in (True,):
            yield {"model": model, "explicit_cot": explicit_cot, "reasoning_effort": None}

    # Effort-based reasoning models
    for model in ["azure_pool/gpt-5.4", "gemini-3-flash-preview"]:
        for reasoning_effort in ("high",):
            yield {"model": model, "reasoning_effort": reasoning_effort, "explicit_cot": None}

    # Budget-based reasoning models
    for model in ["claude-sonnet-4-6"]:
        # 2 orders of magnitude (min is 1024)
        for reasoning_budget in (10_000,):
            yield {"model": model, "reasoning_effort": reasoning_budget, "explicit_cot": None}


def attacks():
    yield from ["none", "outcome_optimality", "privacy", "due_diligence"]


def attack_styles(attack: str):
    # None
    if attack == "none":
        yield "none"
    else:
        yield from ["whimsical", "handcrafted"]


def defenses():
    yield from ["none", "all"]


def data_paths(attack: str, attack_style: str, path_prefix: str):
    if attack_style == "whimsical":
        yield str(Path(path_prefix, f"{DATA_SIZE}-whimsical-{attack}.yaml"))
    else:
        yield str(Path(path_prefix, f"{DATA_SIZE}.yaml"))


def variant(
    benchmark: str,
    assistant: dict[str, Any],
    defense: str,
    attack: str,
    attack_style: str,
):

    parts = [benchmark]

    parts.append(assistant["model"])

    reasoning_effort = assistant.get("reasoning_effort", assistant.get("reasoning_budget", None))
    explicit_cot = assistant.get("explicit_cot", None)

    if reasoning_effort:
        parts.append(str(reasoning_effort))
    if explicit_cot:
        parts.append("cot" if explicit_cot else "no_cot")

    parts.append(defense)
    parts.append(attack_style)
    parts.append(attack)

    variant_name = "_".join(parts)
    # Replace path-unsafe characters with '-'
    variant_name = "".join(c if c.isalnum() or c in ("_", "-") else "-" for c in variant_name)
    return variant_name


# --- Calendar ---


def experiment_calendar():
    for assistant in assistants():
        for attack in attacks():
            for attack_style in attack_styles(attack):
                for defense in defenses():
                    for path in data_paths(attack, attack_style, "data/calendar-scheduling"):
                        yield CalendarRunConfig(
                            paths=[path],
                            # Assistant
                            assistant_model=assistant["model"],
                            assistant_explicit_cot=assistant["explicit_cot"],
                            assistant_reasoning_effort=assistant["reasoning_effort"],
                            system_prompt=defense,
                            expose_preferences=True,
                            # Requestor
                            requestor_model=COUNTERPARTY["model"],
                            requestor_explicit_cot=COUNTERPARTY["explicit_cot"],
                            requestor_reasoning_effort=COUNTERPARTY["reasoning_effort"],
                            attack_types=[attack] if attack_style == "handcrafted" else [],
                            # Judge
                            judge_model=JUDGE["model"],
                            judge_reasoning_effort=JUDGE["reasoning_effort"],
                            # Concurrency
                            batch_size=CONCURRENCY["batch_size"],
                            task_concurrency=CONCURRENCY["task_concurrency"],
                            llm_concurrency=CONCURRENCY["llm_concurrency"],
                            # Rounds
                            max_rounds=ROUNDS["max_rounds"],
                            max_steps_per_turn=ROUNDS["max_steps_per_turn"],
                            variant=variant("calendar", assistant, defense, attack, attack_style),
                        )


# --- Marketplace ---


def experiment_marketplace():
    for assistant in assistants():
        for attack in attacks():
            for attack_style in attack_styles(attack):
                for defense in defenses():
                    for path in data_paths(attack, attack_style, "data/marketplace"):
                        yield MarketplaceRunConfig(
                            paths=[path],
                            # Assistant
                            buyer_model=assistant["model"],
                            buyer_explicit_cot=assistant["explicit_cot"],
                            buyer_reasoning_effort=assistant["reasoning_effort"],
                            system_prompt=defense,
                            # Requestor
                            seller_model=COUNTERPARTY["model"],
                            seller_explicit_cot=COUNTERPARTY["explicit_cot"],
                            seller_reasoning_effort=COUNTERPARTY["reasoning_effort"],
                            attack_types=[attack] if attack_style == "handcrafted" else [],
                            # Judge
                            judge_model=JUDGE["model"],
                            judge_reasoning_effort=JUDGE["reasoning_effort"],
                            # Concurrency
                            batch_size=CONCURRENCY["batch_size"],
                            task_concurrency=CONCURRENCY["task_concurrency"],
                            llm_concurrency=CONCURRENCY["llm_concurrency"],
                            # Rounds
                            max_rounds=ROUNDS["max_rounds"],
                            max_steps_per_turn=ROUNDS["max_steps_per_turn"],
                            variant=variant(
                                "marketplace", assistant, defense, attack, attack_style
                            ),
                        )
