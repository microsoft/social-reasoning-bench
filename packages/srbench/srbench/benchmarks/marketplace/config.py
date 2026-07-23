"""Marketplace run configuration."""

from __future__ import annotations

import argparse
from typing import Any

from pydantic import Field, field_validator

from ..base import BaseRunConfig


class MarketplaceRunConfig(BaseRunConfig):
    """Run configuration for marketplace benchmark."""

    # Bring your own buyer (assistant) agent
    buyer_agent: str | None = Field(
        default=None,
        description=(
            "Import string for a user-provided buyer agent class "
            "(e.g. 'my_pkg.my_mod:MyClass'). Must subclass BaseAssistantAgent. "
            "When set, the built-in buyer and its model settings are not used."
        ),
    )
    buyer_agent_kwargs: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Extra keyword arguments passed to the buyer agent constructor "
            "(e.g. {'model': ..., 'reasoning_effort': ...}). Only used when "
            "buyer_agent is set."
        ),
    )

    @field_validator("buyer_agent_kwargs", mode="before")
    @classmethod
    def _default_buyer_agent_kwargs(cls, v: Any) -> Any:
        return {} if v is None else v

    # Per-agent model overrides
    buyer_model: str | None = Field(default=None)
    seller_model: str | None = Field(default=None)
    buyer_base_url: str | None = Field(default=None)
    seller_base_url: str | None = Field(default=None)
    buyer_api_version: str | None = Field(default=None)
    seller_api_version: str | None = Field(default=None)
    buyer_reasoning_effort: str | int | None = Field(default=None)
    seller_reasoning_effort: str | int | None = Field(default=None)

    # Per-agent CoT
    buyer_explicit_cot: bool | None = Field(default=None)
    seller_explicit_cot: bool | None = Field(default=None)

    # --- Buyer resolved properties ---

    @property
    def resolved_buyer_model(self) -> str | None:
        return self.buyer_model or self.model

    @property
    def resolved_buyer_base_url(self) -> str | None:
        return self.buyer_base_url or self.base_url

    @property
    def resolved_buyer_api_version(self) -> str | None:
        return self.buyer_api_version or self.api_version

    @property
    def resolved_buyer_reasoning_effort(self) -> str | int | None:
        if self.buyer_reasoning_effort is not None:
            return self.buyer_reasoning_effort
        if self.buyer_model is not None:
            return None
        return self.reasoning_effort

    @property
    def resolved_buyer_explicit_cot(self) -> bool:
        if self.buyer_explicit_cot is not None:
            return self.buyer_explicit_cot
        return self.explicit_cot or False

    # --- Seller resolved properties ---

    @property
    def resolved_seller_model(self) -> str | None:
        return self.seller_model or self.model

    @property
    def resolved_seller_base_url(self) -> str | None:
        return self.seller_base_url or self.base_url

    @property
    def resolved_seller_api_version(self) -> str | None:
        return self.seller_api_version or self.api_version

    @property
    def resolved_seller_reasoning_effort(self) -> str | int | None:
        if self.seller_reasoning_effort is not None:
            return self.seller_reasoning_effort
        if self.seller_model is not None:
            return None
        return self.reasoning_effort

    @property
    def resolved_seller_explicit_cot(self) -> bool:
        if self.seller_explicit_cot is not None:
            return self.seller_explicit_cot
        return self.explicit_cot or False

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> MarketplaceRunConfig:
        return cls.model_validate(vars(args))
