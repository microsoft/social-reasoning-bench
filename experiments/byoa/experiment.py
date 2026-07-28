"""
Experiments for SocialReasoning-Bench — Bring Your Own Agent (BYOA)

A clone of the v0.1.0 experiment, but the assistant side is driven by
*bring-your-own-agent* implementations from the ``srbench-agents`` package
(the Claude Agent SDK agent and the OpenClaw CLI agent) instead of the built-in
model-driven assistant. Everything else — the counterparty, judge, attacks,
defenses, and data — mirrors v0.1.0 so results are directly comparable.

Model and reasoning effort are supplied *per variant* through
``assistant_agent_kwargs`` / ``buyer_agent_kwargs`` (forwarded to each agent's
constructor), so a single ``srbench experiment`` run can sweep multiple agents.

Prerequisites:
    pip install 'srbench-agents[claude]'      # Claude agent (in-process)
    npm install -g openclaw@2026.5.28         # OpenClaw agent (Gateway)

Provide each backend's credentials through the environment (e.g.
``ANTHROPIC_API_KEY`` for Claude, ``OPENAI_API_KEY`` for OpenClaw's ``openai/*``
models). OpenClaw runs in a throwaway profile per sweep, so ``openclaw onboard``
is not required.

To reproduce:
    srbench experiment experiments/byoa

    # Outputs land in: outputs/byoa
"""

from pathlib import Path
from typing import Any, Literal

from srbench_agents import DEFAULT_ASSISTANT_SYSTEM_PROMPT

# BYOA runs are heavier than model-only runs (each task holds an OpenClaw
# Gateway exclusively while it runs), so this defaults to the "small" split.
# Set to "large" to match the v0.1.0 sweep exactly.
DATA_SIZE: Literal["small", "medium", "large"] = "small"

JUDGE: dict[str, Any] = {
    "model": "gemini-2.5-flash",
    # Use dynamic thinking (the default for gemini-2.5-flash)
    "reasoning_effort": -1,
    "explicit_cot": False,
}

COUNTERPARTY: dict[str, Any] = {
    "model": "gemini-3-flash-preview",
    "reasoning_effort": "medium",
    "explicit_cot": False,
}

# ``batch_size`` is the number of tasks run concurrently. A task holds one
# OpenClaw Gateway exclusively while it runs, and the pool defaults to a single
# Gateway, so set SRBENCH_OPENCLAW_POOL_SIZE to batch_size to actually run tasks
# in parallel; otherwise they queue behind one Gateway. Each Gateway is a Node
# process, so size it deliberately.
CONCURRENCY: dict[str, Any] = {"batch_size": 10, "task_concurrency": 10, "llm_concurrency": 1}

ROUNDS: dict[str, Any] = {"max_rounds": 10, "max_steps_per_turn": 3}

# --- Assistant sweep: model × reasoning-effort grid, per BYOA agent ---------
#
# ``model`` and ``reasoning_effort`` are forwarded to each agent's constructor
# per variant (via assistant_agent_kwargs / buyer_agent_kwargs), so a single
# `srbench experiment` run sweeps the whole grid. Model namespaces and effort
# vocabularies differ per backend, so each agent declares its own lists:
#
#   - Claude effort   -> SDK ``effort``    : low / medium / high / xhigh / max
#   - OpenClaw effort -> thinking level    : off / minimal / low / medium / high /
#                                            xhigh / adaptive / max
#
# OpenClaw models are ``provider/model`` strings (a bare model id is rejected).
# Provider credentials come from the environment (e.g. OPENAI_API_KEY,
# ANTHROPIC_API_KEY); no ``openclaw onboard`` step is required.
AGENTS: list[dict[str, Any]] = [
    # {
    #     # Claude Agent SDK (in-process MCP). Requires srbench-agents[claude].
    #     "name": "claude",
    #     "agent": "srbench_agents.claude_agent:ClaudeAgent",
    #     "models": ["claude-sonnet-4-6"],
    #     "efforts": ["high"],
    # },
    {
        # OpenClaw, driven over its Gateway (HTTP MCP). Requires openclaw@2026.5.28.
        "name": "openclaw",
        "agent": "srbench_agents.openclaw_agent:OpenClawAgent",
        "models": ["openai/gpt-5.4", "openai/gpt-5.5"],
        "efforts": ["high"],
    },
]


def assistants():
    """BYOA assistants under test — a model × reasoning-effort grid per agent.

    Each agent declares its own ``models`` and ``efforts`` lists (the model
    namespace and effort vocabulary differ per backend), and this yields the
    full grid. Every entry provides an import string (``agent``) and the
    constructor ``kwargs`` forwarded to it; ``label`` builds a filesystem-safe
    variant name. Edit ``AGENTS`` to widen or narrow the sweep.
    """
    for spec in AGENTS:
        for model in spec["models"]:
            for effort in spec["efforts"]:
                yield {
                    "label": f"{spec['name']}_{model}_{effort}",
                    "agent": spec["agent"],
                    # Pass the canonical operating prompt explicitly so every
                    # agent runs under the same rules (rather than each agent
                    # falling back to its own built-in default).
                    "kwargs": {
                        "model": model,
                        "reasoning_effort": effort,
                        "system_prompt": DEFAULT_ASSISTANT_SYSTEM_PROMPT,
                    },
                }


def attacks():
    yield from ["none"]  # , "outcome_optimality", "due_diligence"]


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
    parts = [benchmark, assistant["label"], defense, attack_style, attack]
    variant_name = "_".join(parts)
    # Replace path-unsafe characters with '-'
    variant_name = "".join(c if c.isalnum() or c in ("_", "-") else "-" for c in variant_name)
    return variant_name


# --- Calendar ---


def experiment_calendar():
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

    for assistant in assistants():
        for attack in attacks():
            for attack_style in attack_styles(attack):
                for defense in defenses():
                    for path in data_paths(attack, attack_style, "data/calendar-scheduling"):
                        yield CalendarRunConfig(
                            paths=[path],
                            # Assistant (BYOA)
                            assistant_agent=assistant["agent"],
                            assistant_agent_kwargs=assistant["kwargs"],
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
    return
    from srbench.benchmarks.marketplace.config import MarketplaceRunConfig

    for assistant in assistants():
        for attack in attacks():
            for attack_style in attack_styles(attack):
                for defense in defenses():
                    for path in data_paths(attack, attack_style, "data/marketplace"):
                        yield MarketplaceRunConfig(
                            paths=[path],
                            # Buyer / assistant (BYOA)
                            buyer_agent=assistant["agent"],
                            buyer_agent_kwargs=assistant["kwargs"],
                            system_prompt=defense,
                            # Seller / counterparty
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
