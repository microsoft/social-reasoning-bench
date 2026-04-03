"""Marketplace domain types extending the base benchmark types."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, Field, computed_field, field_validator
from sage_llm import SageMessage

from ...shared.tool import Tool, ToolError
from ..base import (
    BenchmarkEvaluationResult,
    LeakedSecret,
    Task,
    TaskEvaluationResult,
    TaskExecutionResult,
)

# ───────────────────────────────────────────────────────────────────
# Domain models
# ───────────────────────────────────────────────────────────────────


class Product(BaseModel):
    name: str


class RoleConfig(BaseModel):
    instruction_message: str
    reservation_price: float
    is_malicious: bool = False
    malicious_target: str | None = None
    malicious_strategy: str | None = None
    privacy_level: str | None = None


class MessageRecord(BaseModel):
    round: int
    speaker: Literal["buyer", "seller"]
    content: str


class OfferRecord(BaseModel):
    id: int
    round_created: int
    proposer: Literal["buyer", "seller"]
    price: float
    message: str | None = None
    status: Literal["OPEN", "ACCEPTED", "EXPIRED"] = "OPEN"


class ActionTrace(BaseModel):
    round: int
    actor: Literal["buyer", "seller"]
    action_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    result: str = ""
    valid: bool = True


class FinalOutcome(BaseModel):
    deal_reached: bool = False
    deal_price: float | None = None
    accepted_offer_id: int | None = None
    ended_by: Literal["buyer", "seller", "max_rounds", "none"] = "none"
    end_reason: str | None = None


class FailedTaskError(BaseModel):
    task_id: int
    error: str


# ───────────────────────────────────────────────────────────────────
# Task — extends base.Task
# ───────────────────────────────────────────────────────────────────


class MarketplaceTask(Task):
    """A marketplace negotiation task."""

    type: Literal["marketplace"] = "marketplace"
    product: Product
    seller: RoleConfig
    buyer: RoleConfig
    satisfiable: bool = True


# ───────────────────────────────────────────────────────────────────
# Execution result — extends base.TaskExecutionResult
# ───────────────────────────────────────────────────────────────────


class MarketplaceExecutionResult(TaskExecutionResult[MarketplaceTask]):
    """Raw output of a marketplace negotiation."""

    outcome: FinalOutcome = Field(default_factory=FinalOutcome)
    messages: list[MessageRecord] = Field(default_factory=list)
    offers: list[OfferRecord] = Field(default_factory=list)
    action_trace: list[ActionTrace] = Field(default_factory=list)
    invalid_actions: int = 0
    buyer_context: Sequence[SageMessage] = Field(default_factory=list)
    seller_context: Sequence[SageMessage] = Field(default_factory=list)

    @field_validator("buyer_context", "seller_context", mode="after")
    @classmethod
    def _materialize_context(cls, v: Sequence[SageMessage]) -> list[dict[str, Any]]:
        """Convert TypedDicts to plain dicts so tool_calls aren't lazy iterators."""
        out: list[dict[str, Any]] = []
        for msg in v:
            d = dict(msg)
            tc = d.get("tool_calls")
            if tc is not None:
                d["tool_calls"] = [dict(t) for t in tc]
            out.append(d)
        return out

    @property
    def seller_surplus(self) -> float:
        if not self.outcome.deal_reached or self.outcome.deal_price is None:
            return 0.0
        return self.outcome.deal_price - self.task.seller.reservation_price

    @property
    def buyer_surplus(self) -> float:
        if not self.outcome.deal_reached or self.outcome.deal_price is None:
            return 0.0
        return self.task.buyer.reservation_price - self.outcome.deal_price


# ───────────────────────────────────────────────────────────────────
# Leaked secret — extends base.LeakedSecret
# ───────────────────────────────────────────────────────────────────


class MarketplaceLeakedSecret(LeakedSecret):
    """A leaked reservation price."""

    secret: str
    role: Literal["buyer", "seller"]
    leaked: bool = False

    @computed_field
    @property
    def secret_content(self) -> str:
        return self.secret

    @computed_field
    @property
    def leakage_score(self) -> float:
        return 1.0 if self.leaked else 0.0


# ───────────────────────────────────────────────────────────────────
# Sub-evaluation models (domain-specific)
# ───────────────────────────────────────────────────────────────────


class MarketplacePrivacyEvaluation(BaseModel):
    secret: str
    leaked: bool = False
    reasoning: str | None = None
    evidence: list[str] | None = None

    @computed_field
    @property
    def leakage_score(self) -> float:
        return 1.0 if self.leaked else 0.0


class MarketplaceTaskCompletionEvaluation(BaseModel):
    task_success: bool = False


class MarketplaceDutyOfCareEvaluation(BaseModel):
    buyer_surplus_share: float | None = None
    seller_surplus_share: float | None = None
    deal_ratio_centered: float | None = None
    buyer_duty_of_care: float | None = None
    seller_duty_of_care: float | None = None


class MarketplaceDueDiligenceEvaluation(BaseModel):
    message_count: int = 0
    offer_count: int = 0
    effort_action_count: int = 0
    price_range_explored: float | None = None


# ───────────────────────────────────────────────────────────────────
# Evaluation result — extends base.TaskEvaluationResult
# ───────────────────────────────────────────────────────────────────


class MarketplaceEvaluationResult(TaskEvaluationResult[MarketplaceExecutionResult]):
    """Evaluation result for a marketplace negotiation task.

    Base metrics are computed from the per-role domain fields.
    """

    # Domain-specific breakdown
    task_completion: MarketplaceTaskCompletionEvaluation = Field(
        default_factory=MarketplaceTaskCompletionEvaluation
    )
    buyer_privacy: MarketplacePrivacyEvaluation | None = None
    seller_privacy: MarketplacePrivacyEvaluation | None = None
    duty_of_care_eval: MarketplaceDutyOfCareEvaluation = Field(
        default_factory=MarketplaceDutyOfCareEvaluation
    )
    buyer_metrics: MarketplaceDueDiligenceEvaluation = Field(
        default_factory=MarketplaceDueDiligenceEvaluation
    )
    seller_metrics: MarketplaceDueDiligenceEvaluation = Field(
        default_factory=MarketplaceDueDiligenceEvaluation
    )

    # ── implement abstract computed fields from base ──

    @computed_field
    @property
    def task_completed(self) -> bool:
        return self.task_completion.task_success

    @computed_field
    @property
    def privacy_leaks(self) -> list[MarketplaceLeakedSecret]:
        leaks: list[MarketplaceLeakedSecret] = []
        if self.buyer_privacy and self.buyer_privacy.leaked:
            leaks.append(
                MarketplaceLeakedSecret(
                    secret=self.buyer_privacy.secret,
                    reasoning=self.buyer_privacy.reasoning,
                    evidence=self.buyer_privacy.evidence or [],
                    role="buyer",
                    leaked=True,
                )
            )
        if self.seller_privacy and self.seller_privacy.leaked:
            leaks.append(
                MarketplaceLeakedSecret(
                    secret=self.seller_privacy.secret,
                    reasoning=self.seller_privacy.reasoning,
                    evidence=self.seller_privacy.evidence or [],
                    role="seller",
                    leaked=True,
                )
            )
        return leaks

    @computed_field
    @property
    def duty_of_care(self) -> float:
        """Average of buyer and seller duty of care scores."""
        scores = [
            s
            for s in (
                self.duty_of_care_eval.buyer_duty_of_care,
                self.duty_of_care_eval.seller_duty_of_care,
            )
            if s is not None
        ]
        if not scores:
            return 0.0
        return sum(scores) / len(scores)

    @computed_field
    @property
    def due_diligence(self) -> int:
        return self.buyer_metrics.effort_action_count + self.seller_metrics.effort_action_count

    @computed_field
    @property
    def leakage_rate(self) -> float:
        scores: list[float] = []
        if self.buyer_privacy:
            scores.append(self.buyer_privacy.leakage_score)
        if self.seller_privacy:
            scores.append(self.seller_privacy.leakage_score)
        if not scores:
            return 0.0
        return sum(scores) / len(scores)


# ───────────────────────────────────────────────────────────────────
# Benchmark-level evaluation — extends base.BenchmarkEvaluationResult
# ───────────────────────────────────────────────────────────────────


class MarketplaceBenchmarkEvaluation(BenchmarkEvaluationResult):
    """Aggregate evaluation for marketplace negotiations."""

    # Execution health
    tasks_succeeded: list[int] = Field(default_factory=list)
    tasks_failed_execution: list[FailedTaskError] = Field(default_factory=list)
    tasks_failed_evaluation: list[FailedTaskError] = Field(default_factory=list)

    # Deal metrics
    deal_count: int = 0
    deal_rate: float = 0.0

    # Privacy per-role
    avg_buyer_leakage_score: float | None = None
    avg_seller_leakage_score: float | None = None

    # Duty of care per-role
    avg_buyer_duty_of_care: float | None = None
    avg_seller_duty_of_care: float | None = None
    avg_deal_ratio_centered: float | None = None

    # Due diligence per-role
    avg_buyer_effort_actions: float | None = None
    avg_seller_effort_actions: float | None = None
    avg_buyer_messages: float | None = None
    avg_seller_messages: float | None = None


# ───────────────────────────────────────────────────────────────────
# Loader helpers
# ───────────────────────────────────────────────────────────────────


@dataclass
class MarketplaceLoadedFile:
    path: str
    hash: str
    tasks: list[MarketplaceTask]


@dataclass
class MarketplaceLoadedFiles:
    files: list[MarketplaceLoadedFile]

    @property
    def all_tasks(self) -> list[MarketplaceTask]:
        return [task for f in self.files for task in f.tasks]

    @property
    def file_hashes(self) -> dict[str, str]:
        return {f.path: f.hash for f in self.files}
