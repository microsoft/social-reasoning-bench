"""AgentResources class that encapsulates all resources available to an agent."""

from ..types import Attendee, AttendeeStatus, Contact, Meeting, Tool, ToolError
from .actions import (
    CancelMeeting,
    EndConversation,
    GetEmails,
    ListContacts,
    ListMeetings,
    ReplyMeeting,
    RequestMeeting,
    SendEmail,
    Wait,
)
from .calendar import AgentCalendar
from .email import AgentEmail
from .utils import (
    format_emails,
    format_meeting_as_attachment,
    format_meetings,
    parse_date,
    parse_time,
)


class AgentResources:
    """Encapsulates all resources available to an agent (calendar + email + contacts)."""

    def __init__(
        self,
        owner: str,
        calendar: AgentCalendar,
        email: AgentEmail,
        allowed_date: str,
        contacts: list[Contact] | None = None,
    ) -> None:
        self.owner = owner
        self.calendar = calendar
        self.email = email
        self.allowed_date = allowed_date
        self.contacts = contacts or []

    def execute(self, action: Tool) -> str:
        """Execute a tool action and return the result as a string.

        Args:
            action: The tool action to execute.

        Returns:
            A string describing the result of the action.

        Raises:
            ValueError: If the action type is unknown.
        """
        if isinstance(action, SendEmail):
            return self._handle_send_email(action)
        elif isinstance(action, GetEmails):
            return self._handle_get_emails(action)
        elif isinstance(action, ListMeetings):
            return self._handle_list_meetings(action)
        elif isinstance(action, ListContacts):
            return self._handle_list_contacts(action)
        elif isinstance(action, RequestMeeting):
            return self._handle_request_meeting(action)
        elif isinstance(action, CancelMeeting):
            return self._handle_cancel_meeting(action)
        elif isinstance(action, ReplyMeeting):
            return self._handle_reply_meeting(action)
        elif isinstance(action, Wait):
            return self._handle_wait(action)
        elif isinstance(action, EndConversation):
            return self._handle_end_conversation(action)
        else:
            raise ValueError(f"Unknown action: {type(action).__name__}")

    def _handle_send_email(self, action: SendEmail) -> str:
        """Send a simple email without calendar attachment.

        Args:
            action: The SendEmail action containing recipient and message.

        Returns:
            A confirmation message that the email was sent.
        """
        self.email.send(
            to=action.to,
            subject="Message",
            body=action.message,
        )
        return "Email sent successfully."

    def _handle_get_emails(self, action: GetEmails) -> str:
        """Get unread emails.

        Args:
            action: The GetEmails action.

        Returns:
            Formatted string of unread emails or a no-unread-emails message.
        """
        emails = self.email.get_unread()
        return format_emails(emails)

    def _handle_list_meetings(self, action: ListMeetings) -> str:
        """List all meetings on the calendar.

        Args:
            action: The ListMeetings action.

        Returns:
            Formatted string of all meetings including free time blocks.
        """
        meetings = self.calendar.list_meetings()
        return format_meetings(meetings)

    def _handle_list_contacts(self, action: ListContacts) -> str:
        """List all contacts in the address book.

        Args:
            action: The ListContacts action.

        Returns:
            Formatted string of contacts, or a message if none exist.
        """
        if not self.contacts:
            return "No contacts in address book."
        lines = ["Contacts:"]
        for contact in self.contacts:
            lines.append(f"  - {contact.name} <{contact.email}> ({contact.note})")
        return "\n".join(lines)

    def _handle_request_meeting(self, action: RequestMeeting) -> str:
        """Create a meeting and send invitations to all attendees.

        Args:
            action: The RequestMeeting action with meeting details and attendees.

        Returns:
            Confirmation message with the meeting UID.

        Raises:
            ToolError: If date/time parsing fails or date is not allowed.
        """
        try:
            # Parse flexible date/time formats
            date = parse_date(action.date)
            start_time = parse_time(action.start)
            end_time = parse_time(action.end)
        except ValueError as e:
            raise ToolError(str(e)) from e

        # Validate date matches the allowed date (if constrained)
        if self.allowed_date and date != self.allowed_date:
            raise ToolError(
                f"Insufficient privileges to manage events on {date}. Allowed dates are: [{self.allowed_date},]"
            )

        # Convert email strings to Attendee objects with AWAITING-RESPONSE status
        # Organizer gets ACCEPTED status
        attendees: list[Attendee] = []
        organizer_in_list = action.organizer in action.attendees
        if not organizer_in_list:
            attendees.append(Attendee(email=action.organizer, status=AttendeeStatus.ACCEPTED))
        for email in action.attendees:
            if email == action.organizer:
                attendees.append(Attendee(email=email, status=AttendeeStatus.ACCEPTED))
            else:
                attendees.append(Attendee(email=email, status=AttendeeStatus.AWAITING_RESPONSE))

        # Reject duplicate UIDs — prevents silently overwriting existing meetings
        if self.calendar.get_meeting(action.uid):
            raise ToolError(
                f"A meeting with UID '{action.uid}' already exists on your calendar. "
                f"Use a different UID."
            )

        # Create the meeting
        meeting = Meeting(
            uid=action.uid,
            title=action.title,
            description=action.description or "",
            organizer=action.organizer,
            date=date,
            start_time=start_time,
            end_time=end_time,
            attendees=attendees,
        )

        # Add to organizer's calendar
        self.calendar.add_meeting(meeting)

        # Send email to each attendee (except organizer) and add to their calendar
        event_attachment = f"REQUEST:\n{format_meeting_as_attachment(meeting)}"
        for attendee in attendees:
            if attendee.email != self.owner:
                # Send invitation email
                self.email.send(
                    to=attendee.email,
                    subject=f"Meeting Request: {meeting.title}",
                    body=action.message,
                    event=event_attachment,
                )
                # Add to attendee's calendar (if they have one)
                attendee_calendar = self.calendar.get_other_calendar(attendee.email)
                if attendee_calendar:
                    # Create a copy of the meeting for the attendee's calendar
                    attendee_calendar.add_meeting(meeting.model_copy(deep=True))

        return f"Meeting request sent. UID: {meeting.uid}"

    def _handle_cancel_meeting(self, action: CancelMeeting) -> str:
        """Cancel a meeting and notify attendees.

        Args:
            action: The CancelMeeting action with the meeting UID and message.

        Returns:
            Confirmation message that the meeting was cancelled.

        Raises:
            ToolError: If the meeting is not found or the caller is not the
                organizer.
        """
        meeting = self.calendar.get_meeting(action.meeting_uid)
        if not meeting:
            raise ToolError(f"Meeting '{action.meeting_uid}' not found on your calendar.")

        # Only the organizer can cancel the meeting
        if meeting.organizer != self.owner:
            raise ToolError(f"Only the organizer ({meeting.organizer}) can cancel this meeting.")

        # Remove from caller's calendar
        self.calendar.remove_meeting(action.meeting_uid)

        # Send cancellation to AWAITING-RESPONSE and ACCEPTED attendees
        event_attachment = f"CANCELLED:\n{format_meeting_as_attachment(meeting)}"
        for attendee in meeting.attendees:
            if attendee.email != self.owner and attendee.status in [
                AttendeeStatus.AWAITING_RESPONSE,
                AttendeeStatus.ACCEPTED,
            ]:
                # Send cancellation email
                self.email.send(
                    to=attendee.email,
                    subject=f"Meeting Cancelled: {meeting.title}",
                    body=action.message,
                    event=event_attachment,
                )
                # Remove from their calendar
                attendee_calendar = self.calendar.get_other_calendar(attendee.email)
                if attendee_calendar:
                    attendee_calendar.remove_meeting(action.meeting_uid)

        return f"Meeting '{action.meeting_uid}' cancelled."

    def _handle_reply_meeting(self, action: ReplyMeeting) -> str:
        """Accept, decline, rescind, or send counter-proposal for a meeting.

        Args:
            action: The ReplyMeeting action with meeting UID, status, and
                optional counter-proposal times.

        Returns:
            Confirmation message describing the reply sent.

        Raises:
            ToolError: If the meeting is not found, counter-proposal fields are
                missing, or date/time parsing fails.
        """
        meeting = self.calendar.get_meeting(action.meeting_uid)
        if not meeting:
            raise ToolError(f"Meeting '{action.meeting_uid}' not found on your calendar.")

        # Handle RESCIND status (withdraw a previous counter-proposal)
        if action.status == "RESCIND":
            # Remove meeting from own calendar
            self.calendar.remove_meeting(action.meeting_uid)

            # Collect all other parties (attendees + organizer, excluding self)
            other_emails = {
                attendee.email for attendee in meeting.attendees if attendee.email != self.owner
            }
            if meeting.organizer != self.owner:
                other_emails.add(meeting.organizer)

            for other_email in other_emails:
                other_calendar = self.calendar.get_other_calendar(other_email)
                # Only meaningful to cancel meeting and send email etc if their calendar exists (else they are just a datapoint, not an active agent)
                if other_calendar:
                    other_calendar.remove_meeting(action.meeting_uid)
                    self.email.send(
                        to=other_email,
                        subject=f"Meeting Withdrawn: {meeting.title}",
                        body=action.message
                        or f"I am withdrawing my proposal for '{meeting.title}'.",
                    )

            return (
                f"Counter-proposal rescinded for meeting '{meeting.title}' ({meeting.uid}). "
                f"Meeting removed from all calendars."
            )

        # Handle COUNTER status (propose alternative times)
        if action.status == "COUNTER":
            # Validate required fields for counter-proposal
            if not action.date or not action.start or not action.end:
                raise ToolError(
                    "When status is COUNTER, you must provide date, start, and end times."
                )

            # Parse and validate proposed times
            try:
                date = parse_date(action.date)
                start_time = parse_time(action.start)
                end_time = parse_time(action.end)
            except ValueError as e:
                raise ToolError(str(e)) from e

            # Validate date matches the allowed date (if constrained)
            if self.allowed_date and date != self.allowed_date:
                raise ToolError(
                    f"Insufficient privileges to manage events on {date}. Allowed dates are: [{self.allowed_date},]"
                )

            # Build updated attendees list:
            # - Counter-proposer (self) becomes ACCEPTED
            # - All other attendees become AWAITING_RESPONSE
            updated_attendees: list[Attendee] = []
            for attendee in meeting.attendees:
                if attendee.email == self.owner:
                    updated_attendees.append(
                        Attendee(email=attendee.email, status=AttendeeStatus.ACCEPTED)
                    )
                else:
                    # All other attendees need to respond to the counter
                    updated_attendees.append(
                        Attendee(email=attendee.email, status=AttendeeStatus.AWAITING_RESPONSE)
                    )

            # Create updated meeting with new times and attendee statuses
            updated_meeting = Meeting(
                uid=meeting.uid,
                title=meeting.title,
                description=meeting.description,
                organizer=meeting.organizer,
                date=date,
                start_time=start_time,
                end_time=end_time,
                attendees=updated_attendees,
            )

            # Update meeting on own calendar
            self.calendar.add_meeting(updated_meeting)

            # Update meeting on all other participants' calendars
            for attendee in updated_meeting.attendees:
                if attendee.email != self.owner:
                    other_calendar = self.calendar.get_other_calendar(attendee.email)
                    if other_calendar:
                        other_calendar.add_meeting(updated_meeting.model_copy(deep=True))

            # Send counter-proposal email
            event_attachment = f"COUNTER:\n{format_meeting_as_attachment(updated_meeting)}"
            if self.owner == meeting.organizer:
                # Organizer is countering - send to all other attendees
                for attendee in meeting.attendees:
                    if attendee.email != self.owner:
                        self.email.send(
                            to=attendee.email,
                            subject=f"Counter-Proposal: {meeting.title}",
                            body=action.message,
                            event=event_attachment,
                        )
            else:
                # Attendee is countering - send to organizer
                self.email.send(
                    to=meeting.organizer,
                    subject=f"Counter-Proposal: {meeting.title}",
                    body=action.message,
                    event=event_attachment,
                )

            return f"Counter-proposal sent for meeting '{meeting.title}' ({meeting.uid}). Meeting updated to {date} {start_time}-{end_time}. Awaiting organizer response."

        # Handle ACCEPTED/DECLINED status
        status_enum = AttendeeStatus(action.status)

        # Update status on organizer's calendar
        organizer_calendar = self.calendar.get_other_calendar(meeting.organizer)
        if organizer_calendar:
            organizer_calendar.update_attendee_status(
                action.meeting_uid,
                self.owner,
                status_enum,
            )

        # Also update all other attendees' calendars (e.g., counter-proposer's calendar)
        for attendee in meeting.attendees:
            if attendee.email != self.owner and attendee.email != meeting.organizer:
                other_calendar = self.calendar.get_other_calendar(attendee.email)
                if other_calendar:
                    other_calendar.update_attendee_status(
                        action.meeting_uid,
                        self.owner,
                        status_enum,
                    )

        # Send reply email with calendar attachment
        event_attachment = f"{action.status}:\n{format_meeting_as_attachment(meeting)}"
        if self.owner == meeting.organizer:
            # Organizer is responding to a counter-proposal - send to all other attendees
            for attendee in meeting.attendees:
                if attendee.email != self.owner:
                    self.email.send(
                        to=attendee.email,
                        subject=f"Meeting {action.status}: {meeting.title}",
                        body=action.message,
                        event=event_attachment,
                    )
        else:
            # Attendee is responding to organizer's request - send to organizer
            self.email.send(
                to=meeting.organizer,
                subject=f"Meeting {action.status}: {meeting.title}",
                body=action.message,
                event=event_attachment,
            )

        # If declined, remove from caller's calendar
        if status_enum == AttendeeStatus.DECLINED:
            self.calendar.remove_meeting(action.meeting_uid)
        else:
            # Update own attendee status to ACCEPTED
            self.calendar.update_attendee_status(
                action.meeting_uid,
                self.owner,
                AttendeeStatus.ACCEPTED,
            )

        return f"Reply sent: {action.status} meeting {meeting.title} ({meeting.uid}) from {meeting.start_time}-{meeting.end_time} on {meeting.date}"

    def _handle_wait(self, action: Wait) -> str:
        """Yield turn to wait for other agent.

        Args:
            action: The Wait action.

        Returns:
            A waiting status message.
        """
        return "Waiting for response."

    def _handle_end_conversation(self, action: EndConversation) -> str:
        """End the conversation.

        Args:
            action: The EndConversation action with a reason.

        Returns:
            A message confirming the conversation has ended with the reason.

        Raises:
            ToolError: If there are pending meetings with unresolved responses.
        """
        # Check for pending meeting requests that haven't been fully resolved
        awaiting_response: list[Meeting] = []
        counter_pending: list[Meeting] = []

        for meeting in self.calendar.list_meetings():
            my_status = None
            organizer_status = None

            for attendee in meeting.attendees:
                if attendee.email == self.owner:
                    my_status = attendee.status
                if attendee.email == meeting.organizer:
                    organizer_status = attendee.status

            # Check 1: I need to respond to a meeting request
            if my_status == AttendeeStatus.AWAITING_RESPONSE:
                awaiting_response.append(meeting)
                continue

            # Check 2: I sent a counter-proposal (I'm ACCEPTED) and organizer hasn't responded yet
            if (
                my_status == AttendeeStatus.ACCEPTED
                and organizer_status == AttendeeStatus.AWAITING_RESPONSE
            ):
                counter_pending.append(meeting)
                continue

        if awaiting_response or counter_pending:
            parts: list[str] = ["Cannot end conversation."]

            if awaiting_response:
                titles = ", ".join(f"'{m.title}' ({m.uid})" for m in awaiting_response)
                parts.append(
                    f"You have {len(awaiting_response)} meeting(s) awaiting your response: "
                    f"{titles}. Use ReplyMeeting with status ACCEPTED or DECLINED for each."
                )

            if counter_pending:
                titles = ", ".join(f"'{m.title}' ({m.uid})" for m in counter_pending)
                parts.append(
                    f"You have {len(counter_pending)} pending counter-proposal(s): "
                    f"{titles}. Use Wait to wait for a response, or "
                    f"ReplyMeeting with status RESCIND to withdraw."
                )

            raise ToolError(" ".join(parts))

        return f"Conversation ended: {action.reason}"
