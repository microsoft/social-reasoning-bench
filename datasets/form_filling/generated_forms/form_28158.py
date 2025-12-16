from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class JobDetails(BaseModel):
    """Information about the job being applied for and how the candidate heard about it"""

    job_title: str = Field(
        ...,
        description=(
            "Job title of the vacancy you are applying for .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_you_heard_about_this_vacancy: str = Field(
        default="",
        description=(
            "Explain how you found out about this vacancy (e.g. website, referral, advert) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class PersonalDetails(BaseModel):
    """Candidate's personal and contact information"""

    last_name: str = Field(
        ...,
        description=(
            'Your family name or surname .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Your given name or first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Your date of birth")  # YYYY-MM-DD format

    nationality: str = Field(
        ...,
        description=(
            "Your nationality as it appears on official documents .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Your full current home address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    post_code: str = Field(..., description="Postcode for your home address")

    home_telephone_no: str = Field(
        default="",
        description=(
            'Your home landline telephone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mobile_no: str = Field(
        ...,
        description=(
            'Your mobile/cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Your primary email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    national_insurance_no: str = Field(
        ...,
        description=(
            'Your UK National Insurance number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    eligible_to_take_up_employment_in_the_uk: BooleanLike = Field(
        ..., description="Indicate whether you are eligible to take up employment in the UK"
    )

    eligible_to_take_up_employment_in_the_uk_no: BooleanLike = Field(
        default="",
        description=(
            "Represents selection of 'No' for UK employment eligibility (usually stored "
            "together with the Yes/No field)"
        ),
    )


class DrivingLicense(BaseModel):
    """Information about the candidate's driving license, if relevant to the post"""

    hold_full_clean_uk_driving_license: BooleanLike = Field(
        default="",
        description="Indicate whether you hold a full, clean driving licence valid in the UK",
    )

    hold_full_clean_uk_driving_license_no: BooleanLike = Field(
        default="",
        description=(
            "Represents selection of 'No' for holding a full, clean UK driving licence "
            "(usually stored together with the Yes/No field)"
        ),
    )

    driving_license_if_no_details: str = Field(
        default="",
        description=(
            "Provide details if you do not hold a full, clean UK driving licence .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class DBSandConvictions(BaseModel):
    """Disclosure and Barring Service (DBS) information and unspent convictions"""

    unspent_convictions_details: str = Field(
        default="",
        description=(
            "Provide details of any convictions which are not spent under the "
            'Rehabilitation of Offenders Act 1974 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dbs_check_held: BooleanLike = Field(
        default="", description="Indicate whether you currently hold a DBS check"
    )

    dbs_check_held_no: BooleanLike = Field(
        default="",
        description=(
            "Represents selection of 'No' for holding a DBS check (usually stored together "
            "with the Yes/No field)"
        ),
    )

    dbs_date_issued: str = Field(
        default="", description="Date on which your current DBS certificate was issued"
    )  # YYYY-MM-DD format

    type_of_disclosure_held_enhanced: Literal["Enhanced", "Basic", "N/A", ""] = Field(
        default="", description="Type of DBS disclosure you hold"
    )

    type_of_disclosure_held_basic: Literal["Enhanced", "Basic", "N/A", ""] = Field(
        default="", description="Type of DBS disclosure you hold"
    )

    registered_to_the_update_service: BooleanLike = Field(
        default="", description="Indicate whether your DBS is registered to the update service"
    )

    registered_to_the_update_service_no: BooleanLike = Field(
        default="",
        description=(
            "Represents selection of 'No' for being registered to the DBS update service "
            "(usually stored together with the Yes/No field)"
        ),
    )


class CandidateRegistrationForm(BaseModel):
    """
    Candidate Registration Form

    ''
    """

    job_details: JobDetails = Field(..., description="Job Details")
    personal_details: PersonalDetails = Field(..., description="Personal Details")
    driving_license: DrivingLicense = Field(..., description="Driving License")
    dbs_and_convictions: DBSandConvictions = Field(..., description="DBS and Convictions")
