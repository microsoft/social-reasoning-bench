# sage-llm

LLM client library with direct provider implementations for OpenAI, Anthropic, Gemini, Azure, TRAPI, and PhyAGI. Provides reasoning model handling, structured outputs, multi-turn thinking preservation, and tracing.

## Install

```bash
uv sync --all-packages
```

## Quick Start

```python
import asyncio
from sage_llm import SageModelClient
from sage_llm.types import SageMessage

client = SageModelClient()

async def main():
    msg = await client.acomplete(
        model="gpt-4.1",
        messages=[SageMessage(role="user", content="Hello")],
    )
    print(msg.content)

asyncio.run(main())
```

## Concurrency Control

sage-llm provides three-level concurrency control, all scoped per-provider:

| Level | Controls | Default |
|-------|----------|---------|
| **BATCH_SIZE** | Max parallel benchmark tasks | Set by `TaskPoolExecutor` |
| **TASK_SIZE** | Max concurrent LLM calls per task per provider | Unlimited |
| **LLM_SIZE** | Max total concurrent LLM calls per provider | Unlimited |

### Configuration

**Environment variables** (read at import time):

```bash
# Default limits (apply to all providers)
export SAGE_LLM_SIZE=20          # global per-provider limit
export SAGE_LLM_TASK_SIZE=5      # per-task per-provider limit

# Per-provider overrides
export SAGE_LLM_SIZE_OPENAI=30
export SAGE_LLM_SIZE_ANTHROPIC=10
export SAGE_LLM_TASK_SIZE_TRAPI=3
```

**Programmatic** (overrides env vars):

```python
from sage_llm import concurrency

concurrency.configure(
    llm_size=20,       # default per-provider global limit
    task_size=5,        # default per-task per-provider limit
    providers={
        "anthropic": {"llm_size": 10},
        "trapi": {"task_size": 3},
    },
)
```

### Task Scoping

Wrap benchmark tasks in `task_scope()` so that LLM calls within a task
share per-task semaphores:

```python
from sage_llm.concurrency import task_scope

async with task_scope(task_size=5):
    # All LLM calls in this scope share a per-provider
    # semaphore with capacity 5
    await client.acomplete(model="openai/gpt-4.1", ...)
```

Provider keys: `openai`, `anthropic`, `google`, `azure`, `trapi`, `phyagi`.

## [Documentation](../../docs/vitepress/architecture.md)
