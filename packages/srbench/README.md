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

## Bring your own assistant agent

The assistant side of each benchmark (the agent under evaluation) can be a class you provide. Implement `BaseAssistantAgent`, which requires only the `run(invoke_tool, tools)` coroutine. Your agent acts by passing `Tool` instances to `invoke_tool` and learns everything from tool results. The counterpart's opening move is waiting in the environment, so your first `Wait` returns it.

```python
# my_pkg/my_mod.py
from srbench.shared import BaseAssistantAgent
from srbench.benchmarks.calendar_scheduling.environment.actions import Wait


class MyAgent(BaseAssistantAgent):
    def __init__(self, *, assistant, allowed_contacts, max_actions):
        ...

    async def run(self, invoke_tool, tools):
        opening = await invoke_tool(Wait())
        ...
```

Point the benchmark at it with an import string.

```bash
srbench benchmark calendar --assistant-agent my_pkg.my_mod:MyAgent ...
srbench benchmark marketplace --buyer-agent my_pkg.my_mod:MyBuyer ...
```

The calendar factory is called with keyword arguments `assistant`, `allowed_contacts`, and `max_actions`. The marketplace factory is called with `instruction_message` and `max_actions`. Evaluation reads the environment's own records (emails, offers, action traces), so no transcript reporting is required.

## [Documentation](../../docs/vitepress/)
