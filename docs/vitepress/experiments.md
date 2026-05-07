# Designing experiments

`srbench experiment` runs reproducible benchmark sweeps defined in Python files. It pools tasks across all configs in a sweep so a slow tail in one config doesn't block the rest.

Use it any time you want to compare more than one model, attack, defense, or dataset in a single run.

## Anatomy of an experiment file

An experiment file is any Python file whose name starts with `experiment` (e.g. `experiment.py`, `experiment_full.py`) or is `experiments.py`. Inside, define one or more functions whose names start with `experiment` — the runner discovers and calls each one. Each function:

- **returns** a single config to define one benchmark run, or
- **yields** multiple configs to define a sweep.

```python
# experiments/smoke/experiment.py
from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig
from srbench.benchmarks.marketplace.config import MarketplaceRunConfig

MODEL = "gpt-4.1"


def experiment_calendar():
    return CalendarRunConfig(
        paths=["data/calendar-scheduling/small.yaml"],
        limit=2,
        model=MODEL,
        variant="calendar_smoke",
    )


def experiment_marketplace():
    return MarketplaceRunConfig(
        paths=["data/marketplace/small.yaml"],
        limit=2,
        model=MODEL,
        variant="marketplace_smoke",
    )
```

Run it:

```bash
srbench experiment experiments/smoke
```

You can pass either a file or a directory. Directories are searched recursively for `experiment.py`, `experiment_*.py`, and `experiments.py` files.

## Sweeps

Yield instead of return to produce multiple configs from one function. The runner pools all yielded tasks across all functions and runs them together.

```python
from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

ATTACKS = ["privacy", "due_diligence", "outcome_optimality"]


def experiment_calendar():
    # Benign baseline
    yield CalendarRunConfig(
        paths=["data/calendar-scheduling/small.yaml"],
        model="gpt-4.1",
        variant="calendar_benign",
    )
    # One run per attack type, hand-crafted style
    for attack in ATTACKS:
        yield CalendarRunConfig(
            paths=["data/calendar-scheduling/small.yaml"],
            model="gpt-4.1",
            attack_types=[attack],
            variant=f"calendar_handcrafted_{attack}",
        )
    # One run per attack type, whimsical (pre-generated) style
    for attack in ATTACKS:
        yield CalendarRunConfig(
            paths=[f"data/calendar-scheduling/small-whimsical-{attack}.yaml"],
            model="gpt-4.1",
            variant=f"calendar_whimsical_{attack}",
        )
```

## Config types

Every config inherits from `BaseRunConfig`. The fields below are the most common ones — see the source for the full list.

### Shared fields (BaseRunConfig)

| Field                | Type            | Description                                  |
|----------------------|-----------------|----------------------------------------------|
| `paths`              | `list[str]`     | YAML data files or directories               |
| `limit`              | `int \| None`   | Maximum tasks to run                         |
| `model`              | `str`           | Default model for all agents                 |
| `judge_model`        | `str \| None`   | Override model for evaluation                |
| `judge_votes`        | `int`           | Majority-vote count for the judge            |
| `system_prompt`      | `str`           | Preset: `none`, `privacy`, `dd_info_gathering`, `dd_advocacy`, `oo`, `all` |
| `attack_types`       | `list[str]`     | Hand-crafted attacks: `privacy`, `outcome_optimality`, `due_diligence` |
| `max_rounds`         | `int`           | Max conversation rounds                      |
| `max_steps_per_turn` | `int`           | Max tool calls per agent turn                |
| `batch_size`         | `int`           | Parallel task count                          |
| `task_concurrency`   | `int \| None`   | Max LLM calls per task                       |
| `llm_concurrency`    | `int \| None`   | Max LLM calls per provider total             |
| `variant`            | `str`           | Name segment used in the output directory    |
| `output_dir`         | `str`           | Base output directory                        |

### CalendarRunConfig

Adds:

| Field                          | Description                                    |
|--------------------------------|------------------------------------------------|
| `assistant_model`              | Override model for the calendar assistant      |
| `requestor_model`              | Override model for the meeting requestor       |
| `assistant_reasoning_effort`   | Reasoning effort for the assistant             |
| `requestor_reasoning_effort`   | Reasoning effort for the requestor             |
| `assistant_explicit_cot`       | Chain-of-thought toggle for the assistant      |
| `requestor_explicit_cot`       | Chain-of-thought toggle for the requestor      |
| `expose_preferences`           | Share scheduling preferences with the assistant |

### MarketplaceRunConfig

Adds:

| Field                       | Description                              |
|-----------------------------|------------------------------------------|
| `buyer_model`               | Override model for the buyer             |
| `seller_model`              | Override model for the seller            |
| `buyer_reasoning_effort`    | Reasoning effort for the buyer           |
| `seller_reasoning_effort`   | Reasoning effort for the seller          |
| `buyer_explicit_cot`        | Chain-of-thought toggle for the buyer    |
| `seller_explicit_cot`       | Chain-of-thought toggle for the seller   |

## Override groups

`--set key=value` overrides a config field on every yielded config. `--and` separates multiple override groups, producing a cross-product.

```bash
# Replace the model on every config in the file
srbench experiment experiments/v0.1.0 --set model=claude-sonnet-4-5

# Override several fields at once
srbench experiment experiments/v0.1.0 \
    --set model=gpt-4.1 \
    --set batch_size=64

# Cross-product across three models — every config runs three times
srbench experiment experiments/v0.1.0 \
    --set model=gpt-4.1 \
    --and --set model=claude-sonnet-4-5 \
    --and --set model=gemini-2.5-flash
```

Each override group's values are appended to the variant name (e.g. `calendar_benign,model=gpt-4.1`) so output directories stay unique. Configs that collapse to the same content after overrides are deduplicated.

## Filtering and previewing

```bash
# Preview without executing
srbench experiment experiments/v0.1.0 --collect

# Filter by variant pattern (repeatable)
srbench experiment experiments/v0.1.0 -k calendar
srbench experiment experiments/v0.1.0 -k handcrafted_privacy

# Combine — preview only matching, cross-product configs
srbench experiment experiments/v0.1.0 -k calendar \
    --set model=gpt-4.1 --and --set model=claude-sonnet-4-5 \
    --collect
```

## Concurrency, resume, and logging

These work the same as on `srbench benchmark`:

```bash
srbench experiment experiments/v0.1.0 \
    --batch-size 200 \
    --task-concurrency 5 \
    --llm-concurrency 64 \
    --logger progress
```

| Flag             | Description                                                   |
|------------------|---------------------------------------------------------------|
| `--batch-size`   | Tasks running in parallel across the pool                      |
| `--task-concurrency` | Max LLM calls per task                                     |
| `--llm-concurrency`  | Max LLM calls per provider total                           |
| `--restart-exec` | Re-run executions, ignoring checkpoints                        |
| `--restart-eval` | Re-run evaluation, keeping cached executions                   |
| `--finalize`     | Build `results.json` from existing checkpoints without running |
| `--logger`       | `verbose`, `progress`, or `quiet`                              |
| `--output-base`  | Base directory for sweep outputs                               |

## Output

```
outputs/
  sweep_metadata.json
  calendar_benign_gpt-4.1_20260507T120000/
    results.json
  calendar_handcrafted_privacy_gpt-4.1_20260507T120000/
    results.json
  ...
```

Open the [Results](/results) page pre-loaded with the sweep you just ran:

```bash
srbench dashboard outputs/v0.1.0/
```

Pass any mix of `results.json` files or sweep directories — directories are scanned recursively. Always scope to a specific sweep folder rather than `outputs/` itself, since `outputs/` holds every run you've ever done.

## Reference: real sweep

The repo ships with the v0.1.0 paper sweep at `experiments/v0.1.0/`. It crosses several models against benign and adversarial conditions, and is a good starting template for your own sweeps:

```bash
srbench experiment experiments/v0.1.0
```
