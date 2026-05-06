# Calendar Scheduling Tests

This document describes the behaviors validated by the calendar scheduling test suite.

## Overview

The tests validate an iTIP-style (iCalendar Transport-Independent Interoperability Protocol) email-based calendar scheduling system where agents communicate via email with calendar attachments.

## Actions Tested

### SendEmail
**Allowed:**
- Send emails to any recipient (including non-existent agents)

**Disallowed:** None

---

### GetEmails
**Allowed:**
- Retrieve unread emails from inbox
- Emails are marked as read after retrieval (won't appear again)

**Disallowed:** None

---

### ListMeetings
**Allowed:**
- View all meetings on the agent's calendar

**Disallowed:** None

---

### RequestMeeting
**Allowed:**
- Create meetings with flexible date formats (ISO, human-readable, etc.)
- Create meetings with flexible time formats (24-hour, 12-hour AM/PM)
- Organizer is automatically added as ACCEPTED attendee
- Meeting appears on both organizer and attendees' calendars
- Attendees receive email invitations

**Disallowed:**
- Invalid/unparseable date formats → `ToolError`
- Invalid/unparseable time formats → `ToolError`
- Scheduling on wrong date when `allowed_date` constraint is set → `ToolError`

---

### CancelMeeting
**Allowed:**
- Organizer can cancel their own meetings
- Cancellation removes meeting from all calendars
- Only active attendees (AWAITING_RESPONSE, ACCEPTED) receive cancellation emails

**Disallowed:**
- Cancelling a non-existent meeting → `ToolError`
- Non-organizer attempting to cancel → `ToolError`

---

### ReplyMeeting
**Allowed:**
- Accept meeting invitation (status=ACCEPTED, keeps meeting on calendar, notifies organizer)
- Decline meeting invitation (status=DECLINED, removes meeting from calendar, notifies organizer)
- Propose alternative times (status=COUNTER):
  - Updates meeting to new times on both calendars
  - Counter-proposer becomes ACCEPTED
  - Organizer becomes AWAITING_RESPONSE (must accept/decline/counter)
  - Sends counter-proposal email to organizer

**Disallowed:**
- Replying to a non-existent meeting → `ToolError`
- Counter-proposal without providing date, start, and end times → `ToolError`
- Counter-proposal with invalid/unparseable time formats → `ToolError`
- Counter-proposal on wrong date when `allowed_date` constraint is set → `ToolError`

---

### Wait
**Allowed:**
- Yield turn to wait for other agent's response

**Disallowed:** None

---

### EndConversation
**Allowed:**
- End conversation when no pending meeting requests exist
- End conversation after accepting all pending requests
- End conversation after declining all pending requests

**Disallowed:**
- Ending conversation with unanswered meeting requests → `ToolError`

---

### Unknown Actions
**Disallowed:**
- Executing unrecognized action types → `ValueError`
