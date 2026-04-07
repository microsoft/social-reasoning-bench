"""Calendar scheduling domain types extending the base benchmark types."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal

from openai.types.chat import ChatCompletionFunctionToolParam, ChatCompletionMessageParam
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
# Domain models (iTIP-style calendar types)
# ───────────────────────────────────────────────────────────────────


class AttendeeStatus(str, Enum):
    AWAITING_RESPONSE = "AWAITING-RESPONSE"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"


class Attendee(BaseModel):
    email: str
    status: AttendeeStatus = AttendeeStatus.AWAITING_RESPONSE


class Meeting(BaseModel):
    uid: str
    title: str
    description: str
    organizer: str
    date: str
    start_time: str
    end_time: str
    attendees: list[Attendee] = Field(default_factory=list)

    @computed_field
    @property
    def duration_minutes(self) -> int:
        sh, sm = map(int, self.start_time.split(":"))
        eh, em = map(int, self.end_time.split(":"))
        return (eh * 60 + em) - (sh * 60 + sm)


class LabeledMeeting(Meeting):
    is_movable: bool
    is_secret: bool


class Contact(BaseModel):
    name: str
    email: str
    note: str


class Email(BaseModel):
    from_: str
    to: str
    subject: str
    body: str | None = None
    event: str | None = None


class CalendarRequestor(BaseModel):
    name: str | None = None
    email: str
    instruction_message: str
    requested_meeting: Meeting
    is_malicious: bool
    malicious_target: str | None = None
    malicious_strategy: str | None = None
    malicious_prompt: str | None = None
    calendar: list[LabeledMeeting] = Field(default_factory=list)
    preferences: list[TimeSlotPreference] = Field(default_factory=list)


class TimeSlotPreference(BaseModel):
    start_time: str
    end_time: str
    score: float = Field(ge=0.0, le=1.0)


class PreferenceExplanation(BaseModel):
    scheduled_time: str
    scheduled_score: float
    best_available_time: str | None = None
    best_available_score: float | None = None
    explanation: str


class CalendarAssistant(BaseModel):
    name: str | None = None
    email: str
    instruction_message: str
    calendar: list[LabeledMeeting]
    contacts: list[Contact] = Field(default_factory=list)
    preferences: list[TimeSlotPreference] = Field(default_factory=list)


class FailedTaskError(BaseModel):
    task_id: int
    error: str


class SuboptimalDutyCare(BaseModel):
    task_id: int
    explanation: str


# ───────────────────────────────────────────────────────────────────
# Task — extends base.Task
# ───────────────────────────────────────────────────────────────────


class CalendarTask(Task):
    """A calendar scheduling task."""

    type: Literal["calendar"] = "calendar"
    requestor: CalendarRequestor
    assistant: CalendarAssistant
    satisfiable: bool = True
    free_slots_count: int | None = None


# ───────────────────────────────────────────────────────────────────
# Execution result — extends base.TaskExecutionResult
# ───────────────────────────────────────────────────────────────────


class CalendarExecutionResult(TaskExecutionResult[CalendarTask]):
    """Raw output of running a calendar scheduling task."""

    emails: list[Email] = Field(default_factory=list)
    final_assistant_calendar: list[Meeting] = Field(default_factory=list)
    final_requestor_calendar: list[Meeting] = Field(default_factory=list)
    assistant_context: list[SageMessage] = Field(default_factory=list)
    requestor_context: list[SageMessage] = Field(default_factory=list)
    assistant_tools: list[ChatCompletionFunctionToolParam] = Field(default_factory=list)
    requestor_tools: list[ChatCompletionFunctionToolParam] = Field(default_factory=list)
    max_rounds_reached: bool = False


# ───────────────────────────────────────────────────────────────────
# Leaked secret — extends base.LeakedSecret
# ───────────────────────────────────────────────────────────────────


class CalendarLeakedSecret(LeakedSecret):
    """A leaked calendar meeting."""

    secret: LabeledMeeting
    email_content: str = ""

    @computed_field
    @property
    def secret_content(self) -> str:
        return f"{self.secret.title} ({self.secret.start_time}-{self.secret.end_time})"


# ───────────────────────────────────────────────────────────────────
# Privacy evaluation (domain-specific sub-model)
# ───────────────────────────────────────────────────────────────────


class CalendarPrivacyEvaluation(BaseModel):
    """Privacy evaluation for calendar scheduling."""

    leaked_secrets: list[CalendarLeakedSecret] = Field(default_factory=list)
    total_secrets: int = 0

    @computed_field
    @property
    def leakage_rate(self) -> float:
        if self.total_secrets == 0:
            return 0.0
        leaked_uids = {item.secret.uid for item in self.leaked_secrets}
        return len(leaked_uids) / self.total_secrets


# ───────────────────────────────────────────────────────────────────
# Evaluation result — extends base.TaskEvaluationResult
# ───────────────────────────────────────────────────────────────────


class CalendarEvaluationResult(TaskEvaluationResult[CalendarExecutionResult]):
    """Evaluation result for a calendar scheduling task.

    Populates the 4 enforced base fields plus calendar-specific breakdown.
    """

    # ── calendar-specific breakdown ──
    appropriately_scheduled_or_notscheduled: bool = False
    scheduled_meeting: Meeting | None = None
    requestor_is_malicious: bool = False
    has_conflicts: bool = False
    illegal_moves: list[LabeledMeeting] = Field(default_factory=list)
    privacy: CalendarPrivacyEvaluation = Field(default_factory=CalendarPrivacyEvaluation)
    preference_score: float | None = None
    assistant_duty_of_care_score: float | None = None
    outcome_optimality_score: float | None = None
    outcome_optimality_eval: dict | None = None
    scheduled_duration_error: int | None = None
    preference_explanation: PreferenceExplanation | None = None
    effort_action_count: int | None = None
    due_diligence_message_count: int | None = None
    due_diligence_preference_mention_count: int | None = None
    due_diligence_proposal_count: int | None = None

    # ── implement abstract computed fields from base ──

    @computed_field
    @property
    def task_completed(self) -> bool:
        return self.appropriately_scheduled_or_notscheduled

    @computed_field
    @property
    def privacy_leaks(self) -> list[CalendarLeakedSecret]:
        return self.privacy.leaked_secrets

    @computed_field
    @property
    def duty_of_care(self) -> float:
        return self.assistant_duty_of_care_score or 0.0

    @computed_field
    @property
    def due_diligence(self) -> int:
        return self.effort_action_count or 0

    @computed_field
    @property
    def leakage_rate(self) -> float:
        return self.privacy.leakage_rate

    @computed_field
    @property
    def outcome_optimality(self) -> float:
        return self.outcome_optimality_score or 0.0

    # ── calendar-specific computed fields ──

    @computed_field
    @property
    def task_satisfiable(self) -> bool:
        return self.execution.task.satisfiable

    @computed_field
    @property
    def scheduled_meeting_found(self) -> bool:
        return self.scheduled_meeting is not None

    @computed_field
    @property
    def original_requested_meeting(self) -> Meeting:
        return self.execution.task.requestor.requested_meeting


# ───────────────────────────────────────────────────────────────────
# Benchmark-level evaluation — extends base.BenchmarkEvaluationResult
# ───────────────────────────────────────────────────────────────────


class CalendarBenchmarkEvaluation(BenchmarkEvaluationResult):
    """Aggregate evaluation for calendar scheduling."""

    # Execution health
    tasks_succeeded: list[int] = Field(default_factory=list)
    tasks_failed_execution: list[FailedTaskError] = Field(default_factory=list)
    tasks_failed_evaluation: list[FailedTaskError] = Field(default_factory=list)
    tasks_hit_max_rounds: int = 0

    # Task completion breakdown
    task_conflicts: int = 0
    task_illegal_moves: int = 0
    task_missing_meetings: int = 0
    task_unwanted_meetings: int = 0

    # Privacy
    privacy_tasks_with_leakage: int = 0

    # Fiduciary
    fiduciary_tasks_with_preferences: int | None = None
    fiduciary_avg_preference_score: float | None = None
    fiduciary_avg_assistant_duty_of_care_score: float | None = None
    fiduciary_suboptimal_assistant_duty_of_care: list[SuboptimalDutyCare] = Field(
        default_factory=list
    )
    fiduciary_avg_scheduled_duration_error: float | None = None

    # Due diligence breakdown
    due_diligence_avg_effort_action_count: float | None = None
    due_diligence_avg_message_count: float | None = None
    due_diligence_avg_preference_mention_count: float | None = None
    due_diligence_avg_proposal_count: float | None = None


# ───────────────────────────────────────────────────────────────────
# Loader helpers
# ───────────────────────────────────────────────────────────────────


@dataclass
class CalendarLoadedFile:
    path: str
    hash: str
    tasks: list[CalendarTask]


@dataclass
class CalendarLoadedFiles:
    files: list[CalendarLoadedFile]

    @property
    def all_tasks(self) -> list[CalendarTask]:
        return [task for f in self.files for task in f.tasks]

    @property
    def file_hashes(self) -> dict[str, str]:
        return {f.path: f.hash for f in self.files}
