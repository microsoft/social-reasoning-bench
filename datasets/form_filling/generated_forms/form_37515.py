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
    """Basic identifying information for the message"""

    incident_name_optional: str = Field(
        default="",
        description=(
            'Name of the incident, if applicable .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    to_name_and_position: str = Field(
        ...,
        description=(
            "Name and position/title of the message recipient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_name_and_position: str = Field(
        ...,
        description=(
            "Name and position/title of the message sender .If you cannot fill this, write "
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

    date: str = Field(..., description="Date the message is created")  # YYYY-MM-DD format

    time: str = Field(
        ...,
        description=(
            'Time the message is created .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class MessageContent(BaseModel):
    """Primary message text and approval details"""

    message: str = Field(
        ...,
        description=(
            "Full text of the message being communicated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approved_by_name: str = Field(
        ...,
        description=(
            "Name of the person approving the message .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approved_by_signature: str = Field(
        ...,
        description=(
            "Signature of the person approving the message .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approved_by_position_title: str = Field(
        ...,
        description=(
            "Position or title of the person approving the message .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Reply(BaseModel):
    """Reply text and responder details"""

    reply: str = Field(
        default="",
        description=(
            "Reply or response to the original message .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    replied_by_name: str = Field(
        default="",
        description=(
            "Name of the person providing the reply .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    replied_by_position_title: str = Field(
        default="",
        description=(
            "Position or title of the person providing the reply .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    replied_by_signature: str = Field(
        default="",
        description=(
            "Signature of the person providing the reply .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_time: str = Field(
        default="",
        description=(
            "Date and time the ICS 213 form was completed or logged .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class GeneralMessageics213(BaseModel):
    """GENERAL MESSAGE (ICS 213)"""

    message_header: MessageHeader = Field(..., description="Message Header")
    message_content: MessageContent = Field(..., description="Message Content")
    reply: Reply = Field(..., description="Reply")
