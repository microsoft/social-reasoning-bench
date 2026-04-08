"""Experiment discovery and collection from Python files."""

import importlib.util
import json
import logging
import sys
from pathlib import Path
from typing import Any, Generator, Iterator

from ..benchmarks.base.types import BaseRunConfig

logger = logging.getLogger(__name__)


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


def collect_experiments(module: Any) -> Iterator[tuple[str, BaseRunConfig]]:
    """Extract experiment configs from a module.

    Looks for functions named ``experiment_*`` and calls them.
    Functions can either:
    - Return a single BaseRunConfig (or subclass)
    - Yield multiple BaseRunConfig objects (generator)

    Args:
        module: Loaded Python module

    Yields:
        Tuples of (name, config)
    """
    for name in dir(module):
        if not name.startswith("experiment"):
            continue

        func = getattr(module, name)
        if not callable(func):
            continue

        try:
            result = func()

            if isinstance(result, Generator):
                for i, config in enumerate(result):
                    if isinstance(config, BaseRunConfig):
                        yield_name = config.variant or f"{name}_{i}"
                        yield (yield_name, config)
            elif isinstance(result, BaseRunConfig):
                yield_name = result.variant or name.replace("experiment_", "")
                yield (yield_name, result)

        except Exception as e:
            logger.warning("Failed to collect %s: %s", name, e)


def _config_key(config: BaseRunConfig) -> str:
    """Generate a hashable key for config deduplication.

    Serializes all fields except variant and output_dir (which are just
    labels/paths and don't affect experiment behaviour).

    Args:
        config: The run configuration to generate a key for.

    Returns:
        A deterministic JSON string suitable for use as a dict key or set member.
    """
    data = config.model_dump(exclude={"variant", "output_dir"})
    return json.dumps(data, sort_keys=True, default=str)


def _apply_override_groups(
    configs: list[tuple[Path, str, BaseRunConfig]],
    override_groups: list[dict[str, Any]],
) -> list[tuple[Path, str, BaseRunConfig]]:
    """Apply override groups to expand configs.

    Each config is duplicated once per override group.

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
            override_parts = [f"{k}={v}" for k, v in overrides.items() if k != "limit"]
            if override_parts:
                new_name = f"{name},{','.join(override_parts)}"
            else:
                new_name = name
            updated = {**config.model_dump(), **overrides, "variant": new_name}
            new_config = type(config).model_validate(updated)
            expanded.append((file_path, new_name, new_config))

    return expanded


def collect_all(
    path: Path,
    patterns: list[str] | None = None,
    override_groups: list[dict[str, Any]] | None = None,
) -> list[tuple[Path, str, BaseRunConfig]]:
    """Collect all experiments from path.

    Args:
        path: File or directory to search
        patterns: Optional list of patterns to filter experiment names (OR logic)
        override_groups: Optional list of override dicts to apply

    Returns:
        List of (file_path, name, config) tuples
    """
    files = discover_experiment_files(path)

    if not files:
        logger.warning("No experiment files found in %s", path)
        return []

    configs: list[tuple[Path, str, BaseRunConfig]] = []
    seen_names: set[str] = set()
    seen_keys: set[str] = set()

    for file_path in files:
        try:
            module = load_module(file_path)

            for name, config in collect_experiments(module):
                if patterns and not all(p in name for p in patterns):
                    continue

                if name in seen_names:
                    logger.warning("Duplicate experiment name: %s (from %s)", name, file_path)
                    continue
                seen_names.add(name)

                key = _config_key(config)
                if key in seen_keys:
                    logger.warning("Duplicate config detected: %s", name)
                    continue
                seen_keys.add(key)

                configs.append((file_path, name, config))

        except Exception as e:
            logger.error("Failed to load %s: %s", file_path, e)

    if override_groups:
        configs = _apply_override_groups(configs, override_groups)

        # Deduplicate after overrides
        seen_keys_dedup: set[str] = set()
        deduped: list[tuple[Path, str, BaseRunConfig]] = []
        for file_path, name, config in configs:
            key = _config_key(config)
            if key not in seen_keys_dedup:
                seen_keys_dedup.add(key)
                deduped.append((file_path, name, config))
            else:
                logger.debug("Deduplicated after override: %s", name)

        if len(deduped) < len(configs):
            logger.info(
                "Deduplicated %d -> %d experiments after overrides", len(configs), len(deduped)
            )
        configs = deduped

    return configs
