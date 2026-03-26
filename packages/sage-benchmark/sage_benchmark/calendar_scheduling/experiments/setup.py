"""Setup utilities for experiment execution."""

import logging
from pathlib import Path

from sage_llm import ModelClient

from ..agents.assistant import get_system_prompt
from ..checkpoints import RunConfig
from ..loader import load_tasks
from ..run_paths import RunPaths
from ..types import KeyedCalendarTask

logger = logging.getLogger(__name__)

# Alias for clarity in this module
ExperimentConfig = RunConfig


def create_run_paths(config: ExperimentConfig) -> RunPaths:
    """Create RunPaths for the experiment.

    Uses config.output_dir if set, otherwise generates a path based on model names.
    """
    if config.output_dir:
        return RunPaths(config.output_dir)

    return RunPaths.create_for_run(
        config.resolved_assistant_model or "unknown",
        config.resolved_requestor_model or "unknown",
        config.resolved_judge_model or "unknown",
    )


def load_experiment_tasks(
    paths: list[str],
    limit: int | None = None,
) -> tuple[list[KeyedCalendarTask], dict[str, str]]:
    """Load tasks from YAML files.

    Args:
        paths: YAML files or directories containing task definitions
        limit: Optional limit on number of tasks

    Returns:
        Tuple of (tasks_with_keys, file_hashes)
    """
    loaded = load_tasks(paths, limit=limit)

    return loaded.all_tasks, loaded.file_hashes


def create_assistant_client(config: ExperimentConfig) -> ModelClient:
    """Create model client for assistant agent."""
    reasoning_effort = config.assistant_reasoning_effort or config.reasoning_effort

    return ModelClient(
        base_url=config.assistant_base_url or config.base_url,
        api_version=config.assistant_api_version or config.api_version,
        reasoning_effort=reasoning_effort,
    )


def create_requestor_client(config: ExperimentConfig) -> ModelClient:
    """Create model client for requestor agent."""
    reasoning_effort = config.requestor_reasoning_effort or config.reasoning_effort

    return ModelClient(
        base_url=config.requestor_base_url or config.base_url,
        api_version=config.requestor_api_version or config.api_version,
        reasoning_effort=reasoning_effort,
    )


def create_judge_client(config: ExperimentConfig) -> ModelClient:
    """Create model client for judge."""
    reasoning_effort = config.judge_reasoning_effort or config.reasoning_effort

    return ModelClient(
        base_url=config.judge_base_url or config.base_url,
        api_version=config.judge_api_version or config.api_version,
        reasoning_effort=reasoning_effort,
    )


def load_system_prompt(config: ExperimentConfig) -> str | None:
    """Load system prompt from file or preset.

    Returns:
        System prompt string or None
    """
    if config.assistant_system_prompt_file:
        prompt_file = Path(config.assistant_system_prompt_file)
        if not prompt_file.exists():
            raise FileNotFoundError(f"System prompt file not found: {prompt_file}")
        logger.info(f"Using custom system prompt from {prompt_file}")
        return prompt_file.read_text().strip()

    if config.assistant_system_prompt:
        system_prompt = get_system_prompt(config.assistant_system_prompt)
        if system_prompt is None:
            logger.info("Running without system prompt")
        else:
            logger.info(f"Using system prompt preset: {config.assistant_system_prompt}")
        return system_prompt

    return None


def resolve_explicit_cot(config: ExperimentConfig) -> tuple[bool, bool]:
    """Resolve explicit CoT flags for assistant and requestor.

    Returns:
        Tuple of (assistant_explicit_cot, requestor_explicit_cot)
    """
    assistant_explicit_cot = (
        config.assistant_explicit_cot
        if config.assistant_explicit_cot is not None
        else (config.explicit_cot or False)
    )
    requestor_explicit_cot = (
        config.requestor_explicit_cot
        if config.requestor_explicit_cot is not None
        else (config.explicit_cot or False)
    )
    return assistant_explicit_cot, requestor_explicit_cot
