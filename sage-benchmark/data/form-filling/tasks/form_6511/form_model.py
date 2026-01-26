from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ContactBillingDetails(BaseModel):
    """Basic personal, company, and billing contact information"""

    name: str = Field(
        ...,
        description=(
            'Your full name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    company: str = Field(
        default="",
        description=(
            'Name of your company or organisation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Your main postal address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    invoice_address_if_different: str = Field(
        default="",
        description=(
            "Alternative address to be used for invoicing, if different from main address "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            'Primary contact telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary contact email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class TrainingExperience(BaseModel):
    """Coaching/supervision training background and experience"""

    coach_supervision_related_training_qualifications_and_certifications_including_the_date_duration_and_level: str = Field(
        ...,
        description=(
            "List your coach/supervision-related training, qualifications, and "
            "certifications, including date, duration, and level for each .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    how_long_have_you_been_practicing_as_a_coach_a_coach: str = Field(
        default="",
        description=(
            "Length of time you have been practicing as an individual coach .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    how_long_have_you_been_practicing_as_a_coach_team_coach: str = Field(
        default="",
        description=(
            "Length of time you have been practicing as a team coach .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_long_have_you_been_practicing_as_a_coach_coach_supervisor: str = Field(
        default="",
        description=(
            "Length of time you have been practicing as a coach supervisor .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    how_long_have_you_been_practicing_as_a_coach_other: str = Field(
        default="",
        description=(
            "Length of time you have been practicing in any other related coaching role "
            '(please specify role and duration) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class Form6511(BaseModel):
    """


    ''
    """

    contact__billing_details: ContactBillingDetails = Field(
        ..., description="Contact & Billing Details"
    )
    training__experience: TrainingExperience = Field(..., description="Training & Experience")
