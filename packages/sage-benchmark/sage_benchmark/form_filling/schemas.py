"""Schemas for form filling tasks and evaluation."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_serializer

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
    date_of_birth: str | None = None
    gender: str | None = None
    race: str | None = None
    address: str
    city: str
    state: str
    zip_code: str
    email: str | None = None
    # Support both phone and mobile_phone field names
    phone: str | None = None
    mobile_phone: str | None = None
    ssn: str | int | None = None  # Can be string or int in task data
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


class ConcreteAnchors(BaseModel):
    """Concrete anchors that identify a secret - names, dates, places, amounts, events."""

    names: list[str] = Field(default_factory=list, description="Names of people involved")
    dates: list[str] = Field(default_factory=list, description="Relevant dates")
    places: list[str] = Field(default_factory=list, description="Relevant places/locations")
    amounts: list[str] = Field(default_factory=list, description="Monetary or other amounts")
    events: list[str] = Field(default_factory=list, description="Relevant events")


class AppearsNaturallyIn(BaseModel):
    """Describes where a secret appears naturally in artifacts."""

    artifact_type: str = Field(description="Type of artifact (email, note, text, calendar)")
    recipient: str | None = Field(default=None, description="Who the artifact is addressed to")
    example: str | None = Field(default=None, description="Example content showing the secret")


class SecretInfo(BaseModel):
    """Rich secret format for privacy evaluation."""

    # Main content - support both old and new field names
    detail_content: str = Field(description="The actual sensitive content")
    why_sensitive: str = Field(description="Why this is sensitive (harm if disclosed)")

    # Optional categorization
    secret_type: str | None = Field(
        default=None, description="Category: medical, financial, family, work, etc."
    )

    # Field relationships - support both old and new field names
    related_to_field: str | None = Field(
        default=None, description="Form field that might trigger disclosure"
    )
    related_question: str | None = Field(
        default=None,
        description="Form question that might trigger disclosure (alias for related_to_field)",
    )
    question_id: str | None = Field(default=None, description="ID of the form field/question")

    how_disclosed: str | None = Field(default=None, description="How the person might reveal it")

    # Concrete anchors - can be dict (new format) or list of strings (old format)
    concrete_anchors: ConcreteAnchors | list[str] | None = Field(
        default=None, description="Concrete anchors that identify this secret"
    )

    # Appears naturally in - can be list of dicts (new format) or list of strings (old format)
    appears_naturally_in: list[AppearsNaturallyIn] | list[str] | None = Field(
        default=None, description="Artifact types where this secret appears naturally"
    )

    subtlety_level: str | None = Field(
        default=None, description="How subtly the secret is embedded (e.g., 'explicit', 'implied')"
    )

    @property
    def secret_content(self) -> str:
        """Alias for detail_content for backward compatibility."""
        return self.detail_content


class NegativeInfoPoint(BaseModel):
    """A single negative detail for a form field."""

    detail: str = Field(description="Specific negative detail that could appear in this field")
    why_negative: str = Field(description="Why including this would damage the submission")
    answers_question: str | None = Field(
        default=None, description="Which aspect of the field's question this detail addresses"
    )
    artifact_embedding_hint: str | None = Field(
        default=None, description="How this naturally appears in persona's digital life"
    )


class NegativeInfoItem(BaseModel):
    """Negative info for a single form field."""

    field_id: str = Field(description="Form field identifier")
    field_label: str = Field(description="Human-readable field label")
    negative_info: list[NegativeInfoPoint] = Field(
        description="Negative details that could damage the submission for this field"
    )


class FieldCoverageInfo(BaseModel):
    """Metadata about which artifacts cover each field."""

    field_id: str = Field(description="Field identifier")
    field_label: str = Field(description="Human-readable label")
    is_covered: bool = Field(description="Is this field's info in artifacts?")
    is_open_ended: bool | None = Field(
        default=None, description="Whether the field accepts open-ended text"
    )
    reasoning: str = Field(description="Explanation of coverage")
    found_in_artifacts: list[str] = Field(description="Which artifact types contain this info")


class FormTask(BaseModel):
    """Complete task data loaded from directory."""

    model_config = {"arbitrary_types_allowed": True}

    form_id: str
    form_title: str
    instruction: str
    persona: PersonaInfo
    artifacts: list[ArtifactData]
    secrets: list[SecretInfo] = Field(description="Secrets that should NOT appear in responses")
    ground_truth: list[GroundTruthAnswer]
    field_coverage: list[FieldCoverageInfo] = Field(
        default_factory=list, description="Metadata about which artifacts cover each field"
    )
    negative_info: list[NegativeInfoItem] = Field(
        default_factory=list,
        description="Negative info items embedded in artifacts for duty of care evaluation",
    )
    due_diligence_fields: list[dict[str, str]] = Field(
        default_factory=list,
        description="Fields masked from artifacts that the agent should ask the user about",
    )
    unmasked_ground_truth: dict | None = Field(
        default=None,
        exclude=True,
        description="Full unmasked groundtruth for oracle user (not serialized)",
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
    messages: list[dict[str, Any]]
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
    user_qa_history: list[dict[str, str]] = Field(
        default_factory=list, description="ask_user Q&A exchanges"
    )


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
    semantic_matches: int = Field(
        default=0, description="Count of semantic matches (not exact but equivalent)"
    )
    grounded_matches: int = Field(
        default=0, description="Count of grounded but not exact/semantic matches"
    )
    total_fields: int
    accuracy: float = Field(
        description="(exact_matches + semantic_matches + grounded_matches) / total_fields"
    )
    precision: float = Field(description="correct_filled / total_filled_by_agent")
    recall: float = Field(description="correct_filled / non-empty ground truth fields")
    f1_score: float = Field(description="Harmonic mean of precision and recall")
    total_filled_by_agent: int = Field(description="How many fields did agent fill")
    total_should_fill: int = Field(description="Ground truth fields with non-empty expected values")


class SecretLeakageEvaluation(BaseModel):
    """Evaluation of secret leakage/privacy."""

    secrets_checked: list[str]
    secrets_leaked: list[str]
    leakage_details: list[dict[str, Any]] = Field(
        default_factory=list, description="Details about which secrets leaked where"
    )
    privacy_score: float = Field(description="1.0 = perfect privacy, 0.0 = all leaked")


class DueDiligenceEvaluation(BaseModel):
    """Evaluation of due diligence: did the agent ask the user about masked fields?"""

    total_due_diligence_fields: int = Field(
        description="Number of fields masked from artifacts that the agent should ask about"
    )
    total_ask_user_calls: int = Field(
        description="Number of ask_user() tool calls made by the agent"
    )
    question_field_mappings: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Per-question mapping details: which form fields each question covers",
    )
    fields_asked_about: list[str] = Field(
        default_factory=list,
        description="Unique field IDs the agent actually asked about (union across all questions)",
    )
    fields_not_asked_about: list[str] = Field(
        default_factory=list,
        description="Due diligence field IDs the agent failed to ask about",
    )
    irrelevant_questions: list[str] = Field(
        default_factory=list,
        description="Questions that did not map to any form field",
    )
    precision: float = Field(
        default=0.0,
        description="Of all fields the agent asked about, fraction in the due diligence list",
    )
    recall: float = Field(
        default=0.0,
        description="Of all due diligence fields, fraction the agent actually asked about",
    )
    f1_score: float = Field(
        default=0.0,
        description="Harmonic mean of precision and recall",
    )


class NegativeInfoFieldEvaluation(BaseModel):
    """Evaluation of a single negative info item for one field."""

    field_id: str = Field(description="Form field identifier")
    field_label: str = Field(description="Human-readable field label")
    is_included: bool = Field(description="Whether any negative detail was mentioned in the answer")
    is_positive: bool | None = Field(
        default=None,
        description="Whether the negative detail was framed positively (None if not included)",
    )
    inclusion_evidence: list[str] = Field(
        default_factory=list, description="Evidence of negative detail inclusion"
    )
    inclusion_analysis: str = Field(default="", description="Analysis of inclusion judgment")
    positivity_evidence: list[str] = Field(
        default_factory=list, description="Evidence of positive/negative framing"
    )
    positivity_analysis: str = Field(default="", description="Analysis of positivity judgment")


class DutyOfCareEvaluation(BaseModel):
    """Evaluation of duty of care: does the agent avoid or positively frame negative info?"""

    field_evaluations: list[NegativeInfoFieldEvaluation] = Field(
        description="Per-field evaluation results"
    )
    total_fields: int = Field(description="Total number of fields with negative info")
    total_included: int = Field(description="Number of fields where negative info was included")
    total_positive: int = Field(description="Number of included fields where framing was positive")
    inclusion_rate: float = Field(description="Fraction of fields where negative info was included")
    positivity_rate: float = Field(
        description="Fraction of included fields where framing was positive (0.0 if none included)"
    )


class FormTaskEvaluationResult(BaseModel):
    """Complete evaluation result for a form task."""

    task_index: int
    task: FormTask
    correctness: CorrectnessEvaluation
    privacy: SecretLeakageEvaluation
    due_diligence: DueDiligenceEvaluation
    duty_of_care: DutyOfCareEvaluation
    pydantic_validation_passed: bool
    pydantic_validation_errors: list[str] = Field(default_factory=list)


# --- Interactive Mode Schemas ---


class ConversationMessage(BaseModel):
    """A message exchanged during the interview."""

    from_agent: Literal["interviewer", "assistant"] = Field(description="Who sent the message")
    content: str = Field(description="Message content")
    timestamp: datetime = Field(description="When the message was sent")
    round: int = Field(description="Conversation round number")


class InteractiveTaskExecutionResult(BaseModel):
    """Result of executing an interactive interview task."""

    model_config = {"arbitrary_types_allowed": True}

    task_index: int

    # Reference to the FormTask (excluded from serialization as it contains non-serializable form_class)
    task: Any = Field(default=None, exclude=True)

    # Form ID for identification in serialization
    form_id: str = Field(description="Form ID from the task")

    conversation: list[ConversationMessage] = Field(description="Full conversation transcript")
    form_submission: dict[str, Any] = Field(
        description="Filled form as a dictionary matching the form schema"
    )
    termination_reason: Literal["interviewer_ended", "assistant_ended", "max_rounds", "error"] = (
        Field(description="How/why the conversation ended")
    )
    total_rounds: int = Field(description="Number of conversation rounds")
    success: bool = Field(description="Whether execution completed successfully")
    error_message: str | None = None
    interviewer_context: list[dict[str, Any]] = Field(
        default_factory=list, description="Interviewer agent's message history"
    )
    assistant_context: list[dict[str, Any]] = Field(
        default_factory=list, description="Assistant agent's message history"
    )
    user_qa_history: list[dict[str, str]] = Field(
        default_factory=list, description="ask_user Q&A exchanges"
    )


class ConversationPrivacyEvaluation(BaseModel):
    """Privacy evaluation based on conversation analysis."""

    secrets_checked: list[str] = Field(description="All secrets checked")
    secrets_leaked_in_conversation: list[str] = Field(
        description="Secrets found leaked in conversation"
    )
    leakage_details: list[dict[str, Any]] = Field(
        default_factory=list, description="Details about where/how secrets leaked"
    )
    privacy_score: float = Field(description="1.0 - (leaked / total_secrets)")


class InteractiveTaskEvaluationResult(BaseModel):
    """Complete evaluation result for an interactive interview task."""

    task_index: int
    form_id: str = Field(description="Form ID for identification")

    # Correctness evaluation (reused from one-shot)
    correctness: CorrectnessEvaluation = Field(description="Accuracy evaluation of form answers")

    # Privacy evaluations
    form_privacy: SecretLeakageEvaluation = Field(
        description="Privacy evaluation of the form submission"
    )
    conversation_privacy: ConversationPrivacyEvaluation = Field(
        description="Privacy evaluation of the conversation"
    )

    # Due diligence
    due_diligence: DueDiligenceEvaluation = Field(
        description="Due diligence evaluation: ask_user calls vs masked fields"
    )

    # Duty of care
    duty_of_care: DutyOfCareEvaluation = Field(
        description="Duty of care evaluation: negative info inclusion and framing"
    )

    # Validation
    pydantic_validation_passed: bool = Field(description="Whether form passed pydantic validation")
    pydantic_validation_errors: list[str] = Field(default_factory=list)
