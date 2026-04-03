"""Whimsical adversarial strategy generation for form filling tasks."""

from sage_data_gen.shared.whimsical import (
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
