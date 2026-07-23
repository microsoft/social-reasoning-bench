"""Bring-your-own-agent (BYOA) tests.

Covers the three pieces that make a user-provided assistant agent work end
to end. The protocol hierarchy (BaseAgent -> BaseAssistantAgent /
BaseCounterpartAgent -> benchmark agents), the import-string loader, and the
executors' ``*_agent_factory`` path, where a custom agent that only
implements ``run(invoke_tool, tools)`` drives a full task and evaluation
still works from the environment's action trace.
"""

import asyncio
import textwrap

import pytest
from srbench.benchmarks.calendar_scheduling.agents import (
    CalendarAssistantAgent,
    CalendarRequestorAgent,
)
from srbench.benchmarks.calendar_scheduling.environment.actions import (
    EndConversation,
    ListMeetings,
    ReplyMeeting,
    RequestMeeting,
    Wait,
)
from srbench.benchmarks.calendar_scheduling.evaluation.due_diligence.reasonable_agent import (
    CalendarReasonableAssistant,
)
from srbench.benchmarks.calendar_scheduling.executor import (
    execute_task as calendar_execute_task,
)
from srbench.benchmarks.calendar_scheduling.types import (
    CalendarActionTrace,
    CalendarAssistant,
    CalendarAssistantTask,
    CalendarExecutionResult,
    CalendarRequestor,
    CalendarTask,
    Meeting,
    TimeSlotPreference,
)
from srbench.benchmarks.marketplace.agents import BuyerAgent, SellerAgent
from srbench.benchmarks.marketplace.executor import (
    execute_task as marketplace_execute_task,
)
from srbench.benchmarks.marketplace.types import (
    MarketplaceBuyerTask,
    MarketplaceTask,
    Product,
    RoleConfig,
)
from srbench.shared import (
    BaseAgent,
    BaseAssistantAgent,
    BaseCounterpartAgent,
    LLMAgent,
    load_agent_class,
)
from test_executor_integration import ScriptedModelClient

_GUARD_SECONDS = 10.0


# ------------------------------------------------------------------ #
# Protocol hierarchy
# ------------------------------------------------------------------ #


def test_base_agent_only_requires_run():
    assert BaseAgent.__abstractmethods__ == frozenset({"run"})


def test_assistant_protocol_adds_nothing_beyond_run():
    assert BaseAssistantAgent.__abstractmethods__ == frozenset({"run"})


def test_counterpart_protocol_requires_forced_opening_hooks():
    assert BaseCounterpartAgent.__abstractmethods__ == frozenset(
        {"run", "generate_text_response", "add_forced_action"}
    )


def test_builtin_agents_implement_role_protocols():
    assert issubclass(CalendarAssistantAgent, BaseAssistantAgent)
    assert issubclass(CalendarRequestorAgent, BaseCounterpartAgent)
    assert issubclass(BuyerAgent, BaseAssistantAgent)
    assert issubclass(SellerAgent, BaseCounterpartAgent)
    for cls in (CalendarAssistantAgent, CalendarRequestorAgent, BuyerAgent, SellerAgent):
        assert issubclass(cls, LLMAgent)
        assert issubclass(cls, BaseAgent)


# ------------------------------------------------------------------ #
# Import-string loader
# ------------------------------------------------------------------ #


def test_load_agent_class_from_import_string(tmp_path, monkeypatch):
    """A class is loadable with 'my_pkg.my_mod:MyClass' syntax."""
    pkg = tmp_path / "my_byoa_pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text('"""Test package."""\n')
    (pkg / "my_mod.py").write_text(
        textwrap.dedent(
            """
            from srbench.shared import BaseAssistantAgent


            class MyAgent(BaseAssistantAgent):
                def __init__(self, **kwargs):
                    self.kwargs = kwargs

                async def run(self, invoke_tool, tools):
                    pass


            class NotAnAgent:
                pass
            """
        )
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    cls = load_agent_class("my_byoa_pkg.my_mod:MyAgent", expected=BaseAssistantAgent)
    assert issubclass(cls, BaseAssistantAgent)
    assert cls.__name__ == "MyAgent"

    with pytest.raises(TypeError, match="not a subclass"):
        load_agent_class("my_byoa_pkg.my_mod:NotAnAgent", expected=BaseAssistantAgent)

    with pytest.raises(AttributeError, match="no attribute"):
        load_agent_class("my_byoa_pkg.my_mod:Missing", expected=BaseAssistantAgent)


def test_load_agent_class_rejects_malformed_specs():
    with pytest.raises(ValueError, match="my_pkg.my_mod:MyClass"):
        load_agent_class("just_a_module", expected=BaseAssistantAgent)
    with pytest.raises(ValueError):
        load_agent_class(":MyClass", expected=BaseAssistantAgent)
    with pytest.raises(ValueError):
        load_agent_class("my_mod:", expected=BaseAssistantAgent)
    with pytest.raises(ModuleNotFoundError):
        load_agent_class("definitely_not_a_module:MyClass", expected=BaseAssistantAgent)


# ------------------------------------------------------------------ #
# Custom calendar assistant end to end
# ------------------------------------------------------------------ #


class ScriptedCalendarAssistant(BaseAssistantAgent):
    """A minimal custom assistant that only implements run.

    It waits for the opening request (delivered as its Wait result, not
    pushed into any context), accepts the meeting, and ends the
    conversation.
    """

    def __init__(self, *, task):
        self.task = task
        self.granted_tools: list | None = None
        self.wait_result: str | None = None

    async def run(self, invoke_tool, tools):
        self.granted_tools = tools
        self.wait_result = await invoke_tool("Wait", {})
        await invoke_tool(
            "ReplyMeeting",
            {"meeting_uid": "sync-001", "status": "ACCEPTED", "message": "Sure!"},
        )
        await invoke_tool("EndConversation", {"reason": "Meeting scheduled."})


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


async def test_calendar_byoa_assistant_drives_full_task():
    """A custom assistant built from only run(invoke_tool, tools) completes a task."""
    factories_built: list[ScriptedCalendarAssistant] = []

    def factory(**kwargs):
        agent = ScriptedCalendarAssistant(**kwargs)
        factories_built.append(agent)
        return agent

    async with asyncio.timeout(_GUARD_SECONDS):
        result = await calendar_execute_task(
            task=_calendar_task(),
            assistant_model=None,
            assistant_client=ScriptedModelClient(tool_script=[]),
            requestor_model="scripted",
            requestor_client=ScriptedModelClient(tool_script=[]),
            max_actions_per_agent=10,
            system_prompt=None,
            assistant_explicit_cot=False,
            requestor_explicit_cot=False,
            expose_preferences=False,
            assistant_agent_factory=factory,
        )

    assert result.error is None
    assert result.max_rounds_reached is False

    # The factory received the documented keyword argument.
    agent = factories_built[0]
    assert agent.task.assistant.email == "alice@example.com"
    assert agent.task.max_actions == 10

    # The environment granted the assistant its tool space through run().
    assert agent.granted_tools is not None
    granted_names = {t["function"]["name"] for t in agent.granted_tools}
    assert "ReplyMeeting" in granted_names
    assert "EndConversation" in granted_names

    # The forced opening request reached the agent through its first Wait.
    assert agent.wait_result is not None
    assert "Project Sync" in agent.wait_result

    # The accept landed on both calendars.
    assert any(m.uid == "sync-001" for m in result.final_assistant_calendar)
    assert any(m.uid == "sync-001" for m in result.final_requestor_calendar)

    # The environment recorded the custom agent's actions even though the
    # agent exposes no transcript.
    assert result.assistant_context == []
    assistant_actions = [
        t.action_type for t in result.action_trace if t.actor == "alice@example.com"
    ]
    assert assistant_actions == ["Wait", "ReplyMeeting", "EndConversation"]


# ------------------------------------------------------------------ #
# Custom marketplace buyer end to end
# ------------------------------------------------------------------ #


class ScriptedBuyer(BaseAssistantAgent):
    """A minimal custom buyer that accepts the opening offer and ends."""

    def __init__(self, *, task):
        self.task = task

    async def run(self, invoke_tool, tools):
        await invoke_tool("Wait", {})
        await invoke_tool("AcceptOffer", {"offer_id": 1, "message": "Deal."})
        await invoke_tool("EndConversation", {"reason": "Deal reached."})


async def test_marketplace_byoa_buyer_drives_full_task():
    task = MarketplaceTask(
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

    async with asyncio.timeout(_GUARD_SECONDS):
        result = await marketplace_execute_task(
            task=task,
            buyer_model=None,
            seller_model="scripted",
            buyer_client=ScriptedModelClient(tool_script=[]),
            seller_client=ScriptedModelClient(tool_script=[]),
            buyer_explicit_cot=False,
            seller_explicit_cot=False,
            max_actions_per_agent=10,
            buyer_agent_factory=lambda **kwargs: ScriptedBuyer(**kwargs),
        )

    assert result.error is None
    assert result.outcome.deal_reached is True
    assert result.outcome.deal_price == 550.0
    assert result.outcome.ended_by == "buyer"
    assert result.buyer_context == []


# ------------------------------------------------------------------ #
# Evaluation from the action trace
# ------------------------------------------------------------------ #


def _trace_entry(actor: str, action) -> CalendarActionTrace:
    return CalendarActionTrace(
        actor=actor,
        action_type=type(action).__name__,
        payload=action.model_dump(),
        result="ok",
        valid=True,
    )


def test_reasonable_assistant_scores_from_action_trace():
    """Due diligence scoring needs no agent transcript, only the trace."""
    task = _calendar_task()
    task.assistant.preferences = [
        TimeSlotPreference(start_time="14:00", end_time="15:00", score=0.9),
        TimeSlotPreference(start_time="09:00", end_time="10:00", score=0.4),
    ]

    request = RequestMeeting(
        message="Please meet.",
        uid="sync-001",
        title="Project Sync",
        description="Align on Q3.",
        organizer="bob@external.com",
        date="2024-01-15",
        start="14:00",
        end="15:00",
        attendees=["alice@example.com"],
    )
    trace = [
        _trace_entry("bob@external.com", request),
        _trace_entry("alice@example.com", Wait()),
        _trace_entry("alice@example.com", ListMeetings()),
        _trace_entry(
            "alice@example.com",
            ReplyMeeting(meeting_uid="sync-001", status="ACCEPTED", message="Sure!"),
        ),
        _trace_entry("alice@example.com", EndConversation(reason="Scheduled.")),
    ]
    result = CalendarExecutionResult(task=task, action_trace=trace)

    # The assistant checked its calendar and accepted its top-preference
    # slot, matching the reasonable policy on both decisions.
    assert CalendarReasonableAssistant(result).score() == 1.0


def test_reasonable_assistant_ignores_invalid_actions():
    """Actions the environment rejected carry no decision to score."""
    task = _calendar_task()
    task.assistant.preferences = [
        TimeSlotPreference(start_time="14:00", end_time="15:00", score=0.9),
    ]
    rejected = CalendarActionTrace(
        actor="alice@example.com",
        action_type="ReplyMeeting",
        payload=ReplyMeeting(meeting_uid="nope", status="ACCEPTED").model_dump(),
        result="Error: unknown meeting",
        valid=False,
    )
    result = CalendarExecutionResult(task=task, action_trace=[rejected])

    assert CalendarReasonableAssistant(result).score() is None


# ------------------------------------------------------------------ #
# BYOA agent kwargs (model / reasoning effort per variant)
# ------------------------------------------------------------------ #


def _write_recording_agent(tmp_path, monkeypatch) -> str:
    """Create a loadable BYOA agent that records its constructor kwargs."""
    pkg = tmp_path / "kwargs_byoa_pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text('"""Test package."""\n')
    (pkg / "rec.py").write_text(
        textwrap.dedent(
            """
            from srbench.shared import BaseAssistantAgent


            class RecordingAgent(BaseAssistantAgent):
                def __init__(self, *, task, model=None, reasoning_effort=None):
                    self.task = task
                    self.model = model
                    self.reasoning_effort = reasoning_effort

                async def run(self, invoke_tool, tools):
                    pass
            """
        )
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    return "kwargs_byoa_pkg.rec:RecordingAgent"


def test_agent_kwargs_default_to_empty_dict():
    """A None kwargs value (the CLI default) coerces to an empty dict."""
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig
    from srbench.benchmarks.marketplace.config import MarketplaceRunConfig

    # The CLI passes None (argparse default) through model_validate(vars(args)).
    cal = CalendarRunConfig.model_validate(
        {"paths": ["x"], "assistant_agent": "a:B", "assistant_agent_kwargs": None}
    )
    assert cal.assistant_agent_kwargs == {}
    assert CalendarRunConfig(paths=["x"]).assistant_agent_kwargs == {}

    mkt = MarketplaceRunConfig.model_validate(
        {"paths": ["x"], "buyer_agent": "a:B", "buyer_agent_kwargs": None}
    )
    assert mkt.buyer_agent_kwargs == {}
    assert MarketplaceRunConfig(paths=["x"]).buyer_agent_kwargs == {}


def test_calendar_setup_forwards_agent_kwargs(tmp_path, monkeypatch):
    """CalendarBenchmark.setup binds assistant_agent_kwargs into the factory."""
    from srbench.benchmarks.calendar_scheduling.benchmark import CalendarBenchmark
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

    spec = _write_recording_agent(tmp_path, monkeypatch)
    config = CalendarRunConfig(
        paths=["x"],
        assistant_agent=spec,
        assistant_agent_kwargs={"model": "claude-sonnet-4-6", "reasoning_effort": "high"},
    )

    bench = CalendarBenchmark.__new__(CalendarBenchmark)
    bench.setup(config)

    agent = bench.assistant_agent_factory(task="TASK")
    assert agent.task == "TASK"
    assert agent.model == "claude-sonnet-4-6"
    assert agent.reasoning_effort == "high"


def test_marketplace_setup_forwards_agent_kwargs(tmp_path, monkeypatch):
    """MarketplaceBenchmark.setup binds buyer_agent_kwargs into the factory."""
    from srbench.benchmarks.marketplace.benchmark import MarketplaceBenchmark
    from srbench.benchmarks.marketplace.config import MarketplaceRunConfig

    spec = _write_recording_agent(tmp_path, monkeypatch)
    config = MarketplaceRunConfig(
        paths=["x"],
        buyer_agent=spec,
        buyer_agent_kwargs={"model": "openai/gpt-5.4", "reasoning_effort": "medium"},
    )

    bench = MarketplaceBenchmark.__new__(MarketplaceBenchmark)
    bench.setup(config)

    agent = bench.buyer_agent_factory(task="TASK")
    assert agent.task == "TASK"
    assert agent.model == "openai/gpt-5.4"
    assert agent.reasoning_effort == "medium"


def test_setup_without_agent_leaves_factory_none(tmp_path, monkeypatch):
    """No BYOA agent set -> factory stays None (built-in path)."""
    from srbench.benchmarks.calendar_scheduling.benchmark import CalendarBenchmark
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

    config = CalendarRunConfig(paths=["x"], assistant_model="some-model")
    bench = CalendarBenchmark.__new__(CalendarBenchmark)
    bench.setup(config)
    assert bench.assistant_agent_factory is None
