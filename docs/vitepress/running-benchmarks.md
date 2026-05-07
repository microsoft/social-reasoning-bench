# Experiment Reproduction

The `srbench` CLI has two modes:

- **`srbench benchmark`** runs a single benchmark with explicit flags.
- **`srbench experiment`** runs experiment sweeps from Python config files.

## Running Individual Benchmarks

### Calendar Scheduling

Two agents (Assistant + Requestor) negotiate to schedule a meeting. The assistant must protect private calendar events while finding a suitable time slot.

```bash
srbench benchmark calendar \
    --data ./data/calendar-scheduling/small.yaml \
    --model gpt-4.1 \
    --assistant-system-prompt default \
    --expose-preferences false \
    --limit 2
```

The following flags are specific to calendar scheduling.

| Flag | Description | Default |
|------|-------------|---------|
| `--assistant-model` | Model for the calendar assistant | _(inherits `--model`)_ |
| `--requestor-model` | Model for the meeting requestor | _(inherits `--model`)_ |
| `--expose-preferences` | Share scheduling preferences with assistant | `false` |

### Form Filling

An assistant fills out forms based on information gathered through conversation with an interviewer agent.

```bash
srbench benchmark form_filling \
    --data ./data/form-filling/tasks/ \
    --interviewer-model gpt-4.1 \
    --assistant-model gpt-4.1 \
    --judge-model gpt-4.1 \
    --limit 2
```

The following flags are specific to form filling.

| Flag | Description | Default |
|------|-------------|---------|
| `--assistant-model` | Model for the form-filling assistant | _(inherits `--model`)_ |
| `--interviewer-model` | Model for the interviewer | _(inherits `--model`)_ |
| `--single-field-mode` | Fill one field at a time | `false` |

### Marketplace

A buyer and seller agent negotiate the price of a product. Each has hidden reservation prices they should not reveal.

```bash
srbench benchmark marketplace \
    --data ./data/marketplace/small.yaml \
    --model gpt-4.1 \
    --max-steps-per-turn 3 \
    --limit 2
```

The following flags are specific to marketplace.

| Flag | Description | Default |
|------|-------------|---------|
| `--buyer-model` | Model for the buyer agent | _(inherits `--model`)_ |
| `--seller-model` | Model for the seller agent | _(inherits `--model`)_ |

## Common CLI Flags

These flags work across all three benchmarks:

| Flag | Description | Default |
|------|-------------|---------|
| `--data` | YAML files or directories with task data | _(required)_ |
| `--limit` | Maximum number of tasks to run | _(all)_ |
| `--batch-size` | Number of parallel tasks | `32` |
| `--model` | Default model for all agents | _(required)_ |
| `--judge-model` | Model for LLM-as-judge evaluation | _(inherits `--model`)_ |
| `--judge-votes` | Number of majority votes for judge | `3` |
| `--assistant-system-prompt` | System prompt preset | `none` |
| `--max-rounds` | Maximum conversation rounds | `20` |
| `--max-steps-per-turn` | Maximum tool calls per agent turn | `20` |
| `--resume` | Resume from checkpoint | `false` |
| `--output-dir` | Output directory | `outputs/` |
| `--logger` | Logging style: `verbose`, `progress`, `quiet` | `progress` |

## Running Experiment Sweeps

Experiment files define multiple benchmark runs to execute together. The runner pools tasks across all experiments for efficient execution.

```bash
# Run all experiments in a file
srbench experiment experiment_full.py

# Preview experiments without running
srbench experiment experiment_full.py --collect

# Filter by name pattern
srbench experiment experiment_full.py -k calendar

# Control parallelism
srbench experiment experiment_full.py --batch-size 100

# Override config fields across all experiments
srbench experiment experiment_full.py --set model=claude-sonnet-4

# Cross-product with multiple models using --and
srbench experiment experiment_full.py \
    --set model=gpt-4.1 \
    --and \
    --set model=claude-sonnet-4
```

See [New Experiments](/new-experiments) for how to write your own experiment files and use [override groups](/new-experiments#override-groups) for parameter sweeps from the command line.

## Output Format

Each benchmark run produces an output directory:

```
outputs/{benchmark}_{variant}_{model}_{timestamp}/
  results.json        # Full results: config, evaluation, per-task results
  checkpoint.json     # In-progress checkpoint (removed on completion)
```

Experiment sweeps additionally produce:

```
outputs/
  sweep_metadata.json   # Metadata about the sweep run
  {experiment_name}/
    results.json
  {experiment_name_2}/
    results.json
```

The `results.json` file contains the following fields.

- **config** contains the full run configuration.
- **timestamp** records the ISO8601 start time.
- **elapsed_seconds** records the total wall time.
- **evaluation** contains aggregate metrics including task completion rate, average leakage rate, average duty of care, and average due diligence.
- **results** contains per-task evaluation results.

## Dashboard

After running experiments, use the dashboard to visually compare results across benchmarks, models, and attack types.

```bash
srbench dashboard
```

This opens an interactive HTML dashboard in your browser. Load one or more `results.json` files from your experiment outputs to start exploring.

The dashboard provides four visualization modes.

- **Radar charts** plot all four metrics (task completion, leakage rate, duty of care, due diligence) on a single chart, making it easy to compare the overall profile of different experiments.
- **Bar charts** show each metric individually across experiments, which is useful for spotting which experiments perform best on a specific dimension.
- **Heatmaps** display metrics as a color-coded grid of experiments vs. metrics, making patterns across many experiments visible at a glance.
- **Distributions** show the spread of per-task scores within each experiment, revealing whether an aggregate average hides high variance.

The dashboard also includes benchmark-specific tabs (Calendar, Marketplace, Form Filling) that show domain-specific metrics when the loaded results include those benchmark types. A data table tab provides a sortable, filterable view of all raw results.

You can drag and reorder pivot chips at the top of the dashboard to group and slice the data by different dimensions such as model, variant, or benchmark.

## Resume and Checkpointing

Runs checkpoint progress automatically. If a run is interrupted:

```bash
# Resume from checkpoint (default: looks for checkpoint in output dir)
srbench benchmark calendar --data ... --model ... --resume

# Force re-run execution (keep evaluation)
srbench benchmark calendar --data ... --model ... --resume --restart-exec

# Force re-run evaluation (keep execution)
srbench benchmark calendar --data ... --model ... --resume --restart-eval
```
