"""Tests for ConversationSignals wake/end/stalemate coordination.

Every waiting test runs under an asyncio timeout guard so a coordination
regression fails as a timeout instead of hanging the suite.
"""

import asyncio

import pytest
from srbench.benchmarks.calendar_scheduling.environment import (
    CalendarSchedulingEnvironment,
)
from srbench.benchmarks.marketplace.environment import MarketplaceEnvironment
from srbench.shared.conversation import ConversationSignals

_GUARD_SECONDS = 5.0


@pytest.fixture
def signals() -> ConversationSignals:
    s = ConversationSignals()
    s.register("alice")
    s.register("bob")
    return s


class TestNotifyAndWait:
    async def test_notify_before_wait_returns_immediately(self, signals):
        signals.notify("alice")
        async with asyncio.timeout(_GUARD_SECONDS):
            assert await signals.wait_for_activity("alice") is True

    async def test_notify_while_waiting_wakes(self, signals):
        async def notify_later():
            await asyncio.sleep(0)
            signals.notify("alice")

        async with asyncio.timeout(_GUARD_SECONDS):
            _, woke = await asyncio.gather(notify_later(), signals.wait_for_activity("alice"))
        assert woke is True

    async def test_notification_is_consumed_on_wake(self, signals):
        """After one wake the event is cleared, so the next Wait blocks again."""
        signals.notify("alice")
        async with asyncio.timeout(_GUARD_SECONDS):
            assert await signals.wait_for_activity("alice") is True

        second_wait = asyncio.create_task(signals.wait_for_activity("alice"))
        await asyncio.sleep(0)
        assert not second_wait.done(), "Wait must block until a fresh notification"
        signals.end(reason="test cleanup")
        async with asyncio.timeout(_GUARD_SECONDS):
            assert await second_wait is False

    async def test_notify_unregistered_owner_is_ignored(self, signals):
        signals.notify("charlie@nowhere.example")

    async def test_clear_consumes_pending_notification(self, signals):
        signals.notify("alice")
        signals.clear("alice")
        waiting = asyncio.create_task(signals.wait_for_activity("alice"))
        await asyncio.sleep(0)
        assert not waiting.done(), "Cleared notification must not wake the wait"
        signals.end(reason="test cleanup")
        async with asyncio.timeout(_GUARD_SECONDS):
            assert await waiting is False


class TestEnd:
    async def test_end_wakes_waiter_with_false(self, signals):
        waiting = asyncio.create_task(signals.wait_for_activity("alice"))
        await asyncio.sleep(0)
        signals.end(reason="done")
        async with asyncio.timeout(_GUARD_SECONDS):
            assert await waiting is False
        assert signals.end_reason == "done"

    async def test_end_is_idempotent(self, signals):
        signals.end(reason="first")
        signals.end(reason="second")
        assert signals.end_reason == "first"

    async def test_wait_after_end_returns_false_immediately(self, signals):
        signals.end(reason="done")
        async with asyncio.timeout(_GUARD_SECONDS):
            assert await signals.wait_for_activity("alice") is False


class TestStalemate:
    async def test_all_waiting_with_no_pending_content_ends_conversation(self, signals):
        async with asyncio.timeout(_GUARD_SECONDS):
            results = await asyncio.gather(
                signals.wait_for_activity("alice"),
                signals.wait_for_activity("bob"),
            )
        assert results == [False, False]
        assert signals.end_reason == "stalemate"

    async def test_pending_content_prevents_stalemate(self, signals):
        signals.notify("bob")
        async with asyncio.timeout(_GUARD_SECONDS):
            alice_task = asyncio.create_task(signals.wait_for_activity("alice"))
            await asyncio.sleep(0)
            assert await signals.wait_for_activity("bob") is True
        assert signals.end_reason is None
        signals.end(reason="test cleanup")
        async with asyncio.timeout(_GUARD_SECONDS):
            await alice_task


class TestActionCounter:
    def test_count_action_is_monotonic(self, signals):
        assert signals.count_action() == 1
        assert signals.count_action() == 2
        assert signals.action_count == 2


class TestEnvironmentWiring:
    async def test_calendar_email_delivery_notifies_recipient(self):
        env = CalendarSchedulingEnvironment()
        alice = env.create_agent_resources(owner="alice@example.com", allowed_date="2024-01-15")
        env.create_agent_resources(owner="bob@example.com", allowed_date="2024-01-15")

        alice.email.send(to="bob@example.com", subject="Hi", body="Hello Bob")
        async with asyncio.timeout(_GUARD_SECONDS):
            assert await env.signals.wait_for_activity("bob@example.com") is True

    def test_marketplace_roles_are_registered(self):
        env = MarketplaceEnvironment()
        env.create_agent_resources("buyer")
        env.create_agent_resources("seller")
        env.signals.notify("buyer")
        env.signals.clear("buyer")
