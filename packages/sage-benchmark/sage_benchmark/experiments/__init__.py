"""Shared experiments framework for running benchmark sweeps.

Provides generic infrastructure for running multiple experiment
configurations across any benchmark domain.  Each domain provides a
``benchmark_factory`` callable that creates a concrete
:class:`~sage_benchmark.benchmarks.base.Benchmark` subclass from a
:class:`~sage_benchmark.benchmarks.base.BaseRunConfig`.

Usage::

    from . import (
        ExperimentPoolExecutor,
        RunCancelled,
        collect_all,
        run_multiple,
        run_single,
        run_single_async,
    )
"""

from .collect import collect_all, collect_experiments, discover_experiment_files
from .runner import (
    ExperimentPoolExecutor,
    RunCancelled,
    run_multiple,
    run_single,
    run_single_async,
)

__all__ = [
    "ExperimentPoolExecutor",
    "RunCancelled",
    "collect_all",
    "collect_experiments",
    "discover_experiment_files",
    "run_multiple",
    "run_single",
    "run_single_async",
]
