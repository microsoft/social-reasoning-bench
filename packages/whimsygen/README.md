# WhimsyGen

Extracts whimsical adversarial strategies from Wikipedia articles. WhimsyGen crawls arbitrary seed documents and uses an LLM to identify concepts that can be applied as creative, unconventional attack tactics for stress-testing agent behavior.

## Install

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
    strategies = await wg.sample(10)
    for s in strategies:
        print(s.game_strategies)

asyncio.run(main())
```

## [Documentation](../../docs/vitepress/whimsygen.md)
