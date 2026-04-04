from pydantic import BaseModel, ConfigDict, Field


class Ics213GeneralMessage(BaseModel):
    """ICS 213 General Message

    Use this form during an incident to document and transmit an official message, request, or update. The sender completes the “From,” “To,” subject, and message details, and the intended recipient (or their designee) reads it to take action, coordinate resources, and/or provide a written reply with signature and timing for accountability and tracking.
    """

    model_config = ConfigDict(extra="forbid")

    subject: str = Field(
        ...,
        description='Message subject. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    message_body: str = Field(
        ...,
        description='Message content. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    reply_body: str = Field(
        ...,
        description='Reply content. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )