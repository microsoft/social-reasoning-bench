# Calendar Scheduling Benchmark

Test whether LLM agents can schedule meetings while protecting private calendar information.

## What It Measures

Two agents negotiate a meeting via email:
- **Requestor** — wants to schedule a meeting at a specific time
- **Assistant** — manages a calendar with existing events

The benchmark evaluates:
- `appropriate_scheduling` — Did the assistant agent appropriate schedule or not schedule the meeting?
- `privacy_preservation_rate` — Percentage of sensitive event details kept private.

## Quick Start

```bash
cd sage-benchmark

# Set API key
export OPENAI_API_KEY="your-key"

# Run 1 task to verify setup
uv run -m sage_benchmark.calendar_scheduling \
    ./data/calendar-scheduling/calendar-tasks.yaml \
    --limit 1 \
    --model gpt-4.1
```

## Full Benchmark

```bash
uv run -m sage_benchmark.calendar_scheduling \
    ./data/calendar-scheduling/calendar-tasks.yaml \
    --max-rounds 10 \
    --assistant-model gpt-4.1 \
    --requestor-model gpt-4.1 \
    --judge-model gpt-4.1
```

## Output

Results are saved to:
```
outputs/calendar_scheduling/calendar_scheduling_MODEL_YYYYMMDD_HHMMSS.json
```

## Visualization

Open these HTML files in a browser to explore tasks and results. Load the result JSON files as needed.

| File | Purpose | Input |
|------|---------|-------|
| `html/calendar_data_viewer.html` | Inspect task dataset (calendars, events, labels) | `calendar-tasks.yaml` |
| `html/calendar_eval_viewer.html` | Analyze a single run (calendars, messages, trajectories) | Output `.json` file |
| `html/calendar_eval_comparison.html` | Compare multiple models (charts, filters) | Multiple `.json` files |

