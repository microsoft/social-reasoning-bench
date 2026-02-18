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
    """Basic personal and contact information, position, and eligibility"""

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
            'Primary phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    legal_eligibility_to_work_us: BooleanLike = Field(
        ...,
        description="Indicate if you can provide proof of legal eligibility to work in the U.S.",
    )

    minimum_salary_expected: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Minimum salary you are willing to accept"
    )

    position_apply_for: str = Field(
        ...,
        description=(
            "Job title or position you are applying for .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sexual_harassment_history: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you have ever been disciplined, terminated, or resigned due to "
            "sexual harassment in the workplace"
        ),
    )

    date_you_can_begin_work: str = Field(
        ..., description="Earliest date you are available to start work"
    )  # YYYY-MM-DD format

    are_you_18_years_of_age_or_older: BooleanLike = Field(
        ..., description="Indicate if you are at least 18 years old"
    )


class Education(BaseModel):
    """Educational background and related training"""

    name_of_high_school_attended: str = Field(
        default="",
        description=(
            "Full name of the high school you attended .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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

    graduate_yn_high_school: BooleanLike = Field(
        default="", description="Indicate if you graduated from high school"
    )

    ged_yn_high_school: BooleanLike = Field(
        default="", description="Indicate if you obtained a GED"
    )

    name_of_college_or_technical_school: str = Field(
        default="",
        description=(
            "Name of the college or technical school attended .If you cannot fill this, "
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

    graduate_yn_college_or_technical_school: BooleanLike = Field(
        default="", description="Indicate if you graduated from this college or technical school"
    )

    degree_yn_college_or_technical_school: BooleanLike = Field(
        default="", description="Indicate if you received a degree from this institution"
    )

    major: str = Field(
        default="",
        description=(
            'Your major field of study .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    additional_training_or_education: str = Field(
        default="",
        description=(
            "Any additional training, certifications, or education .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    are_you_presently_enrolled_in_school: BooleanLike = Field(
        default="", description="Indicate if you are currently enrolled in any school"
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
            "Job-related skills, accomplishments, and any military service details .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class WorkAvailability(BaseModel):
    """Days, times, and scheduling needs for work"""

    monday_work_availability: str = Field(
        default="",
        description=(
            "Hours you are available to work on Monday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tuesday_work_availability: str = Field(
        default="",
        description=(
            "Hours you are available to work on Tuesday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    wednesday_work_availability: str = Field(
        default="",
        description=(
            "Hours you are available to work on Wednesday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    thursday_work_availability: str = Field(
        default="",
        description=(
            "Hours you are available to work on Thursday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    friday_work_availability: str = Field(
        default="",
        description=(
            "Hours you are available to work on Friday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    saturday_work_availability: str = Field(
        default="",
        description=(
            "Hours you are available to work on Saturday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sunday_work_availability: str = Field(
        default="",
        description=(
            "Hours you are available to work on Sunday .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    availability_from_time: str = Field(
        default="",
        description=(
            "Earliest time you are available to work each day .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    availability_to_time: str = Field(
        default="",
        description=(
            "Latest time you are available to work each day .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    total_hours_per_week_available: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of hours per week you are available to work"
    )

    special_requests_or_needs_for_work_schedule: str = Field(
        default="",
        description=(
            "Any special scheduling requests or needs .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RenderhrLlcPayrollhumanResourceServiceApplicationForEmployment(BaseModel):
    """
        RenderHR LLC
    Payroll/Human Resource Service

    Application For Employment

        RenderHR LLC is an Equal Opportunity Employer. Reasonable accommodation under the U.S. Americans with Disabilities Act, as amended, or California Fair Employment and Housing Act will be provided as required by applicable law. Any offer of employment is conditioned upon background, credit and drug test results and are at the sole discretion of RendHR LLC.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    education: Education = Field(..., description="Education")
    work_availability: WorkAvailability = Field(..., description="Work Availability")
