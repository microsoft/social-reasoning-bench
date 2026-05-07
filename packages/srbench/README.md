# srbench

Benchmark runner for evaluating LLM agents on calendar scheduling and marketplace negotiation. Provides parallel execution, checkpointing, resume, and LLM-as-judge evaluation across four dimensions: task completion, privacy, duty of care, and due diligence.

## Install

```bash
uv sync --all-packages
```

## Quick Start

```bash
# Run a single benchmark
srbench benchmark calendar \
    --data ./data/calendar-scheduling/small.yaml \
    --model gpt-4.1 \
    --limit 2

# Run an experiment sweep
srbench experiment experiment_smoke.py
```

## [Documentation](../../docs/vitepress/)
