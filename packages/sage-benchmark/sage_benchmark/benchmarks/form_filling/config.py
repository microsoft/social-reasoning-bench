"""Form-filling run configuration."""

from __future__ import annotations

import argparse

from pydantic import Field

from ..base import BaseRunConfig


class FormFillingRunConfig(BaseRunConfig):
    """Run configuration for form-filling benchmark."""

    # Per-agent model overrides
    assistant_model: str | None = Field(default=None)
    interviewer_model: str | None = Field(default=None)
    assistant_base_url: str | None = Field(default=None)
    interviewer_base_url: str | None = Field(default=None)
    assistant_api_version: str | None = Field(default=None)
    interviewer_api_version: str | None = Field(default=None)
    assistant_reasoning_effort: str | int | None = Field(default=None)
    interviewer_reasoning_effort: str | int | None = Field(default=None)

    # Form-filling specific
    prompt_type: str = Field(default="none")
    single_field_mode: bool = Field(default=False)
    eval_batch_size: int = Field(
        default=0,
        description="Max concurrent evaluation work items per task. "
        "0 = auto-scale based on batch_size to keep total concurrency ~80.",
    )

    # --- Assistant resolved properties ---

    @property
    def resolved_assistant_model(self) -> str | None:
        return self.assistant_model or self.model

    @property
    def resolved_assistant_base_url(self) -> str | None:
        return self.assistant_base_url or self.base_url

    @property
    def resolved_assistant_api_version(self) -> str | None:
        return self.assistant_api_version or self.api_version

    @property
    def resolved_assistant_reasoning_effort(self) -> str | int | None:
        return self.assistant_reasoning_effort or self.reasoning_effort

    # --- Interviewer resolved properties ---

    @property
    def resolved_interviewer_model(self) -> str | None:
        return self.interviewer_model or self.model

    @property
    def resolved_interviewer_base_url(self) -> str | None:
        return self.interviewer_base_url or self.base_url

    @property
    def resolved_interviewer_api_version(self) -> str | None:
        return self.interviewer_api_version or self.api_version

    @property
    def resolved_interviewer_reasoning_effort(self) -> str | int | None:
        return self.interviewer_reasoning_effort or self.reasoning_effort

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> FormFillingRunConfig:
        return cls.model_validate(vars(args))
