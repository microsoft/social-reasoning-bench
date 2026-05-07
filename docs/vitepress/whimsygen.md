# WhimsyGen

WhimsyGen extracts whimsical adversarial strategies from arbitrary seed documents, primarily Wikipedia articles.

A **task** is any scenario where an agent pursues objectives under constraints, such as negotiating a deal, scheduling meetings, filling out forms, or navigating a conversation. The strategies are **whimsical** because they come from unexpected places. Rather than using obvious tactics, WhimsyGen extracts ideas from Wikipedia articles on psychology, game theory, rhetoric, and even coffee culture, then applies them creatively to your task. The result is unconventional, surprising approaches that stress-test how agents behave when faced with unusual adversarial tactics.

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

- The **seed producer** fetches seeds from cache or Wikipedia and buffers them ahead.
- The **strategy producer** extracts strategies via LLM and buffers them ahead.
- The **consumer** yields strategies while producers continue working in the background.

While you're processing strategy #1, the system is already fetching seeds and extracting strategies #2, #3, etc. The `prefetch_seeds` and `prefetch_strategies` parameters control buffer sizes.

## Python API

### Simple Usage

```python
from whimsygen import WhimsyGen

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
    max_seeds=100,
    max_chunks_per_seed=5,
    max_strategies_per_chunk=3,
    max_strategies_per_seed=10,
    max_strategies=50,
    prefetch_seeds=2,
    prefetch_strategies=3,
):
    print(strategy.game_strategies)

# Save/load strategies
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
wg.task.set("...")         # from string

# 3. Sample strategies
strategies = await wg.sample(10)
```

### Seeds Manager

```python
wg.seeds.dir = Path("seeds/")

# Unified async iterator: loads cached seeds first, then crawls for more
async for seed in wg.seeds.sample():
    print(seed.title)

# Lower-level methods
wg.seeds.load()   # sync iterator — yield cached seeds
wg.seeds.crawl()  # async iterator — yield seeds from Wikipedia
wg.seeds.list()   # list cached filenames
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
wg.strategies.cache        # get cached strategies
wg.strategies.save("strategies.yaml")
wg.strategies.load("strategies.yaml")
wg.strategies.clear()      # clear cache
```

## How It Works

### Seed Loading

Seeds are Wikipedia article snapshots stored as YAML files. The `SeedManager` uses a hybrid approach:

1. **Cache-first** loads seeds from the local `seeds/` directory using fast synchronous disk I/O.
2. **Crawl-as-needed** crawls Wikipedia starting from configured topics using async network I/O if more seeds are required.

### Strategy Extraction

The `StrategyExtractor` processes each seed through an LLM:

1. Chunks the Wikipedia text (default 5000 chars with 500 char overlap)
2. For each chunk, sends it to the LLM along with the task description
3. The LLM identifies concepts in the article that could be applied as adversarial tactics
4. Parses the YAML response to extract structured strategies

Each strategy contains the following fields.
- **grounding_texts** contains relevant excerpts from the Wikipedia article.
- **game_strategies** describes how to apply the concept as an adversarial tactic.
- **source** provides a reference to the Wikipedia article.

### Pipeline

The `SamplingPipeline` orchestrates everything with backpressure-aware queues:

```
seed_queue (bounded) -> strategy_queue (bounded) -> consumer
```

This hides latency because while the consumer processes results, producers continue fetching and extracting in the background.

## Models

WhimsyGen uses `srbench-llm` for model access. The following formats are supported.

- `openai/gpt-4.1`
- `gemini/gemini-2.5-pro`
- `anthropic/claude-sonnet-4`
- `azure_pool/gpt-4.1`
