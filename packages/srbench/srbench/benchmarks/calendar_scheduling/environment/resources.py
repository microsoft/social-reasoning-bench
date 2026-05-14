"""AgentResources class that encapsulates all resources available to an agent."""

from __future__ import annotations

import asyncio
from typing import Callable

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
    """Encapsulates all resources available to an agent (calendar + email + contacts).

    ``execute(action)`` is async because ``Wait`` blocks until the counterpart
    delivers mail (or until ``end_event`` fires). All other actions complete
    synchronously and return immediately. Recipient validation for outbound
    mail also lives here (was previously enforced on the agent side).
    """

    def __init__(
        self,
        owner: str,
        calendar: AgentCalendar,
        email: AgentEmail,
        allowed_date: str,
        contacts: list[Contact] | None = None,
        allowed_recipients: list[str] | None = None,
        new_content_event: asyncio.Event | None = None,
        end_event: asyncio.Event | None = None,
        wake_recipient: Callable[[str], None] | None = None,
        mark_ended: Callable[[str], None] | None = None,
    ) -> None:
        self.owner = owner
        self.calendar = calendar
        self.email = email
        self.allowed_date = allowed_date
        self.contacts = contacts or []
        self._allowed_recipients: frozenset[str] | None = (
            frozenset(allowed_recipients) if allowed_recipients is not None else None
        )
        self._new_content_event: asyncio.Event = new_content_event or asyncio.Event()
        self._end_event: asyncio.Event = end_event or asyncio.Event()
        self._wake_recipient: Callable[[str], None] = wake_recipient or (lambda _to: None)
        self._mark_ended: Callable[[str], None] = mark_ended or (lambda _reason: None)

    async def execute(self, action: Tool) -> str:
        """Execute a tool action and return the result as a string.

        Args:
            action: The tool action to execute.

        Returns:
            A string describing the result of the action.

        Raises:
            ValueError: If the action type is unknown.
            ToolError: If the action is invalid for the current env state
                (e.g. SendEmail to a disallowed recipient, RequestMeeting on a
                date outside ``allowed_date``).
        """
        if isinstance(action, SendEmail):
            return self._handle_send_email(action)
        if isinstance(action, GetEmails):
            return self._handle_get_emails(action)
        if isinstance(action, ListMeetings):
            return self._handle_list_meetings(action)
        if isinstance(action, ListContacts):
            return self._handle_list_contacts(action)
        if isinstance(action, RequestMeeting):
            return self._handle_request_meeting(action)
        if isinstance(action, CancelMeeting):
            return self._handle_cancel_meeting(action)
        if isinstance(action, ReplyMeeting):
            return self._handle_reply_meeting(action)
        if isinstance(action, Wait):
            return await self._handle_wait(action)
        if isinstance(action, EndConversation):
            return self._handle_end_conversation(action)
        raise ValueError(f"Unknown action: {type(action).__name__}")

    # ------------------------------------------------------------------ #
    # Handlers
    # ------------------------------------------------------------------ #

    def _handle_send_email(self, action: SendEmail) -> str:
        if self._allowed_recipients is not None and action.to not in self._allowed_recipients:
            raise ToolError(
                f"Cannot SendEmail to {action.to}. "
                f"Allowed recipients are: {sorted(self._allowed_recipients)}"
            )
        self.email.send(
            to=action.to,
            subject="Message",
            body=action.message,
        )
        self._wake_recipient(action.to)
        return "Email sent successfully."

    def _handle_get_emails(self, action: GetEmails) -> str:
        """Drain unread emails. Returns immediately, even when the inbox is
        empty -- agents that want to yield until the counterpart acts should
        call :class:`Wait`.
        """
        self._new_content_event.clear()
        emails = self.email.get_unread()
        return format_emails(emails)

    async def _handle_wait(self, action: Wait) -> str:
        """Yield until the counterpart acts (delivers mail) or the conversation ends.

        Races ``self._new_content_event.wait()`` against
        ``self._end_event.wait()``; whichever fires first determines the
        return value.

        External cancellation (the executor's ``cancel_event``, wall-clock
        timeout, etc.) is *not* watched here. The executor races
        ``cancel_event`` at the outer level and cancels the agent's ``run()``
        task; ``CancelledError`` propagates through ``asyncio.wait`` and out
        via the ``finally`` block, which is the right behavior.

        Args:
            action: The Wait action.

        Returns:
            A status string describing what unblocked the wait.
        """
        if self._end_event.is_set():
            return "Conversation has ended."
        end_wait = asyncio.create_task(self._end_event.wait())
        content_wait = asyncio.create_task(self._new_content_event.wait())
        try:
            done, pending = await asyncio.wait(
                {end_wait, content_wait}, return_when=asyncio.FIRST_COMPLETED
            )
            for t in pending:
                t.cancel()
            if end_wait in done:
                return "Conversation has ended."
            return "Counterpart activity detected; check your inbox."
        finally:
            for t in (end_wait, content_wait):
                if not t.done():
                    t.cancel()

    def _handle_list_meetings(self, action: ListMeetings) -> str:
        meetings = self.calendar.list_meetings()
        return format_meetings(meetings)

    def _handle_list_contacts(self, action: ListContacts) -> str:
        if not self.contacts:
            return "No contacts in address book."
        lines = ["Contacts:"]
        for contact in self.contacts:
            lines.append(f"  - {contact.name} <{contact.email}> ({contact.note})")
        return "\n".join(lines)

    def _handle_request_meeting(self, action: RequestMeeting) -> str:
        try:
            date = parse_date(action.date)
            start_time = parse_time(action.start)
            end_time = parse_time(action.end)
        except ValueError as e:
            raise ToolError(str(e)) from e

        if self.allowed_date and date != self.allowed_date:
            raise ToolError(
                f"Insufficient privileges to manage events on {date}. Allowed dates are: [{self.allowed_date},]"
            )

        attendees: list[Attendee] = []
        organizer_in_list = action.organizer in action.attendees
        if not organizer_in_list:
            attendees.append(Attendee(email=action.organizer, status=AttendeeStatus.ACCEPTED))
        for email in action.attendees:
            if email == action.organizer:
                attendees.append(Attendee(email=email, status=AttendeeStatus.ACCEPTED))
            else:
                attendees.append(Attendee(email=email, status=AttendeeStatus.AWAITING_RESPONSE))

        if self.calendar.get_meeting(action.uid):
            raise ToolError(
                f"A meeting with UID '{action.uid}' already exists on your calendar. "
                f"Use a different UID."
            )

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

        self.calendar.add_meeting(meeting)

        event_attachment = f"REQUEST:\n{format_meeting_as_attachment(meeting)}"
        for attendee in attendees:
            if attendee.email != self.owner:
                self.email.send(
                    to=attendee.email,
                    subject=f"Meeting Request: {meeting.title}",
                    body=action.message,
                    event=event_attachment,
                )
                attendee_calendar = self.calendar.get_other_calendar(attendee.email)
                if attendee_calendar:
                    attendee_calendar.add_meeting(meeting.model_copy(deep=True))

        return f"Meeting request sent. UID: {meeting.uid}"

    def _handle_cancel_meeting(self, action: CancelMeeting) -> str:
        if self.calendar.is_initial_meeting(action.meeting_uid):
            raise ToolError(f"Meeting '{action.meeting_uid}' cannot be modified.")

        meeting = self.calendar.get_meeting(action.meeting_uid)
        if not meeting:
            raise ToolError(f"Meeting '{action.meeting_uid}' not found on your calendar.")

        if meeting.organizer != self.owner:
            raise ToolError(f"Only the organizer ({meeting.organizer}) can cancel this meeting.")

        self.calendar.remove_meeting(action.meeting_uid)

        event_attachment = f"CANCELLED:\n{format_meeting_as_attachment(meeting)}"
        for attendee in meeting.attendees:
            if attendee.email != self.owner and attendee.status in [
                AttendeeStatus.AWAITING_RESPONSE,
                AttendeeStatus.ACCEPTED,
            ]:
                self.email.send(
                    to=attendee.email,
                    subject=f"Meeting Cancelled: {meeting.title}",
                    body=action.message,
                    event=event_attachment,
                )
                attendee_calendar = self.calendar.get_other_calendar(attendee.email)
                if attendee_calendar:
                    attendee_calendar.remove_meeting(action.meeting_uid)

        return f"Meeting '{action.meeting_uid}' cancelled."

    def _handle_reply_meeting(self, action: ReplyMeeting) -> str:
        if self.calendar.is_initial_meeting(action.meeting_uid):
            raise ToolError(f"Meeting '{action.meeting_uid}' cannot be modified.")

        meeting = self.calendar.get_meeting(action.meeting_uid)
        if not meeting:
            raise ToolError(f"Meeting '{action.meeting_uid}' not found on your calendar.")

        if action.status == "RESCIND":
            self.calendar.remove_meeting(action.meeting_uid)

            other_emails = {
                attendee.email for attendee in meeting.attendees if attendee.email != self.owner
            }
            if meeting.organizer != self.owner:
                other_emails.add(meeting.organizer)

            for other_email in other_emails:
                other_calendar = self.calendar.get_other_calendar(other_email)
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

        if action.status == "COUNTER":
            if not action.date or not action.start or not action.end:
                raise ToolError(
                    "When status is COUNTER, you must provide date, start, and end times."
                )

            try:
                date = parse_date(action.date)
                start_time = parse_time(action.start)
                end_time = parse_time(action.end)
            except ValueError as e:
                raise ToolError(str(e)) from e

            if self.allowed_date and date != self.allowed_date:
                raise ToolError(
                    f"Insufficient privileges to manage events on {date}. Allowed dates are: [{self.allowed_date},]"
                )

            updated_attendees: list[Attendee] = []
            for attendee in meeting.attendees:
                if attendee.email == self.owner:
                    updated_attendees.append(
                        Attendee(email=attendee.email, status=AttendeeStatus.ACCEPTED)
                    )
                else:
                    updated_attendees.append(
                        Attendee(email=attendee.email, status=AttendeeStatus.AWAITING_RESPONSE)
                    )

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

            self.calendar.add_meeting(updated_meeting)

            for attendee in updated_meeting.attendees:
                if attendee.email != self.owner:
                    other_calendar = self.calendar.get_other_calendar(attendee.email)
                    if other_calendar:
                        other_calendar.add_meeting(updated_meeting.model_copy(deep=True))

            event_attachment = f"COUNTER:\n{format_meeting_as_attachment(updated_meeting)}"
            if self.owner == meeting.organizer:
                for attendee in meeting.attendees:
                    if attendee.email != self.owner:
                        self.email.send(
                            to=attendee.email,
                            subject=f"Counter-Proposal: {meeting.title}",
                            body=action.message,
                            event=event_attachment,
                        )
            else:
                self.email.send(
                    to=meeting.organizer,
                    subject=f"Counter-Proposal: {meeting.title}",
                    body=action.message,
                    event=event_attachment,
                )

            return f"Counter-proposal sent for meeting '{meeting.title}' ({meeting.uid}). Meeting updated to {date} {start_time}-{end_time}. Awaiting organizer response."

        status_enum = AttendeeStatus(action.status)

        organizer_calendar = self.calendar.get_other_calendar(meeting.organizer)
        if organizer_calendar:
            organizer_calendar.update_attendee_status(
                action.meeting_uid,
                self.owner,
                status_enum,
            )

        for attendee in meeting.attendees:
            if attendee.email != self.owner and attendee.email != meeting.organizer:
                other_calendar = self.calendar.get_other_calendar(attendee.email)
                if other_calendar:
                    other_calendar.update_attendee_status(
                        action.meeting_uid,
                        self.owner,
                        status_enum,
                    )

        event_attachment = f"{action.status}:\n{format_meeting_as_attachment(meeting)}"
        if self.owner == meeting.organizer:
            for attendee in meeting.attendees:
                if attendee.email != self.owner:
                    self.email.send(
                        to=attendee.email,
                        subject=f"Meeting {action.status}: {meeting.title}",
                        body=action.message,
                        event=event_attachment,
                    )
        else:
            self.email.send(
                to=meeting.organizer,
                subject=f"Meeting {action.status}: {meeting.title}",
                body=action.message,
                event=event_attachment,
            )

        if status_enum == AttendeeStatus.DECLINED:
            self.calendar.remove_meeting(action.meeting_uid)
        else:
            self.calendar.update_attendee_status(
                action.meeting_uid,
                self.owner,
                AttendeeStatus.ACCEPTED,
            )

        return f"Reply sent: {action.status} meeting {meeting.title} ({meeting.uid}) from {meeting.start_time}-{meeting.end_time} on {meeting.date}"

    def _handle_end_conversation(self, action: EndConversation) -> str:
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

            if my_status == AttendeeStatus.AWAITING_RESPONSE:
                awaiting_response.append(meeting)
                continue

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
                    f"{titles}. Use ReplyMeeting with status RESCIND to withdraw."
                )

            raise ToolError(" ".join(parts))

        self._mark_ended(action.reason)
        return f"Conversation ended: {action.reason}"
