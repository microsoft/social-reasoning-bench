from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CitizenConcern(BaseModel):
    """Information submitted by the citizen about their concern"""

    name: str = Field(
        ...,
        description=(
            'Your full name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    concern: str = Field(
        ...,
        description=(
            "Short description or title of your concern .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_if_applicable: str = Field(
        default="",
        description=(
            "Location related to the concern, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates_if_applicable: str = Field(
        default="",
        description=(
            "Relevant date or range of dates for the concern, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    details: str = Field(
        ...,
        description=(
            'Detailed description of the concern .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ForTownUse(BaseModel):
    """Internal use section for town staff processing the concern"""

    referred_to: str = Field(
        default="",
        description=(
            "Department, person, or office to which this concern is referred .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_referred_to: str = Field(
        default="", description="Date the concern was referred"
    )  # YYYY-MM-DD format

    referred_by: str = Field(
        default="",
        description=(
            "Name or role of the person who referred the concern .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments: str = Field(
        default="",
        description=(
            "Internal comments or notes by town staff .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reply: str = Field(
        default="",
        description=(
            "Reply or response provided to the citizen .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signed: str = Field(
        default="",
        description=(
            "Signature of the town staff member completing the form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_signed: str = Field(
        default="", description="Date the form was signed"
    )  # YYYY-MM-DD format


class CitizenConcernForm(BaseModel):
    """
    Citizen Concern Form

    ''
    """

    citizen_concern: CitizenConcern = Field(..., description="Citizen Concern")
    for_town_use: ForTownUse = Field(..., description="For Town Use")
