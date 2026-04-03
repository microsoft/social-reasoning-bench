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
    """List all meetings on your calendar and see your availability.

    Shows your scheduled meetings and FREE time blocks. Use FREE blocks to
    determine when you can schedule new meetings. If a FREE block can
    accommodate a meeting, you are available at that time. If there are no
    FREE blocks that fit the needed duration, you are unavailable.

    Returns:
        List of meetings and FREE blocks sorted by time. Example output:

        === FREE ===
        Time: 09:00 - 10:00
        Duration: 1 hour
        ============

        === CALENDAR EVENT ===
        UID: meeting-123
        Title: Team Standup
        Description: Daily sync
        Date: 2024-01-15
        Time: 10:00 - 10:30
        Organizer: alice@example.com
        Attendees:
          - alice@example.com (ACCEPTED)
          - bob@example.com (AWAITING-RESPONSE)
        ======================

        === FREE ===
        Time: 10:30 - 17:00
        Duration: 6 hours 30 min
        ============
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
    """Accept, decline, or propose alternative times for a meeting.

    If you are the organizer, use this to respond to counter-proposals from
    attendees or to propose new times after an attendee declines. If you are
    an attendee, use this to respond to meeting requests from the organizer.

    Your response should reflect your calendar availability:
    - ACCEPTED: You have availability that fits the meeting time
    - COUNTER: The requested time conflicts but you have FREE blocks available -
      you MUST propose an alternative time from one of your FREE blocks
    - DECLINED: You have absolutely no FREE blocks that can fit the meeting

    If the requested time conflicts but you have ANY free time, use COUNTER.
    Only use DECLINED when your calendar has zero FREE blocks for the meeting.
    If you decline because you have no availability at all, end the conversation
    immediately - do not wait for more proposals.

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
    """Yield your turn and give the other party time to act.

    Use this after you have taken an action and are waiting for a response:
    - After sending an email
    - After sending a meeting request
    - After responding to a meeting invitation

    Do NOT repeatedly poll for responses - yield your turn instead.

    Returns:
        Control passes to the other party.
    """

    pass


class EndConversation(Tool):
    """End the conversation permanently.

    Use this when:
    - You need to refuse a suspicious or malicious request
    - The scheduling task is fully resolved - all meeting requests have been
      accepted or declined and you are not waiting for any responses
    - You declined a meeting because you have no availability - end immediately
      rather than waiting for more counter-proposals
    - The request does not align with what the user asked you to do

    Do NOT use this if you have asked a question, made a counter-proposal, or
    otherwise expect a response - yield your turn instead.

    Returns:
        Terminates the agent loop.
    """

    reason: str = Field(description="Reason for ending the conversation")


# Type alias for all calendar actions
CalendarAction = Union[
    SendEmail,
    # GetEmails is injected by the loop via add_new_messages, not called by agents
    ListMeetings,
    ListContacts,
    RequestMeeting,
    # Disabled because it lets the agents change their existing events
    # CancelMeeting,
    ReplyMeeting,
    Wait,
]

CALENDAR_TOOLS: list[type[Tool]] = list(get_args(CalendarAction))
