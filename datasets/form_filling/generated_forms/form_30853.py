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
    """Basic personal and contact details for the applicant"""

    full_name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Complete mailing address where you receive mail .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            "Home telephone number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        ...,
        description=(
            "Cell/mobile phone number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Primary email address for contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    male: BooleanLike = Field(default="", description="Check if the applicant identifies as male")

    female: BooleanLike = Field(
        default="", description="Check if the applicant identifies as female"
    )

    social_security_number: str = Field(..., description="Applicant's Social Security Number")

    date_of_birth: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format


class CollegeInformation(BaseModel):
    """Details about the applicant's current or continuing college"""

    continuing_college_name: str = Field(
        ...,
        description=(
            "Name of the college or university you will be attending or continuing at .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    continuing_college_address: str = Field(
        ...,
        description=(
            "Mailing address of the continuing college or university .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_college_year: str = Field(
        ...,
        description=(
            "Your current year in college (e.g., Freshman, Sophomore, 1st year, 2nd year) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    current_gpa: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Your current cumulative grade point average"
    )


class ActivitiesandInvolvement(BaseModel):
    """School and community involvement information"""

    school_involvement_include_offices_held_honors_and_awards: str = Field(
        ...,
        description=(
            "Describe your school activities, including offices held, honors, and awards "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    community_involvement: str = Field(
        ...,
        description=(
            "Describe your involvement and activities in the community .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TwentyPearlsIncorporatedDrTamaraAJonesUndergraduateScholarship(BaseModel):
    """
        Twenty Pearls Incorporated
    Dr. Tamara A. Jones Undergraduate Scholarship

        ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    college_information: CollegeInformation = Field(..., description="College Information")
    activities_and_involvement: ActivitiesandInvolvement = Field(
        ..., description="Activities and Involvement"
    )
