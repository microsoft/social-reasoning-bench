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
    """Personal and contact information about the applicant, including work authorization and age"""

    name_last_name_first_name_middle_name: str = Field(
        ...,
        description=(
            "Applicant's full legal name in the order last, first, middle .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    street_address: str = Field(
        ...,
        description=(
            'Applicant\'s street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of current residence .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of current residence")

    zip_code: str = Field(..., description="ZIP code for current address")

    email_address: str = Field(
        ...,
        description=(
            "Primary email address for contacting the applicant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mobile_telephone: str = Field(
        ...,
        description=(
            'Applicant\'s mobile/cell phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_telephone: str = Field(
        default="",
        description=(
            "Applicant's home/landline phone number, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    authorized_to_work_us_yes: BooleanLike = Field(
        ...,
        description="Indicates that the applicant is legally authorized to work in the United States",
    )

    authorized_to_work_us_no: BooleanLike = Field(
        ...,
        description=(
            "Indicates that the applicant is not legally authorized to work in the United States"
        ),
    )

    at_least_18_yes: BooleanLike = Field(
        ..., description="Indicates that the applicant is at least 18 years old"
    )

    at_least_18_no: BooleanLike = Field(
        ..., description="Indicates that the applicant is under 18 years old"
    )

    if_yes_when: str = Field(
        default="",
        description=(
            "If previously applied, the approximate date of prior application .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    if_yes_what_position: str = Field(
        default="",
        description=(
            "If previously applied, the position previously applied for .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PositionInformation(BaseModel):
    """Details about the position being applied for and related preferences"""

    position_applying_for: str = Field(
        ...,
        description=(
            "Title or name of the position the applicant is seeking .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applying_for_full_time: BooleanLike = Field(
        default="", description="Indicates that the applicant is seeking full-time employment"
    )

    applying_for_part_time: BooleanLike = Field(
        default="", description="Indicates that the applicant is seeking part-time employment"
    )

    desired_rate_of_pay: str = Field(
        default="",
        description=(
            "Desired rate of pay (e.g., hourly or annual salary expectation) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    how_did_you_learn_about_position: str = Field(
        default="",
        description=(
            "Source where the applicant learned about the job opening .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    available_start_date: str = Field(
        default="", description="Earliest date the applicant would be available to start work"
    )  # YYYY-MM-DD format

    computer_software_tools_equipment: str = Field(
        default="",
        description=(
            "List of computer software, tools, or equipment the applicant can use "
            "proficiently that are relevant to the job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class pythonSouthwestWisconsinCommActionEmpApp(BaseModel):
    """
        SWCAP
    SOUTHWESTERN WISCONSIN COMMUNITY ACTION PROGRAM

    Employment Application

        The Southwestern Wisconsin Community Action Program is an Equal Opportunity Employer. The information requested in this employment application is needed for legally permissible reasons, including, without limitation, determination of bona fide occupational qualification or business necessity.
        The Civil Rights Act of 1964 prohibits discrimination because of race, color, religion, sex or national origin. Federal law also prohibits discrimination based on age and citizenship. The laws of Wisconsin prohibit discrimination based upon ancestry or marital status. The Americans with Disabilities Act prohibits discrimination against job applicants with disabilities who are qualified to perform the essential activities of the job and requires employers to provide individuals with a reasonable accommodation to enable them to meet legitimate job criteria.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    position_information: PositionInformation = Field(..., description="Position Information")
