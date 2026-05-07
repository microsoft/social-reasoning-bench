# Running benchmarks

`srbench benchmark` runs a single benchmark with explicit flags. It's the right entry point when you want to evaluate one model on one dataset.

For multi-model or multi-condition sweeps, use [`srbench experiment`](/experiments) instead.

## Basic usage

```bash
srbench benchmark <name> --data <path> --model <model> [options]
```

Available benchmarks:

| Name           | Scenario                                                                |
|----------------|-------------------------------------------------------------------------|
| `calendar`     | Assistant + requestor schedule a meeting while protecting calendar privacy |
| `marketplace`  | Buyer + seller negotiate price while each hides a reservation price     |

## Calendar scheduling

```bash
srbench benchmark calendar \
    --data data/calendar-scheduling/small.yaml \
    --model gpt-4.1 \
    --limit 2
```

| Flag                          | Description                                       |
|-------------------------------|---------------------------------------------------|
| `--assistant-model`           | Override model for the calendar assistant         |
| `--requestor-model`           | Override model for the meeting requestor          |
| `--assistant-reasoning-effort` | Reasoning effort for the assistant               |
| `--requestor-reasoning-effort` | Reasoning effort for the requestor               |
| `--assistant-explicit-cot`    | `true`/`false` — chain-of-thought for the assistant |
| `--requestor-explicit-cot`    | `true`/`false` — chain-of-thought for the requestor |
| `--expose-preferences`        | `true`/`false` — share scheduling preferences (default `true`) |

## Marketplace

```bash
srbench benchmark marketplace \
    --data data/marketplace/small.yaml \
    --model gpt-4.1 \
    --limit 2
```

| Flag                       | Description                                |
|----------------------------|--------------------------------------------|
| `--buyer-model`            | Override model for the buyer               |
| `--seller-model`           | Override model for the seller              |
| `--buyer-reasoning-effort` | Reasoning effort for the buyer             |
| `--seller-reasoning-effort` | Reasoning effort for the seller           |

## Common flags

These flags work on every benchmark.

### Data and limits

| Flag             | Description                                | Default |
|------------------|--------------------------------------------|---------|
| `--data`         | YAML file or directory of task data        | _(required)_ |
| `--limit`        | Maximum number of tasks to run             | _(all)_ |
| `--max-rounds`   | Maximum conversation rounds per task       | `20`    |
| `--max-steps-per-turn` | Maximum tool calls per agent turn    | varies  |

### Model

| Flag             | Description                                |
|------------------|--------------------------------------------|
| `--model`        | Default model for all agents (required unless per-agent overrides set) |
| `--reasoning-effort` | Default reasoning effort for all agents |
| `--explicit-cot`     | `true`/`false` — explicit chain-of-thought |
| `--base-url`     | Override base URL (for self-hosted endpoints) |
| `--api-version`  | Override API version                       |

### Judge

The judge is the LLM-as-judge that evaluates each task on the four dimensions.

| Flag                        | Description                                |
|-----------------------------|--------------------------------------------|
| `--judge-model`             | Model for evaluation (defaults to `--model`) |
| `--judge-votes`             | Majority-vote count                        |
| `--judge-reasoning-effort`  | Reasoning effort for the judge             |

### System prompt

The `--system-prompt` flag controls what social-reasoning guidance the assistant agent receives. Use it to baseline a model with no guidance, or to test specific defenses.

| Preset              | What it adds                                                          |
|---------------------|------------------------------------------------------------------------|
| `none`              | No guidance (default)                                                  |
| `privacy`           | Protect private information; share only the minimum necessary          |
| `dd_info_gathering` | Verify information and consult sources before acting                   |
| `dd_advocacy`       | Push back and persist on the user's behalf                             |
| `oo`                | Maximize the user's outcome                                            |

### Adversarial injection

```bash
srbench benchmark calendar \
    --data data/calendar-scheduling/small.yaml \
    --model gpt-4.1 \
    --attack-types privacy due_diligence
```

`--attack-types` injects hand-crafted adversarial prompts at runtime. Available types: `privacy`, `outcome_optimality`, `due_diligence`. Multiple types can be combined.

For pre-generated whimsical attacks, point `--data` at the whimsical dataset instead:

```bash
srbench benchmark calendar \
    --data data/calendar-scheduling/small-whimsical-privacy.yaml \
    --model gpt-4.1
```

### Concurrency

| Flag                  | Description                                                |
|-----------------------|------------------------------------------------------------|
| `--batch-size`        | Number of tasks executed in parallel                       |
| `--task-concurrency`  | Max concurrent LLM calls per task                          |
| `--llm-concurrency`   | Max total concurrent LLM calls per provider                |

### Output and logging

| Flag             | Description                                       | Default |
|------------------|---------------------------------------------------|---------|
| `--output-dir`   | Output directory                                  | `outputs/` |
| `--logger`       | `verbose`, `progress`, or `quiet`                 | `progress` |
| `--log-level`    | `debug`, `info`, `warning`, `error`               | `warning` |

### Resume and re-run

Runs checkpoint progress automatically; if interrupted, re-running with the same flags resumes from the checkpoint.

| Flag             | Description                                                   |
|------------------|---------------------------------------------------------------|
| `--resume`       | Explicitly resume from a checkpoint path                       |
| `--restart-exec` | Discard execution checkpoint and re-run executions             |
| `--restart-eval` | Keep executions, re-run evaluation only                        |
| `--finalize`     | Convert an existing `checkpoint.json` to `results.json` without running anything |

## Output

Each run produces a directory under `--output-dir`:

```
outputs/{benchmark}_{variant}_{model}_{timestamp}/
  results.json        # Final results — config, evaluation, per-task results
  checkpoint.json     # In-progress checkpoint (removed on completion)
```

`results.json` contains:

| Field             | Description                                                          |
|-------------------|----------------------------------------------------------------------|
| `config`          | Full run configuration                                                |
| `timestamp`       | ISO 8601 start time                                                   |
| `elapsed_seconds` | Total wall time                                                       |
| `evaluation`      | Aggregate metrics: task completion, leakage rate, duty of care, due diligence |
| `results`         | Per-task evaluation results                                           |

## Evaluation dimensions

Every task is evaluated on four dimensions:

| Dimension       | Question it answers                                       |
|-----------------|-----------------------------------------------------------|
| Task completion | Did the agent achieve the primary objective?              |
| Privacy preservation         | Did the agent protect confidential information?           |
| Outcome optimality   | Did the agent maximize the user's preferences?            |
| Due diligence   | Did the agent verify information before acting?           |

Load `results.json` files into the [Dashboard](/dashboard) to compare runs across models and conditions.
