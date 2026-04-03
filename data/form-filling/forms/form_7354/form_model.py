from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic personal and contact information for the applicant"""

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

    middle_initial: str = Field(
        default="",
        description=(
            'Middle initial of applicant\'s name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    social_security_number: str = Field(..., description="Applicant's Social Security Number")

    street_address: str = Field(
        ...,
        description=(
            'Street address of current residence .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_state: str = Field(
        ...,
        description=(
            'City and state of current residence .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip_code: str = Field(..., description="Zip code of current residence")

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number where applicant can be reached .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    legal_eligibility_to_work_us: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you can provide documentation of legal authorization to work "
            "in the U.S."
        ),
    )

    minimum_salary_expected: str = Field(
        default="",
        description=(
            "Minimum salary or wage you are willing to accept .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position_apply_for: str = Field(
        ...,
        description=(
            "Job title or position for which you are applying .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    disciplined_for_sexual_harassment: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have ever been disciplined, terminated, or resigned due "
            "to sexual harassment in the workplace"
        ),
    )

    date_you_can_begin_work: str = Field(
        ..., description="Earliest date you are available to start work"
    )  # YYYY-MM-DD format

    are_you_18_years_of_age_or_older: BooleanLike = Field(
        ..., description="Indicate whether you are at least 18 years old"
    )


class Education(BaseModel):
    """High school, college, and other education details"""

    name_of_high_school_attended: str = Field(
        default="",
        description=(
            'Name of the high school you attended .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_state_high_school: str = Field(
        default="",
        description=(
            "City and state where the high school is located .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    graduate_high_school: BooleanLike = Field(
        default="", description="Indicate whether you graduated from high school"
    )

    ged_high_school: BooleanLike = Field(
        default="", description="Indicate whether you received a GED"
    )

    name_of_college_or_technical_school: str = Field(
        default="",
        description=(
            "Name of the college or technical school you attended .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_college_or_technical_school: str = Field(
        default="",
        description=(
            "City and state where the college or technical school is located .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    graduate_college_or_technical_school: BooleanLike = Field(
        default="",
        description="Indicate whether you graduated from this college or technical school",
    )

    degree_college_or_technical_school: BooleanLike = Field(
        default="", description="Indicate whether you received a degree from this institution"
    )

    major: str = Field(
        default="",
        description=(
            "Your major field of study at the college or technical school .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    are_you_presently_enrolled_in_school: BooleanLike = Field(
        default="", description="Indicate whether you are currently enrolled in any school"
    )

    current_school_name_address_and_expected_degree_date: str = Field(
        default="",
        description=(
            "Name and address of current school and your expected degree completion date "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    job_related_skills_or_accomplishments: str = Field(
        default="",
        description=(
            "Describe any job-related skills, accomplishments, or military service .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class WorkAvailability(BaseModel):
    """Days, times, and scheduling needs for work"""

    from_monday: str = Field(
        default="",
        description=(
            "Time you are available to start work on Monday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    to_monday: str = Field(
        default="",
        description=(
            "Time you are available to finish work on Monday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_tuesday: str = Field(
        default="",
        description=(
            "Time you are available to start work on Tuesday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to_tuesday: str = Field(
        default="",
        description=(
            "Time you are available to finish work on Tuesday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_wednesday: str = Field(
        default="",
        description=(
            "Time you are available to start work on Wednesday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to_wednesday: str = Field(
        default="",
        description=(
            "Time you are available to finish work on Wednesday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_thursday: str = Field(
        default="",
        description=(
            "Time you are available to start work on Thursday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to_thursday: str = Field(
        default="",
        description=(
            "Time you are available to finish work on Thursday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_friday: str = Field(
        default="",
        description=(
            "Time you are available to start work on Friday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    to_friday: str = Field(
        default="",
        description=(
            "Time you are available to finish work on Friday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_saturday: str = Field(
        default="",
        description=(
            "Time you are available to start work on Saturday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to_saturday: str = Field(
        default="",
        description=(
            "Time you are available to finish work on Saturday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_sunday: str = Field(
        default="",
        description=(
            "Time you are available to start work on Sunday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    to_sunday: str = Field(
        default="",
        description=(
            "Time you are available to finish work on Sunday .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    total_hours_per_week_available: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of hours per week you are available to work"
    )

    special_requests_or_needs_for_work_schedule: str = Field(
        default="",
        description=(
            "Describe any special scheduling requests or needs .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RenderhrLlcPayrollhumanResourceServiceApplicationForEmployment(BaseModel):
    """
        RenderHR LLC
    Payroll/Human Resource Service

    Application For Employment

        RenderHR LLC. is an Equal Opportunity Employer. Reasonable accommodation under the U.S. Americans with Disabilities Act, as amended, or California Fair Employment and Housing Act will be provided as required by applicable law.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    education: Education = Field(..., description="Education")
    work_availability: WorkAvailability = Field(..., description="Work Availability")
