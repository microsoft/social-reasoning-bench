"""``sage_benchmark.benchmarks.base`` — abstract base classes and enforced types for SAGE benchmarks.

Subclassing ``Benchmark`` is the single thing needed to implement a new
benchmark.  The package provides:

Enforced base types
    ``BaseRunConfig``, ``Task``, ``TaskExecutionResult``, ``LeakedSecret``,
    ``TaskEvaluationResult``, ``BenchmarkEvaluationResult``,
    ``CheckpointData``, and ``BenchmarkOutput``.  Every benchmark extends
    these with domain-specific fields.

Abstract methods
    The genuinely domain-specific parts: setup, execute, evaluate, summarize,
    error handling, CLI argument parsing, and display.

Concrete lifecycle
    Checkpointing, skip-set resume, parallel execution via
    ``TaskPoolExecutor``, output serialization, and the CLI entry-point.
    Subclasses inherit all of this for free.
"""

from .benchmark import Benchmark
from .checkpoint import CheckpointManager
from .types import (
    BaseRunConfig,
    BenchmarkEvaluationResult,
    BenchmarkOutput,
    CheckpointData,
    LeakedSecret,
    Task,
    TaskEvaluationResult,
    TaskExecutionResult,
    TBenchmarkEvalResult,
    TConfig,
    TEvalResult,
    TExecResult,
    TTask,
)

__all__ = [
    "BaseRunConfig",
    "Benchmark",
    "BenchmarkEvaluationResult",
    "BenchmarkOutput",
    "CheckpointData",
    "CheckpointManager",
    "LeakedSecret",
    "Task",
    "TaskEvaluationResult",
    "TaskExecutionResult",
    "TBenchmarkEvalResult",
    "TConfig",
    "TEvalResult",
    "TExecResult",
    "TTask",
]
