"""Internal sampling pipeline for WhimsyGen."""

import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass

from ..core.models import Seed, Strategy
from ..seeds.manager import SeedManager
from ..strategies.manager import StrategyManager

DEFAULT_PREFETCH_SEEDS = 100
DEFAULT_PREFETCH_STRATEGIES = 100


@dataclass
class SamplingConfig:
    """Configuration for a sampling pipeline."""

    task: str
    topics: list[str] | None
    chunk_size: int
    max_seeds: int | None
    max_chunks_per_seed: int | None
    max_strategies_per_chunk: int | None
    max_strategies_per_seed: int | None
    max_strategies: int | None
    prefetch_seeds: int
    prefetch_strategies: int


class SamplingPipeline:
    """Producer/consumer pipeline for strategy sampling with prefetching.

    This class implements a two-stage async pipeline that overlaps I/O operations
    to maximize throughput:

        [SeedManager] -> seed_queue -> [StrategyManager] -> strategy_queue -> [consumer]
              |                              |                                    |
         (crawl/load)                   (LLM calls)                           (yield)

    Why this approach:
        1. **Latency hiding**: While the consumer processes a strategy, the producers
           can fetch the next seeds and extract the next strategies in parallel.
        2. **Backpressure**: Bounded queues prevent unbounded memory growth. If the
           consumer is slow, producers will block on queue.put() rather than
           accumulating unlimited items.
        3. **Clean cancellation**: The stop_event allows graceful shutdown when limits
           are reached, and the run() method ensures proper cleanup.

    Data flow:
        1. produce_seeds() fetches seeds (from cache or Wikipedia) and puts them
           in seed_queue until max_seeds is reached or stop is signaled.
        2. produce_strategies() pulls seeds from seed_queue, calls the LLM to extract
           strategies, and puts them in strategy_queue until limits are reached.
        3. run() launches producers as tasks and yields strategies from strategy_queue.

    Synchronization:
        - stop_event: Set when any limit is reached; all producers check this flag.
        - None sentinel: Signals end-of-stream through each queue.
        - Queue maxsize: Provides backpressure and bounds memory usage.
    """

    def __init__(
        self,
        config: SamplingConfig,
        seeds_manager: SeedManager,
        strategies_manager: StrategyManager,
    ):
        self._config = config
        self._seeds = seeds_manager
        self._strategies = strategies_manager

        # Queues and synchronization
        self._seed_queue: asyncio.Queue[Seed | None] = asyncio.Queue(
            maxsize=config.max_seeds or config.prefetch_seeds
        )
        self._strategy_queue: asyncio.Queue[Strategy | None] = asyncio.Queue(
            maxsize=config.max_strategies or config.prefetch_strategies
        )
        self._stop_event = asyncio.Event()

    def stop(self) -> None:
        """Signal all producers to stop."""
        self._stop_event.set()

    @property
    def stopped(self) -> bool:
        """Check if pipeline has been stopped."""
        return self._stop_event.is_set()

    async def produce_seeds(self) -> None:
        """Fetch seeds and put them in the queue."""
        cfg = self._config
        seed_count = 0
        try:
            async for seed in self._seeds.sample(topics=cfg.topics):
                if self.stopped:
                    break
                if cfg.max_seeds is not None and seed_count >= cfg.max_seeds:
                    break
                await self._seed_queue.put(seed)
                seed_count += 1
        finally:
            await self._seed_queue.put(None)

    async def produce_strategies(self) -> None:
        """Extract strategies from seeds and put them in the queue."""
        cfg = self._config
        try:
            strategy_count = 0

            while not self.stopped:
                if cfg.max_strategies is not None and strategy_count >= cfg.max_strategies:
                    self.stop()
                    break

                seed = await self._seed_queue.get()
                if seed is None:
                    break

                seed_strategy_count = 0
                async for strategy in self._strategies.sample(
                    seed,
                    cfg.task,
                    chunk_size=cfg.chunk_size,
                    max_chunks_per_seed=cfg.max_chunks_per_seed,
                    max_strategies_per_chunk=cfg.max_strategies_per_chunk,
                ):
                    if self.stopped:
                        break

                    await self._strategy_queue.put(strategy)
                    strategy_count += 1
                    seed_strategy_count += 1

                    if (
                        cfg.max_strategies_per_seed is not None
                        and seed_strategy_count >= cfg.max_strategies_per_seed
                    ):
                        break

                    if cfg.max_strategies is not None and strategy_count >= cfg.max_strategies:
                        self.stop()
                        break
        finally:
            await self._strategy_queue.put(None)

    async def run(self) -> AsyncIterator[Strategy]:
        """Run the pipeline and yield strategies.

        Launches producer tasks, yields strategies from the queue, and ensures
        proper cleanup on exit (whether normal completion or early termination).
        """
        tasks = [
            asyncio.create_task(self.produce_seeds()),
            asyncio.create_task(self.produce_strategies()),
        ]

        try:
            async for strategy in self._consume_strategies():
                yield strategy
        finally:
            self.stop()
            for task in tasks:
                task.cancel()
            # Wait for tasks with timeout to avoid hanging on unresponsive I/O
            done, pending = await asyncio.wait(tasks, timeout=2.0)
            for task in pending:
                task.cancel()

    async def _consume_strategies(self) -> AsyncIterator[Strategy]:
        """Yield strategies from the queue (internal)."""
        cfg = self._config
        strategy_count = 0

        while True:
            strategy = await self._strategy_queue.get()
            if strategy is None:
                break

            yield strategy
            strategy_count += 1

            if cfg.max_strategies is not None and strategy_count >= cfg.max_strategies:
                self.stop()
                break
