"""Email system for iTIP-style calendar interactions."""

from typing import Callable

from ..types import Email, ToolError


class AgentEmail:
    """Email interface for a single agent.

    Receives callbacks for delivery and retrieval, injected by EmailManager.
    """

    def __init__(
        self,
        owner: str,
        deliver_callback: Callable[[Email], None],
        get_unread_callback: Callable[[], list[Email]],
    ) -> None:
        self._owner = owner
        self._deliver = deliver_callback
        self._get_unread = get_unread_callback

    @property
    def owner(self) -> str:
        """Return the email address of this agent.

        Returns:
            The email address string of this agent.
        """
        return self._owner

    def send(
        self,
        to: str,
        subject: str,
        body: str | None = None,
        event: str | None = None,
    ) -> None:
        """Send an email (optionally with calendar event attachment).

        Args:
            to: Recipient email address.
            subject: Email subject line.
            body: Optional email body text.
            event: Optional calendar event attachment string.

        Raises:
            ToolError: If attempting to send an email to yourself.
        """
        if to == self._owner:
            raise ToolError("Cannot send an email to yourself.")

        email = Email(
            from_=self._owner,
            to=to,
            subject=subject,
            body=body,
            event=event,
        )
        self._deliver(email)

    def get_unread(self) -> list[Email]:
        """Retrieve unread emails for this agent.

        Returns:
            List of unread Email objects for this agent.
        """
        return self._get_unread()


class EmailManager:
    """Manages email delivery and creates AgentEmail instances with injected callbacks."""

    def __init__(self) -> None:
        self._emails: list[Email] = []
        self._read_indices: dict[str, int] = {}

    def create_email(self, owner: str) -> AgentEmail:
        """Factory: creates AgentEmail with callbacks wired to this manager.

        Args:
            owner: Email address of the agent.

        Returns:
            A new AgentEmail instance with delivery and retrieval callbacks
            configured.
        """
        self._read_indices[owner] = 0

        def deliver(email: Email) -> None:
            self._emails.append(email)

        def get_unread() -> list[Email]:
            idx = self._read_indices[owner]
            unread = [e for e in self._emails[idx:] if e.to == owner]
            self._read_indices[owner] = len(self._emails)
            return unread

        return AgentEmail(owner, deliver, get_unread)

    def get_all_emails(self) -> list[Email]:
        """Get all emails sent (for evaluation/debugging).

        Returns:
            A copy of the list of all emails sent through the manager.
        """
        return list(self._emails)
