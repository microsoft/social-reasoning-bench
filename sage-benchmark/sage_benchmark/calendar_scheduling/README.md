# Calendar Scheduling Benchmark

Test whether LLM agents can schedule meetings while protecting private calendar information.

## What It Measures

Two agents negotiate a meeting:

- **Requestor** — wants to schedule a meeting at a specific time
- **Assistant** — manages a calendar with existing events

The benchmark evaluates:

- `appropriate_scheduling` — Did the assistant agent appropriate schedule or not schedule the meeting?
- `privacy_preservation_rate` — Percentage of sensitive event details kept private.
- `duty_of_care` — (Optional) How well did the assistant optimize for user scheduling preferences?

## Quick Start

```bash
cd sage-benchmark

# Set API key
export OPENAI_API_KEY="your-key"

# Run 1 task to verify setup
uv run -m sage_benchmark.calendar_scheduling \
    ./data/calendar-scheduling/generated/generated-tasks.yaml \
    --limit 1 \
    --model trapi/msraif/shared/gpt-4.1 \
    --assistant-system-prompt default \
    --expose-preferences false \
    --explicit-cot false \
    --max-rounds 10
```

## Run Full Benchmark

```bash
uv run -m sage_benchmark.calendar_scheduling \
    ./data/calendar-scheduling/generated/generated-tasks.yaml \
    --model trapi/msraif/shared/gpt-4.1 \
    --assistant-system-prompt default \
    --expose-preferences false \
    --explicit-cot false \
    --max-rounds 10
    # --limit 10 \
    # --assistant-model trapi/msraif/shared/other-model \
    # --requestor-model trapi/msraif/shared/other-model \
    # --judge-model trapi/msraif/shared/other-model \
```

Results are saved to: `outputs/calendar_scheduling/*.json`

**Full CLI Arguments:**

| Argument                                | Default                         | Description                                                               |
| --------------------------------------- | ------------------------------- | ------------------------------------------------------------------------- |
| **Required**                            |                                 |                                                                           |
| `paths`                                 | (required)                      | YAML files or directories containing task definitions                     |
| `--model`                               | (required)                      | Default model for all agents                                              |
| `--assistant-system-prompt`             | (required)                      | System prompt preset (none/default/privacy-focused/...)                   |
| `--expose-preferences {true,false}`     | (required)                      | Include or exclude scheduling preferences in assistant agent prompt       |
| `--explicit-cot {true,false}`           | (required)                      | Enable or disable explicit chain-of-thought prompting for all agents      |
| **Run parameters**                      |                                 |                                                                           |
| `--max-rounds`                          | 20                              | Maximum conversation rounds per task                                      |
| `--max-steps-per-turn`                  | 20                              | Maximum tool calls per agent turn                                         |
| `--batch-size`                          | 32                              | Number of tasks/evals to run in parallel                                  |
| `--limit`                               | None                            | Limit the number of tasks to load (loads all by default)                  |
| **Per-agent model overrides**           |                                 |                                                                           |
| `--base-url`                            | None                            | Default base URL for OpenAI-compatible API                                |
| `--api-version`                         | None                            | Default API version for all agents                                        |
| `--assistant-model`                     | (inherits `--model`)            | Model for assistant agent                                                 |
| `--assistant-base-url`                  | (inherits `--base-url`)         | Base URL for assistant agent                                              |
| `--assistant-api-version`               | (inherits `--api-version`)      | API version for assistant agent                                           |
| `--requestor-model`                     | (inherits `--model`)            | Model for requestor agent                                                 |
| `--requestor-base-url`                  | (inherits `--base-url`)         | Base URL for requestor agent                                              |
| `--requestor-api-version`               | (inherits `--api-version`)      | API version for requestor agent                                           |
| `--judge-model`                         | (inherits `--model`)            | Model for LLM-as-judge evaluation                                         |
| `--judge-base-url`                      | (inherits `--base-url`)         | Base URL for judge                                                        |
| `--judge-api-version`                   | (inherits `--api-version`)      | API version for judge                                                     |
| **Reasoning effort**                    |                                 |                                                                           |
| `--reasoning-effort`, `-r`              | None                            | Default reasoning effort for all agents (none/low/medium/high/xhigh)      |
| `--assistant-reasoning-effort`          | (inherits `--reasoning-effort`) | Reasoning effort for assistant agent                                      |
| `--requestor-reasoning-effort`          | (inherits `--reasoning-effort`) | Reasoning effort for requestor agent                                      |
| `--judge-reasoning-effort`              | (inherits `--reasoning-effort`) | Reasoning effort for judge                                                |
| **Per-agent CoT overrides**             |                                 |                                                                           |
| `--assistant-explicit-cot {true,false}` | (inherits `--explicit-cot`)     | Explicit CoT override for assistant agent                                 |
| `--requestor-explicit-cot {true,false}` | (inherits `--explicit-cot`)     | Explicit CoT override for requestor agent                                 |
| **Prompts and context**                 |                                 |                                                                           |
| `--assistant-system-prompt-file`        | None                            | Path to custom system prompt file (overrides `--assistant-system-prompt`) |
| `--artifacts`                           | None                            | Path to artifacts JSON file to inject into assistant context              |
| **Output and logging**                  |                                 |                                                                           |
| `--output-dir`                          | `outputs/calendar_scheduling`   | Base directory for run outputs                                            |
| `--log-level`                           | info                            | Logging level (debug/info/warning/error)                                  |
| **Resume**                              |                                 |                                                                           |
| `--resume`                              | None                            | Resume from a previous run directory or checkpoint path                   |
| `--force-resume`                        | False                           | Allow resume even if source files have changed                            |

## Visualization

Open these HTML files in a browser to explore tasks and results. Load the result JSON files as needed.

| File                                 | Purpose                                                  | Input                  |
| ------------------------------------ | -------------------------------------------------------- | ---------------------- |
| `html/calendar_data_viewer.html`     | Inspect task dataset (calendars, events, labels)         | `calendar-tasks.yaml`  |
| `html/calendar_eval_viewer.html`     | Analyze a single run (calendars, messages, trajectories) | Output `.json` file    |
| `html/calendar_eval_comparison.html` | Compare multiple models (charts, filters)                | Multiple `.json` files |
