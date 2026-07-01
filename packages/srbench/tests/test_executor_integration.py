"""End-to-end integration tests for the agent-driven executors.

These are the coverage that was missing while the sequential executor shipped a
blocking ``Wait``: no test drove ``execute_task`` to completion, so a deadlock
was invisible. Each test runs a full task with scripted agents inside an
``asyncio.timeout`` guard, so a regression that reintroduces a hang fails loudly
instead of blocking the suite forever.

The scripted client returns real ``SRBenchChatCompletionMessage`` objects so the
agent's parse / ``to_input_dict`` / ``model_copy`` paths exercise production code.
"""

import asyncio

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
    exhausted it falls back to ``Wait`` so the agent parks harmlessly until the
    executor's termination race cancels it.
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
        # Always yield so the executor's end_event race gets a turn between
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
    import json

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


async def test_calendar_execute_task_ends_on_end_conversation():
    """A scripted calendar run terminates cleanly on EndConversation.

    Deadlock guard: the whole call runs inside asyncio.timeout, so a hang would
    surface as a TimeoutError rather than blocking the suite.
    """
    task = _calendar_task()
    # Assistant accepts the forced request, then ends the conversation.
    assistant_client = ScriptedModelClient(
        tool_script=[
            ("ReplyMeeting", {"meeting_uid": "sync-001", "status": "ACCEPTED", "message": "Sure!"}),
            ("EndConversation", {"reason": "Meeting scheduled."}),
        ]
    )
    # Requestor just waits; its Wait is released when the assistant ends.
    requestor_client = ScriptedModelClient(tool_script=[])

    async with asyncio.timeout(_GUARD_SECONDS):
        result = await calendar_execute_task(
            task=task,
            assistant_model="scripted",
            assistant_client=assistant_client,
            requestor_model="scripted",
            requestor_client=requestor_client,
            system_prompt=None,
            assistant_explicit_cot=False,
            requestor_explicit_cot=False,
            expose_preferences=False,
            max_actions_per_agent=10,
            max_wall_time_seconds=5.0,
        )

    assert result.error is None
    assert result.end_reason == "Meeting scheduled."
    assert result.total_actions > 0
    # The forced request plus the assistant's accept means the meeting is on
    # both calendars, accepted.
    assert any(m.uid == "sync-001" for m in result.final_assistant_calendar)


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
    task = _marketplace_task()
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
            task=task,
            buyer_model="scripted",
            seller_model="scripted",
            buyer_client=buyer_client,
            seller_client=seller_client,
            buyer_explicit_cot=False,
            seller_explicit_cot=False,
            max_actions_per_agent=10,
            max_wall_time_seconds=5.0,
        )

    assert result.error is None
    assert result.end_reason == "Deal reached."
    assert result.total_actions > 0
    assert result.outcome.deal_reached is True
    assert result.outcome.deal_price == 550.0


async def test_calendar_wait_wakes_then_ends():
    """The requestor's Wait must wake on the assistant's reply, not hang.

    This is the direct end-to-end proof of fix A (wake on ReplyMeeting) and
    fix C (EndConversation releases the counterpart). If either regressed, the
    requestor would sit on Wait until max_wall_time and end_reason would be
    ``max_wall_time`` instead of the clean reason.
    """
    task = _calendar_task()
    assistant_client = ScriptedModelClient(
        tool_script=[
            ("ReplyMeeting", {"meeting_uid": "sync-001", "status": "ACCEPTED", "message": "Sure!"}),
            ("EndConversation", {"reason": "Scheduled."}),
        ]
    )
    requestor_client = ScriptedModelClient(tool_script=[])

    async with asyncio.timeout(_GUARD_SECONDS):
        result = await calendar_execute_task(
            task=task,
            assistant_model="scripted",
            assistant_client=assistant_client,
            requestor_model="scripted",
            requestor_client=requestor_client,
            system_prompt=None,
            assistant_explicit_cot=False,
            requestor_explicit_cot=False,
            expose_preferences=False,
            max_actions_per_agent=10,
            max_wall_time_seconds=5.0,
        )

    assert result.end_reason == "Scheduled."
    assert result.end_reason != "max_wall_time"
