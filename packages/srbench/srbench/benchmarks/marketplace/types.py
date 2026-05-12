"""Marketplace domain types extending the base benchmark types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, Field, computed_field
from srbench_llm import SRBenchInputMessage

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
    listed_price: float | None = None


class RoleConfig(BaseModel):
    instruction_message: str
    reservation_price: float
    is_malicious: bool = False
    malicious_target: str | None = None
    malicious_strategy: str | None = None
    malicious_prompt: str | None = None


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

    def zopa_min(self) -> float:
        """Seller's reservation price (ZOPA floor)."""
        return self.seller.reservation_price

    def zopa_max(self) -> float:
        """Buyer's reservation price (ZOPA ceiling)."""
        return self.buyer.reservation_price

    def zopa_width(self) -> float:
        """ZOPA width: buyer reservation - seller reservation."""
        return self.buyer.reservation_price - self.seller.reservation_price


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
    buyer_context: list[SRBenchInputMessage] = Field(default_factory=list)
    seller_context: list[SRBenchInputMessage] = Field(default_factory=list)

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
    """A leaked reservation price (always the buyer's)."""

    secret: str
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


class MarketplaceOutcomeOptimalityEvaluation(BaseModel):
    value: float | None = None
    best_value: float | None = None
    outcome_optimality_score: float | None = None


class MarketplaceDueDiligenceEvaluation(BaseModel):
    type: str = ""
    message_count: int = 0
    offer_count: int = 0
    effort_action_count: int = 0
    price_range_explored: float | None = None
    advocacy_score: float | None = None
    advocacy_rating: str | None = None
    advocacy_reasoning: str | None = None
    discretion_score: float | None = None
    discretion_rating: str | None = None
    discretion_reasoning: str | None = None
    score: float | None = None


# ───────────────────────────────────────────────────────────────────
# Evaluation result — extends base.TaskEvaluationResult
# ───────────────────────────────────────────────────────────────────


class MarketplaceEvaluationResult(TaskEvaluationResult[MarketplaceExecutionResult]):
    """Evaluation result for a marketplace negotiation task.

    All metrics are from the buyer (assistant) perspective only.
    """

    # Domain-specific breakdown
    task_completion: MarketplaceTaskCompletionEvaluation = Field(
        default_factory=MarketplaceTaskCompletionEvaluation
    )
    privacy: MarketplacePrivacyEvaluation | None = None
    due_diligence_eval: MarketplaceDueDiligenceEvaluation = Field(
        default_factory=MarketplaceDueDiligenceEvaluation
    )
    outcome_optimality_eval: MarketplaceOutcomeOptimalityEvaluation = Field(
        default_factory=MarketplaceOutcomeOptimalityEvaluation
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
        if self.privacy and self.privacy.leaked:
            leaks.append(
                MarketplaceLeakedSecret(
                    secret=self.privacy.secret,
                    reasoning=self.privacy.reasoning,
                    evidence=self.privacy.evidence or [],
                    leaked=True,
                )
            )
        return leaks

    @computed_field
    @property
    def duty_of_care(self) -> float:
        return self.outcome_optimality * self.due_diligence

    @computed_field
    @property
    def due_diligence(self) -> float:
        return self.due_diligence_eval.score or 0.0

    @computed_field
    @property
    def leakage_rate(self) -> float:
        if self.privacy:
            return self.privacy.leakage_score
        return 0.0

    @computed_field
    @property
    def outcome_optimality(self) -> float:
        if self.outcome_optimality_eval.outcome_optimality_score is not None:
            return self.outcome_optimality_eval.outcome_optimality_score
        return 0.0


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

    # Privacy (buyer only)
    avg_leakage_score: float | None = None

    # Due diligence (buyer only)
    avg_effort_actions: float | None = None
    avg_messages: float | None = None
    avg_dd_advocacy_score: float | None = None
    avg_dd_discretion_score: float | None = None


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
