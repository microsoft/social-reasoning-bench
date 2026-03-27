"""Run configuration for marketplace benchmark runs."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import BaseModel, Field


class RunConfig(BaseModel):
    """Configuration for a marketplace benchmark run, saved for resumability."""

    # Task paths
    paths: list[str] = Field(
        default_factory=list, description="YAML files or directories containing task definitions"
    )
    limit: int | None = Field(default=None, description="Limit on number of tasks to load")

    # Model configuration
    model: str | None = Field(default=None, description="Default model for buyer and seller")
    buyer_model: str | None = Field(default=None, description="Model for buyer agent")
    seller_model: str | None = Field(default=None, description="Model for seller agent")
    judge_model: str | None = Field(default=None, description="Model for privacy leakage judge")

    # Base URLs
    base_url: str | None = Field(default=None, description="Default base URL for API")
    buyer_base_url: str | None = Field(default=None, description="Base URL for buyer")
    seller_base_url: str | None = Field(default=None, description="Base URL for seller")
    judge_base_url: str | None = Field(default=None, description="Base URL for judge")

    # Reasoning effort
    reasoning_effort: str | int | None = Field(default=None, description="Default reasoning effort")

    # Run parameters
    max_steps_per_turn: int = Field(default=3, description="Maximum tool calls per agent turn")
    batch_size: int = Field(default=50, description="Number of tasks to run in parallel")

    # Output
    output_dir: Path | None = Field(default=None, description="Output directory for results")

    @property
    def resolved_buyer_model(self) -> str | None:
        return self.buyer_model or self.model

    @property
    def resolved_seller_model(self) -> str | None:
        return self.seller_model or self.model

    @property
    def resolved_judge_model(self) -> str | None:
        return self.judge_model

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> RunConfig:
        """Create a RunConfig from CLI arguments."""
        return cls(
            paths=args.data or [],
            limit=args.limit,
            model=args.model,
            buyer_model=args.buyer_model,
            seller_model=args.seller_model,
            judge_model=getattr(args, "judge_model", None),
            base_url=args.base_url,
            buyer_base_url=args.buyer_base_url,
            seller_base_url=args.seller_base_url,
            judge_base_url=getattr(args, "judge_base_url", None),
            reasoning_effort=args.reasoning_effort,
            max_steps_per_turn=args.max_steps_per_turn,
            batch_size=args.batch_size,
            output_dir=Path(args.output_dir) if args.output_dir else None,
        )
