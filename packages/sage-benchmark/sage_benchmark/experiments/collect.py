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
        if path.suffix == ".py" and (
            path.name.startswith("experiment") or path.name == "experiments.py"
        ):
            return [path]
        return []

    files = []
    for pattern in ["experiment_*.py", "experiment.py", "experiments.py"]:
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


def _collect_base(path: Path, files: list[Path]) -> list[tuple[Path, str, BaseRunConfig]]:
    """Collect all experiments from discovered files without filtering.

    Args:
        path: Original search path (for logging).
        files: Pre-discovered experiment files.

    Returns:
        List of (file_path, name, config) tuples.
    """
    configs: list[tuple[Path, str, BaseRunConfig]] = []
    seen_names: set[str] = set()

    for file_path in files:
        try:
            module = load_module(file_path)

            for name, config in collect_experiments(module):
                if name in seen_names:
                    logger.warning("Duplicate experiment name: %s (from %s)", name, file_path)
                    continue
                seen_names.add(name)
                configs.append((file_path, name, config))

        except Exception as e:
            logger.error("Failed to load %s: %s", file_path, e)

    return configs


def _matches_patterns(name: str, patterns: list[str]) -> bool:
    """Check if name matches all patterns (AND logic within a group).

    Args:
        name: Experiment name to check.
        patterns: List of patterns that must all appear in name.

    Returns:
        True if all patterns are substrings of name.
    """
    return all(p in name for p in patterns)


def collect_all(
    path: Path,
    pattern_groups: list[list[str]] | None = None,
    override_groups: list[dict[str, Any]] | None = None,
) -> list[tuple[Path, str, BaseRunConfig]]:
    """Collect experiments from path, applying per-group filters and overrides.

    Each ``--and``-separated group specifies an independent collection pass
    with its own ``-k`` patterns (AND'd within group) and ``--set`` overrides.
    Results across groups are unioned (OR across groups), then deduplicated.

    Args:
        path: File or directory to search.
        pattern_groups: List of pattern lists, one per ``--and`` group.
            Within a group, all patterns must match (AND). Across groups,
            results are unioned (OR). If None or all groups empty, no filtering.
        override_groups: List of override dicts, one per ``--and`` group.
            Each group's overrides are applied to experiments matched by
            that group's patterns.

    Returns:
        Deduplicated list of (file_path, name, config) tuples.
    """
    files = discover_experiment_files(path)

    if not files:
        logger.warning("No experiment files found in %s", path)
        return []

    all_base = _collect_base(path, files)

    # Normalize groups
    if pattern_groups is None:
        pattern_groups = [[]]
    if override_groups is None:
        override_groups = [{}]

    # Pad shorter list to match lengths
    n_groups = max(len(pattern_groups), len(override_groups))
    while len(pattern_groups) < n_groups:
        pattern_groups.append([])
    while len(override_groups) < n_groups:
        override_groups.append({})

    # Collect per-group, then union
    configs: list[tuple[Path, str, BaseRunConfig]] = []
    seen_keys: set[str] = set()

    for patterns, overrides in zip(pattern_groups, override_groups):
        # Filter by this group's patterns
        if patterns:
            group_configs = [
                (fp, name, cfg)
                for fp, name, cfg in all_base
                if _matches_patterns(name, patterns)
            ]
        else:
            group_configs = list(all_base)

        # Apply this group's overrides
        if overrides:
            group_configs = _apply_override_groups(group_configs, [overrides])

        # Union with deduplication
        for fp, name, cfg in group_configs:
            key = _config_key(cfg)
            if key not in seen_keys:
                seen_keys.add(key)
                configs.append((fp, name, cfg))

    return configs
