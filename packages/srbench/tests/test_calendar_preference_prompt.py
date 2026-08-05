"""Tests for natural-language preference injection into the assistant prompt.

Covers the ``<user_preference>`` block added to the assistant's user turn and
the guidance appended to its system prompt, plus the guarantee that tasks
carrying only numeric preferences keep their existing prompt.
"""

from unittest.mock import MagicMock

import pytest
from srbench.benchmarks.calendar_scheduling.agents.assistant.calendar_assistant import (
    CalendarAssistantAgent,
)
from srbench.benchmarks.calendar_scheduling.agents.assistant.prompts import (
    CALENDAR_ADVOCACY_GUIDANCE,
    CALENDAR_PREFERENCE_GUIDANCE,
    CALENDAR_ROLE,
    USER_PREFERENCE_TAG,
    format_user_preference_block,
    get_system_prompt,
)
from srbench.benchmarks.calendar_scheduling.agents.calendar_base import (
    format_preferences_for_prompt,
)
from srbench.benchmarks.calendar_scheduling.types import (
    CalendarAssistant,
    CalendarAssistantTask,
    LabeledMeeting,
    TimeSlotPreference,
)

PREFERENCE_MD = """# Scheduling preferences

- User prefers meetings in the afternoon, from 1pm onwards.
- User never takes meetings during the noon hour.
"""

NUMERIC_PREFERENCES = [
    TimeSlotPreference(start_time="09:00", end_time="11:00", score=0.9),
]


def _make_calendar() -> list[LabeledMeeting]:
    """Return a one-meeting calendar with no secret events."""
    return [
        LabeledMeeting(
            uid="mtg-001",
            title="Team Standup",
            description="Daily sync",
            organizer="alice@example.com",
            date="2024-06-15",
            start_time="09:00",
            end_time="09:30",
            attendees=[],
            is_movable=True,
            is_secret=False,
        )
    ]


def _make_assistant(
    preference_md: str | None = None,
    preferences: list[TimeSlotPreference] | None = None,
) -> CalendarAssistant:
    """Build an assistant carrying the given preference flavors.

    Args:
        preference_md: Natural-language preference text, if any.
        preferences: Numeric time-slot preferences, if any.

    Returns:
        A ``CalendarAssistant`` suitable for constructing an agent.
    """
    return CalendarAssistant(
        name="Alice Johnson",
        email="alice@example.com",
        instruction_message="Schedule incoming requests for me.",
        calendar=_make_calendar(),
        preferences=preferences or [],
        preference_file="preferences/alice.md" if preference_md else None,
        preference_md=preference_md,
    )


def _messages(
    assistant: CalendarAssistant,
    expose_preferences: bool = True,
    preference_guidance: bool = True,
    advocacy_guidance: bool = False,
):
    """Build an assistant agent and return its seeded system and user messages.

    Args:
        assistant: The principal the agent acts for.
        expose_preferences: Whether preferences are shown to the model.
        preference_guidance: Whether the system prompt explains the tag.
        advocacy_guidance: Whether the system prompt adds the negotiation
            procedure.

    Returns:
        A ``(system_content, user_content)`` tuple.
    """
    agent = CalendarAssistantAgent(
        model="test",
        model_client=MagicMock(),
        task=CalendarAssistantTask(assistant=assistant),
        expose_preferences=expose_preferences,
        preference_guidance=preference_guidance,
        advocacy_guidance=advocacy_guidance,
    )
    system_message, user_message = agent.messages[0], agent.messages[1]
    return system_message["content"], user_message["content"]


class TestFormatUserPreferenceBlock:
    """Tests for the tag wrapper itself."""

    def test_wraps_text_in_the_tag(self):
        """Preference text is wrapped verbatim in open and close tags."""
        block = format_user_preference_block("User prefers mornings.")

        assert block == f"<{USER_PREFERENCE_TAG}>\nUser prefers mornings.\n</{USER_PREFERENCE_TAG}>"

    def test_surrounding_whitespace_is_stripped(self):
        """Leading and trailing blank lines do not leak into the block."""
        block = format_user_preference_block("\n\n  User prefers mornings.  \n\n")

        assert block == f"<{USER_PREFERENCE_TAG}>\nUser prefers mornings.\n</{USER_PREFERENCE_TAG}>"

    @pytest.mark.parametrize("empty", [None, "", "   \n  "])
    def test_empty_text_produces_no_block(self, empty):
        """Absent or blank preference text yields an empty string, not a bare tag."""
        assert format_user_preference_block(empty) == ""


class TestNaturalLanguagePreferences:
    """A task carrying ``preference_md`` gets the tag and the guidance."""

    def test_user_turn_contains_the_tagged_block(self):
        """The preference text is injected verbatim into the user message."""
        _, user = _messages(_make_assistant(preference_md=PREFERENCE_MD))

        assert f"<{USER_PREFERENCE_TAG}>" in user
        assert "User never takes meetings during the noon hour." in user

    def test_system_prompt_explains_the_tag(self):
        """The guidance defining hard vs soft constraints is appended."""
        system, _ = _messages(_make_assistant(preference_md=PREFERENCE_MD))

        assert CALENDAR_PREFERENCE_GUIDANCE in system
        assert system.startswith(CALENDAR_ROLE)

    def test_guidance_can_be_suppressed_without_dropping_the_block(self):
        """The ablation keeps the tagged block but leaves the system prompt bare."""
        system, user = _messages(
            _make_assistant(preference_md=PREFERENCE_MD), preference_guidance=False
        )

        assert CALENDAR_PREFERENCE_GUIDANCE not in system
        assert f"<{USER_PREFERENCE_TAG}>" in user
        assert "User never takes meetings during the noon hour." in user

    def test_system_prompt_defers_to_the_block_for_bookable_hours(self):
        """No working day is hard-coded; the preference block decides."""
        system, _ = _messages(_make_assistant(preference_md=PREFERENCE_MD))

        assert "only authority on when your principal is bookable" in system

    def test_system_prompt_says_to_follow_a_stated_ranking(self):
        """Documents rank their soft preferences, so counting them is not enough."""
        system, _ = _messages(_make_assistant(preference_md=PREFERENCE_MD))

        assert "follow the ranking the block gives them" in system

    def test_advocacy_guidance_is_opt_in(self):
        """The existing prompt stays unchanged unless the new treatment is enabled."""
        default_system, _ = _messages(_make_assistant(preference_md=PREFERENCE_MD))
        advocacy_system, _ = _messages(
            _make_assistant(preference_md=PREFERENCE_MD), advocacy_guidance=True
        )

        assert CALENDAR_ADVOCACY_GUIDANCE not in default_system
        assert advocacy_system.count(CALENDAR_ADVOCACY_GUIDANCE) == 1

    def test_advocacy_and_preference_guidance_are_independent(self):
        """The negotiation procedure can be tested without the tag explanation."""
        system, _ = _messages(
            _make_assistant(preference_md=PREFERENCE_MD),
            preference_guidance=False,
            advocacy_guidance=True,
        )

        assert CALENDAR_ADVOCACY_GUIDANCE in system
        assert CALENDAR_PREFERENCE_GUIDANCE not in system

    def test_numeric_preferences_are_not_also_injected(self):
        """Natural-language preferences take precedence over numeric ones."""
        assistant = _make_assistant(preference_md=PREFERENCE_MD, preferences=NUMERIC_PREFERENCES)

        _, user = _messages(assistant)

        assert f"<{USER_PREFERENCE_TAG}>" in user
        assert format_preferences_for_prompt(NUMERIC_PREFERENCES) not in user

    def test_not_injected_when_preferences_are_hidden(self):
        """``expose_preferences=False`` suppresses both the block and the guidance."""
        system, user = _messages(
            _make_assistant(preference_md=PREFERENCE_MD), expose_preferences=False
        )

        assert USER_PREFERENCE_TAG not in user
        assert CALENDAR_PREFERENCE_GUIDANCE not in system


class TestNumericPreferencesUnchanged:
    """Tasks without ``preference_md`` keep the prompt they have on main."""

    def test_user_turn_uses_legacy_formatting(self):
        """Numeric preferences are still rendered by the legacy formatter."""
        _, user = _messages(_make_assistant(preferences=NUMERIC_PREFERENCES))

        assert format_preferences_for_prompt(NUMERIC_PREFERENCES) in user
        assert USER_PREFERENCE_TAG not in user

    def test_system_prompt_has_no_preference_guidance(self):
        """The guidance is only added for tasks that actually carry the tag."""
        system, _ = _messages(_make_assistant(preferences=NUMERIC_PREFERENCES))

        assert CALENDAR_PREFERENCE_GUIDANCE not in system

    def test_numeric_tasks_do_not_get_advocacy_guidance(self):
        """The treatment is scoped to tasks with natural-language preferences."""
        system, _ = _messages(
            _make_assistant(preferences=NUMERIC_PREFERENCES), advocacy_guidance=True
        )

        assert CALENDAR_ADVOCACY_GUIDANCE not in system

    def test_messages_match_the_pre_change_prompt_exactly(self):
        """Regression guard: the legacy prompt is reproduced byte for byte.

        This mirrors how the prompt was assembled before natural-language
        preferences existed, so any accidental change to the numeric path fails
        here rather than silently shifting every legacy benchmark result.
        """
        assistant = _make_assistant(preferences=NUMERIC_PREFERENCES)

        system, user = _messages(assistant)

        expected_system = "\n\n".join(
            [
                get_system_prompt("none") or "",
                f"You are {assistant.name}'s calendar scheduling personal assistant.",
            ]
        )
        expected_user = "\n\n".join(
            [
                assistant.instruction_message,
                format_preferences_for_prompt(NUMERIC_PREFERENCES),
            ]
        )
        assert system == expected_system
        assert user == expected_user
