"""Schemas for form filling tasks and evaluation."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_serializer

from sage_benchmark.shared.schemas import ChatMessage

# --- Task Data Schemas ---


class ArtifactData(BaseModel):
    """A digital artifact (email, note, calendar entry)."""

    artifact_type: str = Field(description="Type of artifact (email, note, calendar, text)")
    content: str = Field(description="The actual artifact content")
    metadata: dict[str, Any] = Field(description="Type-specific metadata (sender, date, etc.)")
    contains_secrets: list[str] = Field(description="Which secrets are embedded in this artifact")


class PersonaInfo(BaseModel):
    """Complete persona information."""

    full_name: str
    age: int
    gender: str | None = None
    race: str | None = None
    address: str
    city: str
    state: str
    zip_code: str
    email: str
    phone: str
    ssn: str | None = None
    occupation: str | None = None
    employer: str | None = None
    education: str | None = None
    family_members: list[str] | None = None
    background_context: str = Field(
        description="Rich narrative about the person's life and background"
    )


class GroundTruthAnswer(BaseModel):
    """Expected answer for a single form field."""

    field_id: str = Field(description="Flattened field path (e.g., 'participant_details.name')")
    field_label: str = Field(description="Human-readable field label")
    value: Any = Field(description="Expected correct value")
    reasoning: str = Field(description="Why this value is correct")


class SecretInfo(BaseModel):
    """Rich secret format for privacy evaluation."""

    secret_type: str = Field(description="Category: medical, financial, family, work, etc.")
    secret_content: str = Field(description="The actual sensitive content")
    why_sensitive: str = Field(description="Why this is sensitive (harm if disclosed)")
    related_to_field: str | None = Field(
        default=None, description="Form field that might trigger disclosure"
    )
    how_disclosed: str | None = Field(default=None, description="How the person might reveal it")


class FieldCoverageInfo(BaseModel):
    """Metadata about which artifacts cover each field."""

    field_id: str = Field(description="Field identifier")
    field_label: str = Field(description="Human-readable label")
    is_covered: bool = Field(description="Is this field's info in artifacts?")
    reasoning: str = Field(description="Explanation of coverage")
    found_in_artifacts: list[str] = Field(description="Which artifact types contain this info")


class FormTask(BaseModel):
    """Complete task data loaded from directory."""

    model_config = {"arbitrary_types_allowed": True}

    form_id: int
    form_title: str
    instruction: str
    persona: PersonaInfo
    artifacts: list[ArtifactData]
    secrets: list[SecretInfo] = Field(description="Secrets that should NOT appear in responses")
    ground_truth: list[GroundTruthAnswer]
    field_coverage: list[FieldCoverageInfo] = Field(
        default_factory=list, description="Metadata about which artifacts cover each field"
    )
    form_model_path: str = Field(description="Path to form_model.py file")
    form_class: type[BaseModel] = Field(description="Dynamically loaded pydantic form class")

    @field_serializer("form_class")
    def serialize_form_class(self, form_class: type[BaseModel]) -> str:
        return form_class.__name__


# --- Execution Schemas ---


class FormFillingAction(BaseModel):
    """The action taken by the model."""

    action_type: Literal["fill", "reject"]
    fill_responses: dict[str, Any] | None = None
    reject_reason: str | None = None


class LLMCallLog(BaseModel):
    """Log entry for a single LLM call attempt."""

    timestamp: datetime
    attempt_number: int
    messages: list[ChatMessage]
    raw_response: str | None
    parsed_action: FormFillingAction | None
    error: str | None = None


class TaskExecutionResult(BaseModel):
    """Result of executing a single task."""

    task_index: int
    task: FormTask
    action: FormFillingAction | None
    llm_calls: list[LLMCallLog]
    success: bool
    error_message: str | None = None


# --- Evaluation Schemas ---


class FieldEvaluation(BaseModel):
    """Evaluation of a single form field."""

    field_id: str
    expected_value: Any
    actual_value: Any
    is_correct: bool
    is_grounded: bool
    reason: str | None = None


class CorrectnessEvaluation(BaseModel):
    """Overall correctness evaluation against ground truth."""

    field_evaluations: list[FieldEvaluation]
    exact_matches: int
    total_fields: int
    accuracy: float = Field(description="(exact_matches + semantic_matches) / total_fields")
    precision: float = Field(description="correct_filled / total_filled_by_agent")
    recall: float = Field(description="correct_filled / should_be_filled (based on field_coverage)")
    total_filled_by_agent: int = Field(description="How many fields did agent fill")
    total_should_fill: int = Field(description="How many fields had info in artifacts")


class SecretLeakageEvaluation(BaseModel):
    """Evaluation of secret leakage/privacy."""

    secrets_checked: list[str]
    secrets_leaked: list[str]
    leakage_details: list[dict[str, Any]] = Field(
        default_factory=list, description="Details about which secrets leaked where"
    )
    privacy_score: float = Field(description="1.0 = perfect privacy, 0.0 = all leaked")


class FormTaskEvaluationResult(BaseModel):
    """Complete evaluation result for a form task."""

    task_index: int
    task: FormTask
    correctness: CorrectnessEvaluation
    privacy: SecretLeakageEvaluation
    pydantic_validation_passed: bool
    pydantic_validation_errors: list[str] = Field(default_factory=list)
