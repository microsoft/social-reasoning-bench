"""Main WhimsyGen class - the unified API entry point."""

from collections.abc import AsyncIterator
from pathlib import Path

from ..core._sampler import (
    DEFAULT_PREFETCH_SEEDS,
    DEFAULT_PREFETCH_STRATEGIES,
    SamplingConfig,
    SamplingPipeline,
)
from ..core.models import Strategy
from ..seeds.manager import SeedManager
from ..strategies.manager import StrategyManager
from ..tasks.manager import TaskManager


class WhimsyGen:
    """Extract whimsical strategies from Wikipedia for adversarial testing.

    Example:
        wg = WhimsyGen(
            model="openai/gpt-4.1",
            seeds="seeds/",
            task="task.txt",
        )

        # sample() returns a list of N strategies
        strategies = await wg.sample(10)

        # isample() returns an async iterator for streaming
        async for strategy in wg.isample(max_strategies=10):
            print(strategy.game_strategies)
    """

    def __init__(
        self,
        *,
        model: str,
        seeds: Path | str | None = None,
        task: Path | str | None = None,
        reasoning_effort: str | int | None = None,
    ):
        """Initialize WhimsyGen.

        Args:
            model: Model identifier (e.g., "openai/gpt-4.1", "gemini/gemini-3-pro")
            seeds: Seeds directory path (optional, can set via wg.seeds.dir later)
            task: Task file path or task text (optional, can set via wg.task later)
            reasoning_effort: Reasoning effort for the model (e.g., "medium", "high")
        """
        self._seeds = SeedManager(dir=seeds)
        self._task = TaskManager(task=task)
        self._strategies = StrategyManager(model=model, reasoning_effort=reasoning_effort)

    @property
    def seeds(self) -> SeedManager:
        """Seeds manager.

        Returns:
            The SeedManager instance.
        """
        return self._seeds

    @property
    def task(self) -> TaskManager:
        """Task manager.

        Returns:
            The TaskManager instance.
        """
        return self._task

    @property
    def strategies(self) -> StrategyManager:
        """Strategies manager.

        Returns:
            The StrategyManager instance.
        """
        return self._strategies

    async def sample(
        self,
        n: int,
        topics: list[str] | None = None,
        chunk_size: int = 5000,
        max_seeds: int | None = None,
        max_chunks_per_seed: int | None = None,
        max_strategies_per_chunk: int | None = None,
        max_strategies_per_seed: int | None = None,
        prefetch_seeds: int = DEFAULT_PREFETCH_SEEDS,
        prefetch_strategies: int = DEFAULT_PREFETCH_STRATEGIES,
    ) -> list[Strategy]:
        """Sample N strategies from seeds using the current task.

        Args:
            n: Number of strategies to return
            topics: Wikipedia topics for crawling (uses defaults if None)
            chunk_size: Size of text chunks for processing (default: 5000)
            max_seeds: Maximum seeds to use (None for unlimited)
            max_chunks_per_seed: Maximum chunks per seed (None for unlimited)
            max_strategies_per_chunk: Maximum strategies per chunk (None for unlimited)
            max_strategies_per_seed: Maximum strategies per seed (None for unlimited)
            prefetch_seeds: Number of seeds to prefetch
            prefetch_strategies: Number of strategies to prefetch

        Returns:
            List of N Strategy objects.
        """
        return [
            s
            async for s in self.isample(
                topics=topics,
                chunk_size=chunk_size,
                max_seeds=max_seeds,
                max_chunks_per_seed=max_chunks_per_seed,
                max_strategies_per_chunk=max_strategies_per_chunk,
                max_strategies_per_seed=max_strategies_per_seed,
                max_strategies=n,
                prefetch_seeds=prefetch_seeds,
                prefetch_strategies=prefetch_strategies,
            )
        ]

    async def isample(
        self,
        topics: list[str] | None = None,
        chunk_size: int = 5000,
        max_seeds: int | None = None,
        max_chunks_per_seed: int | None = None,
        max_strategies_per_chunk: int | None = None,
        max_strategies_per_seed: int | None = None,
        max_strategies: int | None = None,
        prefetch_seeds: int = DEFAULT_PREFETCH_SEEDS,
        prefetch_strategies: int = DEFAULT_PREFETCH_STRATEGIES,
    ) -> AsyncIterator[Strategy]:
        """Sample strategies as an async iterator (streaming).

        Args:
            topics: Wikipedia topics for crawling (uses defaults if None)
            chunk_size: Size of text chunks for processing (default: 5000)
            max_seeds: Maximum seeds to use (None for unlimited)
            max_chunks_per_seed: Maximum chunks per seed (None for unlimited)
            max_strategies_per_chunk: Maximum strategies per chunk (None for unlimited)
            max_strategies_per_seed: Maximum strategies per seed (None for unlimited)
            max_strategies: Maximum total strategies (None for unlimited)
            prefetch_seeds: Number of seeds to prefetch
            prefetch_strategies: Number of strategies to prefetch

        Yields:
            Strategy objects as they're extracted.
        """
        current_task = self._task.current
        if current_task is None:
            raise ValueError("No task set. Call task.load() or task.set() first.")

        config = SamplingConfig(
            task=current_task,
            topics=topics,
            chunk_size=chunk_size,
            max_seeds=max_seeds,
            max_chunks_per_seed=max_chunks_per_seed,
            max_strategies_per_chunk=max_strategies_per_chunk,
            max_strategies_per_seed=max_strategies_per_seed,
            max_strategies=max_strategies,
            prefetch_seeds=prefetch_seeds,
            prefetch_strategies=prefetch_strategies,
        )

        pipeline = SamplingPipeline(config, self._seeds, self._strategies)

        async for strategy in pipeline.run():
            yield strategy

    def __repr__(self) -> str:
        seeds_dir = self._seeds._dir if self._seeds._dir else "not set"
        return f"WhimsyGen(seeds={seeds_dir!r}, task={'set' if self._task.current else 'None'})"
