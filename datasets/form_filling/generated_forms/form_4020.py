from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MandatoryDemographicInformationToBeCompletedByApprentice(BaseModel):
    """
    Mandatory Demographic Information – to be completed by Apprentice

    Mandatory Demographic Information – to be completed by Apprentice
    """

    social_security_number: str = Field(..., description="Apprentice's Social Security Number")

    email: str = Field(
        ...,
        description=(
            'Apprentice\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Apprentice's date of birth")  # YYYY-MM-DD format

    phone: str = Field(
        ...,
        description=(
            'Apprentice\'s primary phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    gender: str = Field(..., description="Apprentice's gender (selected from drop-down)")

    highest_level_of_school_completed: str = Field(
        ..., description="Highest level of education completed (selected from drop-down)"
    )

    veteran: str = Field(..., description="Veteran status (selected from drop-down)")

    ethnicity_white: BooleanLike = Field(
        default="", description="Check if the apprentice identifies as White"
    )

    ethnicity_black_or_african_american: BooleanLike = Field(
        default="", description="Check if the apprentice identifies as Black or African American"
    )

    ethnicity_hispanic_or_latino: BooleanLike = Field(
        default="", description="Check if the apprentice identifies as Hispanic or Latino"
    )

    ethnicity_asian_or_pacific_islander: BooleanLike = Field(
        default="", description="Check if the apprentice identifies as Asian or Pacific Islander"
    )

    ethnicity_american_indian_or_alaskan_native: BooleanLike = Field(
        default="",
        description="Check if the apprentice identifies as American Indian or Alaskan Native",
    )

    indicate_any_special_accommodations_you_may_require: str = Field(
        default="",
        description=(
            "Describe any special accommodations needed to participate in the "
            'apprenticeship .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    how_did_you_hear_about_this_apprenticeship_program: str = Field(
        default="",
        description=(
            "Explain how you learned about this apprenticeship program .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    did_you_graduate_from_a_pre_apprenticeship_program: BooleanLike = Field(
        default="", description="Indicate whether you graduated from a pre-apprenticeship program"
    )

    if_yes_which_pre_apprenticeship_program: str = Field(
        default="",
        description=(
            "Name of the pre-apprenticeship program, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )
