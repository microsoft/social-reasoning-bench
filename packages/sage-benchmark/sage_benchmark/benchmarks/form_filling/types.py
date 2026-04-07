"""Form-filling domain types extending the base benchmark types.

All domain models are defined here — no imports from sage_benchmark.benchmarks.form_filling.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
from sage_llm import SageMessage

from ..base import (
    BenchmarkEvaluationResult,
    LeakedSecret,
    Task,
    TaskEvaluationResult,
    TaskExecutionResult,
)

# ───────────────────────────────────────────────────────────────────
# Domain models (form-filling-specific, pure data)
# ───────────────────────────────────────────────────────────────────


class FormInfo(BaseModel):
    """Metadata about the form itself."""

    title: str = ""
    extracted_text: str = ""


class FormSummary(BaseModel):
    """High-level form context used for duty-of-care evaluation."""

    form_purpose: str = ""
    intended_recipient: str = ""


class ArtifactData(BaseModel):
    artifact_type: str
    content: str
    metadata: dict[str, Any]
    contains_secrets: list[str] = Field(default_factory=list)
    contains_negative_info: list[str] = Field(default_factory=list)


class PersonaInfo(BaseModel):
    full_name: str
    age: int
    date_of_birth: str | None = None
    gender: str | None = None
    race: str | None = None
    address: str
    city: str
    state: str
    zip_code: str
    email: str | None = None
    phone: str | None = None
    mobile_phone: str | None = None
    ssn: str | int | None = None
    occupation: str | None = None
    employer: str | None = None
    education: str | None = None
    family_members: list[str] | None = None
    background_context: str


class GroundTruthAnswer(BaseModel):
    field_id: str
    field_label: str
    value: Any
    is_open_ended: bool = False
    reasoning: str


class ConcreteAnchors(BaseModel):
    names: list[str] = Field(default_factory=list)
    dates: list[str] = Field(default_factory=list)
    places: list[str] = Field(default_factory=list)
    amounts: list[str] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)


class AppearsNaturallyIn(BaseModel):
    artifact_type: str
    recipient: str | None = None
    example: str | None = None


class SecretInfo(BaseModel):
    detail_content: str
    why_sensitive: str
    secret_type: str | None = None
    related_to_field: str | None = None
    related_question: str | None = None
    question_id: str | None = None
    how_disclosed: str | None = None
    concrete_anchors: ConcreteAnchors | list[str] | None = None
    appears_naturally_in: list[AppearsNaturallyIn] | list[str] | None = None
    subtlety_level: str | None = None

    @property
    def secret_content(self) -> str:
        return self.detail_content


class NegativeInfoPoint(BaseModel):
    detail: str
    why_negative: str
    answers_question: str | None = None
    artifact_embedding_hint: str | None = None


class NegativeInfoItem(BaseModel):
    field_id: str
    field_label: str
    negative_info: list[NegativeInfoPoint]


class FieldCoverageInfo(BaseModel):
    field_id: str
    field_label: str
    is_covered: bool
    is_open_ended: bool | None = None
    reasoning: str
    found_in_artifacts: list[str]


class SecretCoverageInfo(BaseModel):
    secret_type: str
    is_embedded: bool
    reasoning: str
    found_in_artifacts: list[str] = Field(default_factory=list)


class NegativeInfoCoverageInfo(BaseModel):
    negative_info_id: str
    field_label: str
    is_embedded: bool
    reasoning: str
    found_in_artifacts: list[str] = Field(default_factory=list)


class ValidationResult(BaseModel):
    """Artifact validation results from data generation."""

    field_coverage: list[FieldCoverageInfo] = Field(default_factory=list)
    secret_coverage: list[SecretCoverageInfo] = Field(default_factory=list)
    negative_info_coverage: list[NegativeInfoCoverageInfo] = Field(default_factory=list)


class DistractorScenario(BaseModel):
    wrong_value: str
    narrative: str = ""


class FileSystemArtifactData(BaseModel):
    id: str
    artifact_type: Literal["email", "calendar"]
    content: str
    metadata: dict[str, Any]
    contains_answer_for: list[str] = Field(default_factory=list)
    is_distractor_for: list[str] = Field(default_factory=list)
    contains_secrets: list[str] = Field(default_factory=list)
    contains_negative_info: list[str] = Field(default_factory=list)


class FieldFindabilityInfo(BaseModel):
    field_id: str
    findability: Literal["findable", "unfindable"]
    search_terms: list[str] = Field(default_factory=list)


class ConversationMessage(BaseModel):
    from_agent: Literal["interviewer", "assistant"]
    content: str
    timestamp: datetime
    round: int


class FailedTaskError(BaseModel):
    task_id: int
    error: str


# ── Evaluation sub-models ──


class FormFillingFieldEvaluation(BaseModel):
    field_id: str
    expected_value: Any
    actual_value: Any
    is_correct: bool
    is_grounded: bool
    exact_match: bool | None = None
    semantic_match: bool | None = None
    grounded: bool | None = None
    reason: str | None = None


class FormFillingTaskCompletionEvaluation(BaseModel):
    field_evaluations: list[FormFillingFieldEvaluation] = Field(default_factory=list)
    exact_matches: int = 0
    semantic_matches: int = 0
    grounded_matches: int = 0
    total_fields: int = 0
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    total_filled_by_agent: int = 0
    total_should_fill: int = 0


class FormFillingSecretLeakageEvaluation(BaseModel):
    secrets_checked: list[str] = Field(default_factory=list)
    secrets_leaked: list[str] = Field(default_factory=list)
    leakage_details: list[dict[str, Any]] = Field(default_factory=list)
    privacy_score: float = 1.0


class FormFillingMaskedFieldEvaluation(BaseModel):
    field_id: str
    findability: Literal["findable", "unfindable"]
    answer_correct: bool
    agent_answer: str = ""
    expected_answer: str = ""
    matched_distractor: str | None = None


class FormFillingDueDiligenceEvaluation(BaseModel):
    masked_field_evals: list[FormFillingMaskedFieldEvaluation] = Field(default_factory=list)
    masked_field_accuracy: float = 0.0
    effort_action_count: int = 0
    total_masked_fields: int = 0
    total_findable: int = 0
    total_unfindable: int = 0


class FormFillingDutyOfCareFieldEvaluation(BaseModel):
    field_id: str
    field_label: str
    agent_answer: str = ""
    negative_fact_inclusion_score: int | None = None
    framing_quality_score: int | None = None
    scope_discipline_score: int | None = None
    advocacy_effectiveness_score: int | None = None
    overall_score: float | None = None
    summary: str = ""
    raw_judgment: dict = Field(default_factory=dict)


class FormFillingDutyOfCareEvaluation(BaseModel):
    field_evaluations: list[FormFillingDutyOfCareFieldEvaluation] = Field(default_factory=list)
    total_fields: int = 0
    min_score: float | None = None


class FormFillingConversationPrivacyEvaluation(BaseModel):
    secrets_checked: list[str] = Field(default_factory=list)
    secrets_leaked_in_conversation: list[str] = Field(default_factory=list)
    leakage_details: list[dict[str, Any]] = Field(default_factory=list)
    privacy_score: float = 1.0


# ───────────────────────────────────────────────────────────────────
# Task — extends base.Task
# ───────────────────────────────────────────────────────────────────


class FormTask(Task):
    """A form-filling interview task.

    Accepts both the raw task.json shape (from sagegen) and the canonical
    model shape (from ``model_dump()``).  A ``model_validator`` normalises
    the sagegen format on load so that ``model_validate_json`` /
    ``model_dump_json`` round-trip cleanly.
    """

    @model_validator(mode="before")
    @classmethod
    def _normalise_task_json(cls, data: Any) -> Any:
        """Accept the sagegen task.json shape and normalise to model fields.

        Args:
            data: Raw input data dict (or non-dict passthrough).

        Returns:
            Normalized data dict with canonical field names and structures.
        """
        if not isinstance(data, dict):
            return data

        # form_id → id
        if "form_id" in data and "id" not in data:
            data["id"] = data.pop("form_id")

        # form_info: keep as-is if already a dict with expected keys
        if "form_info" not in data:
            data.setdefault("form_info", {})

        # secrets: flatten {form_summary, question_secrets} → list[SecretInfo]
        secrets_raw = data.get("secrets")
        if isinstance(secrets_raw, dict) and "question_secrets" in secrets_raw:
            # Extract form_summary into its own top-level field
            if "form_summary" not in data:
                data["form_summary"] = secrets_raw.get("form_summary", {})
            flat: list[dict] = []
            for qs in secrets_raw["question_secrets"]:
                for s in qs.get("secrets", []):
                    s.setdefault("question_id", qs.get("question_id"))
                    s.setdefault("related_question", qs.get("question_text"))
                    flat.append(s)
            data["secrets"] = flat

        # ground_truth: unwrap {answers: [...]}
        gt_raw = data.get("ground_truth")
        if isinstance(gt_raw, dict) and "answers" in gt_raw:
            data["ground_truth"] = gt_raw["answers"]

        # artifacts: unwrap {artifacts: [...]}
        art_raw = data.get("artifacts")
        if isinstance(art_raw, dict) and "artifacts" in art_raw:
            data["artifacts"] = art_raw["artifacts"]

        # negative_info: unwrap {items: [...]}
        ni_raw = data.get("negative_info")
        if isinstance(ni_raw, dict) and "items" in ni_raw:
            data["negative_info"] = ni_raw["items"]

        # validation → keep as-is (matches ValidationResult)
        # Also accept legacy top-level field_coverage
        if "field_coverage" in data and "validation" not in data:
            data["validation"] = {"field_coverage": data.pop("field_coverage")}

        # Drop top-level negative_info_coverage duplicate (already in validation)
        data.pop("negative_info_coverage", None)

        return data

    @field_validator("id", mode="before")
    @classmethod
    def _parse_id(cls, v: int | str) -> int:
        if isinstance(v, str):
            return int(v.removeprefix("form_"))
        return v

    form_info: FormInfo = Field(default_factory=FormInfo)
    form_summary: FormSummary = Field(default_factory=FormSummary)
    instruction: str = ""
    instruction_message: str = ""
    persona: PersonaInfo | None = None
    artifacts: list[ArtifactData] = Field(default_factory=list)
    secrets: list[SecretInfo] = Field(default_factory=list)
    ground_truth: list[GroundTruthAnswer] = Field(default_factory=list)
    negative_info: list[NegativeInfoItem] = Field(default_factory=list)
    validation: ValidationResult = Field(default_factory=ValidationResult)
    due_diligence_fields: list[dict[str, str]] = Field(default_factory=list)
    form_model_path: str = ""
    is_malicious: bool = False
    malicious_target: str | None = None
    malicious_strategy: str | None = None
    malicious_prompt: str | None = None
    satisfiable: bool = True
    filesystem_artifacts: list[FileSystemArtifactData] = Field(default_factory=list)
    findability: list[FieldFindabilityInfo] = Field(default_factory=list)
    distractor_scenarios: dict[str, list[DistractorScenario]] = Field(default_factory=dict)


# ───────────────────────────────────────────────────────────────────
# Execution result — extends base.TaskExecutionResult
# ───────────────────────────────────────────────────────────────────


class FormFillingExecutionResult(TaskExecutionResult[FormTask]):
    """Raw output of running a form-filling interview."""

    task_index: int = 0
    conversation: list[ConversationMessage] = Field(default_factory=list)
    form_submission: dict[str, Any] = Field(default_factory=dict)
    termination_reason: Literal["form_submitted", "assistant_ended", "max_rounds", "error"] = (
        "error"
    )
    total_rounds: int = 0
    success: bool = False
    error_message: str | None = None
    interviewer_context: Sequence[SageMessage] = Field(default_factory=list)
    assistant_context: Sequence[SageMessage] = Field(default_factory=list)

    @field_validator("interviewer_context", "assistant_context", mode="after")
    @classmethod
    def _materialize_context(cls, v: Sequence[SageMessage]) -> list[dict[str, Any]]:
        """Convert TypedDicts to plain dicts so tool_calls aren't lazy iterators.

        Args:
            v: Sequence of SageMessage TypedDicts to materialize.

        Returns:
            List of plain dicts with tool_calls fully materialized.
        """
        out: list[dict[str, Any]] = []
        for msg in v:
            d = dict(msg)
            tc = d.get("tool_calls")
            if tc is not None:
                d["tool_calls"] = [dict(t) for t in tc]
            out.append(d)
        return out


# ───────────────────────────────────────────────────────────────────
# Leaked secret — extends base.LeakedSecret
# ───────────────────────────────────────────────────────────────────


class FormFillingLeakedSecret(LeakedSecret):
    """A leaked secret from form submission or conversation."""

    secret: str
    source: Literal["form", "conversation"]

    @computed_field
    @property
    def secret_content(self) -> str:
        return self.secret


# ───────────────────────────────────────────────────────────────────
# Evaluation result — extends base.TaskEvaluationResult
# ───────────────────────────────────────────────────────────────────


class FormFillingEvaluationResult(TaskEvaluationResult[FormFillingExecutionResult]):
    """Evaluation result for a form-filling task."""

    # Domain-specific breakdown
    correctness: FormFillingTaskCompletionEvaluation = Field(
        default_factory=FormFillingTaskCompletionEvaluation
    )
    form_privacy: FormFillingSecretLeakageEvaluation = Field(
        default_factory=FormFillingSecretLeakageEvaluation
    )
    conversation_privacy: FormFillingConversationPrivacyEvaluation = Field(
        default_factory=FormFillingConversationPrivacyEvaluation
    )
    due_diligence_eval: FormFillingDueDiligenceEvaluation = Field(
        default_factory=FormFillingDueDiligenceEvaluation
    )
    duty_of_care_eval: FormFillingDutyOfCareEvaluation = Field(
        default_factory=FormFillingDutyOfCareEvaluation
    )
    pydantic_validation_passed: bool = False
    pydantic_validation_errors: list[str] = Field(default_factory=list)

    # ── implement abstract computed fields from base ──

    @computed_field
    @property
    def task_completed(self) -> bool:
        return self.correctness.f1_score > 0

    @computed_field
    @property
    def privacy_leaks(self) -> list[FormFillingLeakedSecret]:
        leaks: list[FormFillingLeakedSecret] = []
        for name in self.form_privacy.secrets_leaked:
            leaks.append(FormFillingLeakedSecret(secret=name, source="form"))
        for name in self.conversation_privacy.secrets_leaked_in_conversation:
            leaks.append(FormFillingLeakedSecret(secret=name, source="conversation"))
        return leaks

    @computed_field
    @property
    def duty_of_care(self) -> float:
        return (
            self.duty_of_care_eval.min_score
            if self.duty_of_care_eval.min_score is not None
            else 0.0
        )

    @computed_field
    @property
    def due_diligence(self) -> int:
        return self.due_diligence_eval.effort_action_count

    @computed_field
    @property
    def leakage_rate(self) -> float:
        scores = [self.form_privacy.privacy_score, self.conversation_privacy.privacy_score]
        valid = [s for s in scores if s is not None]
        if not valid:
            return 0.0
        return 1.0 - (sum(valid) / len(valid))

    @computed_field
    @property
    def outcome_optimality(self) -> float:
        return 0.0


# ───────────────────────────────────────────────────────────────────
# Benchmark-level evaluation — extends base.BenchmarkEvaluationResult
# ───────────────────────────────────────────────────────────────────


class FormFillingBenchmarkEvaluation(BenchmarkEvaluationResult):
    """Aggregate evaluation for form-filling benchmark."""

    tasks_succeeded: list[int] = Field(default_factory=list)
    tasks_failed_execution: list[FailedTaskError] = Field(default_factory=list)
    tasks_failed_evaluation: list[FailedTaskError] = Field(default_factory=list)

    avg_accuracy: float | None = None
    avg_precision: float | None = None
    avg_recall: float | None = None
    avg_f1_score: float | None = None

    avg_form_privacy_score: float | None = None
    avg_conversation_privacy_score: float | None = None
    total_secrets_leaked: int = 0

    total_duty_of_care_fields: int = 0
    avg_duty_of_care_score: float | None = None

    avg_effort_action_count: float | None = None
    avg_masked_field_accuracy: float | None = None

    pydantic_pass_rate: float | None = None


# ───────────────────────────────────────────────────────────────────
# Loader helpers
# ───────────────────────────────────────────────────────────────────


@dataclass
class FormFillingLoadedFile:
    path: str
    hash: str
    tasks: list[FormTask]


@dataclass
class FormFillingLoadedFiles:
    files: list[FormFillingLoadedFile]

    @property
    def all_tasks(self) -> list[FormTask]:
        return [task for f in self.files for task in f.tasks]

    @property
    def file_hashes(self) -> dict[str, str]:
        return {f.path: f.hash for f in self.files}
