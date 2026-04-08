# New Experiments

The experiment framework lets you define reproducible benchmark configurations as Python files and run them as sweeps.

## What is an Experiment File?

An experiment file is any Python file named `experiment_*.py` (or `experiments.py`) that contains functions named `experiment_*`. Each function does one of the following.

- **Returns** a single config, which defines one benchmark run.
- **Yields** multiple configs, which define a parameter sweep.

## Simple Experiment

A function that returns a single `BaseRunConfig` subclass defines one benchmark run:

```python
# experiment_smoke.py
from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig

def experiment_calendar():
    return CalendarRunConfig(
        paths=["data/calendar-scheduling/small.yaml"],
        limit=2,
        model="gpt-4.1",
        variant="calendar_smoke",
    )
```

You can run it with the following command.

```bash
sagebench experiment experiment_smoke.py
```

## Sweep Experiment

A generator function that yields multiple configs defines a parameter sweep. All yielded configs run together with unified task pooling:

```python
# experiment_full.py
from sage_benchmark.benchmarks.calendar_scheduling.config import CalendarRunConfig

MODEL = "gpt-4.1"
ATTACK_TYPES = ["privacy", "duty_of_care", "due_diligence"]

def experiment_calendar():
    # Normal (benign) run
    yield CalendarRunConfig(
        paths=["data/calendar-scheduling/small.yaml"],
        model=MODEL,
        variant="calendar_normal",
    )
    # Adversarial variants
    for attack in ATTACK_TYPES:
        yield CalendarRunConfig(
            paths=[f"data/small-malicious-hand-crafted-{attack}.yaml"],
            model=MODEL,
            variant=f"calendar_hand_crafted_{attack}",
        )
        yield CalendarRunConfig(
            paths=[f"data/small-whimsical-{attack}.yaml"],
            model=MODEL,
            variant=f"calendar_whimsical_{attack}",
        )
```

This produces 7 experiments, consisting of 1 normal, 3 hand-crafted, and 3 whimsical.

## Config Types

Each benchmark has its own config class extending `BaseRunConfig`:

### CalendarRunConfig

| Field | Type | Description |
|-------|------|-------------|
| `assistant_model` | `str \| None` | Override model for calendar assistant |
| `requestor_model` | `str \| None` | Override model for meeting requestor |
| `expose_preferences` | `bool` | Share scheduling preferences with assistant |
| `assistant_system_prompt` | `str` | System prompt preset or file path |
| `explicit_cot` | `bool` | Enable explicit chain-of-thought |

### FormFillingRunConfig

| Field | Type | Description |
|-------|------|-------------|
| `assistant_model` | `str \| None` | Override model for form-filling assistant |
| `interviewer_model` | `str \| None` | Override model for the interviewer |
| `prompt_type` | `str` | System prompt strategy: `none`, `simple`, `strong`, `ci` |
| `single_field_mode` | `bool` | Fill one field at a time |

### MarketplaceRunConfig

| Field | Type | Description |
|-------|------|-------------|
| `buyer_model` | `str \| None` | Override model for the buyer |
| `seller_model` | `str \| None` | Override model for the seller |

### Shared Fields (BaseRunConfig)

All configs inherit these fields:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `paths` | `list[str]` | — | YAML data files or directories |
| `limit` | `int \| None` | `None` | Maximum tasks to run |
| `batch_size` | `int` | `32` | Parallel task count |
| `model` | `str` | — | Default model for all agents |
| `judge_model` | `str \| None` | `None` | Judge model (defaults to `model`) |
| `judge_votes` | `int` | `3` | Majority vote count for judge |
| `max_rounds` | `int` | `20` | Max conversation rounds |
| `variant` | `str` | `""` | Name used in output directory |
| `output_dir` | `str` | `"outputs"` | Base output directory |

## Running Experiments

```bash
# Run all experiments in a file
sagebench experiment experiment_full.py

# Preview without running
sagebench experiment experiment_full.py --collect

# Filter by pattern (matches variant names)
sagebench experiment experiment_full.py -k calendar
sagebench experiment experiment_full.py -k hand_crafted_privacy

# Run from a directory (discovers all experiment_*.py files)
sagebench experiment ./experiments/
```

## Override Groups

Override groups let you cross-product your experiment configs with parameter variations from the command line, without editing the experiment file. Use `--set key=value` to override any config field, and `--and` to separate multiple groups. Every experiment config is duplicated once per override group.

### Single Override

Run all experiments with a different model than what the file specifies.

```bash
sagebench experiment experiment_full.py --set model=claude-sonnet-4
```

This replaces the `model` field on every config yielded by the experiment file.

### Multiple Overrides in One Group

You can pass `--set` multiple times within the same group to override several fields at once.

```bash
sagebench experiment experiment_full.py \
    --set model=gpt-4.1 \
    --set batch_size=64
```

### Cross-Product with --and

Separate override groups with `--and` to create a cross-product. Each experiment config is duplicated once per group.

```bash
sagebench experiment experiment_full.py \
    --set model=gpt-4.1 \
    --and \
    --set model=claude-sonnet-4 \
    --and \
    --set model=gemini-2.5-flash
```

If the experiment file yields 7 configs, this produces 21 total experiments (7 configs times 3 models). Each duplicated config gets a variant name with the override appended, such as `calendar_normal,model=gpt-4.1`.

### Preview Before Running

Use `--collect` to see the expanded list of experiments before executing them.

```bash
sagebench experiment experiment_full.py \
    --set model=gpt-4.1 --and --set model=claude-sonnet-4 \
    --collect
```

### How It Works

1. The CLI splits the command line on `--and` into separate groups.
2. Each group's `--set key=value` pairs are collected into an override dict.
3. Every experiment config is duplicated once per override group, with the override values applied via `model_copy(update=...)`.
4. The variant name is updated to include the override suffix for uniqueness.
5. Configs that become identical after overrides are deduplicated by content hash.

## How the Runner Works

1. **Discovery** scans files for `experiment_*` functions and calls them to collect configs.
2. **Deduplication** removes configs with identical content hashes.
3. **Unified pooling** places all tasks across all experiments into a single task pool, preventing "tail draining" where one slow experiment blocks others.
4. **Checkpointing** saves each experiment independently for resume support.
5. **Output** writes results per-experiment and saves sweep metadata separately.

## Output Organization

```
outputs/
  sweep_metadata.json
  calendar_normal_gpt-4.1_20260401T120000/
    results.json
  calendar_hand_crafted_privacy_gpt-4.1_20260401T120000/
    results.json
  ...
```

The variant name, model, and timestamp form the output directory name for each experiment.
