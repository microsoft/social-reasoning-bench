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
    CALENDAR_ADVOCACY_GUIDANCE,
    CALENDAR_PREFERENCE_GUIDANCE,
    CALENDAR_PROGRAMMATIC_PREFERENCE_TOOL_GUIDANCE,
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


def _agent(task: CalendarAssistantTask, **kwargs) -> CalendarOpenClawAgent:
    return CalendarOpenClawAgent(
        task=task,
        model="anthropic/claude-opus-4-8",
        **kwargs,
    )


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


def test_advocacy_guidance_is_opt_in_and_scoped_to_document_tasks():
    """Only an enabled natural-language preference task gets the procedure."""
    default_system, _ = _sent(_agent(_task(preference_md=PREFERENCE_MD)))
    advocacy_system, _ = _sent(_agent(_task(preference_md=PREFERENCE_MD), advocacy_guidance=True))
    numeric_system, _ = _sent(_agent(_task(preference_md=None), advocacy_guidance=True))

    assert CALENDAR_ADVOCACY_GUIDANCE not in default_system
    assert advocacy_system.count(CALENDAR_ADVOCACY_GUIDANCE) == 1
    assert CALENDAR_ADVOCACY_GUIDANCE not in numeric_system


def test_programmatic_tool_guidance_is_opt_in_and_scoped_to_document_tasks():
    """Only an enabled verifier-backed task receives the tool requirement."""
    default_system, _ = _sent(_agent(_task(preference_md=PREFERENCE_MD)))
    tool_system, _ = _sent(
        _agent(
            _task(preference_md=PREFERENCE_MD),
            programmatic_preference_tool=True,
        )
    )
    numeric_system, _ = _sent(
        _agent(
            _task(preference_md=None),
            programmatic_preference_tool=True,
        )
    )

    assert CALENDAR_PROGRAMMATIC_PREFERENCE_TOOL_GUIDANCE not in default_system
    assert tool_system.count(CALENDAR_PROGRAMMATIC_PREFERENCE_TOOL_GUIDANCE) == 1
    assert CALENDAR_PROGRAMMATIC_PREFERENCE_TOOL_GUIDANCE not in numeric_system


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


def test_advocacy_and_preference_guidance_are_independent():
    """The procedure remains testable when the tag explanation is absent."""
    agent = CalendarOpenClawAgent(
        task=_task(preference_md=PREFERENCE_MD),
        model="anthropic/claude-opus-4-8",
        preference_guidance=False,
        advocacy_guidance=True,
    )

    system, _ = _sent(agent)

    assert CALENDAR_ADVOCACY_GUIDANCE in system
    assert CALENDAR_PREFERENCE_GUIDANCE not in system


def test_programmatic_tool_and_preference_guidance_are_independent():
    """The helper requirement remains when tag guidance is removed."""
    agent = CalendarOpenClawAgent(
        task=_task(preference_md=PREFERENCE_MD),
        model="anthropic/claude-opus-4-8",
        preference_guidance=False,
        programmatic_preference_tool=True,
    )

    system, _ = _sent(agent)

    assert CALENDAR_PROGRAMMATIC_PREFERENCE_TOOL_GUIDANCE in system
    assert CALENDAR_PREFERENCE_GUIDANCE not in system


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
        advocacy_guidance=False,
    )

    assert _sent(_agent(task)) == _sent(explicit)


# --- Stock OpenClaw arm -----------------------------------------------------
#
# prompt_delivery="user" is the harness as it ships: OpenClaw's own ~36 KB
# system prompt stands and the benchmark says everything it has to say in the
# opening user turn, which OpenClaw labels as untrusted sender metadata. It is
# the baseline the system-prompt arms are measured against.


def _stock(**kwargs) -> CalendarOpenClawAgent:
    agent = CalendarOpenClawAgent(
        task=_task(preference_md=PREFERENCE_MD),
        model="anthropic/claude-opus-4-8",
        prompt_delivery="user",
        **kwargs,
    )
    agent.system_prompt = get_system_prompt("none")
    return agent


def test_the_stock_arm_sends_no_system_prompt():
    """Returning None is what leaves OpenClaw's own prompt in place."""
    assert _stock()._system_prompt_message() is None


def test_the_stock_arm_moves_the_same_text_into_the_user_turn():
    """Only the channel changes: no instruction is added, dropped, or reworded."""
    system, user = _sent(_agent(_task(preference_md=PREFERENCE_MD)))

    stock_user = _stock()._opening_message()

    assert stock_user == f"{system.strip()}\n\n{user}"


def test_the_stock_arm_still_honors_the_guidance_flag():
    """It is the one prompt factor swept in this arm, so it has to bite."""
    with_guidance = _stock(preference_guidance=True)._opening_message()
    without = _stock(preference_guidance=False)._opening_message()

    assert CALENDAR_PREFERENCE_GUIDANCE in with_guidance
    assert CALENDAR_PREFERENCE_GUIDANCE not in without
    # The preference itself is not part of that treatment.
    assert "<user_preference>" in without


def test_the_stock_arm_moves_advocacy_guidance_into_the_user_turn():
    """The treatment follows the existing delivery factor rather than patching stock."""
    agent = _stock(advocacy_guidance=True)

    assert agent._system_prompt_message() is None
    assert agent._opening_message().count(CALENDAR_ADVOCACY_GUIDANCE) == 1


def test_the_stock_arm_moves_programmatic_tool_guidance_into_the_user_turn():
    """The helper requirement follows the existing delivery treatment."""
    agent = _stock(programmatic_preference_tool=True)

    assert agent._system_prompt_message() is None
    assert agent._opening_message().count(CALENDAR_PROGRAMMATIC_PREFERENCE_TOOL_GUIDANCE) == 1


def test_delivery_defaults_to_the_system_channel():
    """The stock arm is the deviation, so it has to be asked for explicitly."""
    assert _agent(_task(preference_md=PREFERENCE_MD))._system_prompt_message() is not None
