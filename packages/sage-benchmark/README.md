# sage-benchmark

Benchmark runner for evaluating LLM agents on calendar scheduling, form filling, and marketplace negotiation. Provides parallel execution, checkpointing, resume, and LLM-as-judge evaluation across four dimensions: task completion, privacy, duty of care, and due diligence.

## Install

```bash
uv sync --all-packages
```

## Quick Start

```bash
# Run a single benchmark
sagebench benchmark calendar \
    --data ./data/calendar-scheduling/small.yaml \
    --model gpt-4.1 \
    --limit 2

# Run an experiment sweep
sagebench experiment experiment_smoke.py
```

## [Documentation](../../docs/vitepress/)
