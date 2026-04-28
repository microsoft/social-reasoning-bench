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

    # Per-agent CoT
    assistant_explicit_cot: bool | None = Field(default=None)
    interviewer_explicit_cot: bool | None = Field(default=None)

    # Form-filling specific
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
        if self.assistant_reasoning_effort is not None:
            return self.assistant_reasoning_effort
        if self.assistant_model is not None:
            return None
        return self.reasoning_effort

    @property
    def resolved_assistant_explicit_cot(self) -> bool:
        if self.assistant_explicit_cot is not None:
            return self.assistant_explicit_cot
        return self.explicit_cot or False

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
        if self.interviewer_reasoning_effort is not None:
            return self.interviewer_reasoning_effort
        if self.interviewer_model is not None:
            return None
        return self.reasoning_effort

    @property
    def resolved_interviewer_explicit_cot(self) -> bool:
        if self.interviewer_explicit_cot is not None:
            return self.interviewer_explicit_cot
        return self.explicit_cot or False

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> FormFillingRunConfig:
        return cls.model_validate(vars(args))
