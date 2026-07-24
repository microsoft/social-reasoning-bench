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
from typing import TYPE_CHECKING, cast

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
    AssistantTask,
    BaseAgent,
    BaseAssistantAgent,
    BaseCounterpartAgent,
    LLMAgent,
    load_agent_class,
)
from test_executor_integration import ScriptedModelClient

if TYPE_CHECKING:
    from srbench_llm import SRBenchModelClient

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


def test_evaluator_surfaces_execution_error_without_scoring():
    """A failed execution short-circuits eval and reports the real error.

    When execution fails there is no trace to score, so the evaluator must not
    run the deterministic scorers (which would raise a misleading "no scorable
    decisions" error). Instead it returns an error result carrying the actual
    execution error, and never touches the judge client.
    """
    from srbench.benchmarks.calendar_scheduling.evaluation.evaluator import (
        evaluate_single_task,
    )

    task = _calendar_task()
    exec_error = (
        "Calendar execution error: openclaw exited with code 1; stderr tail: 'rate limited'"
    )
    result = CalendarExecutionResult(task=task, action_trace=[], error=exec_error)

    eval_result = asyncio.run(
        evaluate_single_task(
            result,
            judge_model="unused",
            judge_client=cast("SRBenchModelClient", None),
        )
    )

    assert eval_result.error == exec_error
    assert eval_result.appropriately_scheduled_or_notscheduled is False
    assert eval_result.scheduled_meeting is None


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


def test_calendar_agent_kwargs_mirror_reporting_fields():
    """A BYOA agent's model/effort surface on assistant_* reporting fields."""
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

    config = CalendarRunConfig(
        paths=["x"],
        assistant_agent="a:B",
        assistant_agent_kwargs={"model": "openai/gpt-5.5", "reasoning_effort": "high"},
    )
    assert config.assistant_model == "openai/gpt-5.5"
    assert config.assistant_reasoning_effort == "high"
    # Kwargs stay intact so they still forward to the agent constructor.
    assert config.assistant_agent_kwargs["model"] == "openai/gpt-5.5"


def test_marketplace_agent_kwargs_mirror_reporting_fields():
    """A BYOA agent's model/effort surface on buyer_* reporting fields."""
    from srbench.benchmarks.marketplace.config import MarketplaceRunConfig

    config = MarketplaceRunConfig(
        paths=["x"],
        buyer_agent="a:B",
        buyer_agent_kwargs={"model": "openai/gpt-5.4", "reasoning_effort": "medium"},
    )
    assert config.buyer_model == "openai/gpt-5.4"
    assert config.buyer_reasoning_effort == "medium"


def test_explicit_reporting_fields_win_over_agent_kwargs():
    """Explicit assistant_model/effort are not overwritten by agent kwargs."""
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

    config = CalendarRunConfig(
        paths=["x"],
        assistant_agent="a:B",
        assistant_model="explicit-model",
        assistant_reasoning_effort="low",
        assistant_agent_kwargs={"model": "openai/gpt-5.5", "reasoning_effort": "high"},
    )
    assert config.assistant_model == "explicit-model"
    assert config.assistant_reasoning_effort == "low"


def test_agent_kwargs_without_model_leaves_reporting_fields_none():
    """No model in kwargs -> reporting fields stay None (no false labels)."""
    from srbench.benchmarks.calendar_scheduling.config import CalendarRunConfig

    config = CalendarRunConfig(paths=["x"], assistant_agent="a:B", assistant_agent_kwargs={})
    assert config.assistant_model is None
    assert config.assistant_reasoning_effort is None


# ------------------------------------------------------------------ #
# OpenClaw agent robustness (retry + loud failure)
# ------------------------------------------------------------------ #


def _openclaw_agent(monkeypatch, *, max_retries=2):
    """Build an OpenClawAgent with a trivial task, retries configurable."""
    from srbench_agents import openclaw_agent as oc

    monkeypatch.setenv("SRBENCH_OPENCLAW_MAX_RETRIES", str(max_retries))
    return oc.OpenClawAgent(task=AssistantTask(max_actions=2)), oc


async def _instant_sleep(*_args, **_kwargs):
    """Drop-in for asyncio.sleep that returns immediately (no real delay)."""
    return None


class _FakeProc:
    def __init__(self):
        self.pid = 424242
        self.returncode = 0


def test_openclaw_retries_noop_then_succeeds(monkeypatch):
    """A no-op first attempt is retried; a subsequent engaged run succeeds."""
    agent, oc = _openclaw_agent(monkeypatch)

    spawned = {"n": 0}

    async def fake_spawn(*args, **kwargs):
        spawned["n"] += 1
        return _FakeProc()

    outcomes = iter(
        [
            oc._RunOutcome(
                returncode=0, stdout="", stderr="rate limited", timed_out=False, tool_calls=0
            ),
            oc._RunOutcome(returncode=0, stdout="ok", stderr="", timed_out=False, tool_calls=3),
        ]
    )

    async def fake_drive(proc):
        out = next(outcomes)
        agent._tool_calls = out.tool_calls
        return out

    monkeypatch.setattr(oc.asyncio, "create_subprocess_exec", fake_spawn)
    monkeypatch.setattr(agent, "_drive", fake_drive)
    monkeypatch.setattr(oc.asyncio, "sleep", _instant_sleep)

    asyncio.run(agent._run_agent_with_retries("srbench-deadbeef"))
    assert spawned["n"] == 2  # retried once


def test_openclaw_raises_loud_error_on_persistent_noop(monkeypatch):
    """Exhausted retries surface a clear error instead of an empty trace."""
    agent, oc = _openclaw_agent(monkeypatch, max_retries=1)

    async def fake_spawn(*args, **kwargs):
        return _FakeProc()

    async def fake_drive(proc):
        return oc._RunOutcome(
            returncode=0, stdout="nothing", stderr="", timed_out=False, tool_calls=0
        )

    monkeypatch.setattr(oc.asyncio, "create_subprocess_exec", fake_spawn)
    monkeypatch.setattr(agent, "_drive", fake_drive)
    monkeypatch.setattr(oc.asyncio, "sleep", _instant_sleep)

    with pytest.raises(RuntimeError, match="no MCP tool calls"):
        asyncio.run(agent._run_agent_with_retries("srbench-deadbeef"))


def test_openclaw_does_not_retry_after_engaging(monkeypatch):
    """Once the agent has acted, a failure is not retried (state is mutated)."""
    agent, oc = _openclaw_agent(monkeypatch, max_retries=3)

    spawned = {"n": 0}

    async def fake_spawn(*args, **kwargs):
        spawned["n"] += 1
        return _FakeProc()

    async def fake_drive(proc):
        # Engaged (made a tool call) but exited non-zero: must not retry.
        agent._tool_calls += 2
        return oc._RunOutcome(
            returncode=1, stdout="", stderr="boom", timed_out=False, tool_calls=agent._tool_calls
        )

    monkeypatch.setattr(oc.asyncio, "create_subprocess_exec", fake_spawn)
    monkeypatch.setattr(agent, "_drive", fake_drive)

    with pytest.raises(RuntimeError, match="exited with code 1"):
        asyncio.run(agent._run_agent_with_retries("srbench-deadbeef"))
    assert spawned["n"] == 1  # no retry after engaging
