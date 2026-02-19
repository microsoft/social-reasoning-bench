# WhimsyGen

Extract whimsical task strategies from arbitrary seed documents.

A **task** is any scenario where an agent pursues objectives under constraints—negotiating a deal, scheduling meetings, filling out forms, or navigating a conversation. From the agent's perspective, a task defines what it's trying to achieve and the rules it must follow.

The strategies are **whimsical** because they come from unexpected places. Rather than using obvious tactics, WhimsyGen extracts ideas from arbitrary Wikipedia articles—psychology, game theory, rhetoric, even coffee culture—and applies them creatively to your task. The result is unconventional, surprising approaches that stress-test how agents behave when faced with unusual adversarial tactics.

## Installation

```bash
uv sync --all-packages
```

## Quick Start

```python
import asyncio
from whimsygen import WhimsyGen

async def main():
    wg = WhimsyGen(
        model="openai/gpt-4.1",
        seeds="seeds/",
        task="task.txt",
    )

    # Get N strategies as a list
    strategies = await wg.sample(10)

    # Or stream strategies one at a time
    async for strategy in wg.isample(max_strategies=10):
        print(strategy.game_strategies)

asyncio.run(main())
```

## High-Throughput Sampling

WhimsyGen uses a producer/consumer pipeline to maximize throughput:

```
[SeedManager] -> seed_queue -> [StrategyManager] -> strategy_queue -> [consumer]
      |                              |                                    |
 (crawl/load)                   (LLM calls)                           (yield)
```

**How it works:**
- **Seed producer** fetches seeds from cache or Wikipedia and buffers them ahead
- **Strategy producer** extracts strategies via LLM and buffers them ahead
- **Consumer** yields strategies while producers continue working in the background

This means while you're processing strategy #1, the system is already fetching seeds and extracting strategies #2, #3, etc. The `prefetch_seeds` and `prefetch_strategies` parameters control buffer sizes.

## Python API

### Simple Usage

```python
from whimsygen import WhimsyGen

# Pass seeds dir and task file (or task text) to constructor
wg = WhimsyGen(
    model="openai/gpt-4.1",
    seeds="seeds/",
    task="task.txt",  # or pass task text directly
)

# sample(n) returns a list of N strategies
strategies = await wg.sample(10)

# isample() returns an async iterator for streaming
async for strategy in wg.isample(
    topics=["Negotiation", "Game theory"],  # Wikipedia topics for crawling
    # Controls (all optional, None = unlimited)
    max_seeds=100,
    max_chunks_per_seed=5,
    max_strategies_per_chunk=3,
    max_strategies_per_seed=10,
    max_strategies=50,
    # Prefetching (for better throughput)
    prefetch_seeds=2,       # Fetch seeds ahead while processing
    prefetch_strategies=3,  # Extract strategies ahead while yielding
):
    print(strategy.game_strategies)

# Save/load strategies (strategies are cached after sampling)
wg.strategies.save("strategies.yaml")
wg.strategies.load("strategies.yaml")
```

### Step-by-Step Usage

For more control, use the managers directly:

```python
wg = WhimsyGen(model="openai/gpt-4.1")

# 1. Set seeds directory
wg.seeds.dir = Path("seeds/")

# 2. Define a task
wg.task.load("task.txt")  # from file
wg.task.set("...")        # from string

# 3. Sample strategies (loads cached seeds, crawls for more if needed)
strategies = await wg.sample(10)
```

### Seeds Manager

```python
wg.seeds.dir = Path("seeds/")

# Unified async iterator: loads cached seeds first, then crawls for more
# Caller controls how many to consume by stopping iteration
i = 0
async for seed in wg.seeds.sample():
    print(seed.title)
    i += 1
    if i >= 10:
        break

# Lower-level methods
wg.seeds.load()   # sync iterator - yield cached seeds (disk I/O is fast)
wg.seeds.crawl()  # async iterator - yield seeds as crawled from Wikipedia
wg.seeds.list()   # list filenames (returns list)
```

### Task Manager

```python
wg.task.load("task.txt")   # from file
wg.task.set("...")         # from string
wg.task.current            # get current task
wg.task.save("task.txt")   # save to file
```

### Strategies Manager

```python
# Strategies are cached as they're sampled
wg.strategies.cache        # get cached strategies
wg.strategies.save("strategies.yaml")
wg.strategies.load("strategies.yaml")
wg.strategies.clear()      # clear cache
```

## Models

Uses `sage-llm`. Supported formats:

- `openai/gpt-4.1`
- `gemini/gemini-3-pro`
- `anthropic/claude-sonnet-4`
- `trapi/msraif/shared/gpt-4.1` (internal)
