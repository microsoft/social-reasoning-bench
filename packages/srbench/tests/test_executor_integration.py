"""End-to-end integration tests for the agent-driven executors.

Each test runs a full ``execute_task`` with scripted agents inside an
``asyncio.timeout`` guard, so a coordination regression that reintroduces a
hang fails loudly as a timeout instead of blocking the suite forever.

The scripted client returns real ``SRBenchChatCompletionMessage`` objects so
the agent's parse / ``to_input_dict`` / ``model_copy`` paths exercise
production code.
"""

import asyncio
import json

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from srbench.benchmarks.calendar_scheduling.executor import (
    execute_task as calendar_execute_task,
)
from srbench.benchmarks.calendar_scheduling.types import (
    CalendarAssistant,
    CalendarRequestor,
    CalendarTask,
    Meeting,
)
from srbench.benchmarks.marketplace.executor import (
    execute_task as marketplace_execute_task,
)
from srbench.benchmarks.marketplace.types import MarketplaceTask, Product, RoleConfig
from srbench_llm import SRBenchModelClient
from srbench_llm.types import SRBenchChatCompletionMessage

# A generous outer bound. A healthy run finishes in well under a second; this
# only exists so a reintroduced deadlock fails as a timeout instead of hanging.
_GUARD_SECONDS = 10.0


class ScriptedModelClient(SRBenchModelClient):
    """A model client that replays a fixed queue of tool calls.

    Calls without ``tools`` (the counterparty's forced-opening text generation
    and any explicit-CoT step) return ``opening_text``. Calls with ``tools``
    pop the next scripted ``(tool_name, arguments)`` pair; once the script is
    exhausted it falls back to ``Wait`` so the agent parks harmlessly until
    the executor's termination race cancels it.
    """

    def __init__(
        self,
        tool_script: list[tuple[str, dict]],
        opening_text: str = "Hello.",
    ) -> None:
        super().__init__()
        self._script = list(tool_script)
        self._i = 0
        self._opening_text = opening_text
        self.tool_calls_made = 0

    async def acomplete(self, model, messages, *, tools=None, **kwargs):  # type: ignore[override]
        # Always yield so the executor's termination race gets a turn between
        # actions; without this an exhausted agent could spin synchronously.
        await asyncio.sleep(0)
        if not tools:
            return _text_message(self._opening_text)
        if self._i < len(self._script):
            name, arguments = self._script[self._i]
            self._i += 1
        else:
            name, arguments = ("Wait", {})
        self.tool_calls_made += 1
        return _tool_message(name, arguments, call_id=f"call-{self.tool_calls_made}")


def _text_message(text: str) -> SRBenchChatCompletionMessage:
    return SRBenchChatCompletionMessage(role="assistant", content=text)


def _tool_message(name: str, arguments: dict, *, call_id: str) -> SRBenchChatCompletionMessage:
    return SRBenchChatCompletionMessage(
        role="assistant",
        content=None,
        tool_calls=[
            ChatCompletionMessageToolCall(
                id=call_id,
                type="function",
                function=Function(name=name, arguments=json.dumps(arguments)),
            )
        ],
    )


def _calendar_task() -> CalendarTask:
    requested = Meeting(
        uid="sync-001",
        title="Project Sync",
        description="Align on Q3.",
        organizer="bob@external.com",
        date="2024-01-15",
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
            calendar=[],
            preferences=[],
        ),
        assistant=CalendarAssistant(
            name="Alice Assistant",
            email="alice@example.com",
            instruction_message="Manage Alice's calendar.",
            calendar=[],
            contacts=[],
            preferences=[],
        ),
    )


async def _run_calendar_task(
    assistant_client: SRBenchModelClient, requestor_client: SRBenchModelClient
):
    async with asyncio.timeout(_GUARD_SECONDS):
        return await calendar_execute_task(
            task=_calendar_task(),
            assistant_model="scripted",
            assistant_client=assistant_client,
            requestor_model="scripted",
            requestor_client=requestor_client,
            max_actions_per_agent=10,
            system_prompt=None,
            assistant_explicit_cot=False,
            requestor_explicit_cot=False,
            expose_preferences=False,
        )


async def test_calendar_execute_task_ends_on_end_conversation():
    """A scripted calendar run terminates cleanly on EndConversation."""
    # Assistant accepts the forced request, then ends the conversation.
    assistant_client = ScriptedModelClient(
        tool_script=[
            ("ReplyMeeting", {"meeting_uid": "sync-001", "status": "ACCEPTED", "message": "Sure!"}),
            ("EndConversation", {"reason": "Meeting scheduled."}),
        ]
    )
    # Requestor just waits; its Wait is released when the assistant ends.
    requestor_client = ScriptedModelClient(tool_script=[])

    result = await _run_calendar_task(assistant_client, requestor_client)

    assert result.error is None
    assert result.max_rounds_reached is False
    # The forced request plus the assistant's accept means the meeting is on
    # both calendars.
    assert any(m.uid == "sync-001" for m in result.final_assistant_calendar)
    assert any(m.uid == "sync-001" for m in result.final_requestor_calendar)


def _assert_well_formed_transcript(context: list) -> None:
    """Every assistant tool call must be followed by a matching tool result."""
    for i, message in enumerate(context):
        if message.get("role") != "assistant" or not message.get("tool_calls"):
            continue
        follower = context[i + 1] if i + 1 < len(context) else None
        assert follower is not None and follower.get("role") == "tool", (
            f"Dangling tool call at message {i}: {message}"
        )


async def test_calendar_wait_wakes_on_counterpart_reply():
    """The requestor's Wait must wake on the assistant's reply, not hang.

    If waking regressed, both agents would end up blocked and the run would
    finish as a stalemate (max_rounds_reached True) instead of the clean end.
    Regardless of how the race between the wake and the end lands, both
    transcripts must remain well-formed tool-call histories.
    """
    assistant_client = ScriptedModelClient(
        tool_script=[
            ("ReplyMeeting", {"meeting_uid": "sync-001", "status": "ACCEPTED", "message": "Sure!"}),
            ("EndConversation", {"reason": "Scheduled."}),
        ]
    )
    requestor_client = ScriptedModelClient(tool_script=[])

    result = await _run_calendar_task(assistant_client, requestor_client)

    assert result.error is None
    assert result.max_rounds_reached is False
    _assert_well_formed_transcript(result.assistant_context)
    _assert_well_formed_transcript(result.requestor_context)


async def test_calendar_stalemate_is_detected():
    """Both agents waiting with nothing pending ends the run, not hangs it.

    The assistant never responds to the forced request (it just waits), so
    once both agents are blocked the environment must declare a stalemate.
    """
    result = await _run_calendar_task(
        ScriptedModelClient(tool_script=[]),
        ScriptedModelClient(tool_script=[]),
    )

    assert result.max_rounds_reached is True
    assert result.error is None


def _marketplace_task() -> MarketplaceTask:
    return MarketplaceTask(
        id=1,
        product=Product(name="Industrial Widget", listed_price=550.0),
        seller=RoleConfig(
            instruction_message="Sell the widget for as much as possible.",
            reservation_price=400.0,
        ),
        buyer=RoleConfig(
            instruction_message="Buy the widget for a fair price.",
            reservation_price=600.0,
        ),
    )


async def test_marketplace_execute_task_ends_on_accept_and_end():
    """A scripted marketplace run reaches a deal then ends cleanly."""
    # Buyer accepts the seller's forced opening offer (id 1), then ends.
    buyer_client = ScriptedModelClient(
        tool_script=[
            ("AcceptOffer", {"offer_id": 1, "message": "Deal."}),
            ("EndConversation", {"reason": "Deal reached."}),
        ]
    )
    # Seller waits after its forced opening offer.
    seller_client = ScriptedModelClient(tool_script=[])

    async with asyncio.timeout(_GUARD_SECONDS):
        result = await marketplace_execute_task(
            task=_marketplace_task(),
            buyer_model="scripted",
            seller_model="scripted",
            buyer_client=buyer_client,
            seller_client=seller_client,
            buyer_explicit_cot=False,
            seller_explicit_cot=False,
            max_actions_per_agent=10,
        )

    assert result.error is None
    assert result.outcome.deal_reached is True
    assert result.outcome.deal_price == 550.0
    assert result.outcome.ended_by == "buyer"
    assert result.outcome.end_reason == "Deal reached."
    assert result.invalid_actions == 0


async def test_marketplace_stalemate_is_detected():
    """Both marketplace agents waiting ends with a harness stalemate outcome."""
    async with asyncio.timeout(_GUARD_SECONDS):
        result = await marketplace_execute_task(
            task=_marketplace_task(),
            buyer_model="scripted",
            seller_model="scripted",
            buyer_client=ScriptedModelClient(tool_script=[]),
            seller_client=ScriptedModelClient(tool_script=[]),
            buyer_explicit_cot=False,
            seller_explicit_cot=False,
            max_actions_per_agent=10,
        )

    assert result.outcome.deal_reached is False
    assert result.outcome.ended_by == "max_rounds"
    assert result.outcome.end_reason is not None
    assert "stalemate" in result.outcome.end_reason
