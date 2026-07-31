"""Calendar scheduling run configuration."""

from __future__ import annotations

import argparse
from typing import Any

from pydantic import Field, field_validator, model_validator

from ..base import BaseRunConfig


class CalendarRunConfig(BaseRunConfig):
    """Run configuration for calendar scheduling benchmark."""

    # Bring your own assistant agent
    assistant_agent: str | None = Field(
        default=None,
        description=(
            "Import string for a user-provided assistant agent class "
            "(e.g. 'my_pkg.my_mod:MyClass'). Must subclass BaseAssistantAgent. "
            "When set, the built-in assistant and its model settings are not used."
        ),
    )
    assistant_agent_kwargs: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Extra keyword arguments passed to the assistant agent constructor "
            "(e.g. {'model': ..., 'reasoning_effort': ...}). Only used when "
            "assistant_agent is set."
        ),
    )

    @field_validator("assistant_agent_kwargs", mode="before")
    @classmethod
    def _default_assistant_agent_kwargs(cls, v: Any) -> Any:
        return {} if v is None else v

    # Per-agent model overrides
    assistant_model: str | None = Field(default=None, description="Model for assistant agent")
    requestor_model: str | None = Field(default=None, description="Model for requestor agent")
    assistant_base_url: str | None = Field(default=None)
    requestor_base_url: str | None = Field(default=None)
    assistant_api_version: str | None = Field(default=None)
    requestor_api_version: str | None = Field(default=None)
    assistant_reasoning_effort: str | int | None = Field(default=None)
    requestor_reasoning_effort: str | int | None = Field(default=None)

    # Per-agent CoT
    assistant_explicit_cot: bool | None = Field(default=None)
    requestor_explicit_cot: bool | None = Field(default=None)

    # Calendar-specific
    expose_preferences: bool = Field(default=True)
    # When False, the <user_preference> block is still injected into the user
    # turn but the system prompt gets no explanation of it. Ablation only.
    preference_guidance: bool = Field(default=True)

    @model_validator(mode="after")
    def _mirror_assistant_agent_model(self) -> CalendarRunConfig:
        """Surface a BYOA agent's model/effort on the reporting fields.

        BYOA agents receive ``model`` and ``reasoning_effort`` through
        ``assistant_agent_kwargs``. Mirror those onto ``assistant_model`` /
        ``assistant_reasoning_effort`` (when not set explicitly) so results and
        the dashboard report them like any built-in run.
        """
        if self.assistant_agent:
            kwargs = self.assistant_agent_kwargs
            if self.assistant_model is None and kwargs.get("model") is not None:
                self.assistant_model = kwargs["model"]
            if (
                self.assistant_reasoning_effort is None
                and kwargs.get("reasoning_effort") is not None
            ):
                self.assistant_reasoning_effort = kwargs["reasoning_effort"]
        return self

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
        if self.requestor_reasoning_effort is not None:
            return self.requestor_reasoning_effort
        if self.requestor_model is not None:
            return None
        return self.reasoning_effort

    @property
    def resolved_requestor_explicit_cot(self) -> bool:
        if self.requestor_explicit_cot is not None:
            return self.requestor_explicit_cot
        return self.explicit_cot or False

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> CalendarRunConfig:
        return cls.model_validate(vars(args))
