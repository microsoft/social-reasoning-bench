"""Data models for whimsygen."""

from pydantic import BaseModel, Field


class Seed(BaseModel):
    """Crawled Wikipedia document (source material for strategy extraction)."""

    title: str
    url: str
    depth: int = 0
    content: str
    links: list[str] = Field(default_factory=list)
    total_links: int = 0


class Strategy(BaseModel):
    """Extracted strategy from a Seed."""

    grounding_texts: str  # Source Wikipedia content
    game_strategies: str  # How to apply in game
    source_seed: str = ""  # Title of the source seed
    source_chunk: int = 0


class StrategyCollection(BaseModel):
    """Collection of strategies from a Seed."""

    source_seed: "Seed"
    total_chunks: int
    strategies: list[Strategy] = Field(default_factory=list)


# Enable forward references
Strategy.model_rebuild()
StrategyCollection.model_rebuild()
