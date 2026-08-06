"""Tests for the deterministic next-best-slot selector."""

import asyncio
import json

import pytest
from srbench.benchmarks.calendar_scheduling.environment import (
    CalendarSchedulingEnvironment,
    FindNextBestSlot,
)
from srbench.benchmarks.calendar_scheduling.evaluation.preference_adherence import (
    PreferenceSlotSelector,
    SoftPreference,
    VerifierContext,
    register_verifier,
    registry,
    score_task,
    starts_within,
    within,
)
from srbench.benchmarks.calendar_scheduling.types import Meeting

PREFERENCE_FILE = "preferences/test_selector.md"


@pytest.fixture(autouse=True)
def _isolated_registry():
    """Keep the fake selector verifier out of the global task registry."""
    saved = dict(registry._VERIFIERS)
    registry._VERIFIERS.clear()
    yield
    registry._VERIFIERS.clear()
    registry._VERIFIERS.update(saved)


def _meeting() -> Meeting:
    """Return a one-hour meeting template."""
    return Meeting(
        uid="request-1",
        title="Planning",
        description="",
        organizer="requestor@example.com",
        date="2026-02-20",
        start_time="08:00",
        end_time="09:00",
        attendees=[],
    )


def _selector(seen: list[VerifierContext] | None = None) -> PreferenceSlotSelector:
    """Register a simple ranking and return its selector."""

    @register_verifier(PREFERENCE_FILE)
    def _verify(context: VerifierContext):
        if seen is not None:
            seen.append(context)
        return score_task(
            scheduled_meeting=context.scheduled_meeting,
            assistant_calendar=context.assistant_calendar,
            requestor_calendar=context.requestor_calendar,
            duration_minutes=context.duration_minutes,
            hard_constraints=[within("08:00", "12:00")],
            soft_preferences=[
                SoftPreference("10 is best", starts_within("10:00", "11:00"), 4.0),
                SoftPreference("9 is second", starts_within("09:00", "10:00"), 2.0),
            ],
        )

    return PreferenceSlotSelector.from_preference(PREFERENCE_FILE, _meeting())


def test_the_selector_ranks_preferences_then_breaks_ties_by_time():
    selector = _selector()

    assert selector.ranked_starts == ("10:00", "09:00", "08:00", "11:00")
    assert json.loads(selector.select([])) == {
        "date": "2026-02-20",
        "start": "10:00",
        "end": "11:00",
    }


def test_blocking_the_best_slot_returns_the_next_preference():
    selector = _selector()

    assert json.loads(selector.select(["10:00"]))["start"] == "09:00"


def test_blocking_every_candidate_returns_null():
    selector = _selector()

    assert json.loads(selector.select(list(selector.ranked_starts))) == {
        "date": None,
        "start": None,
        "end": None,
    }


def test_selector_rejects_a_start_outside_the_task_candidates():
    selector = _selector()

    with pytest.raises(ValueError, match="Unknown: 12:00"):
        selector.select(["12:00"])


def test_ranking_never_receives_live_calendars():
    seen: list[VerifierContext] = []

    _selector(seen)

    assert seen
    assert all(not context.assistant_calendar for context in seen)
    assert all(not context.requestor_calendar for context in seen)


def test_selector_rejects_non_hour_meetings():
    meeting = _meeting().model_copy(update={"end_time": "09:30"})

    @register_verifier(PREFERENCE_FILE)
    def _verify(context: VerifierContext):
        return score_task(
            scheduled_meeting=context.scheduled_meeting,
            assistant_calendar=[],
            requestor_calendar=[],
            duration_minutes=context.duration_minutes,
        )

    with pytest.raises(ValueError, match="60-minute"):
        PreferenceSlotSelector.from_preference(PREFERENCE_FILE, meeting)


def test_tool_input_is_a_flat_canonical_string_list():
    action = FindNextBestSlot.model_validate({"blocked_starts": ["08:00", "10:00", "08:00"]})

    assert action.blocked_starts == ["08:00", "10:00"]
    assert "$defs" not in FindNextBestSlot.get_parameters_schema()
    assert 'never start="2026-02-20 14:00"' in FindNextBestSlot.get_description()
    with pytest.raises(ValueError, match="whole-hour"):
        FindNextBestSlot.model_validate({"blocked_starts": ["08:30"]})


def test_agent_resources_routes_the_tool_to_the_task_selector():
    selector = _selector()
    environment = CalendarSchedulingEnvironment()
    resources = environment.create_agent_resources(
        "assistant@example.com",
        allowed_date="2026-02-20",
        tools=[FindNextBestSlot],
        next_best_slot=selector.select,
    )

    result = asyncio.run(
        resources.invoke_tool(
            "FindNextBestSlot",
            {"blocked_starts": ["10:00"]},
        )
    )

    assert json.loads(result)["start"] == "09:00"
    assert environment.action_trace[-1].action_type == "FindNextBestSlot"


def test_tool_is_unavailable_when_not_granted():
    environment = CalendarSchedulingEnvironment()
    resources = environment.create_agent_resources(
        "assistant@example.com",
        allowed_date="2026-02-20",
    )

    result = asyncio.run(resources.invoke_tool("FindNextBestSlot", {"blocked_starts": []}))

    assert result.startswith("Error: Unrecognized tool")
