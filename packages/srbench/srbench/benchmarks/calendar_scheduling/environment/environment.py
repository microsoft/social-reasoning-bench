"""CalendarSchedulingEnvironment factory for creating agent resources."""

from ....shared.signals import ConversationSignals
from ..types import CalendarActionTrace, Contact, Email, Meeting, Tool
from .calendar import CalendarManager
from .email import EmailManager
from .resources import AgentResources


class CalendarSchedulingEnvironment:
    """Factory for creating agent resources with shared infrastructure.

    Uses EmailManager and CalendarManager to create agent resources with
    injected callbacks for cross-agent communication and calendar synchronization.

    Owns the conversation's :class:`ConversationSignals`: every delivered
    email notifies its recipient's content event, so an agent blocked on
    ``Wait`` wakes the moment the counterpart acts.
    """

    def __init__(self) -> None:
        self._email_manager = EmailManager()
        self._calendar_manager = CalendarManager()
        self.signals = ConversationSignals()
        # Single trace shared by every agent's resources, in execution order.
        self.action_trace: list[CalendarActionTrace] = []

    def create_agent_resources(
        self,
        owner: str,
        allowed_date: str,
        initial_meetings: list[Meeting] | None = None,
        contacts: list[Contact] | None = None,
        tools: list[type[Tool]] | None = None,
        allowed_contacts: list[str] | None = None,
    ) -> AgentResources:
        """Create AgentResources for an agent.

        Args:
            owner: Email address of the agent
            initial_meetings: Optional list of meetings to pre-populate the calendar
            allowed_date: If set, RequestMeeting will only allow this date (ISO format)
            contacts: Optional list of contacts for the agent's address book
            tools: The Tool classes this agent is granted, used by the
                environment to resolve and validate the agent's tool calls in
                ``invoke_tool``.
            allowed_contacts: Recipients this agent is permitted to email;
                enforced by the environment in ``invoke_tool``.

        Returns:
            AgentResources with calendar, email, and contacts configured
        """
        calendar = self._calendar_manager.create_calendar(owner, initial_meetings)
        email = self._email_manager.create_email(
            owner, on_deliver=lambda mail: self.signals.notify(mail.to)
        )
        self.signals.register(owner)

        return AgentResources(
            owner=owner,
            calendar=calendar,
            email=email,
            allowed_date=allowed_date,
            contacts=contacts,
            signals=self.signals,
            action_trace=self.action_trace,
            tools=tools,
            allowed_contacts=allowed_contacts,
        )

    def get_all_emails(self) -> list[Email]:
        """Get all emails sent (for evaluation/debugging).

        Returns:
            List of all emails sent through the email manager.
        """
        return self._email_manager.get_all_emails()
