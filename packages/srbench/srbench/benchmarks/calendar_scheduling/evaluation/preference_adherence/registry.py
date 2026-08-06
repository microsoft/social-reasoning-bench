"""Resolves a task's preference document to the verifier that grades it.

The document is prose the assistant reads; the verifier is its executable
counterpart. Keying the registry on the document's path keeps the pair
together, so a task names one file and gets both.
"""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import PurePosixPath

from ...types import CalendarTask, LabeledMeeting, Meeting
from .types import PreferenceAdherenceResult


@dataclass(frozen=True)
class VerifierContext:
    """Everything a verifier needs to grade one run of a task."""

    scheduled_meeting: Meeting | None
    assistant_calendar: list[LabeledMeeting]
    requestor_calendar: list[LabeledMeeting]
    duration_minutes: int
    has_conflicts: bool = False


Verifier = Callable[[VerifierContext], PreferenceAdherenceResult]

_VERIFIERS: dict[str, Verifier] = {}


def _registry_key(preference_file: str) -> str:
    """Normalize a declared path so equivalent spellings resolve alike."""
    return PurePosixPath(preference_file).as_posix()


def register_verifier(preference_file: str) -> Callable[[Verifier], Verifier]:
    """Register the decorated function as the verifier for *preference_file*.

    Args:
        preference_file: Path to the preference document, as tasks declare it.

    Returns:
        A decorator that records the verifier and returns it unchanged.

    Raises:
        ValueError: If a verifier is already registered for the document.
    """

    def decorator(verifier: Verifier) -> Verifier:
        key = _registry_key(preference_file)
        if key in _VERIFIERS:
            raise ValueError(f"A verifier is already registered for {key!r}.")
        _VERIFIERS[key] = verifier
        return verifier

    return decorator


def resolve_verifier(preference_file: str | None) -> Verifier | None:
    """Resolve a declared preference document to its verifier.

    Args:
        preference_file: Path to the preference document, as a task declares
            it. ``None`` denotes a numeric-preference task.

    Returns:
        The registered verifier, or ``None`` for a task without a preference
        document.

    Raises:
        LookupError: If a document is declared but has no registered verifier.
    """
    if not preference_file:
        return None

    key = _registry_key(preference_file)
    verifier = _VERIFIERS.get(key)
    if verifier is None:
        raise LookupError(
            f"Task declares preference file {key!r}, but no verifier is registered "
            f"for it. Renaming a preference document requires updating the "
            f"@register_verifier decorator that names it."
        )
    return verifier


def evaluate_preference_adherence(
    task: CalendarTask,
    scheduled_meeting: Meeting | None,
    has_conflicts: bool = False,
) -> PreferenceAdherenceResult | None:
    """Grade *task* against the preference document it declares.

    Args:
        task: The task that was run.
        scheduled_meeting: The meeting the assistant scheduled, or None.
        has_conflicts: Whether task completion found overlaps in the final
            calendar.

    Returns:
        The verifier's result, or None for a task that declares no document
        and is therefore graded on numeric preferences instead.

    Raises:
        LookupError: If the task declares a document that has no verifier.
            Scoring such a task would silently grade prose nothing checks.
    """
    verifier = resolve_verifier(task.assistant.preference_file)
    if verifier is None:
        return None

    return verifier(
        VerifierContext(
            scheduled_meeting=scheduled_meeting,
            assistant_calendar=task.assistant.calendar,
            requestor_calendar=task.requestor.calendar,
            duration_minutes=task.requestor.requested_meeting.duration_minutes,
            has_conflicts=has_conflicts,
        )
    )
