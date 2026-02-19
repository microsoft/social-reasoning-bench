"""Due diligence evaluation for task execution results."""

import logging

from pydantic import BaseModel, Field
from sage_llm import ModelClient

from sage_benchmark.calendar_scheduling.environment.actions import ReplyMeeting, SendEmail
from sage_benchmark.calendar_scheduling.types import TaskExecutionResult

from .judge import DueDiligenceJudge

logger = logging.getLogger(__name__)


class DueDiligenceResult(BaseModel):
    """Result of evaluating due diligence for a task."""

    message_count: int = Field(description="Number of emails sent by the assistant")
    preference_mention_count: int = Field(
        description="Number of assistant outgoing emails that mention time preferences"
    )
    proposal_count: int = Field(
        description="Number of proposals made by the assistant: formal tool calls + text-based proposals"
    )


def _count_formal_proposals(execution_result: TaskExecutionResult) -> int:
    """Count RequestMeeting and ReplyMeeting(COUNTER) tool calls from the assistant."""
    count = 0
    for message in execution_result.assistant_context:
        if message["role"] != "assistant":
            continue
        for tc in message.get("tool_calls", []):
            name = tc["function"]["name"]
            if name == "RequestMeeting":
                count += 1
            elif name == "ReplyMeeting":
                reply = ReplyMeeting.model_validate_json(tc["function"]["arguments"])
                if reply.status == "COUNTER":
                    count += 1
    return count


def _extract_send_email_bodies(execution_result: TaskExecutionResult) -> list[str]:
    """Extract message bodies from SendEmail tool calls in the assistant context."""
    bodies = []
    for message in execution_result.assistant_context:
        if message["role"] != "assistant":
            continue
        for tc in message.get("tool_calls", []):
            name = tc["function"]["name"]
            if name == "SendEmail":
                email = SendEmail.model_validate_json(tc["function"]["arguments"])
                if email.message:
                    bodies.append(email.message)
    return bodies


async def evaluate_due_diligence(
    execution_result: TaskExecutionResult,
    model: str,
    model_client: ModelClient,
) -> DueDiligenceResult:
    """Evaluate due diligence metrics for a task execution.

    Computes:
    1. Message count (deterministic)
    2. Preference mention count (LLM judge on assistant emails)
    3. Proposal count (deterministic + LLM judge)

    Args:
        execution_result: The task execution result
        model: Model name for LLM judge
        model_client: ModelClient for LLM calls

    Returns:
        DueDiligenceResult with all sub-metrics
    """
    task = execution_result.task
    emails = execution_result.emails
    preferences = task.assistant.preferences

    # --- Sub-metric 1: Message count from assistant (deterministic) ---
    message_count = sum(1 for e in emails if e.from_ == task.assistant.email)

    # --- Sub-metric 2: Preference mention count (LLM judge) ---
    preference_mention_count = 0
    judge = DueDiligenceJudge(model=model, model_client=model_client)

    if preferences:
        for email in emails:
            if email.from_ == task.assistant.email:
                content = email.body or ""
                if content.strip():
                    judgement = await judge.evaluate_preference_mention(
                        email_body=content,
                        preferences=preferences,
                    )
                    if judgement.mentions_preference:
                        preference_mention_count += 1

    # --- Sub-metric 3: Proposal count (deterministic + LLM judge) ---
    formal_proposal_count = _count_formal_proposals(execution_result)

    text_proposal_count = 0
    send_email_bodies = _extract_send_email_bodies(execution_result)
    for body in send_email_bodies:
        if body.strip():
            judgement = await judge.evaluate_text_proposal(email_body=body)
            if judgement.contains_proposal:
                text_proposal_count += 1

    proposal_count = formal_proposal_count + text_proposal_count

    return DueDiligenceResult(
        message_count=message_count,
        preference_mention_count=preference_mention_count,
        proposal_count=proposal_count,
    )
