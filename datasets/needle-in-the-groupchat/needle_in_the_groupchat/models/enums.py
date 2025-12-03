"""Enumeration types for needle-in-the-groupchat."""

from enum import Enum


class NeedlePosition(str, Enum):
    """Position of the needle message in the conversation."""

    EARLY = "early"
    MIDDLE = "middle"
    LATE = "late"


class EvaluationMode(str, Enum):
    """Evaluation mode for testing."""

    EXACT_MATCH = "exact-match"
    PREFERENCE = "preference"


class MessageFormat(str, Enum):
    """Message format for evaluation."""

    MESSAGES = "messages"
    PREFIX = "prefix"
    TOOLS = "tools"


class GenerationMode(str, Enum):
    """Generation mode for conversations."""

    RANDOM = "random"
    LLM_EXACT = "llm-exact"
    LLM_PREFERENCE = "llm-preference"
