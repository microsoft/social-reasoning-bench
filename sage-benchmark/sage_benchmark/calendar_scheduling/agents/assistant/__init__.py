"""Assistant agent module for calendar scheduling."""

from .calendar_assistant import CalendarAssistantAgent
from .prompts import get_system_prompt, list_available_presets

__all__ = ["CalendarAssistantAgent", "get_system_prompt", "list_available_presets"]
