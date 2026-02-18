from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MessageHeader(BaseModel):
    """Sender, recipient, and subject details for the message"""

    to: str = Field(
        ...,
        description=(
            "Name or identifier of the message recipient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    position_to: str = Field(
        ...,
        description=(
            "Position or role of the message recipient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    from_: str = Field(
        ...,
        description=(
            "Name or identifier of the message sender .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    position_from: str = Field(
        ...,
        description=(
            "Position or role of the message sender .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    subject: str = Field(
        ...,
        description=(
            'Brief subject or title of the message .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_subject_line: str = Field(
        ..., description="Date the message is created or sent"
    )  # YYYY-MM-DD format

    time_subject_line: str = Field(
        ...,
        description=(
            'Time the message is created or sent .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MessageBody(BaseModel):
    """Main message content and sender signature"""

    message: str = Field(
        ...,
        description=(
            'Full content of the message .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the person sending the message .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    position_signature: str = Field(
        ...,
        description=(
            "Position or role of the person signing the message .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Reply(BaseModel):
    """Reply content and reply signature details"""

    reply: str = Field(
        default="",
        description=(
            "Reply or response to the original message .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_reply_section: str = Field(
        default="", description="Date the reply is completed"
    )  # YYYY-MM-DD format

    time_reply_section: str = Field(
        default="",
        description=(
            'Time the reply is completed .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    signature_position_reply_section: str = Field(
        default="",
        description=(
            "Signature and position of the person providing the reply .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class GeneralMessage(BaseModel):
    """
    GENERAL MESSAGE

    ''
    """

    message_header: MessageHeader = Field(..., description="Message Header")
    message_body: MessageBody = Field(..., description="Message Body")
    reply: Reply = Field(..., description="Reply")
