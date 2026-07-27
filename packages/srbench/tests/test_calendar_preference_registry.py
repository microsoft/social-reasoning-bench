"""Tests for resolving a task's preference document to its verifier.

The registry is the seam between a preference document and the code that
grades it, so these tests focus on how a task is looked up and what happens
when the lookup fails.
"""

import pytest
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    PreferenceAdherenceResult,
    VerifierContext,
    evaluate_preference_adherence,
    register_verifier,
    registry,
)
from srbench.benchmarks.calendar_scheduling.types import (
    CalendarAssistant,
    CalendarRequestor,
    CalendarTask,
    LabeledMeeting,
    Meeting,
)


@pytest.fixture(autouse=True)
def _isolated_registry():
    """Keep registrations made by one test out of the others."""
    saved = dict(registry._VERIFIERS)
    registry._VERIFIERS.clear()
    yield
    registry._VERIFIERS.clear()
    registry._VERIFIERS.update(saved)


def _meeting(start_time: str = "09:00", end_time: str = "10:00") -> Meeting:
    """Return the meeting the requestor asked for."""
    return Meeting(
        uid="req-001",
        title="Project sync",
        description="",
        organizer="alice@example.com",
        date="2024-06-15",
        start_time=start_time,
        end_time=end_time,
        attendees=[],
    )


def _busy(start_time: str, end_time: str) -> LabeledMeeting:
    """Return a calendar entry occupying the given window."""
    return LabeledMeeting(
        uid=f"busy-{start_time}",
        title="Existing commitment",
        description="",
        organizer="someone@example.com",
        date="2024-06-15",
        start_time=start_time,
        end_time=end_time,
        attendees=[],
        is_movable=False,
        is_secret=False,
    )


def _task(preference_file: str | None, assistant_calendar=None) -> CalendarTask:
    """Return a task declaring the given preference document."""
    return CalendarTask(
        id=1,
        requestor=CalendarRequestor(
            email="alice@example.com",
            instruction_message="Please book a sync.",
            calendar=[],
            requested_meeting=_meeting(),
            is_malicious=False,
        ),
        assistant=CalendarAssistant(
            email="bob@example.com",
            instruction_message="Handle Bob's calendar.",
            calendar=assistant_calendar or [],
            preference_file=preference_file,
            preference_md="User prefers mornings." if preference_file else None,
        ),
    )


def _result(explanation: str) -> PreferenceAdherenceResult:
    """Return a stand-in result a fake verifier can hand back."""
    return PreferenceAdherenceResult(
        hard_constraints_satisfied=True,
        soft_preferences_score=1.0,
        explanation=explanation,
    )


class TestLookup:
    """Tests for resolving a task to the verifier that grades it."""

    def test_a_registered_document_routes_to_its_verifier(self):
        """The decorated function grades any task naming that document."""

        @register_verifier("preferences/amara_okafor.md")
        def _verify(context: VerifierContext) -> PreferenceAdherenceResult:
            return _result("graded by amara's verifier")

        result = evaluate_preference_adherence(_task("preferences/amara_okafor.md"), None)

        assert result is not None
        assert result.explanation == "graded by amara's verifier"

    def test_a_task_without_a_document_is_not_graded_here(self):
        """Numeric-preference tasks fall through to outcome optimality."""
        assert evaluate_preference_adherence(_task(None), None) is None

    def test_an_unregistered_document_fails_loudly(self):
        """Silently scoring None would grade prose that nothing checks."""
        with pytest.raises(LookupError, match="no verifier is registered"):
            evaluate_preference_adherence(_task("preferences/nobody.md"), None)

    def test_registering_a_document_twice_is_rejected(self):
        """Two verifiers for one document means one of them never runs."""

        @register_verifier("preferences/amara_okafor.md")
        def _first(context: VerifierContext) -> PreferenceAdherenceResult:
            return _result("first")

        with pytest.raises(ValueError, match="already registered"):

            @register_verifier("preferences/amara_okafor.md")
            def _second(context: VerifierContext) -> PreferenceAdherenceResult:
                return _result("second")

    def test_the_decorator_returns_the_function_unchanged(self):
        """Registration is a side effect, so the verifier stays callable."""

        def _verify(context: VerifierContext) -> PreferenceAdherenceResult:
            return _result("direct call")

        decorated = register_verifier("preferences/amara_okafor.md")(_verify)

        assert decorated is _verify


class TestKeyNormalization:
    """Tests for spellings of the same path resolving to one verifier."""

    @pytest.mark.parametrize(
        "declared",
        ["preferences/amara_okafor.md", "./preferences/amara_okafor.md"],
    )
    def test_equivalent_spellings_find_the_verifier(self, declared: str):
        """A leading ``./`` in the YAML should not unregister the verifier."""

        @register_verifier("preferences/amara_okafor.md")
        def _verify(context: VerifierContext) -> PreferenceAdherenceResult:
            return _result("found")

        result = evaluate_preference_adherence(_task(declared), None)

        assert result is not None

    def test_different_documents_stay_distinct(self):
        """Sharing a filename across directories must not collide."""

        @register_verifier("personas/amara.md")
        def _personas(context: VerifierContext) -> PreferenceAdherenceResult:
            return _result("personas")

        @register_verifier("archive/amara.md")
        def _archive(context: VerifierContext) -> PreferenceAdherenceResult:
            return _result("archive")

        result = evaluate_preference_adherence(_task("archive/amara.md"), None)

        assert result is not None
        assert result.explanation == "archive"


class TestContext:
    """Tests for what the registry hands the verifier."""

    def test_the_context_carries_the_task_and_the_run(self):
        """A verifier grades a run, so it needs both calendars and the outcome."""
        seen: list[VerifierContext] = []

        @register_verifier("preferences/amara_okafor.md")
        def _verify(context: VerifierContext) -> PreferenceAdherenceResult:
            seen.append(context)
            return _result("captured")

        calendar = [_busy("10:00", "11:00")]
        scheduled = _meeting("14:00", "15:00")

        evaluate_preference_adherence(
            _task("preferences/amara_okafor.md", assistant_calendar=calendar),
            scheduled,
            has_conflicts=True,
        )

        context = seen[0]
        assert context.scheduled_meeting == scheduled
        assert context.assistant_calendar == calendar
        assert context.has_conflicts

    def test_the_duration_comes_from_the_requested_meeting(self):
        """The assistant may move a meeting but not resize it."""
        seen: list[VerifierContext] = []

        @register_verifier("preferences/amara_okafor.md")
        def _verify(context: VerifierContext) -> PreferenceAdherenceResult:
            seen.append(context)
            return _result("captured")

        evaluate_preference_adherence(
            _task("preferences/amara_okafor.md"), _meeting("14:00", "16:00")
        )

        assert seen[0].duration_minutes == 60
