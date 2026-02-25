"""Experiment framework for calendar scheduling benchmarks.

Example usage:
    from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig, run_single

    config = ExperimentConfig(
        paths=["data/tasks.yaml"],
        model="gpt-4o",
        assistant_system_prompt="default",
        expose_preferences=True,
        explicit_cot=False,
    )
    output = run_single(config)
    print(output.summary.task_success_rate)
"""

from ..checkpoints import RunConfig
from .collect import collect_all, collect_experiments, discover_experiment_files
from .runner import (
    Experiment,
    ExperimentOutput,
    ExperimentPoolExecutor,
    RunCancelled,
    run_multiple,
    run_single,
    run_single_async,
)

# Backwards compatibility alias
ExperimentConfig = RunConfig
run_experiment = run_single
run_experiment_async = run_single_async

__all__ = [
    "Experiment",
    "ExperimentConfig",
    "ExperimentOutput",
    "ExperimentPoolExecutor",
    "RunCancelled",
    "RunConfig",
    "collect_all",
    "collect_experiments",
    "discover_experiment_files",
    "run_experiment",
    "run_experiment_async",
    "run_multiple",
    "run_single",
    "run_single_async",
]
