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


# --- Prompt ablation -------------------------------------------------------
#
# OpenClaw injects a large system prompt of its own that this agent cannot see.
# These flags exist so a run can measure what the benchmark's framing adds on
# top of it, and each cell of that ablation is only meaningful if the flag it is
# named after actually removed the text it claims to remove.


def test_dropping_the_srbench_prompt_leaves_only_the_ground_rules_and_the_task():
    """With the benchmark's system text off, no part of it survives."""
    task = _task(preference_md=PREFERENCE_MD)
    agent = CalendarOpenClawAgent(
        task=task,
        model="anthropic/claude-opus-4-8",
        srbench_system_prompt=False,
    )
    agent.system_prompt = get_system_prompt("none")

    message = agent._opening_message()

    base = get_system_prompt("none")
    assert base is not None
    assert base.strip() not in message
    assert "calendar scheduling personal assistant" not in message
    # The task itself is not part of the treatment and always survives.
    assert "Please handle my scheduling." in message
    assert "<user_preference>" in message


def test_the_ground_rules_survive_every_setting():
    """They are the harness protocol contract, not a prompt treatment."""
    for srbench in (True, False):
        for guidance in (True, False):
            agent = CalendarOpenClawAgent(
                task=_task(preference_md=PREFERENCE_MD),
                model="anthropic/claude-opus-4-8",
                srbench_system_prompt=srbench,
                preference_guidance=guidance,
            )
            agent.system_prompt = get_system_prompt("none")

            assert "call `EndConversation` with a brief reason" in agent._opening_message()


def test_the_guidance_can_be_dropped_without_dropping_the_preference():
    """The no-guidance arm still shows the document; only the explanation goes."""
    agent = CalendarOpenClawAgent(
        task=_task(preference_md=PREFERENCE_MD),
        model="anthropic/claude-opus-4-8",
        preference_guidance=False,
    )
    agent.system_prompt = get_system_prompt("none")

    message = agent._opening_message()

    assert CALENDAR_PREFERENCE_GUIDANCE not in message
    assert f"<user_preference>\n{PREFERENCE_MD}" in message


def test_both_flags_default_to_the_faithful_setting():
    """An ordinary run must not have to know the ablation exists."""
    task = _task(preference_md=PREFERENCE_MD)
    plain = _agent(task)
    plain.system_prompt = get_system_prompt("none")
    explicit = CalendarOpenClawAgent(
        task=task,
        model="anthropic/claude-opus-4-8",
        srbench_system_prompt=True,
        preference_guidance=True,
    )
    explicit.system_prompt = get_system_prompt("none")

    assert plain._opening_message() == explicit._opening_message()
