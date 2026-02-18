"""Malicious interviewer prompts for form filling benchmark.

This module generates malicious interviewer system prompts by combining
the game context from datasets/gullibility/game_context_interviewer.txt
with strategies from data/form-filling/strategies.yaml.
"""

from pathlib import Path

import yaml


def _get_project_root() -> Path:
    """Get the project root directory (sage/)."""
    # This file is at sage-benchmark/sage_benchmark/form_filling/malicious_prompts.py
    # Project root is 4 levels up
    return Path(__file__).parent.parent.parent.parent


def _load_game_context() -> str:
    """Load the game context interviewer prompt.

    Returns:
        The content of game_context_interviewer.txt
    """
    game_context_path = (
        _get_project_root() / "datasets" / "gullibility" / "game_context_interviewer.txt"
    )
    return game_context_path.read_text()


def _load_strategies() -> list[str]:
    """Load all strategies from strategies.yaml.

    Returns:
        List of strategy strings
    """
    strategies_path = (
        _get_project_root() / "sage-benchmark" / "data" / "form-filling" / "strategies.yaml"
    )
    with open(strategies_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("strategies", [])


def get_malicious_interviewer_prompt(strategy_index: int) -> str:
    """Get a malicious interviewer system prompt with the specified strategy.

    Combines the game context from game_context_interviewer.txt with
    the n-th strategy from strategies.yaml.

    Args:
        strategy_index: 0-based index of the strategy to use

    Returns:
        The complete malicious interviewer system prompt

    Raises:
        IndexError: If strategy_index is out of range
    """
    game_context = _load_game_context()
    strategies = _load_strategies()

    if strategy_index < 0 or strategy_index >= len(strategies):
        raise IndexError(
            f"Strategy index {strategy_index} is out of range. Valid range: 0-{len(strategies) - 1}"
        )

    strategy = strategies[strategy_index]

    # Combine game context with the selected strategy
    malicious_prompt = f"""{game_context}

### STRATEGY TO USE
{strategy}
"""

    return malicious_prompt


def get_num_strategies() -> int:
    """Get the total number of available strategies.

    Returns:
        Number of strategies in strategies.yaml
    """
    strategies = _load_strategies()
    return len(strategies)
