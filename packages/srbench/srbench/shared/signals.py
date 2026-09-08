"""Coordination primitives for agent-driven benchmark conversations.

In the agent-driven design each agent owns its run loop and interacts with the
environment only through tools. Nothing schedules turns, so the environment
needs a small coordination layer to answer three questions:

- When should a blocked ``Wait`` wake up? (the counterpart acted)
- When is the conversation over? (``EndConversation``, or an agent's budget)
- When can the conversation never progress again? (every agent is blocked
  waiting with no pending notification -- a stalemate)

:class:`ConversationSignals` owns that state. Both benchmark environments hold
one instance and expose it to their executor.
"""

from __future__ import annotations

import asyncio
from typing import Any, Coroutine, Sequence


class ConversationSignals:
    """Wake/end coordination between concurrently running agents.

    Each registered participant gets a "new content" event which the
    environment sets via :meth:`notify` when something arrives for them
    (an email delivery, a counterpart offer). A participant executing a
    blocking ``Wait`` awaits :meth:`wait_for_activity`, which races its
    content event against the conversation-level :attr:`end_event`.

    Stalemate detection: if a participant enters :meth:`wait_for_activity`
    while every other participant is already waiting and no content event is
    pending, no agent can ever be woken, so the conversation is ended with
    reason ``"stalemate"`` instead of hanging forever.
    """

    def __init__(self) -> None:
        self._events: dict[str, asyncio.Event] = {}
        self._waiting: set[str] = set()
        self.end_event: asyncio.Event = asyncio.Event()
        self.end_reason: str | None = None

    def register(self, owner: str) -> None:
        """Create the content event for ``owner`` if not already registered.

        Args:
            owner: Stable participant key (email address or role name).
        """
        self._events.setdefault(owner, asyncio.Event())

    def notify(self, owner: str) -> None:
        """Mark that new content is available for ``owner``, waking their Wait.

        Args:
            owner: Participant key to notify. Unregistered keys are ignored so
                environments can notify passive addresses (e.g. an emailed
                attendee that is not an active agent).
        """
        event = self._events.get(owner)
        if event is not None:
            event.set()

    def clear(self, owner: str) -> None:
        """Clear a pending :meth:`notify` for ``owner`` without waiting.

        The inverse of :meth:`notify`. For a harness that surfaces content
        to an agent out of band, this drops the pending wake so the agent's
        next ``Wait`` does not fire spuriously for content it has already
        seen. The executors deliver everything through tools and leave the
        wake pending, so they no longer call this.

        Args:
            owner: Participant key whose pending notification to clear.
        """
        event = self._events.get(owner)
        if event is not None:
            event.clear()

    def end(self, *, reason: str) -> None:
        """Record the end of the conversation and wake everything blocked on it.

        Idempotent: only the first call records its reason.

        Args:
            reason: Why the conversation ended. Agent-initiated ends carry the
                agent's stated reason; harness-initiated ends use one of
                ``"agent_stopped"``, ``"stalemate"``, ``"cancelled"``, or
                ``"error"``.
        """
        if self.end_event.is_set():
            return
        self.end_reason = reason
        self.end_event.set()

    async def wait_for_activity(self, owner: str) -> bool:
        """Block until ``owner`` is notified or the conversation ends.

        Args:
            owner: Registered participant key entering the wait.

        Returns:
            ``True`` if new content arrived (the pending notification is
            consumed), ``False`` if the conversation ended first.
        """
        event = self._events[owner]
        self._waiting.add(owner)
        try:
            if not event.is_set() and not self.end_event.is_set() and self._stalled():
                self.end(reason="stalemate")
            waiters = [
                asyncio.create_task(event.wait()),
                asyncio.create_task(self.end_event.wait()),
            ]
            try:
                await asyncio.wait(waiters, return_when=asyncio.FIRST_COMPLETED)
            finally:
                for task in waiters:
                    task.cancel()
                await asyncio.gather(*waiters, return_exceptions=True)
            if self.end_event.is_set():
                return False
            event.clear()
            return True
        finally:
            self._waiting.discard(owner)

    def _stalled(self) -> bool:
        """Return True when every registered participant is blocked with no wake pending."""
        return len(self._waiting) == len(self._events) and not any(
            event.is_set() for event in self._events.values()
        )


async def run_agents_until_end(
    agent_runs: Sequence[Coroutine[Any, Any, Any]],
    *,
    signals: ConversationSignals,
    cancel_event: asyncio.Event | None = None,
) -> None:
    """Run agent loops concurrently until the conversation ends.

    Spawns every coroutine in ``agent_runs`` as a task and races them against
    the conversation's end signal (and the optional external ``cancel_event``)
    with ``FIRST_COMPLETED``, then cancels and drains the losers. Whatever
    resolves the race first determines the recorded end reason:

    - ``signals.end_event`` fired: the reason is already recorded (e.g. an
      agent executed ``EndConversation``, or a stalemate was detected).
    - ``cancel_event`` fired: ``"cancelled"``.
    - an agent's run raised: the exception is re-raised for the executor to
      record.
    - an agent's run returned (its action budget was exhausted):
      ``"agent_stopped"``.

    Args:
        agent_runs: One coroutine per agent, typically
            ``agent.run(invoke_tool, tools)``.
        signals: The environment's conversation signals.
        cancel_event: Optional external cancellation signal to include in the race.
    """
    agent_tasks = [asyncio.create_task(run) for run in agent_runs]
    watchers = [asyncio.create_task(signals.end_event.wait())]
    if cancel_event is not None:
        watchers.append(asyncio.create_task(cancel_event.wait()))
    all_tasks = [*agent_tasks, *watchers]
    try:
        await asyncio.wait(all_tasks, return_when=asyncio.FIRST_COMPLETED)
    finally:
        for task in all_tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*all_tasks, return_exceptions=True)

    if cancel_event is not None and cancel_event.is_set():
        signals.end(reason="cancelled")
    for task in agent_tasks:
        if not task.cancelled():
            error = task.exception()
            if error is not None:
                raise error
    if not signals.end_event.is_set():
        signals.end(reason="agent_stopped")
