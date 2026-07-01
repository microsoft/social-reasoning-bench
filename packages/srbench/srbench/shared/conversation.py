"""Coordination primitives for agent-driven benchmark conversations.

In the agent-driven design each agent owns its run loop and interacts with the
environment only through tools. Nothing schedules turns, so the environment
needs a small coordination layer to answer three questions:

- When should a blocked ``Wait`` wake up? (the counterpart acted)
- When is the conversation over? (``EndConversation``, budget, wall clock)
- When can the conversation never progress again? (every agent is blocked
  waiting with no pending notification -- a stalemate)

:class:`ConversationSignals` owns that state. Both benchmark environments hold
one instance and expose it to their executor.
"""

from __future__ import annotations

import asyncio


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
    reason ``"stalemate"`` instead of hanging until the wall-clock limit.
    """

    def __init__(self) -> None:
        self._events: dict[str, asyncio.Event] = {}
        self._waiting: set[str] = set()
        self.end_event: asyncio.Event = asyncio.Event()
        self.end_reason: str | None = None
        self.action_count: int = 0

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
        """Consume a pending notification for ``owner`` without waiting.

        Used by the executor after it injects already-read content into an
        agent's context at startup, so the agent's first ``Wait`` does not
        wake spuriously for content it has already seen.

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
                ``"agent_stopped"``, ``"max_wall_time"``, ``"stalemate"``,
                ``"cancelled"``, or ``"error"``.
        """
        if self.end_event.is_set():
            return
        self.end_reason = reason
        self.end_event.set()

    def count_action(self) -> int:
        """Increment and return the monotonic action counter (1-based).

        Returns:
            The new total number of actions executed in this conversation.
        """
        self.action_count += 1
        return self.action_count

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
