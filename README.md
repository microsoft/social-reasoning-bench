# SAGE

SAGE-Benchmark is a set of tasks for evaluating the social reasoning capabilities of LLM agents in multi-agent settings. We include different benchmarks for different tasks that require social intelligence:

| Benchmark                                                                          | Description                                                                             |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [Calendar Scheduling](sage-benchmark/sage_benchmark/calendar_scheduling/README.md) | Test whether agents can schedule meetings while protecting private calendar information |
| [Form Filling](sage-benchmark/sage_benchmark/form_filling/)                        | Evaluate agents filling forms with sensitive user data (one-shot or interactive modes)  |
| Marketplace -- coming soon!                                                        | Evaluate how well agents negotitate in marketplace settings                             |

## Quick Start

```bash
# Install dependencies
uv sync --all-packages

# Run calendar scheduling benchmark
cd sage-benchmark
uv run -m sage_benchmark.calendar_scheduling \
    ./data/calendar-scheduling/generated/generated-tasks.yaml \
    --model trapi/gpt-4.1 \
    --assistant-system-prompt default \
    --expose-preferences false \
    --explicit-cot false \
    --limit 2

# Run form filling benchmark
uv run -m sage_benchmark.form_filling \
    --data ./data/form-filling/tasks/ \
    --assistant-model trapi/gpt-4.1 \
    --judge-model trapi/gpt-4.1 \
    --limit 2

# Run form filling benchmark (interactive mode)
uv run -m sage_benchmark.form_filling \
    --data ./data/form-filling/tasks/ \
    --execution-mode interactive \
    --interviewer-model trapi/gpt-4.1 \
    --assistant-model trapi/gpt-4.1 \
    --judge-model trapi/gpt-4.1 \
    --limit 2
```

## sage-llm

LiteLLM-based model client library with TRAPI support, reasoning model handling, and tracing. See [sage-llm/README.md](sage-llm/README.md).

```python
from sage_llm import ModelClient

client = ModelClient()
response = client.chat.completions.create(
    model="trapi/msraif/shared/gpt-4.1",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Documentation

- [Sage-Benchmark](sage-benchmark/README.md) — Full setup and usage guide
- [Sage-LLM](sage-llm/README.md) — Model client library
- [Calendar Scheduling](sage-benchmark/sage_benchmark/calendar_scheduling/README.md) — Detailed calendar benchmark docs
- [Data Format](sage-benchmark/data/Data_Format.md) — Task and artifact data schemas
- [DEV.md](DEV.md) — Development setup
- [SYNC.md](SYNC.md) — Syncing results to Azure Blob Storage
