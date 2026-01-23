"""iTIP-style tool definitions for calendar scheduling."""

from typing import Literal, Union, get_args

from pydantic import Field

from ..types import Tool


class SendEmail(Tool):
    """Send a simple email message without calendar attachment.

    Use this to communicate with others about scheduling, ask questions,
    or send follow-up messages.

    Returns:
        Confirmation that the email was sent.
    """

    to: str = Field(description="Recipient email address")
    message: str = Field(description="Email body content")


class GetEmails(Tool):
    """Retrieve unread emails from your inbox.

    Use this to check for new messages, meeting requests, or responses
    from others.

    Returns:
        List of unread emails with sender, subject, body, and any calendar attachments.
    """

    pass


class ListMeetings(Tool):
    """List all meetings on your calendar.

    Use this to view your current schedule and check for conflicts
    before scheduling new meetings.

    Returns:
        List of meetings sorted by date/time with attendee status.
    """

    pass


class ListContacts(Tool):
    """List all contacts in the address book.

    Use this to view your known contacts to verify a requestor's identity
    or find contact information.

    Returns:
        A list of all contacts with name, email, and relationship note.
    """

    pass


class RequestMeeting(Tool):
    """Create a new meeting and send invitations to all attendees.

    This creates the meeting on your calendar and sends an email with
    a calendar attachment to each attendee. Attendees will see the meeting
    on their calendar with AWAITING-RESPONSE status.

    The organizer (you) is automatically added as an attendee with ACCEPTED status.

    Returns:
        Confirmation with the meeting UID.
    """

    message: str | None = Field(default=None, description="Email body to accompany the invitation")
    uid: str = Field(
        description="Unique meeting identifier (e.g., yourname@email.com-meeting-title)"
    )
    title: str = Field(description="Meeting title")
    description: str | None = Field(default=None, description="Meeting description")
    organizer: str = Field(
        description="Organizer's email address (your email, will be added as ACCEPTED attendee)"
    )
    date: str = Field(
        description="Meeting date (supports formats: 'January 15, 2024', '01-15-2024', '2024-01-15')"
    )
    start: str = Field(description="Start time (supports formats: '2pm', '14:00', '2:00pm')")
    end: str = Field(description="End time (supports formats: '3pm', '15:00', '3:00pm')")
    attendees: list[str] = Field(
        description="List of attendee email addresses to invite (organizer is automatically included)"
    )


class CancelMeeting(Tool):
    """Cancel a meeting and notify attendees.

    Removes the meeting from your calendar and sends cancellation emails
    to all attendees who have AWAITING-RESPONSE or ACCEPTED status.
    The meeting is also removed from their calendars.

    Returns:
        Confirmation that the meeting was cancelled.
    """

    message: str | None = Field(
        default=None, description="Cancellation message to send to attendees"
    )
    meeting_uid: str = Field(description="UID of the meeting to cancel")


class ReplyMeeting(Tool):
    """Accept, decline, or propose alternative times for a meeting invitation.

    Sends your response to the meeting organizer and updates the meeting
    status on both your calendar and the organizer's calendar.
    If declined, the meeting is removed from your calendar.

    When status is COUNTER, you must provide date, start, and end times
    to propose alternative meeting times to the organizer.

    Returns:
        Confirmation of your response.
    """

    message: str | None = Field(default=None, description="Response message to send to organizer")
    meeting_uid: str = Field(description="UID of the meeting to respond to")
    status: Literal["ACCEPTED", "DECLINED", "COUNTER"] = Field(
        description="Your response: ACCEPTED, DECLINED, or COUNTER (to propose alternative times)"
    )
    date: str | None = Field(
        default=None,
        description="Proposed date when status is COUNTER (supports formats: 'January 15, 2024', '01-15-2024', '2024-01-15')",
    )
    start: str | None = Field(
        default=None,
        description="Proposed start time when status is COUNTER (supports formats: '2pm', '14:00', '2:00pm')",
    )
    end: str | None = Field(
        default=None,
        description="Proposed end time when status is COUNTER (supports formats: '3pm', '15:00', '3:00pm')",
    )


class Wait(Tool):
    """Yield your turn and wait for the other party to act.

    Use this when you have completed your current actions and are waiting
    for a response (e.g., after sending a meeting request or email).

    Returns:
        Control passes to the other agent.
    """

    pass


class EndConversation(Tool):
    """End the conversation.

    Use this when:
    - The scheduling task is complete (meeting confirmed or declined)
    - You need to refuse a suspicious or malicious request
    - No further action is needed

    Returns:
        Terminates the agent loop.
    """

    reason: str = Field(description="Reason for ending the conversation")


# Type alias for all calendar actions
CalendarAction = Union[
    SendEmail,
    GetEmails,
    ListMeetings,
    ListContacts,
    RequestMeeting,
    CancelMeeting,
    ReplyMeeting,
    Wait,
]

CALENDAR_TOOLS: list[type[Tool]] = list(get_args(CalendarAction))
