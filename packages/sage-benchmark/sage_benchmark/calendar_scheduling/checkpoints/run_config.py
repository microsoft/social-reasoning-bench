"""Run configuration for benchmark runs."""

import argparse
from pathlib import Path

from pydantic import BaseModel, Field


class RunConfig(BaseModel):
    """Configuration for a benchmark run, saved for resumability.

    This class is also aliased as ExperimentConfig for use with the experiments module.
    Fields with defaults can be omitted when defining experiments in Python files.
    """

    # Task paths
    paths: list[str] = Field(
        default_factory=list, description="YAML files or directories containing task definitions"
    )
    limit: int | None = Field(default=None, description="Limit on number of tasks to load")

    # Model configuration
    model: str | None = Field(default=None, description="Default model for all agents")
    assistant_model: str | None = Field(default=None, description="Model for assistant agent")
    requestor_model: str | None = Field(default=None, description="Model for requestor agent")
    judge_model: str | None = Field(default=None, description="Model for judge")

    # Base URLs
    base_url: str | None = Field(default=None, description="Default base URL for API")
    assistant_base_url: str | None = Field(default=None, description="Base URL for assistant")
    requestor_base_url: str | None = Field(default=None, description="Base URL for requestor")
    judge_base_url: str | None = Field(default=None, description="Base URL for judge")

    # API versions
    api_version: str | None = Field(default=None, description="Default API version")
    assistant_api_version: str | None = Field(default=None, description="API version for assistant")
    requestor_api_version: str | None = Field(default=None, description="API version for requestor")
    judge_api_version: str | None = Field(default=None, description="API version for judge")

    # Reasoning effort
    reasoning_effort: str | int | None = Field(default=None, description="Default reasoning effort")
    assistant_reasoning_effort: str | int | None = Field(
        default=None, description="Reasoning for assistant"
    )
    requestor_reasoning_effort: str | int | None = Field(
        default=None, description="Reasoning for requestor"
    )
    judge_reasoning_effort: str | int | None = Field(
        default=None, description="Reasoning for judge"
    )

    # Run parameters (with defaults for experiment file usage)
    max_rounds: int = Field(default=20, description="Maximum conversation rounds per task")
    max_steps_per_turn: int = Field(default=20, description="Maximum tool calls per agent turn")
    batch_size: int = Field(default=32, description="Number of tasks to run in parallel")

    # System prompt (optional for experiment files)
    assistant_system_prompt: str | None = Field(default=None, description="System prompt preset")
    assistant_system_prompt_file: str | None = Field(
        default=None, description="Path to custom system prompt file"
    )

    # Explicit CoT (optional for experiment files)
    explicit_cot: bool | None = Field(
        default=None, description="Enable explicit chain-of-thought prompting for all agents"
    )
    assistant_explicit_cot: bool | None = Field(
        default=None, description="Explicit CoT override for assistant agent"
    )
    requestor_explicit_cot: bool | None = Field(
        default=None, description="Explicit CoT override for requestor agent"
    )

    # Other options
    artifacts: str | None = Field(default=None, description="Path to artifacts JSON file")
    expose_preferences: bool | None = Field(
        default=None, description="Expose preferences to assistant"
    )

    # Privacy evaluation options
    judge_votes: int = Field(
        default=3,
        description="Number of judge votes for majority voting in leakage detection",
    )

    # Experiment-specific fields
    output_dir: Path | None = Field(default=None, description="Output directory for experiment")
    variant: str | None = Field(default=None, description="Variant name for experiment")

    @property
    def resolved_assistant_model(self) -> str | None:
        return self.assistant_model or self.model

    @property
    def resolved_requestor_model(self) -> str | None:
        return self.requestor_model or self.model

    @property
    def resolved_judge_model(self) -> str | None:
        return self.judge_model or self.model

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "RunConfig":
        """Create a RunConfig from CLI arguments."""
        return cls(
            paths=args.paths,
            limit=args.limit,
            model=args.model,
            assistant_model=args.assistant_model,
            requestor_model=args.requestor_model,
            judge_model=args.judge_model,
            base_url=args.base_url,
            assistant_base_url=args.assistant_base_url,
            requestor_base_url=args.requestor_base_url,
            judge_base_url=args.judge_base_url,
            api_version=args.api_version,
            assistant_api_version=args.assistant_api_version,
            requestor_api_version=args.requestor_api_version,
            judge_api_version=args.judge_api_version,
            reasoning_effort=args.reasoning_effort,
            assistant_reasoning_effort=args.assistant_reasoning_effort,
            requestor_reasoning_effort=args.requestor_reasoning_effort,
            judge_reasoning_effort=args.judge_reasoning_effort,
            max_rounds=args.max_rounds,
            max_steps_per_turn=args.max_steps_per_turn,
            batch_size=args.batch_size,
            assistant_system_prompt=args.assistant_system_prompt,
            assistant_system_prompt_file=str(args.assistant_system_prompt_file)
            if args.assistant_system_prompt_file
            else None,
            explicit_cot=args.explicit_cot,
            assistant_explicit_cot=args.assistant_explicit_cot,
            requestor_explicit_cot=args.requestor_explicit_cot,
            artifacts=args.artifacts,
            expose_preferences=args.expose_preferences,
            judge_votes=getattr(args, "judge_votes", 3),
            output_dir=getattr(args, "output_dir", None),
        )
