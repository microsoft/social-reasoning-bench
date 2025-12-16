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
    """Basic routing and subject information for the message"""

    to: str = Field(
        ...,
        description=(
            "Name or identifier of the message recipient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    position_of_recipient: str = Field(
        ...,
        description=(
            "Position or role title of the message recipient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    position_of_sender: str = Field(
        ...,
        description=(
            "Position or role title of the message sender .If you cannot fill this, write "
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

    date: str = Field(..., description="Date the original message is created")  # YYYY-MM-DD format

    time: str = Field(
        ...,
        description=(
            'Time the original message is created .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MessageBody(BaseModel):
    """Main message content and sender signature"""

    message: str = Field(
        ...,
        description=(
            'Full text of the original message .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the person sending the original message .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position_of_signer: str = Field(
        ...,
        description=(
            "Position or role title of the person signing the original message .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Reply(BaseModel):
    """Reply content and reply authentication details"""

    reply: str = Field(
        default="",
        description=(
            "Text of the reply to the original message .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_reply: str = Field(
        default="", description="Date the reply is recorded"
    )  # YYYY-MM-DD format

    time_of_reply: str = Field(
        default="",
        description=(
            'Time the reply is recorded .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    signature_position_of_reply: str = Field(
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
