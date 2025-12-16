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
    """Basic personal and contact information for the applicant"""

    last_name: str = Field(
        ...,
        description=(
            'Applicant\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    middle_initial: str = Field(
        default="",
        description=(
            'Applicant\'s middle initial .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    social_security_number: str = Field(..., description="Applicant's Social Security Number")

    street_address: str = Field(
        ...,
        description=(
            'Applicant\'s street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city_state: str = Field(
        ...,
        description=(
            'City and state of current address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip_code: str = Field(..., description="Zip code of current address")

    phone_number: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    legal_eligibility_to_work_us: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you can provide documentation of legal eligibility to work in "
            "the U.S. if hired"
        ),
    )

    minimum_salary_expected: str = Field(
        ...,
        description=(
            "Minimum salary or wage you are willing to accept .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position_apply_for: str = Field(
        ...,
        description=(
            "Job title or position you are applying for .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    disciplined_for_sexual_harassment: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have ever been disciplined, terminated, or resigned due "
            "to sexual harassment in the workplace"
        ),
    )

    explain_yes_answers_sexual_harassment: str = Field(
        default="",
        description=(
            "If you answered Yes regarding sexual harassment history, provide detailed "
            "explanation with dates and circumstances .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_you_can_begin_work: str = Field(
        ..., description="Earliest date you are available to start work"
    )  # YYYY-MM-DD format

    are_you_18_years_of_age_or_older: BooleanLike = Field(
        ..., description="Indicate whether you are at least 18 years old"
    )

    under_18_documentation_notice: str = Field(
        default="",
        description=(
            "Notice regarding documentation requirements if applicant is under 18 years of "
            'age .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Education(BaseModel):
    """High school, college, and other education or training details"""

    high_school_name: str = Field(
        ...,
        description=(
            'Name of the high school you attended .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    high_school_city_state: str = Field(
        ...,
        description=(
            "City and state where your high school is located .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_graduate_yn: BooleanLike = Field(
        ..., description="Indicate whether you graduated from high school"
    )

    high_school_ged_yn: BooleanLike = Field(
        default="", description="Indicate whether you obtained a GED"
    )

    college_name: str = Field(
        default="",
        description=(
            "Name of the college or technical school you attended .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_city_state: str = Field(
        default="",
        description=(
            "City and state where your college or technical school is located .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    college_graduate_yn: BooleanLike = Field(
        default="",
        description="Indicate whether you graduated from this college or technical school",
    )

    college_degree_yn: BooleanLike = Field(
        default="", description="Indicate whether you received a degree from this institution"
    )

    college_major: str = Field(
        default="",
        description=(
            'Your major field of study .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    presently_enrolled_in_school: BooleanLike = Field(
        default="", description="Indicate whether you are currently enrolled in any school program"
    )

    current_school_details: str = Field(
        default="",
        description=(
            "If currently enrolled, provide the name, address of the school, and your "
            'expected degree completion date .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    job_related_skills: str = Field(
        default="",
        description=(
            "Describe any job-related skills, accomplishments, or military service "
            'experience .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class WorkAvailability(BaseModel):
    """Days and hours available to work and scheduling needs"""

    work_availability_from_monday: str = Field(
        ...,
        description=(
            "Time you are available to start work on Mondays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_from_tuesday: str = Field(
        ...,
        description=(
            "Time you are available to start work on Tuesdays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_from_wednesday: str = Field(
        ...,
        description=(
            "Time you are available to start work on Wednesdays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_from_thursday: str = Field(
        ...,
        description=(
            "Time you are available to start work on Thursdays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_from_friday: str = Field(
        ...,
        description=(
            "Time you are available to start work on Fridays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_from_saturday: str = Field(
        default="",
        description=(
            "Time you are available to start work on Saturdays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_from_sunday: str = Field(
        default="",
        description=(
            "Time you are available to start work on Sundays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_to_monday: str = Field(
        ...,
        description=(
            "Time you are available to end work on Mondays .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_to_tuesday: str = Field(
        ...,
        description=(
            "Time you are available to end work on Tuesdays .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_to_wednesday: str = Field(
        ...,
        description=(
            "Time you are available to end work on Wednesdays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_to_thursday: str = Field(
        ...,
        description=(
            "Time you are available to end work on Thursdays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_to_friday: str = Field(
        ...,
        description=(
            "Time you are available to end work on Fridays .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_to_saturday: str = Field(
        default="",
        description=(
            "Time you are available to end work on Saturdays .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_availability_to_sunday: str = Field(
        default="",
        description=(
            "Time you are available to end work on Sundays .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    total_hours_per_week_available: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of hours per week you are available to work"
    )

    special_work_schedule_requests: str = Field(
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

        RenderHR LLC is an Equal Opportunity Employer. Reasonable accommodation under the U.S. Americans with Disabilities Act, as amended, or California Fair Employment and Housing Act will be provided as required by applicable law.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    education: Education = Field(..., description="Education")
    work_availability: WorkAvailability = Field(..., description="Work Availability")
