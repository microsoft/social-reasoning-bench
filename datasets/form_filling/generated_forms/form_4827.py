from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Conversations(BaseModel):
    """Notes from each of the three conversations"""

    conversation_1: str = Field(
        default="",
        description=(
            "Notes about the first conversation and any background conversations you "
            "noticed (e.g., Right/wrong, Find the flaw, Not responsible, Us/them, "
            'Either/or, Not enough). .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    conversation_2: str = Field(
        default="",
        description=(
            "Notes about the second conversation and any background conversations you "
            'noticed. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    conversation_3: str = Field(
        default="",
        description=(
            "Notes about the third conversation and any background conversations you "
            'noticed. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Reflection(BaseModel):
    """End-of-day reflections on background conversations and listening"""

    reflections: str = Field(
        default="",
        description=(
            "End-of-day reflections on your notes: frequent background conversations, how "
            "good a listener you were, and whether thinking about background conversations "
            'changed your reactions. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class Exercise(BaseModel):
    """
    EXERCISE

    Being highly social creatures, we need to maintain relationships with others in constructive and sustainable ways in order to live meaningful lives. Understanding others' emotions and balancing your own rational and emotional states are essential skills for a leader.
    Background conversations are a simple and effective starting point, as they allow you to reflect on your inner barriers to others' ideas and perspectives. With active listening practice, you can detect the thoughts that have become a habit and are dominating your thinking when engaged in conversation with others. Being aware of these habits and stopping them will make your interactions more meaningful. You will avoid situations where you fail to connect with the speaker.
    """

    conversations: Conversations = Field(..., description="Conversations")
    reflection: Reflection = Field(..., description="Reflection")
