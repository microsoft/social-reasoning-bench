"""Enforced base types, run configuration, and generic type vars for all SAGE benchmarks."""

from __future__ import annotations

import hashlib
import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, TypeVar

import ftfy
from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

_logger = logging.getLogger(__name__)


def _fix_strings(obj: Any) -> None:
    """Recursively apply :func:`ftfy.fix_text` to all strings in a JSON-like structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                obj[k] = ftfy.fix_text(v)
            else:
                _fix_strings(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                obj[i] = ftfy.fix_text(v)
            else:
                _fix_strings(v)


_T = TypeVar("_T", bound=type[BaseModel])


def safe_serializer(cls: _T) -> _T:
    """Class decorator that wraps ``model_dump_json`` with an ftfy fallback.

    Pydantic's Rust-based JSON serializer crashes on non-UTF-8 byte sequences
    (e.g. Windows-1252 fragments from LLM responses).  This decorator wraps
    whatever ``model_dump_json`` the class has — including custom overrides —
    so that on failure it falls back to :func:`ftfy.fix_text` sanitization
    and stdlib ``json`` encoding.

    Usage::

        @safe_serializer
        class MyModel(BaseModel):
            ...
    """
    original = cls.model_dump_json

    def _safe_model_dump_json(self: BaseModel, **kwargs: Any) -> str:
        try:
            return original(self, **kwargs)
        except Exception:
            _logger.debug(
                "%s.model_dump_json failed; falling back to ftfy sanitization",
                type(self).__name__,
            )
            raw = self.model_dump()
            _fix_strings(raw)
            return json.dumps(
                raw,
                indent=kwargs.get("indent"),
                ensure_ascii=False,
                default=str,
            )

    cls.model_dump_json = _safe_model_dump_json  # type: ignore[assignment]
    return cls


# ───────────────────────────────────────────────────────────────────
# Base run configuration
# ───────────────────────────────────────────────────────────────────


class BaseRunConfig(BaseModel):
    """Common run configuration fields shared across all benchmarks.

    Subclasses add role-specific model/url/reasoning overrides and
    benchmark-specific options (e.g. expose_preferences, single_field_mode).
    """

    # --- Task data ---
    paths: list[str] = Field(
        default_factory=list,
        description="YAML files or directories containing task definitions",
    )
    limit: int | None = Field(default=None, description="Limit on number of tasks to load")

    # --- Default model configuration ---
    model: str | None = Field(default=None, description="Default model for all agents")
    base_url: str | None = Field(default=None, description="Default base URL for API")
    api_version: str | None = Field(default=None, description="Default API version")
    reasoning_effort: str | int | None = Field(
        default=None, description="Default reasoning effort for all agents"
    )
    explicit_cot: bool | None = Field(
        default=None, description="Enable explicit chain-of-thought prompting for all agents"
    )

    # --- Judge ---
    judge_model: str | None = Field(default=None, description="Model for LLM-as-judge evaluation")
    judge_base_url: str | None = Field(default=None, description="Base URL for judge API")
    judge_api_version: str | None = Field(default=None, description="API version for judge")
    judge_reasoning_effort: str | int | None = Field(
        default=None, description="Reasoning effort for judge"
    )
    judge_votes: int = Field(default=1, description="Number of judge votes for majority voting")

    # --- Run parameters ---
    max_rounds: int = Field(default=20, description="Maximum conversation rounds per task")
    max_steps_per_turn: int = Field(default=20, description="Maximum tool calls per agent turn")
    batch_size: int = Field(default=32, description="Number of tasks to run in parallel")
    task_concurrency: int | None = Field(
        default=None,
        description="Max concurrent LLM calls per task per provider (None = unlimited)",
    )
    llm_concurrency: int | None = Field(
        default=None,
        description="Max total concurrent LLM calls per provider across all tasks (None = unlimited)",
    )

    # --- System prompt ---
    system_prompt: str | None = Field(
        default=None, description="System prompt preset (e.g. privacy, dd_info_gathering, dd_advocacy, oo)"
    )

    # --- Handcrafted injection ---
    attack_types: list[str] | None = Field(
        default=None,
        description="Hand-crafted attack types to inject at runtime (e.g. privacy, outcome_optimality)",
    )

    # --- Output ---
    output_dir: Path | None = Field(default=None, description="Output directory for results")

    # --- Experiment sweep ---
    variant: str | None = Field(default=None, description="Variant name for experiment sweeps")

    @property
    def resolved_judge_model(self) -> str | None:
        return self.judge_model or self.model

    @property
    def resolved_judge_base_url(self) -> str | None:
        return self.judge_base_url or self.base_url

    @property
    def resolved_judge_api_version(self) -> str | None:
        return self.judge_api_version or self.api_version

    @property
    def resolved_judge_reasoning_effort(self) -> str | int | None:
        if self.judge_reasoning_effort is not None:
            return self.judge_reasoning_effort
        if self.judge_model is not None:
            return None
        return self.reasoning_effort


# ───────────────────────────────────────────────────────────────────
# Enforced base types
# ───────────────────────────────────────────────────────────────────


TTask = TypeVar("TTask", bound="Task")


class Task(BaseModel):
    """Base task.  Every benchmark task must carry at least an id and a
    content-hash for checkpoint deduplication.

    Frozen: tasks are immutable after creation.  The ``hash`` is a
    computed property derived from the task's JSON content, so it is
    always consistent and never needs to be set manually.

    Domain-specific fields (``satisfiable``, ``malicious``, agent
    profiles, etc.) belong on the subclass.
    """

    model_config = ConfigDict(frozen=True)

    CURRENT_VERSION: int = 1

    id: int
    variant: str | None = None
    task_version: int = CURRENT_VERSION

    @model_validator(mode="before")
    @classmethod
    def _version_missing_means_zero(cls, data: dict) -> dict:  # type: ignore[override]
        """Old data without task_version gets version 0, ensuring a hash mismatch.

        Args:
            data: Raw input data dict before model validation.

        Returns:
            The data dict with ``task_version`` set to 0 if it was missing.
        """
        data["task_version"] = data.get("task_version", 0)
        return data

    @computed_field  # type: ignore[prop-decorator]
    @property
    def hash(self) -> str:
        """Content hash for checkpoint dedup (sha256, first 16 hex chars).

        Returns:
            First 16 hex characters of the SHA-256 hash of the task's JSON content.
        """
        content = self.model_dump_json(exclude={"hash", "id"})
        return hashlib.sha256(content.encode()).hexdigest()[:16]


class TaskExecutionResult(ABC, BaseModel, Generic[TTask]):
    """Raw output of running a task — no judgement, just facts."""

    task: TTask
    rounds_completed: int = 0
    error: str | None = None

    @property
    def finished_successfully(self) -> bool:
        # Check truthiness, not just None — error can be "" in some cases.
        return not self.error


class LeakedSecret(ABC, BaseModel):
    """A single detected privacy leak.  Subclass to add domain fields."""

    reasoning: str | None = None
    evidence: list[str] = Field(default_factory=list)

    @computed_field
    @property
    @abstractmethod
    def secret_content(self) -> str:
        """Human-readable summary of what was leaked."""
        ...


TExecResult = TypeVar("TExecResult", bound=TaskExecutionResult)


class TaskEvaluationResult(ABC, BaseModel, Generic[TExecResult]):
    """Per-task evaluation.  The 4 enforced dimensions are always
    present at the same path regardless of benchmark.
    """

    execution: TExecResult

    # ── eval health ──
    error: str | None = None

    # ── 4 enforced evaluation dimensions (computed by subclass) ──

    @computed_field
    @property
    @abstractmethod
    def task_completed(self) -> bool:
        """Whether the task's primary objective was achieved."""
        ...

    @computed_field
    @property
    @abstractmethod
    def privacy_leaks(self) -> Sequence[LeakedSecret]:
        """Detected privacy leaks."""
        ...

    @computed_field
    @property
    @abstractmethod
    def duty_of_care(self) -> float:
        """Duty of care score (0.0-1.0)."""
        ...

    @computed_field
    @property
    @abstractmethod
    def due_diligence(self) -> float:
        """Due diligence score (0.0-1.0)."""
        ...

    @computed_field
    @property
    @abstractmethod
    def leakage_rate(self) -> float:
        """Fraction of secrets leaked."""
        ...

    @computed_field
    @property
    @abstractmethod
    def outcome_optimality(self) -> float:
        """Outcome optimality score (0.0-1.0). Measures how close the agent
        came to the best admissible outcome for the principal."""
        ...

    @property
    def task_hash(self) -> str:
        return self.execution.task.hash

    @property
    def finished_successfully(self) -> bool:
        return not self.error


class BenchmarkEvaluationResult(BaseModel):
    """Aggregate metrics across all tasks — mirrors the 4 task-level
    dimensions.
    """

    total_tasks: int | None = None
    avg_task_completion: float | None = None
    avg_leakage_rate: float | None = None
    avg_duty_of_care: float | None = None
    avg_due_diligence: float | None = None
    avg_outcome_optimality: float | None = None


# ───────────────────────────────────────────────────────────────────
# Generic type vars (single set, used by output, checkpoint, and ABC)
# ───────────────────────────────────────────────────────────────────

TConfig = TypeVar("TConfig", bound=BaseRunConfig)
# TTask is defined above Task; TExecResult is defined above TaskEvaluationResult
TEvalResult = TypeVar("TEvalResult", bound=TaskEvaluationResult)
TBenchmarkEvalResult = TypeVar("TBenchmarkEvalResult", bound=BenchmarkEvaluationResult)


# ───────────────────────────────────────────────────────────────────
# Output envelope
# ───────────────────────────────────────────────────────────────────


@safe_serializer
class BenchmarkOutput(BaseModel, Generic[TConfig, TBenchmarkEvalResult, TEvalResult]):
    config: TConfig
    timestamp: str
    elapsed_seconds: float = 0.0
    evaluation: TBenchmarkEvalResult
    results: list[TEvalResult]


# ───────────────────────────────────────────────────────────────────
# Checkpoint data
# ───────────────────────────────────────────────────────────────────


@safe_serializer
class CheckpointData(BaseModel, Generic[TExecResult, TEvalResult]):
    execution_results: list[TExecResult] = Field(default_factory=list)
    evaluation_results: list[TEvalResult] = Field(default_factory=list)
    completed_task_keys: list[str] = Field(default_factory=list)
    completed_eval_keys: list[str] = Field(default_factory=list)
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())
    config: BaseRunConfig | None = None
    source_file_hashes: dict[str, str] = Field(default_factory=dict)
