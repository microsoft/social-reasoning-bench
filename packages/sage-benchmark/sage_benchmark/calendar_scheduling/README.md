# Calendar Scheduling Benchmark

Test whether LLM agents can schedule meetings while protecting private calendar information.

## Overview

Two agents negotiate a meeting:

- **Assistant** — manages a calendar with existing events (some private)
- **Requestor** — wants to schedule a meeting, may attempt to extract private info

The benchmark evaluates:

| Metric | Description |
|--------|-------------|
| Task Completion | Whether appropriate meeting was scheduled |
| Privacy Leakage | % of messages revealing secret event info |
| Duty of Care | `scheduled_pref_score / best_available_pref_score` |
| Backfire Rate | % where privacy prompt performs worse than default |

## Experiment Matrix

| Dimension | Values |
|-----------|--------|
| Task Type | Normal, Malicious Extraction, Malicious Strategies |
| Assistant Prompt | `default`, `privacy-ci`, `privacy-strong`, `privacy-simple` |
| Model | GPT-5.1, GPT-4.1, GPT-4o, Claude Sonnet 4, Gemini 2.5 Flash, Qwen 7B |
| Reasoning Effort | None, Low, Medium, High |
| Preference Visibility | Hidden, Exposed |
| Calendar Fullness (free slots) | 0, 1, 3, 5, 7, 9, 11 |

## Quick Start

```bash
# Run 1 task to verify setup
sagebench calendar \
    --data ./data/calendar-scheduling/generated/generated-tasks.yaml \
    --model gpt-4.1 \
    --assistant-system-prompt default \
    --expose-preferences false \
    --explicit-cot false \
    --limit 1
```

## Run Benchmark

```bash
sagebench calendar \
    --data ./data/calendar-scheduling/generated/generated-tasks.yaml \
    --model gpt-4.1 \
    --assistant-system-prompt default \
    --expose-preferences false \
    --explicit-cot false
```

Results are saved to `outputs/calendar_scheduling/`.

### With Different Models Per Agent

```bash
sagebench calendar \
    --data ./data/calendar-scheduling/generated/generated-tasks.yaml \
    --model gpt-4.1 \
    --assistant-model claude-sonnet-4 \
    --requestor-model gpt-4.1 \
    --judge-model gpt-4.1 \
    --assistant-system-prompt default \
    --expose-preferences false \
    --explicit-cot false
```

### With Reasoning Models

```bash
sagebench calendar \
    --data ./data/calendar-scheduling/generated/generated-tasks.yaml \
    --model o3 \
    --reasoning-effort medium \
    --assistant-system-prompt default \
    --expose-preferences false \
    --explicit-cot false
```

---

## Analyze

```bash
# Generate Pareto plot (scheduling success vs privacy)
uv run -m sage_benchmark.calendar_scheduling.analysis.plot_pareto outputs/calendar_scheduling/
```

---

## Visualize

Open in browser to explore tasks and results:

| File | Purpose | Input |
|------|---------|-------|
| `html/calendar_data_viewer.html` | Inspect task dataset | Task YAML file |
| `html/calendar_eval_viewer.html` | Analyze a single run | Output JSON file |
| `html/calendar_eval_comparison.html` | Compare multiple models | Multiple JSON files |

---

## Data Generation

See [sage-data-gen](../../../sage-data-gen/README.md).

---

## CLI Reference

### Required Arguments

| Argument | Description |
|----------|-------------|
| `--data` | YAML files or directories containing task definitions |
| `--model` | Default model for all agents |
| `--assistant-system-prompt` | System prompt preset: `none`, `default`, `privacy-focused`, etc. |
| `--expose-preferences {true,false}` | Include scheduling preferences in assistant prompt |
| `--explicit-cot {true,false}` | Enable explicit chain-of-thought prompting |

### Run Parameters

| Argument | Default | Description |
|----------|---------|-------------|
| `--max-rounds` | 20 | Maximum conversation rounds per task |
| `--max-steps-per-turn` | 20 | Maximum tool calls per agent turn |
| `--batch-size` | 32 | Tasks/evals to run in parallel |
| `--limit` | None | Limit number of tasks to load |

### Per-Agent Model Overrides

| Argument | Default | Description |
|----------|---------|-------------|
| `--assistant-model` | `--model` | Model for assistant agent |
| `--requestor-model` | `--model` | Model for requestor agent |
| `--judge-model` | `--model` | Model for LLM-as-judge evaluation |
| `--base-url` | None | Default base URL for OpenAI-compatible API |
| `--assistant-base-url` | `--base-url` | Base URL for assistant |
| `--requestor-base-url` | `--base-url` | Base URL for requestor |
| `--judge-base-url` | `--base-url` | Base URL for judge |
| `--api-version` | None | Default API version |
| `--assistant-api-version` | `--api-version` | API version for assistant |
| `--requestor-api-version` | `--api-version` | API version for requestor |
| `--judge-api-version` | `--api-version` | API version for judge |

### Reasoning Effort

| Argument | Default | Description |
|----------|---------|-------------|
| `--reasoning-effort`, `-r` | None | Default reasoning effort: `none`, `low`, `medium`, `high`, `xhigh` |
| `--assistant-reasoning-effort` | `--reasoning-effort` | Reasoning effort for assistant |
| `--requestor-reasoning-effort` | `--reasoning-effort` | Reasoning effort for requestor |
| `--judge-reasoning-effort` | `--reasoning-effort` | Reasoning effort for judge |

### Per-Agent CoT Overrides

| Argument | Default | Description |
|----------|---------|-------------|
| `--assistant-explicit-cot {true,false}` | `--explicit-cot` | CoT override for assistant |
| `--requestor-explicit-cot {true,false}` | `--explicit-cot` | CoT override for requestor |

### Prompts and Context

| Argument | Default | Description |
|----------|---------|-------------|
| `--assistant-system-prompt-file` | None | Path to custom system prompt file |

### Output and Logging

| Argument | Default | Description |
|----------|---------|-------------|
| `--output-dir` | `outputs/calendar_scheduling` | Base directory for outputs |
| `--log-level` | `info` | Logging level: `debug`, `info`, `warning`, `error` |

### Resume

| Argument | Default | Description |
|----------|---------|-------------|
| `--resume` | None | Resume from previous run directory or checkpoint |
| `--force-resume` | False | Allow resume even if source files changed |
