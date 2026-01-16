"""CalendarSchedulingEnvironment factory for creating agent resources."""

from ..types import Contact, Email, Meeting
from .calendar import CalendarManager
from .email import EmailManager
from .resources import AgentResources


class CalendarSchedulingEnvironment:
    """Factory for creating agent resources with shared infrastructure.

    Uses EmailManager and CalendarManager to create agent resources with
    injected callbacks for cross-agent communication and calendar synchronization.
    """

    def __init__(self) -> None:
        self._email_manager = EmailManager()
        self._calendar_manager = CalendarManager()

    def create_agent_resources(
        self,
        owner: str,
        initial_meetings: list[Meeting] | None = None,
        allowed_date: str | None = None,
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

        return AgentResources(
            owner=owner,
            calendar=calendar,
            email=email,
            allowed_date=allowed_date,
            contacts=contacts,
        )

    def get_all_emails(self) -> list[Email]:
        """Get all emails sent (for evaluation/debugging)."""
        return self._email_manager.get_all_emails()
