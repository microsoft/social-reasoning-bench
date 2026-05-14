"""CalendarSchedulingEnvironment factory for creating agent resources."""

from __future__ import annotations

import asyncio

from ..types import Contact, Email, Meeting
from .calendar import CalendarManager
from .email import EmailManager
from .resources import AgentResources


class CalendarSchedulingEnvironment:
    """Factory for creating agent resources with shared infrastructure.

    Uses EmailManager and CalendarManager to create agent resources with
    injected callbacks for cross-agent communication and calendar synchronization.

    Owns the conversation-level ``end_event`` (set by ``EndConversation`` and
    watched by the executor) and a per-owner ``new_content_event`` registry
    so blocked ``GetEmails`` calls can be woken up the moment a counterpart
    delivers mail.
    """

    def __init__(self) -> None:
        self._new_content_events: dict[str, asyncio.Event] = {}
        self._email_manager = EmailManager(on_delivery=self._notify_recipient)
        self._calendar_manager = CalendarManager()
        self.end_event: asyncio.Event = asyncio.Event()
        self.end_reason: str | None = None

    def _notify_recipient(self, recipient_email: str) -> None:
        """Wake up any agent blocked on GetEmails for ``recipient_email``."""
        event = self._new_content_events.get(recipient_email)
        if event is not None:
            event.set()

    def _new_content_event_for(self, owner: str) -> asyncio.Event:
        event = self._new_content_events.get(owner)
        if event is None:
            event = asyncio.Event()
            self._new_content_events[owner] = event
        return event

    def mark_ended(self, *, reason: str) -> None:
        """Record an end-of-conversation signal and wake up the executor.

        Idempotent: only the first call takes effect (subsequent calls are
        ignored). Called by ``AgentResources.execute(EndConversation(...))``
        and potentially by the executor when ``max_actions`` / wall-clock
        elapsed without an explicit EndConversation.
        """
        if self.end_event.is_set():
            return
        self.end_reason = reason
        self.end_event.set()

    def create_agent_resources(
        self,
        owner: str,
        allowed_date: str,
        initial_meetings: list[Meeting] | None = None,
        contacts: list[Contact] | None = None,
    ) -> AgentResources:
        """Create AgentResources for an agent.

        Args:
            owner: Email address of the agent
            initial_meetings: Optional list of meetings to pre-populate the calendar
            allowed_date: If set, RequestMeeting will only allow this date (ISO format)
            contacts: Optional list of contacts for the agent's address book

        Returns:
            AgentResources with calendar, email, and contacts configured
        """
        calendar = self._calendar_manager.create_calendar(owner, initial_meetings)
        email = self._email_manager.create_email(owner)
        new_content_event = self._new_content_event_for(owner)

        return AgentResources(
            owner=owner,
            calendar=calendar,
            email=email,
            allowed_date=allowed_date,
            contacts=contacts,
            new_content_event=new_content_event,
            env=self,
        )

    def get_all_emails(self) -> list[Email]:
        """Get all emails sent (for evaluation/debugging).

        Returns:
            List of all emails sent through the email manager.
        """
        return self._email_manager.get_all_emails()
