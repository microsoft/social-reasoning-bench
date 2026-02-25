# Calendar Scheduling Experiment Framework

Adds an experiment framework for the calendar scheduling benchmark that enables:
- **Python experiment files** with pytest-style discovery (`experiment_*.py`)
- **Parameter sweeps** via `--and` / `--with` flags
- **Unified task pooling** across multiple experiments for efficient execution
- **Experiment class** for programmatic experiment lifecycle management

## CLI Usage

```bash
# Discover and list experiments
sagebench calendar --experiments experiments/my-experiments/ --collect-only

# Run all experiments in a directory
sagebench calendar --experiments experiments/my-experiments/

# Filter by pattern
sagebench calendar --experiments experiments/my-experiments/ -k "normal"

# Standalone experiments CLI
uv run -m sage_benchmark.calendar_scheduling.experiments experiments/my-experiments/ --collect
```

## Python Usage

```python
from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig, run_single

# Define and run a single experiment
config = ExperimentConfig(
    paths=["data/calendar-scheduling/final/tasks.yaml"],
    model="gpt-4o",
    assistant_system_prompt="default",
    expose_preferences=True,
    explicit_cot=False,
)
output = run_single(config)
print(output.summary.task_success_rate)
```

## Experiment File Format

Create `experiment_*.py` files with functions that return `ExperimentConfig`:

```python
# experiments/my-experiments/experiment_privacy.py
from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig

def experiment_default():
    return ExperimentConfig(
        paths=["data/calendar-scheduling/final/tasks.yaml"],
        model="gpt-4o",
        assistant_system_prompt="default",
        expose_preferences=True,
        explicit_cot=False,
    )

def experiment_privacy():
    return ExperimentConfig(
        paths=["data/calendar-scheduling/final/tasks.yaml"],
        model="gpt-4o",
        assistant_system_prompt="privacy-ci",
        expose_preferences=True,
        explicit_cot=False,
    )
```

## Generating Multiple Experiments with Yield

Use generators to create experiment grids from a single function:

```python
# experiments/my-experiments/experiment_grid.py
from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig

MODELS = ["gpt-4o", "gpt-4.1", "claude-sonnet-4"]
PROMPTS = ["default", "privacy-ci", "privacy-strong"]

def experiment_model_prompt_grid():
    """Generate experiments for all model x prompt combinations."""
    for model in MODELS:
        for prompt in PROMPTS:
            yield ExperimentConfig(
                paths=["data/calendar-scheduling/final/tasks.yaml"],
                model=model,
                assistant_system_prompt=prompt,
                expose_preferences=True,
                explicit_cot=False,
                variant=f"{model.split('/')[-1]}_{prompt}",  # e.g. "gpt-4o_privacy-ci"
            )

def experiment_reasoning_effort_sweep():
    """Sweep reasoning effort levels for a single model."""
    for effort in ["none", "low", "medium", "high"]:
        yield ExperimentConfig(
            paths=["data/calendar-scheduling/final/tasks.yaml"],
            model="gpt-4o",
            assistant_system_prompt="default",
            reasoning_effort=effort,
            expose_preferences=True,
            explicit_cot=False,
            variant=f"reasoning_{effort}",
        )
```

This would generate 9 experiments from `experiment_model_prompt_grid` and 4 from `experiment_reasoning_effort_sweep`:

```bash
$ sagebench calendar --experiments experiments/my-experiments/ --collect-only
Collected 13 experiments
  gpt-4o_default
  gpt-4o_privacy-ci
  gpt-4o_privacy-strong
  gpt-4.1_default
  gpt-4.1_privacy-ci
  gpt-4.1_privacy-strong
  claude-sonnet-4_default
  claude-sonnet-4_privacy-ci
  claude-sonnet-4_privacy-strong
  reasoning_none
  reasoning_low
  reasoning_medium
  reasoning_high
```

## Changes

- Add `experiments/` module with collection, runner, setup, and output utilities
- Add `--experiments`, `--collect-only`, `-k` CLI arguments
- Add `ExperimentConfig` alias and make `RunConfig` fields optional with defaults
- Add `Experiment` class and `ExperimentPoolExecutor` for unified task pooling
