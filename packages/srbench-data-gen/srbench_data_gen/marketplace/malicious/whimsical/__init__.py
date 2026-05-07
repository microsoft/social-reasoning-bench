"""Whimsical adversarial strategy generation for marketplace tasks."""

from srbench_data_gen.shared.whimsical import (
    StrategyProvider,
    build_arg_parser,
    run_strategy_generation,
    save_strategies_yaml,
)

from .inject import build_malicious_instruction

__all__ = [
    "StrategyProvider",
    "build_arg_parser",
    "build_malicious_instruction",
    "run_strategy_generation",
    "save_strategies_yaml",
]
