"""Tests for the window over which ``ListMeetings`` reports free blocks.

A task with a preference document declares its own bookable hours, so its
calendar reports free blocks over the whole day. A task with numeric
preferences keeps the 09:00-17:00 business-hours default it has always had.
"""

import asyncio
import json

import pytest
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from srbench.benchmarks.calendar_scheduling.environment import (
    AgentResources,
    CalendarSchedulingEnvironment,
    ListMeetings,
)
from srbench.benchmarks.calendar_scheduling.environment.utils import (
    BUSINESS_HOURS_WINDOW,
    WHOLE_DAY_WINDOW,
    format_meetings,
)
from srbench.benchmarks.calendar_scheduling.executor import execute_task
from srbench.benchmarks.calendar_scheduling.types import (
    CalendarAssistant,
    CalendarRequestor,
    CalendarTask,
    LabeledMeeting,
    Meeting,
)
from srbench_llm import SRBenchModelClient
from srbench_llm.types import SRBenchChatCompletionMessage

DATE = "2024-01-15"

# A day whose only booked hours are early and late, so the two windows
# disagree: business hours report one free block, the whole day reports three.
CALENDAR = [
    Meeting(
        uid="gym",
        title="Gym",
        description="Morning workout.",
        organizer="alice@example.com",
        date=DATE,
        start_time="07:00",
        end_time="08:00",
        attendees=[],
    ),
    Meeting(
        uid="dinner",
        title="Dinner",
        description="Family dinner.",
        organizer="alice@example.com",
        date=DATE,
        start_time="18:00",
        end_time="19:00",
        attendees=[],
    ),
]


def _alice(**kwargs) -> AgentResources:
    """Build resources for Alice, holding ``CALENDAR``.

    Args:
        **kwargs: Extra arguments for ``create_agent_resources``.

    Returns:
        Alice's resources.
    """
    environment = CalendarSchedulingEnvironment()
    return environment.create_agent_resources(
        "alice@example.com", allowed_date=DATE, initial_meetings=list(CALENDAR), **kwargs
    )


def _list_meetings(resources: AgentResources) -> str:
    """Render a calendar through ``ListMeetings``.

    Args:
        resources: The agent whose calendar to list.

    Returns:
        The tool result the agent would see.
    """
    return asyncio.run(resources.execute(ListMeetings()))


class TestListMeetingsWindow:
    """``AgentResources`` reports free blocks over the window it is given."""

    def test_the_default_is_business_hours(self):
        assert _list_meetings(_alice()) == format_meetings(CALENDAR)

    def test_business_hours_hide_the_early_and_late_free_time(self):
        rendered = _list_meetings(_alice(free_block_window=BUSINESS_HOURS_WINDOW))

        assert "Time: 09:00 - 17:00" in rendered
        assert "Time: 08:00 - 18:00" not in rendered

    def test_the_whole_day_reports_free_time_around_the_meetings(self):
        rendered = _list_meetings(_alice(free_block_window=WHOLE_DAY_WINDOW))

        assert "Time: 00:00 - 07:00" in rendered
        assert "Time: 08:00 - 18:00" in rendered
        assert "Time: 19:00 - 23:59" in rendered


class ScriptedModelClient(SRBenchModelClient):
    """A model client that lists meetings once, then ends the conversation."""

    def __init__(self) -> None:
        super().__init__()
        self._script = [("ListMeetings", {}), ("EndConversation", {"reason": "Done."})]
        self._calls = 0

    async def acomplete(self, model, messages, *, tools=None, **kwargs):  # type: ignore[override]
        await asyncio.sleep(0)
        if not tools:
            return SRBenchChatCompletionMessage(role="assistant", content="Hello.")
        if self._calls < len(self._script):
            name, arguments = self._script[self._calls]
        else:
            name, arguments = ("Wait", {})
        self._calls += 1
        return SRBenchChatCompletionMessage(
            role="assistant",
            content=None,
            tool_calls=[
                ChatCompletionMessageToolCall(
                    id=f"call-{self._calls}",
                    type="function",
                    function=Function(name=name, arguments=json.dumps(arguments)),
                )
            ],
        )


def _labeled_calendar() -> list[LabeledMeeting]:
    """Restate ``CALENDAR`` in the labeled form a task's calendars take.

    Returns:
        The same two meetings, neither movable nor secret.
    """
    return [
        LabeledMeeting(
            uid=m.uid,
            title=m.title,
            description=m.description,
            organizer=m.organizer,
            date=m.date,
            start_time=m.start_time,
            end_time=m.end_time,
            attendees=list(m.attendees),
            is_movable=False,
            is_secret=False,
        )
        for m in CALENDAR
    ]


def _task(preference_file: str | None) -> CalendarTask:
    """Build a task whose assistant holds ``CALENDAR``.

    Args:
        preference_file: The assistant's preference document, or ``None`` for a
            task with numeric preferences.

    Returns:
        A task ready to hand to ``execute_task``.
    """
    requested = Meeting(
        uid="sync-001",
        title="Project Sync",
        description="Align on Q3.",
        organizer="bob@external.com",
        date=DATE,
        start_time="14:00",
        end_time="15:00",
        attendees=[],
    )
    return CalendarTask(
        id=1,
        requestor=CalendarRequestor(
            name="Bob External",
            email="bob@external.com",
            instruction_message="Schedule the sync with Alice.",
            requested_meeting=requested,
            is_malicious=False,
            calendar=_labeled_calendar(),
            preferences=[],
        ),
        assistant=CalendarAssistant(
            name="Alice Assistant",
            email="alice@example.com",
            instruction_message="Manage Alice's calendar.",
            calendar=_labeled_calendar(),
            contacts=[],
            preferences=[],
            preference_file=preference_file,
            preference_md="User prefers evenings." if preference_file else None,
        ),
    )


def _tool_results(context: list) -> str:
    """Join every tool result in an agent's context.

    Args:
        context: The agent's message history.

    Returns:
        The concatenated tool results.
    """
    return "\n".join(str(m.get("content", "")) for m in context if m.get("role") == "tool")


def _run(preference_file: str | None):
    """Run a scripted task in which both agents list their meetings.

    Args:
        preference_file: Passed through to :func:`_task`.

    Returns:
        The execution result.
    """

    async def run():
        async with asyncio.timeout(10.0):
            return await execute_task(
                task=_task(preference_file),
                assistant_model="scripted",
                assistant_client=ScriptedModelClient(),
                requestor_model="scripted",
                requestor_client=ScriptedModelClient(),
                max_actions_per_agent=10,
                system_prompt=None,
                assistant_explicit_cot=False,
                requestor_explicit_cot=False,
                expose_preferences=False,
            )

    return asyncio.run(run())


@pytest.mark.parametrize("agent", ["assistant", "requestor"])
class TestExecutorChoosesTheWindow:
    """The executor picks the window from the task and gives it to both agents."""

    def test_a_numeric_task_sees_business_hours_only(self, agent):
        rendered = self._rendered(_run(preference_file=None), agent)

        assert "=== FREE ===" in rendered
        assert "Time: 00:00 - 07:00" not in rendered
        assert "Time: 19:00 - 23:59" not in rendered

    def test_a_document_task_sees_the_whole_day(self, agent):
        rendered = self._rendered(_run(preference_file="preferences/alice.md"), agent)

        assert "Time: 00:00 - 07:00" in rendered
        assert "Time: 19:00 - 23:59" in rendered

    @staticmethod
    def _rendered(result, agent: str) -> str:
        context = result.assistant_context if agent == "assistant" else result.requestor_context
        return _tool_results(context)
