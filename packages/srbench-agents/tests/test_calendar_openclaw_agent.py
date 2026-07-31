"""The OpenClaw calendar agent must frame a task exactly like the built-in one.

These tests are the reason the prompt lives in one shared function: they pin the
OpenClaw opening message to the built-in agent's own two turns, so the harness is
the only thing that differs between a BYOA run and a native run.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from srbench.benchmarks.calendar_scheduling.agents.assistant import CalendarAssistantAgent
from srbench.benchmarks.calendar_scheduling.agents.assistant.prompts import (
    CALENDAR_PREFERENCE_GUIDANCE,
    get_system_prompt,
)
from srbench.benchmarks.calendar_scheduling.types import (
    CalendarAssistant,
    CalendarAssistantTask,
    TimeSlotPreference,
)
from srbench.shared import AssistantTask
from srbench_agents.calendar_openclaw_agent import CalendarOpenClawAgent, ground_rules
from srbench_agents.prompts import DEFAULT_ASSISTANT_SYSTEM_PROMPT

PREFERENCE_MD = "# Scheduling preferences\n\n- User prefers afternoons, from 1pm onwards.\n"


def _task(*, preference_md: str | None) -> CalendarAssistantTask:
    """Build a task carrying either a preference document or a numeric table."""
    return CalendarAssistantTask(
        assistant=CalendarAssistant(
            name="Amara Okafor",
            email="amara@example.com",
            instruction_message="Please handle my scheduling.",
            calendar=[],
            preferences=[]
            if preference_md
            else [TimeSlotPreference(start_time="09:00", end_time="10:00", score=1.0)],
            preference_file="preferences/task_000.md" if preference_md else None,
            preference_md=preference_md,
        )
    )


def _agent(task: CalendarAssistantTask) -> CalendarOpenClawAgent:
    return CalendarOpenClawAgent(task=task, model="anthropic/claude-opus-4-8")


def _native_turns(task: CalendarAssistantTask) -> tuple[str, str]:
    """Return the built-in agent's seeded (system, user) message contents."""
    agent = CalendarAssistantAgent(
        model="test",
        model_client=MagicMock(),
        task=task,
        system_prompt=get_system_prompt("none"),
        expose_preferences=True,
    )
    # The agent seeds both turns with plain strings; the chat-message type is
    # broader than that, so narrow it for comparison.
    return str(agent.messages[0]["content"]), str(agent.messages[1]["content"])


@pytest.mark.parametrize("preference_md", [PREFERENCE_MD, None], ids=["document", "numeric"])
def test_opening_message_is_the_ground_rules_plus_the_native_turns(preference_md):
    """The opening message is exactly the ground rules and the built-in prompt."""
    task = _task(preference_md=preference_md)
    agent = _agent(task)
    agent.system_prompt = get_system_prompt("none")

    system, instruction = _native_turns(task)

    assert agent._opening_message() == "\n\n".join(
        part.strip() for part in [ground_rules(), system, instruction]
    )


def test_the_ground_rules_do_not_promise_a_json_briefing():
    """The shared rules advertise JSON; this agent sends prose, so it says so."""
    rules = ground_rules()

    assert "arrives as JSON" not in rules
    assert "follows these rules, in this same message" in rules
    # Every other rule is inherited verbatim, not restated.
    assert "call `EndConversation` with a brief reason" in rules
    assert len(rules.splitlines()) == len(DEFAULT_ASSISTANT_SYSTEM_PROMPT.splitlines())


def test_a_document_task_carries_the_tag_and_the_guidance():
    """The soft arm gets both halves of the intervention."""
    agent = _agent(_task(preference_md=PREFERENCE_MD))
    agent.system_prompt = get_system_prompt("none")

    message = agent._opening_message()

    assert CALENDAR_PREFERENCE_GUIDANCE in message
    assert f"<user_preference>\n{PREFERENCE_MD}" in message


def test_a_numeric_task_carries_neither():
    """The numeric arm is provably free of the guidance it is compared against."""
    agent = _agent(_task(preference_md=None))
    agent.system_prompt = get_system_prompt("none")

    message = agent._opening_message()

    assert CALENDAR_PREFERENCE_GUIDANCE not in message
    assert "<user_preference>" not in message
    assert "09:00" in message  # the numeric table is still shown


def test_the_raw_json_briefing_is_not_sent():
    """The base class dumps the task as JSON; this agent must not.

    The dump would repeat the preference document verbatim next to the tagged
    block and leak the principal's calendar, which the built-in agent makes the
    model discover through tools.
    """
    agent = _agent(_task(preference_md=PREFERENCE_MD))
    agent.system_prompt = get_system_prompt("none")

    assert "Your private task briefing (JSON):" not in agent._opening_message()


def test_a_non_calendar_task_is_rejected():
    """Pointing this agent at another benchmark fails loudly, not silently."""
    agent = CalendarOpenClawAgent(task=AssistantTask(), model="anthropic/claude-opus-4-8")

    with pytest.raises(TypeError, match="only handles calendar scheduling tasks"):
        agent._opening_message()
