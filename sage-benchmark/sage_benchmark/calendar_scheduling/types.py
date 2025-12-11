from typing import Literal

from pydantic import BaseModel, Field


class CalendarEvent(BaseModel):
    title: str = Field(description="Event title")
    description: str = Field(description="Event description")
    start_time: int = Field(description="Event start hour in military time")
    duration: int = Field(description="Event duration in hours")
    participants: list[str] = Field(description="List of participant email addresses")


class LabeledCalendarEvent(CalendarEvent):
    # hidden property to llm -- used for eval
    is_movable: bool = Field(
        description="Whether the assistant can move this event to accommodate the requested event",
    )
    is_secret: bool = Field(
        description="Whether this event is secret with respect to the requestor agent"
    )


class CalendarRequestor(BaseModel):
    system_message: str = Field(
        description="Requestor agent description, especially relationship to assistant",
    )
    instruction_message: str = Field(
        description="Instruction message for the task.",
    )
    event: CalendarEvent = Field(description="Visible: The requested event")
    # hidden property to llm -- used for eval
    is_malicious: bool = Field(description="Whether the requestor is attacking or normal")


class CalendarAssistant(BaseModel):
    system_message: str = Field(description="System message for assistant")
    instruction_message: str = Field(description="Instruction message for the task.")
    calendar: list[LabeledCalendarEvent] = Field(description="The assistant's calendar events")


class CalendarTask(BaseModel):
    type: Literal["calendar"]
    requestor: CalendarRequestor = Field(description="The requestor agent configuration")
    assistant: CalendarAssistant = Field(description="The assistant agent configuration")
    # hidden property to llm -- used for eval
    satisfiable: bool = Field(
        description="Hidden: Whether the requested event should be scheduled (Y/N)"
    )
