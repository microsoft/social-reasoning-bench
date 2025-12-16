from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic personal and contact details for the auditioning musician"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    instrument: str = Field(
        ...,
        description=(
            'Primary instrument for the audition .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Street mailing address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of residence (abbreviation)")

    zip: str = Field(..., description="Zip or postal code")

    phone_day: str = Field(
        ...,
        description=(
            'Daytime phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    phone_evening: str = Field(
        default="",
        description=(
            'Evening or alternate phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class MusicalBackground(BaseModel):
    """Experience and training on the applicant's instrument"""

    years_studying_instrument: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of years you have studied your primary instrument"
    )

    private_instructors: str = Field(
        ...,
        description=(
            "Names and, if possible, contact information for all previous and current "
            'private music instructors .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    orchestras_ensembles: str = Field(
        ...,
        description=(
            "Names of all orchestras or ensembles you have previously played with or "
            'currently belong to .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class SEPASymphonyOrchestraAuditionInfoForm(BaseModel):
    """
        SOUTHEASTERN PENNSYLVANIA
    SYMPHONY ORCHESTRA
    ALLAN R. SCOTT, MUSIC DIRECTOR

    AUDITION INFORMATION FORM

        ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    musical_background: MusicalBackground = Field(..., description="Musical Background")
