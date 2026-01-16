"""Schemas for interviewer benchmark tasks and evaluation."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from sage_benchmark.form_filling.schemas import CorrectnessEvaluation, SecretLeakageEvaluation
from sage_benchmark.shared.schemas import ChatMessage

# --- Task Data Schemas ---


class Fact(BaseModel):
    """A fact about the assistant's persona."""

    id: str = Field(description="Unique identifier for this fact")
    value: str = Field(description="The actual fact content")
    sensitivity: Literal["low", "medium", "high"] = Field(description="Sensitivity level")


class AssistantInfo(BaseModel):
    """Information available to the assistant agent."""

    persona: str = Field(description="Brief description of who the assistant represents")
    facts: list[Fact] = Field(description="All facts (including secrets) about the person")


class FormQuestion(BaseModel):
    """A question in the form the interviewer needs to fill."""

    question: str = Field(description="The question text")
    type: Literal["short", "long"] = Field(description="Expected answer length")
    expected_facts: list[str] = Field(
        default_factory=list, description="Fact IDs that should appear in the answer"
    )
    disallowed_facts: list[str] = Field(
        default_factory=list, description="Fact IDs that should NOT appear in the answer (secrets)"
    )


class FormInfo(BaseModel):
    """The form the interviewer is trying to fill."""

    title: str = Field(description="Form title/name")
    questions: list[FormQuestion] = Field(description="List of questions to answer")


class InterviewTask(BaseModel):
    """Complete task data for one interview scenario."""

    id: int = Field(description="Task ID")
    assistant: AssistantInfo = Field(description="Info for assistant agent")
    form: FormInfo = Field(description="Form for interviewer to fill")


class QuestionResponse(BaseModel):
    """Response to a single form question."""

    index: int = Field(description="Question number (0-indexed)")
    question: str = Field(description="The question text for reference")
    answer: str = Field(description="Your answer to this question")


class FormSubmission(BaseModel):
    """Parameters for SubmitForm tool - filled form answers."""

    responses: list[QuestionResponse] = Field(
        description="List of responses, one for each form question. Must include all questions you can answer."
    )


# --- Execution Schemas ---


class ConversationMessage(BaseModel):
    """A message exchanged during the interview."""

    from_agent: Literal["interviewer", "assistant"] = Field(description="Who sent the message")
    content: str = Field(description="Message content")
    timestamp: datetime = Field(description="When the message was sent")
    round: int = Field(description="Conversation round number")


class TaskExecutionResult(BaseModel):
    """Result of executing a single interview task."""

    model_config = {"arbitrary_types_allowed": True}

    task_index: int
    task_format: Literal["yaml", "form_filling"]

    # For backward compatibility with YAML tasks
    task: InterviewTask | None = None

    # For unified interface (use Any to avoid circular import with task_interface)
    # Exclude from serialization since it's not JSON serializable
    task_adapter: Any = Field(default=None, exclude=True)

    conversation: list[ConversationMessage] = Field(description="Full conversation transcript")
    form_submission: dict[str, Any] = Field(
        description="Dict that can be parsed to FormSubmission if coming from yaml or a filled in BaseModel for forms"
    )
    termination_reason: Literal["interviewer_ended", "assistant_ended", "max_rounds", "error"] = (
        Field(description="How/why the conversation ended")
    )
    total_rounds: int = Field(description="Number of conversation rounds")
    success: bool = Field(description="Whether execution completed successfully")
    error_message: str | None = None
    interviewer_context: list[ChatMessage] = Field(
        default_factory=list, description="Interviewer agent's message history"
    )
    assistant_context: list[ChatMessage] = Field(
        default_factory=list, description="Assistant agent's message history"
    )


# --- Evaluation Schemas ---


class QuestionEvaluation(BaseModel):
    """Evaluation of a single form question's answer."""

    question_index: int
    question_text: str
    expected_facts: list[str] = Field(description="Fact IDs that should be present")
    disallowed_facts: list[str] = Field(description="Fact IDs that should NOT be present")
    interviewer_answer: str
    contains_expected: list[str] = Field(description="Which expected facts were found")
    contains_disallowed: list[str] = Field(description="Which disallowed facts were leaked")
    is_correct: bool = Field(
        description="Whether answer contains expected facts and excludes disallowed"
    )
    reasoning: str = Field(description="Judge's reasoning")


class TaskCompletionEvaluation(BaseModel):
    """Overall task completion evaluation."""

    question_evaluations: list[QuestionEvaluation]
    total_questions: int
    correct_answers: int = Field(
        description="Questions with expected facts and no disallowed facts"
    )
    completion_score: float = Field(description="correct_answers / total_questions")


class ConversationPrivacyEvaluation(BaseModel):
    """Privacy evaluation based on conversation analysis (Version 1)."""

    secrets_checked: list[str] = Field(description="All disallowed facts checked")
    secrets_leaked_in_conversation: list[str] = Field(
        description="Disallowed facts found in conversation"
    )
    leakage_details: list[dict[str, Any]] = Field(
        default_factory=list, description="Details about where/how secrets leaked"
    )
    privacy_score: float = Field(description="1.0 - (leaked / total_secrets)")


class TaskEvaluationResult(BaseModel):
    """Complete evaluation result for an interview task.

    Supports both YAML and form_filling task formats.
    """

    task_format: Literal["yaml", "form_filling"]
    task_index: int
    conversation_privacy: ConversationPrivacyEvaluation = Field(
        description="Privacy evaluation of the conversation"
    )

    # YAML-specific fields (optional)
    task: InterviewTask | None = None
    task_completion: TaskCompletionEvaluation | None = None

    # form_filling-specific fields (optional)
    correctness: CorrectnessEvaluation | None = None
    form_privacy: SecretLeakageEvaluation | None = None
    pydantic_validation_passed: bool | None = None
    pydantic_validation_errors: list[str] = Field(default_factory=list)
