# SAGE-Benchmark

SAGE-Benchmark is a set of tasks for evaluating the social reasoning capabilities of LLM agents in multi-agent settings. We include different benchmarks for tasks that require social intelligence:

| Benchmark                                                                                   | Description                                                                             |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [Calendar Scheduling](packages/sage-benchmark/sage_benchmark/calendar_scheduling/README.md) | Test whether agents can schedule meetings while protecting private calendar information |
| [Form Filling](packages/sage-benchmark/sage_benchmark/form_filling/README.md)               | Evaluate agents filling forms with sensitive user data (one-shot or interactive modes)  |
| Marketplace -- coming soon!                                                                 | Evaluate how well agents negotitate in marketplace settings                             |

## Quick Start

```bash
# Install dependencies
uv sync --all-packages

# Run calendar scheduling benchmark
sagebench calendar \
    --data ./data/calendar-scheduling/generated/generated-tasks.yaml \
    --model trapi/gpt-4.1 \
    --assistant-system-prompt default \
    --expose-preferences false \
    --explicit-cot false \
    --limit 2

# Run form filling benchmark
sagebench forms \
    --data ./data/form-filling/tasks/ \
    --assistant-model trapi/gpt-4.1 \
    --judge-model trapi/gpt-4.1 \
    --limit 2

# Run form filling benchmark (interactive mode)
sagebench forms \
    --data ./data/form-filling/tasks/ \
    --execution-mode interactive \
    --interviewer-model trapi/gpt-4.1 \
    --assistant-model trapi/gpt-4.1 \
    --judge-model trapi/gpt-4.1 \
    --limit 2
```

## Documentation

- [Sage-Benchmark](packages/sage-benchmark/README.md) — Full setup and usage guide for each benchmark
- [Sage-LLM](packages/sage-llm/README.md) — Model client library
- [DEV.md](docs/DEV.md) — Development setup
- [SYNC.md](docs/SYNC.md) — Syncing results to Azure Blob Storage
