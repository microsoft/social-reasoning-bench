"""Tests for AgentResources actions."""

import pytest
from srbench.benchmarks.calendar_scheduling.environment import (
    AgentResources,
    CalendarSchedulingEnvironment,
    CancelMeeting,
    EndConversation,
    GetEmails,
    ListMeetings,
    ReplyMeeting,
    RequestMeeting,
    SendEmail,
    Wait,
)
from srbench.benchmarks.calendar_scheduling.types import (
    Attendee,
    AttendeeStatus,
    Meeting,
    ToolError,
)


@pytest.fixture
def environment():
    """Create a fresh CalendarSchedulingEnvironment for each test.

    Returns:
        A new CalendarSchedulingEnvironment instance.
    """
    return CalendarSchedulingEnvironment()


@pytest.fixture
def alice_resources(environment):
    """Create resources for alice@example.com.

    Args:
        environment: The shared CalendarSchedulingEnvironment fixture.

    Returns:
        AgentResources for alice@example.com with allowed_date 2024-01-15.
    """
    return environment.create_agent_resources("alice@example.com", allowed_date="2024-01-15")


@pytest.fixture
def bob_resources(environment):
    """Create resources for bob@example.com.

    Args:
        environment: The shared CalendarSchedulingEnvironment fixture.

    Returns:
        AgentResources for bob@example.com with allowed_date 2024-01-15.
    """
    return environment.create_agent_resources("bob@example.com", allowed_date="2024-01-15")


class TestSendEmail:
    """Tests for SendEmail action."""

    def test_send_email_success(self, alice_resources, bob_resources):
        """Test sending an email to another agent.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        action = SendEmail(to="bob@example.com", message="Hello Bob!")
        result = alice_resources.execute(action)

        assert result == "Email sent successfully."

        # Bob should have received the email
        get_emails = GetEmails()
        emails_result = bob_resources.execute(get_emails)
        assert "alice@example.com" in emails_result
        assert "Hello Bob!" in emails_result

    def test_send_email_to_nonexistent_agent(self, alice_resources):
        """Test sending email to agent without resources still succeeds.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        action = SendEmail(to="unknown@example.com", message="Hello!")
        result = alice_resources.execute(action)

        assert result == "Email sent successfully."


class TestGetEmails:
    """Tests for GetEmails action."""

    def test_get_emails_empty(self, alice_resources):
        """Test getting emails when inbox is empty.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        action = GetEmails()
        result = alice_resources.execute(action)

        assert result == "No unread emails."

    def test_get_emails_with_messages(self, alice_resources, bob_resources):
        """Test getting emails after receiving some.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Bob sends an email to Alice
        bob_resources.execute(SendEmail(to="alice@example.com", message="Hi Alice!"))

        # Alice checks her email
        action = GetEmails()
        result = alice_resources.execute(action)

        assert "bob@example.com" in result
        assert "Hi Alice!" in result

    def test_get_emails_marks_as_read(self, alice_resources, bob_resources):
        """Test that getting emails marks them as read.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Bob sends an email
        bob_resources.execute(SendEmail(to="alice@example.com", message="First message"))

        # Alice reads emails
        alice_resources.execute(GetEmails())

        # Alice reads again - should be empty
        result = alice_resources.execute(GetEmails())
        assert result == "No unread emails."

        # Bob sends another email
        bob_resources.execute(SendEmail(to="alice@example.com", message="Second message"))

        # Alice should only see the new email
        result = alice_resources.execute(GetEmails())
        assert "Second message" in result
        assert "First message" not in result


class TestListMeetings:
    """Tests for ListMeetings action."""

    def test_list_meetings_empty(self, alice_resources):
        """Test listing meetings when calendar is empty.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        action = ListMeetings()
        result = alice_resources.execute(action)

        assert result == "No meetings on your calendar."

    def test_list_meetings_with_meetings(self, environment):
        """Test listing meetings after adding some.

        Args:
            environment: The shared CalendarSchedulingEnvironment fixture.
        """
        meeting = Meeting(
            uid="test-meeting-1",
            title="Team Standup",
            description="Daily standup",
            organizer="alice@example.com",
            date="2024-01-15",
            start_time="09:00",
            end_time="09:30",
            attendees=[Attendee(email="alice@example.com", status=AttendeeStatus.ACCEPTED)],
        )
        alice_resources = environment.create_agent_resources(
            "alice@example.com", allowed_date="2024-01-15", initial_meetings=[meeting]
        )

        action = ListMeetings()
        result = alice_resources.execute(action)

        assert "Team Standup" in result
        assert "test-meeting-1" in result
        assert "2024-01-15" in result


class TestRequestMeeting:
    """Tests for RequestMeeting action."""

    def test_request_meeting_basic(self, alice_resources, bob_resources):
        """Test creating a basic meeting request.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        action = RequestMeeting(
            message="Let's discuss the project",
            uid="alice-project-meeting",
            title="Project Discussion",
            description="Discuss Q1 goals",
            organizer="alice@example.com",
            date="2024-01-15",
            start="14:00",
            end="15:00",
            attendees=["bob@example.com"],
        )
        result = alice_resources.execute(action)

        assert "Meeting request sent" in result
        assert "alice-project-meeting" in result

        # Meeting should be on Alice's calendar
        alice_meetings = alice_resources.execute(ListMeetings())
        assert "Project Discussion" in alice_meetings

        # Meeting should be on Bob's calendar
        bob_meetings = bob_resources.execute(ListMeetings())
        assert "Project Discussion" in bob_meetings

        # Bob should have received an email
        bob_emails = bob_resources.execute(GetEmails())
        assert "Meeting Request: Project Discussion" in bob_emails

    def test_request_meeting_flexible_date_formats(self, alice_resources, bob_resources):
        """Test that various date/time formats are accepted.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        action = RequestMeeting(
            message="Meeting",
            uid="flexible-meeting",
            title="Flexible Format Meeting",
            description="Test",
            organizer="alice@example.com",
            date="January 15, 2024",  # Human-readable date
            start="2pm",  # 12-hour format
            end="3:30pm",  # 12-hour with minutes
            attendees=["bob@example.com"],
        )
        result = alice_resources.execute(action)

        assert "Meeting request sent" in result

        # Check the meeting was created with normalized formats
        alice_meetings = alice_resources.execute(ListMeetings())
        assert "2024-01-15" in alice_meetings
        assert "14:00" in alice_meetings
        assert "15:30" in alice_meetings

    def test_request_meeting_invalid_date(self, alice_resources):
        """Test that invalid date format raises ToolError.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        action = RequestMeeting(
            message="Meeting",
            uid="invalid-meeting",
            title="Invalid Meeting",
            description="Test",
            organizer="alice@example.com",
            date="not-a-date",
            start="14:00",
            end="15:00",
            attendees=[],
        )
        with pytest.raises(ToolError, match="Unable to parse date"):
            alice_resources.execute(action)

    def test_request_meeting_invalid_time(self, alice_resources):
        """Test that invalid time format raises ToolError.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        action = RequestMeeting(
            message="Meeting",
            uid="invalid-meeting",
            title="Invalid Meeting",
            description="Test",
            organizer="alice@example.com",
            date="2024-01-15",
            start="invalid",
            end="15:00",
            attendees=[],
        )
        with pytest.raises(ToolError, match="Unable to parse time"):
            alice_resources.execute(action)

    def test_request_meeting_organizer_auto_added(self, alice_resources):
        """Test that organizer is automatically added as ACCEPTED attendee.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        action = RequestMeeting(
            message="Meeting",
            uid="auto-add-test",
            title="Auto Add Test",
            description="Test",
            organizer="alice@example.com",
            date="2024-01-15",
            start="14:00",
            end="15:00",
            attendees=[],  # No attendees specified
        )
        alice_resources.execute(action)

        # Check Alice's calendar shows her as ACCEPTED
        alice_meetings = alice_resources.execute(ListMeetings())
        assert "alice@example.com" in alice_meetings
        assert "ACCEPTED" in alice_meetings

    def test_request_meeting_organizer_status_updated(self, alice_resources, bob_resources):
        """Test that if organizer is in attendees list, status is set to ACCEPTED.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        action = RequestMeeting(
            message="Meeting",
            uid="status-update-test",
            title="Status Update Test",
            description="Test",
            organizer="alice@example.com",
            date="2024-01-15",
            start="14:00",
            end="15:00",
            attendees=["alice@example.com", "bob@example.com"],
        )
        alice_resources.execute(action)

        # Alice should be ACCEPTED even though she was added as AWAITING-RESPONSE
        alice_meetings = alice_resources.execute(ListMeetings())
        assert "alice@example.com (ACCEPTED)" in alice_meetings

    def test_request_meeting_wrong_date_rejected(self, environment):
        """Test that scheduling on wrong date raises ToolError when allowed_date is set.

        Args:
            environment: The shared CalendarSchedulingEnvironment fixture.
        """
        resources = environment.create_agent_resources(
            "alice@example.com",
            allowed_date="2024-01-15",
        )
        action = RequestMeeting(
            message="Meeting",
            uid="wrong-date-meeting",
            title="Wrong Date",
            description="Test",
            organizer="alice@example.com",
            date="2024-01-20",  # Wrong date
            start="14:00",
            end="15:00",
            attendees=["bob@example.com"],
        )
        with pytest.raises(ToolError, match="2024-01-15"):
            resources.execute(action)

    def test_request_meeting_correct_date_allowed(self, environment):
        """Test that scheduling on correct date works when allowed_date is set.

        Args:
            environment: The shared CalendarSchedulingEnvironment fixture.
        """
        resources = environment.create_agent_resources(
            "alice@example.com",
            allowed_date="2024-01-15",
        )
        action = RequestMeeting(
            message="Meeting",
            uid="correct-date-meeting",
            title="Correct Date",
            description="Test",
            organizer="alice@example.com",
            date="January 15, 2024",  # Correct date, flexible format
            start="14:00",
            end="15:00",
            attendees=["bob@example.com"],
        )
        result = resources.execute(action)
        assert "Meeting request sent" in result


class TestCancelMeeting:
    """Tests for CancelMeeting action."""

    def test_cancel_meeting_success(self, alice_resources, bob_resources):
        """Test cancelling an existing meeting.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # First create a meeting
        alice_resources.execute(
            RequestMeeting(
                message="Let's meet",
                uid="cancel-test-meeting",
                title="Meeting to Cancel",
                description="Test",
                organizer="alice@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["bob@example.com"],
            )
        )

        # Clear Bob's emails from the invite
        bob_resources.execute(GetEmails())

        # Cancel the meeting
        action = CancelMeeting(
            message="Sorry, need to cancel",
            meeting_uid="cancel-test-meeting",
        )
        result = alice_resources.execute(action)

        assert "cancelled" in result.lower()

        # Meeting should be removed from Alice's calendar
        alice_meetings = alice_resources.execute(ListMeetings())
        assert "Meeting to Cancel" not in alice_meetings

        # Meeting should be removed from Bob's calendar
        bob_meetings = bob_resources.execute(ListMeetings())
        assert "Meeting to Cancel" not in bob_meetings

        # Bob should have received a cancellation email
        bob_emails = bob_resources.execute(GetEmails())
        assert "Cancelled" in bob_emails

    def test_cancel_meeting_not_found(self, alice_resources):
        """Test cancelling a non-existent meeting raises ToolError.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        action = CancelMeeting(
            message="Cancel",
            meeting_uid="nonexistent-meeting",
        )
        with pytest.raises(ToolError, match="not found"):
            alice_resources.execute(action)

    def test_cancel_meeting_non_organizer_rejected(self, alice_resources, bob_resources):
        """Test that non-organizer cannot cancel a meeting.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Alice creates a meeting with Bob
        alice_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="organizer-cancel-test",
                title="Organizer Test",
                description="Test",
                organizer="alice@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["bob@example.com"],
            )
        )

        # Bob (non-organizer) tries to cancel
        with pytest.raises(ToolError, match="organizer"):
            bob_resources.execute(
                CancelMeeting(
                    message="Cancelling",
                    meeting_uid="organizer-cancel-test",
                )
            )

    def test_cancel_meeting_only_notifies_active_attendees(self, alice_resources, bob_resources):
        """Test that cancelled meetings only notify AWAITING-RESPONSE and ACCEPTED attendees.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Create meeting
        alice_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="selective-cancel-test",
                title="Selective Cancel Test",
                description="Test",
                organizer="alice@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["bob@example.com"],
            )
        )

        # Bob declines
        bob_resources.execute(GetEmails())  # Clear invite email
        bob_resources.execute(
            ReplyMeeting(
                message="Can't make it",
                meeting_uid="selective-cancel-test",
                status="DECLINED",
            )
        )

        # Clear Alice's emails from decline notification
        alice_resources.execute(GetEmails())

        # Alice cancels
        alice_resources.execute(
            CancelMeeting(
                message="Cancelling",
                meeting_uid="selective-cancel-test",
            )
        )

        # Bob shouldn't get a cancellation email since he already declined
        bob_emails = bob_resources.execute(GetEmails())
        assert bob_emails == "No unread emails."


class TestReplyMeeting:
    """Tests for ReplyMeeting action."""

    def test_reply_meeting_accept(self, alice_resources, bob_resources):
        """Test accepting a meeting invitation.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Alice creates meeting
        alice_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="accept-test-meeting",
                title="Accept Test",
                description="Test",
                organizer="alice@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["bob@example.com"],
            )
        )

        # Clear emails
        bob_resources.execute(GetEmails())
        alice_resources.execute(GetEmails())

        # Bob accepts
        action = ReplyMeeting(
            message="I'll be there!",
            meeting_uid="accept-test-meeting",
            status="ACCEPTED",
        )
        result = bob_resources.execute(action)

        assert "Reply sent" in result
        assert "ACCEPTED" in result

        # Meeting should still be on Bob's calendar
        bob_meetings = bob_resources.execute(ListMeetings())
        assert "Accept Test" in bob_meetings

        # Alice should receive notification
        alice_emails = alice_resources.execute(GetEmails())
        assert "ACCEPTED" in alice_emails

        # Status on Alice's calendar should be updated
        alice_meetings = alice_resources.execute(ListMeetings())
        assert "bob@example.com (ACCEPTED)" in alice_meetings

    def test_reply_meeting_decline(self, alice_resources, bob_resources):
        """Test declining a meeting invitation.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Alice creates meeting
        alice_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="decline-test-meeting",
                title="Decline Test",
                description="Test",
                organizer="alice@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["bob@example.com"],
            )
        )

        # Clear emails
        bob_resources.execute(GetEmails())
        alice_resources.execute(GetEmails())

        # Bob declines
        action = ReplyMeeting(
            message="Sorry, can't make it",
            meeting_uid="decline-test-meeting",
            status="DECLINED",
        )
        result = bob_resources.execute(action)

        assert "Reply sent" in result
        assert "DECLINED" in result

        # Meeting should be removed from Bob's calendar
        bob_meetings = bob_resources.execute(ListMeetings())
        assert "Decline Test" not in bob_meetings

        # Alice should receive notification
        alice_emails = alice_resources.execute(GetEmails())
        assert "DECLINED" in alice_emails

    def test_reply_meeting_not_found(self, bob_resources):
        """Test replying to a non-existent meeting raises ToolError.

        Args:
            bob_resources: The fixture providing AgentResources for bob.
        """
        action = ReplyMeeting(
            message="Reply",
            meeting_uid="nonexistent-meeting",
            status="ACCEPTED",
        )
        with pytest.raises(ToolError, match="not found"):
            bob_resources.execute(action)


class TestWait:
    """Tests for Wait action."""

    def test_wait(self, alice_resources):
        """Test the Wait action.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        action = Wait()
        result = alice_resources.execute(action)

        assert "Waiting" in result


class TestEndConversation:
    """Tests for EndConversation action."""

    def test_end_conversation_success(self, alice_resources):
        """Test ending conversation when no pending requests.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        action = EndConversation(reason="Task completed")
        result = alice_resources.execute(action)

        assert "Conversation ended" in result
        assert "Task completed" in result

    def test_end_conversation_with_pending_requests(self, alice_resources, bob_resources):
        """Test that ending conversation raises ToolError when there are pending meeting requests.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Bob sends Alice a meeting request
        bob_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="pending-meeting",
                title="Pending Meeting",
                description="Test",
                organizer="bob@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["alice@example.com"],
            )
        )

        # Alice tries to end conversation without responding
        action = EndConversation(reason="Done")
        with pytest.raises(ToolError, match="pending"):
            alice_resources.execute(action)

    def test_end_conversation_after_accepting(self, alice_resources, bob_resources):
        """Test that ending conversation succeeds after responding to all requests.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Bob sends Alice a meeting request
        bob_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="will-accept-meeting",
                title="Will Accept",
                description="Test",
                organizer="bob@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["alice@example.com"],
            )
        )

        # Alice accepts
        alice_resources.execute(
            ReplyMeeting(
                message="Accepted",
                meeting_uid="will-accept-meeting",
                status="ACCEPTED",
            )
        )

        # Now Alice can end conversation
        action = EndConversation(reason="Done")
        result = alice_resources.execute(action)

        assert "Conversation ended" in result

    def test_end_conversation_after_declining(self, alice_resources, bob_resources):
        """Test that ending conversation succeeds after declining all requests.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Bob sends Alice a meeting request
        bob_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="will-decline-meeting",
                title="Will Decline",
                description="Test",
                organizer="bob@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["alice@example.com"],
            )
        )

        # Alice declines
        alice_resources.execute(
            ReplyMeeting(
                message="Declined",
                meeting_uid="will-decline-meeting",
                status="DECLINED",
            )
        )

        # Now Alice can end conversation
        action = EndConversation(reason="Done")
        result = alice_resources.execute(action)

        assert "Conversation ended" in result


class TestExecuteUnknownAction:
    """Tests for handling unknown actions."""

    def test_unknown_action_raises_error(self, alice_resources):
        """Test that unknown action types raise ValueError.

        Args:
            alice_resources: The fixture providing AgentResources for alice.

        Returns:
            None. Asserts that ValueError is raised for unknown actions.
        """

        class UnknownAction(SendEmail):
            @classmethod
            def get_name(cls):
                return "UnknownAction"

        action = UnknownAction(to="test@example.com", message="test")

        with pytest.raises(ValueError, match="Unknown action"):
            alice_resources.execute(action)


class TestReplyMeetingCounter:
    """Tests for ReplyMeeting with COUNTER status."""

    def test_reply_meeting_counter_success(self, alice_resources, bob_resources):
        """Test sending a counter-proposal via ReplyMeeting updates calendars.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Bob sends Alice a meeting request for 2pm
        bob_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="counter-test",
                title="Counter Test",
                description="Test",
                organizer="bob@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["alice@example.com"],
            )
        )

        # Clear Alice's emails from invite
        alice_resources.execute(GetEmails())

        # Alice sends counter-proposal for 10am using ReplyMeeting with COUNTER status
        result = alice_resources.execute(
            ReplyMeeting(
                message="I'm not available at that time",
                meeting_uid="counter-test",
                status="COUNTER",
                date="2024-01-15",
                start="10:00",
                end="11:00",
            )
        )

        assert "Counter-proposal sent" in result
        assert "counter-test" in result
        assert "Meeting updated" in result

        # Bob should receive the counter-proposal email with calendar attachment
        bob_emails = bob_resources.execute(GetEmails())
        assert "Counter-Proposal" in bob_emails
        assert "COUNTER:" in bob_emails  # Calendar attachment marker
        assert "CALENDAR EVENT" in bob_emails  # Calendar attachment format
        assert "10:00" in bob_emails

        # Meeting should be updated to new time on Alice's calendar
        alice_meetings = alice_resources.execute(ListMeetings())
        assert "10:00" in alice_meetings  # New time
        assert "14:00" not in alice_meetings  # Old time should be gone
        assert "alice@example.com (ACCEPTED)" in alice_meetings  # Alice is now ACCEPTED

        # Meeting should be updated to new time on Bob's calendar
        bob_meetings = bob_resources.execute(ListMeetings())
        assert "10:00" in bob_meetings  # New time
        assert "14:00" not in bob_meetings  # Old time should be gone
        assert "bob@example.com (AWAITING-RESPONSE)" in bob_meetings  # Bob needs to respond
        # Verify no duplicate events on Bob's calendar (replacement worked, not addition)
        assert bob_meetings.count("counter-test") == 1

    def test_reply_meeting_counter_then_accept(self, alice_resources, bob_resources):
        """Test full counter-proposal workflow: request -> counter -> accept.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Bob sends Alice a meeting request for 2pm
        bob_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="counter-accept-test",
                title="Counter Accept Test",
                description="Test",
                organizer="bob@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["alice@example.com"],
            )
        )

        # Clear emails
        alice_resources.execute(GetEmails())

        # Alice counters with 10am
        alice_resources.execute(
            ReplyMeeting(
                message="How about 10am?",
                meeting_uid="counter-accept-test",
                status="COUNTER",
                date="2024-01-15",
                start="10:00",
                end="11:00",
            )
        )

        # Clear Bob's emails
        bob_resources.execute(GetEmails())

        # Bob accepts the counter-proposal
        result = bob_resources.execute(
            ReplyMeeting(
                message="10am works for me!",
                meeting_uid="counter-accept-test",
                status="ACCEPTED",
            )
        )

        assert "ACCEPTED" in result

        # Both should now have the meeting at 10am with both ACCEPTED
        alice_meetings = alice_resources.execute(ListMeetings())
        assert "10:00" in alice_meetings
        assert "alice@example.com (ACCEPTED)" in alice_meetings

        bob_meetings = bob_resources.execute(ListMeetings())
        assert "10:00" in bob_meetings
        assert "bob@example.com (ACCEPTED)" in bob_meetings

    def test_reply_meeting_counter_not_found(self, alice_resources):
        """Test counter-proposal for non-existent meeting raises ToolError.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
        """
        with pytest.raises(ToolError, match="not found"):
            alice_resources.execute(
                ReplyMeeting(
                    message="Counter",
                    meeting_uid="nonexistent",
                    status="COUNTER",
                    date="2024-01-15",
                    start="10:00",
                    end="11:00",
                )
            )

    def test_reply_meeting_counter_missing_fields(self, alice_resources, bob_resources):
        """Test counter-proposal without required fields raises ToolError.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Bob sends Alice a meeting request
        bob_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="counter-missing-fields",
                title="Counter Missing Fields",
                description="Test",
                organizer="bob@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["alice@example.com"],
            )
        )

        # Try counter without date/start/end
        with pytest.raises(ToolError, match="must provide date, start, and end"):
            alice_resources.execute(
                ReplyMeeting(
                    message="Counter",
                    meeting_uid="counter-missing-fields",
                    status="COUNTER",
                )
            )

    def test_reply_meeting_counter_invalid_time(self, alice_resources, bob_resources):
        """Test counter-proposal with invalid time raises ToolError.

        Args:
            alice_resources: The fixture providing AgentResources for alice.
            bob_resources: The fixture providing AgentResources for bob.
        """
        # Bob sends Alice a meeting request
        bob_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="counter-invalid-time",
                title="Counter Invalid Time",
                description="Test",
                organizer="bob@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["alice@example.com"],
            )
        )

        with pytest.raises(ToolError, match="Unable to parse time"):
            alice_resources.execute(
                ReplyMeeting(
                    message="Counter",
                    meeting_uid="counter-invalid-time",
                    status="COUNTER",
                    date="2024-01-15",
                    start="invalid",
                    end="11:00",
                )
            )

    def test_reply_meeting_counter_wrong_date_rejected(self, environment):
        """Test that counter-proposal on wrong date raises ToolError when allowed_date is set.

        Args:
            environment: The shared CalendarSchedulingEnvironment fixture.
        """
        # Create Bob with allowed_date constraint
        bob_resources = environment.create_agent_resources(
            "bob@example.com", allowed_date="2024-01-15"
        )

        # Create Alice with allowed_date constraint
        alice_resources = environment.create_agent_resources(
            "alice@example.com",
            allowed_date="2024-01-15",
        )

        # Bob sends Alice a meeting request
        bob_resources.execute(
            RequestMeeting(
                message="Meeting",
                uid="counter-wrong-date",
                title="Counter Wrong Date Test",
                description="Test",
                organizer="bob@example.com",
                date="2024-01-15",
                start="14:00",
                end="15:00",
                attendees=["alice@example.com"],
            )
        )

        # Alice tries to counter with wrong date
        with pytest.raises(ToolError, match="2024-01-15"):
            alice_resources.execute(
                ReplyMeeting(
                    message="How about a different day?",
                    meeting_uid="counter-wrong-date",
                    status="COUNTER",
                    date="2024-01-20",  # Wrong date
                    start="10:00",
                    end="11:00",
                )
            )
