"""Calendar scheduling run configuration."""

from __future__ import annotations

import argparse

from pydantic import Field

from ..base import BaseRunConfig


class CalendarRunConfig(BaseRunConfig):
    """Run configuration for calendar scheduling benchmark."""

    # Per-agent model overrides
    assistant_model: str | None = Field(default=None, description="Model for assistant agent")
    requestor_model: str | None = Field(default=None, description="Model for requestor agent")
    assistant_base_url: str | None = Field(default=None)
    requestor_base_url: str | None = Field(default=None)
    assistant_api_version: str | None = Field(default=None)
    requestor_api_version: str | None = Field(default=None)
    assistant_reasoning_effort: str | int | None = Field(default=None)
    requestor_reasoning_effort: str | int | None = Field(default=None)

    # System prompt
    assistant_system_prompt: str | None = Field(default=None)
    assistant_system_prompt_file: str | None = Field(default=None)

    # Per-agent CoT
    assistant_explicit_cot: bool | None = Field(default=None)
    requestor_explicit_cot: bool | None = Field(default=None)

    # Calendar-specific
    expose_preferences: bool | None = Field(default=None)

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

    @property
    def resolved_assistant_explicit_cot(self) -> bool:
        if self.assistant_explicit_cot is not None:
            return self.assistant_explicit_cot
        return self.explicit_cot or False

    # --- Requestor resolved properties ---

    @property
    def resolved_requestor_model(self) -> str | None:
        return self.requestor_model or self.model

    @property
    def resolved_requestor_base_url(self) -> str | None:
        return self.requestor_base_url or self.base_url

    @property
    def resolved_requestor_api_version(self) -> str | None:
        return self.requestor_api_version or self.api_version

    @property
    def resolved_requestor_reasoning_effort(self) -> str | int | None:
        return self.requestor_reasoning_effort or self.reasoning_effort

    @property
    def resolved_requestor_explicit_cot(self) -> bool:
        if self.requestor_explicit_cot is not None:
            return self.requestor_explicit_cot
        return self.explicit_cot or False

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> CalendarRunConfig:
        return cls.model_validate(vars(args))
