"""StrategyManager - Manage strategy extraction and caching."""

from collections.abc import AsyncIterator
from pathlib import Path

import yaml

from ..core.models import Seed, Strategy, StrategyCollection
from .extractor import StrategyExtractor


class StrategyManager:
    """Manages strategy extraction and caching.

    Example:
        manager = StrategyManager(model="openai/gpt-4.1")

        async for strategy in manager.sample(seed, task):
            print(strategy.game_strategies)

        manager.save("strategies.yaml")
    """

    def __init__(self, model: str):
        """Initialize the strategy manager.

        Args:
            model: LLM model identifier (e.g., "openai/gpt-4.1")
        """
        self._extractor = StrategyExtractor(model=model)
        self._cache: list[Strategy] = []

    async def sample(
        self,
        seed: Seed,
        task: str,
        chunk_size: int = 5000,
        max_chunks_per_seed: int | None = None,
        max_strategies_per_chunk: int | None = None,
    ) -> AsyncIterator[Strategy]:
        """Sample strategies from a seed.

        Args:
            seed: Seed to extract strategies from
            task: Task description for strategy context
            chunk_size: Size of text chunks for processing
            max_chunks_per_seed: Maximum chunks to process (None for unlimited)
            max_strategies_per_chunk: Maximum strategies per chunk (None for unlimited)

        Yields:
            Strategy objects as they're extracted
        """
        async for strategy in self._extractor.sample(
            seed,
            task,
            chunk_size=chunk_size,
            max_chunks=max_chunks_per_seed,
            max_strategies_per_chunk=max_strategies_per_chunk,
        ):
            self._cache.append(strategy)
            yield strategy

    def save(self, path: Path | str) -> Path:
        """Save cached strategies to disk.

        Args:
            path: Output file path

        Returns:
            Path to saved file
        """
        if not self._cache:
            raise ValueError("No strategies to save. Call stream() first.")

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        collection = StrategyCollection(
            source_seed=Seed(title="combined", url="", content=""),
            total_chunks=0,
            strategies=self._cache,
        )

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(collection.model_dump(), f, allow_unicode=True, default_flow_style=False)

        return path

    def load(self, path: Path | str) -> list[Strategy]:
        """Load strategies from a file.

        Args:
            path: Path to strategies YAML file

        Returns:
            List of Strategy objects
        """
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        collection = StrategyCollection(**data)
        self._cache = list(collection.strategies)
        return self._cache

    @property
    def cache(self) -> list[Strategy]:
        """Get cached strategies."""
        return self._cache

    def clear(self) -> None:
        """Clear the strategy cache."""
        self._cache.clear()
