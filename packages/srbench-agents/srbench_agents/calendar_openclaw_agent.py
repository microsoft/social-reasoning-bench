"""An OpenClaw agent that frames a calendar task the way the built-in agent does.

:class:`~srbench_agents.openclaw_agent.OpenClawAgent` is task-agnostic: it hands
the model its brief as a JSON dump of the task object. That is enough to
schedule a meeting, but it is not the prompt the built-in
``CalendarAssistantAgent`` sends, so a BYOA run would differ from a native run
in its framing as well as in its harness.

That difference is not cosmetic for natural-language preferences. The guidance
block explaining ``<user_preference>`` lives in the built-in agent's system
turn, and it opens by referring to a ``<user_preference>`` block in the user's
message — neither of which a JSON dump contains.

So this subclass builds its opening turn from
:func:`~srbench.benchmarks.calendar_scheduling.agents.assistant.build_assistant_messages`,
the same function the built-in agent uses, and prepends the BYOA ground rules
because OpenClaw's opening turn has no separate system-prompt channel. Sharing
that function is what keeps the two prompts from drifting apart.
"""

from __future__ import annotations

from srbench.benchmarks.calendar_scheduling.agents.assistant import build_assistant_messages
from srbench.benchmarks.calendar_scheduling.types import CalendarAssistantTask

from srbench_agents.openclaw_agent import OpenClawAgent
from srbench_agents.prompts import DEFAULT_ASSISTANT_SYSTEM_PROMPT

__all__ = ["CalendarOpenClawAgent"]

#: The shared ground rules promise a JSON briefing. This agent sends the
#: built-in agent's prose turns instead, so that one rule is substituted.
_JSON_BRIEFING_RULE = (
    "- Your private task briefing arrives as JSON in the first message. Read it "
    "carefully to understand who you are, your objective, and any constraints.\n"
)
_PROSE_BRIEFING_RULE = (
    "- Your private task briefing follows these rules, in this same message. Read "
    "it carefully to understand who you are, your objective, and any constraints.\n"
)


def ground_rules() -> str:
    """Return the BYOA ground rules, corrected for a prose briefing.

    Substituting one rule rather than restating all seven keeps a single copy of
    the shared text. The check turns an upstream rewording into a loud failure
    instead of leaving a false statement about JSON sitting in the prompt.

    Returns:
        The ground rules to prepend to the opening message.

    Raises:
        RuntimeError: If the shared prompt no longer contains the rule.
    """
    if _JSON_BRIEFING_RULE not in DEFAULT_ASSISTANT_SYSTEM_PROMPT:
        raise RuntimeError(
            "DEFAULT_ASSISTANT_SYSTEM_PROMPT no longer states how the briefing "
            "arrives. Re-check this agent's ground rules against it."
        )
    return DEFAULT_ASSISTANT_SYSTEM_PROMPT.replace(_JSON_BRIEFING_RULE, _PROSE_BRIEFING_RULE)


class CalendarOpenClawAgent(OpenClawAgent):
    """OpenClaw agent whose opening turn mirrors the built-in calendar assistant."""

    def _opening_message(self) -> str:
        """Return the BYOA ground rules followed by the assistant's own two turns.

        ``expose_preferences`` is fixed to ``True`` because a run that hides
        preferences has nothing to compare. Numeric and natural-language tasks
        are told apart by ``build_assistant_messages`` from the task itself, so
        one agent serves both arms and the numeric arm is provably free of the
        preference guidance.

        Returns:
            The full opening message to send to OpenClaw.

        Raises:
            TypeError: If this agent is used outside calendar scheduling.
        """
        task = self.task
        if not isinstance(task, CalendarAssistantTask):
            raise TypeError(
                f"{type(self).__name__} only handles calendar scheduling tasks, "
                f"got {type(task).__name__}."
            )
        system, instruction = build_assistant_messages(
            task,
            system_prompt=self.system_prompt,
            expose_preferences=True,
        )
        return "\n\n".join(part.strip() for part in [ground_rules(), system, instruction])
