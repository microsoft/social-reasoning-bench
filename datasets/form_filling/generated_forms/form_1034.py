from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalInformation(BaseModel):
    """Basic personal and contact details, and position sought"""

    last_name: str = Field(
        ...,
        description=(
            'Applicant\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mi: str = Field(
        default="",
        description=(
            'Middle initial .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    mailing_address_street: str = Field(
        ...,
        description=(
            "Street portion of current mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_and_zip_code: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            'Home telephone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Mobile/cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
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

    todays_date: str = Field(
        ..., description="Date this application is completed"
    )  # YYYY-MM-DD format

    positions_applying_for: str = Field(
        ...,
        description=(
            "Title(s) of the position(s) you are applying for .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_available_to_start: str = Field(
        ..., description="Earliest date you are available to begin work"
    )  # YYYY-MM-DD format

    work_desired_full_time: BooleanLike = Field(
        default="", description="Check if you are seeking full-time work"
    )

    work_desired_part_time: BooleanLike = Field(
        default="", description="Check if you are seeking part-time work"
    )

    work_desired_on_call_occasional: BooleanLike = Field(
        default="", description="Check if you are seeking on-call or occasional work"
    )


class AdditionalEmploymentQuestions(BaseModel):
    """Additional eligibility, prior employment, and work-related questions"""

    accept_shift_work_yes: BooleanLike = Field(
        default="", description="Indicate yes if you are willing to work shift schedules"
    )

    accept_shift_work_no: BooleanLike = Field(
        default="", description="Indicate no if you are not willing to work shift schedules"
    )

    prior_employment_centre_county_yes: BooleanLike = Field(
        default="",
        description="Check yes if you have previously been employed by Centre County Government",
    )

    prior_employment_centre_county_no: BooleanLike = Field(
        default="",
        description="Check no if you have not previously been employed by Centre County Government",
    )

    prior_employment_departments: str = Field(
        default="",
        description=(
            "List the Centre County department(s) where you were previously employed .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    prior_employment_dates: str = Field(
        default="",
        description=(
            "Dates of your prior employment with Centre County Government .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    relatives_employed_yes: BooleanLike = Field(
        default="",
        description="Check yes if you currently have relatives employed by Centre County Government",
    )

    relatives_employed_no: BooleanLike = Field(
        default="",
        description="Check no if you do not have relatives employed by Centre County Government",
    )

    relatives_details_line_1: str = Field(
        default="",
        description=(
            "First line to list relative's name, relationship, and employing department .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    relatives_details_line_2: str = Field(
        default="",
        description=(
            "Second line to list additional relative details if needed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    veteran_status_yes: BooleanLike = Field(
        default="", description="Check yes if you have served in the US Military and are a veteran"
    )

    veteran_status_no: BooleanLike = Field(
        default="", description="Check no if you have not served in the US Military as a veteran"
    )

    military_branch: str = Field(
        default="",
        description=(
            "Branch of the US Military in which you served .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    years_of_service: str = Field(
        default="",
        description=(
            'Total years of military service .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    age_18_requirement_na: BooleanLike = Field(
        default="", description="Select N/A if the position does not involve driving"
    )

    age_18_requirement_yes: BooleanLike = Field(
        default="",
        description="Select yes if you are at least 18 and can meet the driving age requirement",
    )

    age_18_requirement_no: BooleanLike = Field(
        default="",
        description="Select no if you cannot meet the minimum age requirement for driving",
    )

    can_drive_na: BooleanLike = Field(
        default="", description="Select N/A if the position does not involve driving"
    )

    can_drive_yes: BooleanLike = Field(
        default="", description="Select yes if you are able and licensed to drive for the job"
    )

    can_drive_no: BooleanLike = Field(
        default="", description="Select no if you are not able or licensed to drive for the job"
    )

    authorized_to_work_yes: BooleanLike = Field(
        ..., description="Confirm that you are legally authorized to work in the United States"
    )

    authorized_to_work_no: BooleanLike = Field(
        ...,
        description="Indicate no if you are not legally authorized to work in the United States",
    )

    background_check_fee_yes: BooleanLike = Field(
        default="", description="Select yes if you agree to pay any required background check fee"
    )

    background_check_fee_no: BooleanLike = Field(
        default="",
        description="Select no if you do not agree to pay any required background check fee",
    )


class CentreCountyPennsylvania(BaseModel):
    """
        CENTRE COUNTY
    PENNSYLVANIA

        PLEASE NOTE: Complete ALL parts of the application. If you have no information to enter in a section, please write N/A.
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    additional_employment_questions: AdditionalEmploymentQuestions = Field(
        ..., description="Additional Employment Questions"
    )
