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
    """Basic information about the applicant and their college plans"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            'Applicant\'s full home street address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of applicant\'s home address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of applicant's home address")

    zip_code: str = Field(..., description="ZIP code of applicant's home address")

    home_phone: str = Field(
        default="",
        description=(
            'Applicant\'s home telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        ...,
        description=(
            'Applicant\'s mobile/cell phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    social_security_number: str = Field(..., description="Applicant's Social Security Number")

    gender_male: BooleanLike = Field(..., description="Check if the applicant's gender is male")

    gender_female: BooleanLike = Field(..., description="Check if the applicant's gender is female")

    citizenship_us_citizen: BooleanLike = Field(
        ..., description="Check if the applicant is a U.S. citizen"
    )

    citizenship_legal_resident: BooleanLike = Field(
        ..., description="Check if the applicant is a legal resident (non-citizen)"
    )

    citizenship_other: str = Field(
        ...,
        description=(
            "If citizenship is other, specify the applicant's citizenship status .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    college_you_plan_to_attend: str = Field(
        ...,
        description=(
            "Name of the college or university the applicant plans to attend .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    area_of_study: str = Field(
        ...,
        description=(
            "Intended major or area of academic study .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    have_you_been_accepted: BooleanLike = Field(
        ..., description="Indicate whether the applicant has been accepted to the college"
    )

    reasons_for_selecting_college_line_1: str = Field(
        ...,
        description=(
            "First line of explanation for choosing this college and area of study .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reasons_for_selecting_college_line_2: str = Field(
        default="",
        description=(
            "Second line of explanation for choosing this college and area of study .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reasons_for_selecting_college_line_3: str = Field(
        default="",
        description=(
            "Third line of explanation for choosing this college and area of study .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class FamilyInformation(BaseModel):
    """Information about the applicant's father"""

    fathers_name: str = Field(
        default="",
        description=(
            "Applicant's father's full name .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fathers_address_if_different_from_above: str = Field(
        default="",
        description=(
            "Father's address if different from the applicant's home address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    fathers_occupation: str = Field(
        default="",
        description=(
            'Father\'s job title or occupation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fathers_employer: str = Field(
        default="",
        description=(
            'Name of father\'s employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class WalkerFamilyEducationFoundationHighSchoolApplication(BaseModel):
    """
        WALKER FAMILY EDUCATION FOUNDATION
    High School Application

        ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    family_information: FamilyInformation = Field(..., description="Family Information")
