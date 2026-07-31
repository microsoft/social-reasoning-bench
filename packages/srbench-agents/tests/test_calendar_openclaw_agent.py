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


def _sent(agent: CalendarOpenClawAgent) -> tuple[str, str]:
    """Return the ``(system, user)`` pair the agent would send."""
    agent.system_prompt = get_system_prompt("none")
    system = agent._system_prompt_message()
    assert system is not None
    return system, agent._opening_message()


@pytest.mark.parametrize("preference_md", [PREFERENCE_MD, None], ids=["document", "numeric"])
def test_the_turns_are_the_ground_rules_plus_the_native_ones(preference_md):
    """Both turns are exactly what the built-in agent sends, plus the ground rules."""
    task = _task(preference_md=preference_md)
    native_system, native_instruction = _native_turns(task)

    system, user = _sent(_agent(task))

    assert system == "\n\n".join(part.strip() for part in [ground_rules(), native_system])
    assert user == native_instruction


def test_the_system_text_is_sent_as_a_system_prompt():
    """The ablation names a *system* prompt, so it has to travel as one.

    The base class puts its framing in the opening user turn because stock
    OpenClaw has no system-prompt channel. This agent uses the patched build's
    channel instead, so the benchmark's standing instructions carry the weight a
    system prompt carries rather than reading as something the user typed.
    """
    system, user = _sent(_agent(_task(preference_md=PREFERENCE_MD)))

    assert "call `EndConversation` with a brief reason" in system
    assert "call `EndConversation` with a brief reason" not in user
    assert "calendar scheduling personal assistant" in system
    assert "calendar scheduling personal assistant" not in user


def test_the_ground_rules_do_not_promise_a_json_briefing():
    """The shared rules advertise JSON; this agent sends prose, so it says so."""
    rules = ground_rules()

    assert "arrives as JSON" not in rules
    assert "arrives as prose" in rules
    # Every other rule is inherited verbatim, not restated.
    assert "call `EndConversation` with a brief reason" in rules
    assert len(rules.splitlines()) == len(DEFAULT_ASSISTANT_SYSTEM_PROMPT.splitlines())


def test_a_document_task_carries_the_tag_and_the_guidance():
    """The soft arm gets both halves of the intervention, each in its own turn."""
    system, user = _sent(_agent(_task(preference_md=PREFERENCE_MD)))

    assert CALENDAR_PREFERENCE_GUIDANCE in system
    assert f"<user_preference>\n{PREFERENCE_MD}" in user


def test_a_numeric_task_carries_neither():
    """The numeric arm is provably free of the guidance it is compared against."""
    system, user = _sent(_agent(_task(preference_md=None)))

    assert CALENDAR_PREFERENCE_GUIDANCE not in system + user
    assert "<user_preference>" not in system + user
    assert "09:00" in user  # the numeric table is still shown


def test_the_raw_json_briefing_is_not_sent():
    """The base class dumps the task as JSON; this agent must not.

    The dump would repeat the preference document verbatim next to the tagged
    block and leak the principal's calendar, which the built-in agent makes the
    model discover through tools.
    """
    system, user = _sent(_agent(_task(preference_md=PREFERENCE_MD)))

    assert "Your private task briefing (JSON):" not in system + user


def test_a_non_calendar_task_is_rejected():
    """Pointing this agent at another benchmark fails loudly, not silently."""
    agent = CalendarOpenClawAgent(task=AssistantTask(), model="anthropic/claude-opus-4-8")

    with pytest.raises(TypeError, match="only handles calendar scheduling tasks"):
        agent._system_prompt_message()
    with pytest.raises(TypeError, match="only handles calendar scheduling tasks"):
        agent._opening_message()


# --- Prompt ablation -------------------------------------------------------
#
# These flags exist so a run can measure what the benchmark's own framing
# contributes, and each cell of that ablation is only meaningful if the flag it
# is named after actually removed the text it claims to remove.


def test_dropping_the_srbench_prompt_leaves_only_the_ground_rules_and_the_task():
    """With the benchmark's system text off, no part of it survives.

    The two flags are independent, so this drops the guidance as well; the
    result is the floor of the ablation, harness protocol and nothing else.
    """
    agent = CalendarOpenClawAgent(
        task=_task(preference_md=PREFERENCE_MD),
        model="anthropic/claude-opus-4-8",
        srbench_system_prompt=False,
        preference_guidance=False,
    )

    system, user = _sent(agent)

    base = get_system_prompt("none")
    assert base is not None
    assert base.strip() not in system
    assert "calendar scheduling personal assistant" not in system
    assert system.strip() == ground_rules().strip()
    # The task itself is not part of the treatment and always survives.
    assert "Please handle my scheduling." in user
    assert "<user_preference>" in user


def test_the_two_prompt_flags_are_independent():
    """Each names one piece of text, so switching one must not move the other."""
    agent = CalendarOpenClawAgent(
        task=_task(preference_md=PREFERENCE_MD),
        model="anthropic/claude-opus-4-8",
        srbench_system_prompt=False,
        preference_guidance=True,
    )

    system, _ = _sent(agent)

    assert CALENDAR_PREFERENCE_GUIDANCE in system
    assert "calendar scheduling personal assistant" not in system


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

            system, _ = _sent(agent)

            assert "call `EndConversation` with a brief reason" in system


def test_the_guidance_can_be_dropped_without_dropping_the_preference():
    """The no-guidance arm still shows the document; only the explanation goes."""
    agent = CalendarOpenClawAgent(
        task=_task(preference_md=PREFERENCE_MD),
        model="anthropic/claude-opus-4-8",
        preference_guidance=False,
    )

    system, user = _sent(agent)

    assert CALENDAR_PREFERENCE_GUIDANCE not in system
    assert f"<user_preference>\n{PREFERENCE_MD}" in user


def test_both_flags_default_to_the_faithful_setting():
    """An ordinary run must not have to know the ablation exists."""
    task = _task(preference_md=PREFERENCE_MD)
    explicit = CalendarOpenClawAgent(
        task=task,
        model="anthropic/claude-opus-4-8",
        srbench_system_prompt=True,
        preference_guidance=True,
    )

    assert _sent(_agent(task)) == _sent(explicit)
