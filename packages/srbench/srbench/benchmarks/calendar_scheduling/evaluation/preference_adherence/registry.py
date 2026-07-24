"""Registry mapping task ids to their programmatic preference verifiers.

Each task in a soft-preference dataset pairs a natural-language
``preference.md`` (what the model sees) with a verifier function (the ground
truth). Verifier modules live in :mod:`.verifiers` and register themselves with
the :func:`register_verifier` decorator.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from ...types import CalendarTask, Meeting
from .types import PreferenceAdherenceResult


@dataclass(frozen=True)
class VerifierContext:
    """Everything a verifier needs to grade a single task run."""

    task: CalendarTask
    scheduled_meeting: Meeting | None
    has_conflicts: bool = False

    @property
    def duration_minutes(self) -> int:
        """Duration of the meeting the requestor asked for."""
        return self.task.requestor.requested_meeting.duration_minutes


Verifier = Callable[[VerifierContext], PreferenceAdherenceResult]

VERIFIER_REGISTRY: dict[int, Verifier] = {}


def register_verifier(task_id: int) -> Callable[[Verifier], Verifier]:
    """Register the decorated function as the verifier for *task_id*.

    Args:
        task_id: Id of the task the verifier grades.

    Returns:
        A decorator that records the verifier and returns it unchanged.

    Raises:
        ValueError: If a verifier is already registered for *task_id*.
    """

    def decorator(verifier: Verifier) -> Verifier:
        if task_id in VERIFIER_REGISTRY:
            raise ValueError(f"A preference verifier is already registered for task {task_id}")
        VERIFIER_REGISTRY[task_id] = verifier
        return verifier

    return decorator


def evaluate_preference_adherence(
    task: CalendarTask,
    scheduled_meeting: Meeting | None,
    has_conflicts: bool = False,
) -> PreferenceAdherenceResult | None:
    """Grade a task run with its registered verifier.

    Args:
        task: The task that was executed.
        scheduled_meeting: The meeting that ended up on the calendar, if any.
        has_conflicts: Whether task completion detected calendar conflicts.

    Returns:
        The verifier's result, or None when the task has no registered
        verifier (for example the legacy numeric-preference datasets).
    """
    verifier = VERIFIER_REGISTRY.get(task.id)
    if verifier is None:
        return None
    return verifier(
        VerifierContext(
            task=task,
            scheduled_meeting=scheduled_meeting,
            has_conflicts=has_conflicts,
        )
    )
