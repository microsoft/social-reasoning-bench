"""Experiment discovery and collection from Python files."""

import importlib.util
import logging
import sys
from pathlib import Path
from typing import Any, Generator, Iterator

from ..checkpoints import RunConfig

logger = logging.getLogger(__name__)

# Alias for clarity in this module
ExperimentConfig = RunConfig


def discover_experiment_files(path: Path) -> list[Path]:
    """Find experiment files recursively.

    Looks for files matching:
    - experiment_*.py
    - experiments.py

    Args:
        path: File or directory to search

    Returns:
        List of paths to experiment files
    """
    if path.is_file():
        if path.name.startswith("experiment") and path.suffix == ".py":
            return [path]
        return []

    files = []
    for pattern in ["experiment_*.py", "experiments.py"]:
        files.extend(path.rglob(pattern))

    return sorted(files)


def load_module(path: Path) -> Any:
    """Dynamically load a Python module from path.

    Args:
        path: Path to Python file

    Returns:
        Loaded module object
    """
    module_name = f"_experiment_{path.stem}_{id(path)}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def collect_experiments(module: Any) -> Iterator[tuple[str, ExperimentConfig]]:
    """Extract experiment configs from a module.

    Looks for functions named experiment_* and calls them.
    Functions can either:
    - Return a single ExperimentConfig
    - Yield multiple ExperimentConfig objects (generator)

    Args:
        module: Loaded Python module

    Yields:
        Tuples of (name, config)
    """
    for name in dir(module):
        if not name.startswith("experiment_"):
            continue

        func = getattr(module, name)
        if not callable(func):
            continue

        try:
            result = func()

            # Check if it's a generator
            if isinstance(result, Generator):
                for i, config in enumerate(result):
                    if isinstance(config, ExperimentConfig):
                        yield_name = config.variant or f"{name}_{i}"
                        yield (yield_name, config)
            elif isinstance(result, ExperimentConfig):
                yield_name = result.variant or name.replace("experiment_", "")
                yield (yield_name, result)

        except Exception as e:
            logger.warning("Failed to collect %s: %s", name, e)


def _config_key(config: ExperimentConfig) -> tuple:
    """Generate a hashable key for config deduplication.

    Includes all fields that affect experiment behavior, excluding variant name
    and output_dir which are just labels/paths.
    """
    return (
        tuple(config.paths),
        config.model,
        config.assistant_model,
        config.requestor_model,
        config.judge_model,
        config.assistant_system_prompt,
        config.expose_preferences,
        config.explicit_cot,
        config.assistant_explicit_cot,
        config.requestor_explicit_cot,
        config.reasoning_effort,
        config.assistant_reasoning_effort,
        config.requestor_reasoning_effort,
        config.judge_reasoning_effort,
        config.max_rounds,
        config.max_steps_per_turn,
        config.limit,
    )


def _apply_override_groups(
    configs: list[tuple[Path, str, ExperimentConfig]],
    override_groups: list[dict[str, Any]],
) -> list[tuple[Path, str, ExperimentConfig]]:
    """Apply override groups to expand configs.

    Each config is duplicated N times, once for each override group.

    Args:
        configs: List of (file_path, name, config) tuples
        override_groups: List of override dicts to apply

    Returns:
        Expanded list of configs
    """
    if not override_groups:
        return configs

    expanded = []
    for file_path, name, config in configs:
        for i, overrides in enumerate(override_groups):
            # Create variant name
            override_parts = [f"{k}={v}" for k, v in overrides.items()]
            override_suffix = ",".join(override_parts) if override_parts else f"override_{i}"
            new_name = f"{name},{override_suffix}"

            # Apply overrides
            new_config = config.model_copy(update={**overrides, "variant": new_name})
            expanded.append((file_path, new_name, new_config))

    return expanded


def collect_all(
    path: Path,
    pattern: str | None = None,
    override_groups: list[dict[str, Any]] | None = None,
) -> list[tuple[Path, str, ExperimentConfig]]:
    """Collect all experiments from path.

    Args:
        path: File or directory to search
        pattern: Optional pattern to filter experiment names
        override_groups: Optional list of override dicts to apply

    Returns:
        List of (file_path, name, config) tuples
    """
    files = discover_experiment_files(path)

    if not files:
        logger.warning("No experiment files found in %s", path)
        return []

    # Collect experiments from all files
    configs: list[tuple[Path, str, ExperimentConfig]] = []
    seen_names: set[str] = set()
    seen_keys: set[tuple] = set()

    for file_path in files:
        try:
            module = load_module(file_path)

            for name, config in collect_experiments(module):
                # Apply pattern filter
                if pattern and pattern not in name:
                    continue

                # Check for duplicate names
                if name in seen_names:
                    logger.warning("Duplicate experiment name: %s (from %s)", name, file_path)
                    continue
                seen_names.add(name)

                # Check for duplicate configs
                key = _config_key(config)
                if key in seen_keys:
                    logger.warning("Duplicate config detected: %s", name)
                    continue
                seen_keys.add(key)

                configs.append((file_path, name, config))

        except Exception as e:
            logger.error("Failed to load %s: %s", file_path, e)

    # Apply override groups
    if override_groups:
        configs = _apply_override_groups(configs, override_groups)

        # Deduplicate after overrides (configs may become identical)
        seen_keys: set[tuple] = set()
        deduped: list[tuple[Path, str, ExperimentConfig]] = []
        for file_path, name, config in configs:
            key = _config_key(config)
            if key not in seen_keys:
                seen_keys.add(key)
                deduped.append((file_path, name, config))
            else:
                logger.debug("Deduplicated after override: %s", name)

        if len(deduped) < len(configs):
            logger.info(
                "Deduplicated %d -> %d experiments after overrides", len(configs), len(deduped)
            )
        configs = deduped

    return configs
