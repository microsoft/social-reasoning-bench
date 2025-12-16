from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WorkExperienceJob1(BaseModel):
    """Details for the most recent job"""

    employer: str = Field(
        ...,
        description=(
            "Name of the employer for your most recent job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates_worked_from: str = Field(
        ..., description="Start date of employment for this job"
    )  # YYYY-MM-DD format

    dates_worked_to: str = Field(
        ..., description="End date of employment for this job"
    )  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            'Mailing address of the employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Employer’s phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    hours_week: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Average number of hours worked per week at this job"
    )

    job_title: str = Field(
        ...,
        description=(
            "Your job title or position at this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    starting_salary: str = Field(
        default="",
        description=(
            "Salary or wage when you started this job (include rate such as per hour or per "
            'year if applicable) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    current_salary: str = Field(
        default="",
        description=(
            "Most recent or ending salary or wage for this job .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name: str = Field(
        ...,
        description=(
            "Name of your immediate supervisor at this job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving: str = Field(
        default="",
        description=(
            "Brief explanation of why you left this job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_line_1: str = Field(
        ...,
        description=(
            "First line describing your main responsibilities and duties in this job .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_your_duties_line_2: str = Field(
        default="",
        description=(
            "Second line for additional description of your responsibilities and duties in "
            'this job .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class WorkExperienceJob2(BaseModel):
    """Details for the second most recent job"""

    employer_2: str = Field(
        default="",
        description=(
            "Name of the employer for your second most recent job .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dates_worked_from_2: str = Field(
        default="", description="Start date of employment for your second most recent job"
    )  # YYYY-MM-DD format

    dates_worked_to_2: str = Field(
        default="", description="End date of employment for your second most recent job"
    )  # YYYY-MM-DD format

    address_2: str = Field(
        default="",
        description=(
            "Mailing address of the employer for your second most recent job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone_2: str = Field(
        default="",
        description=(
            "Employer’s phone number for your second most recent job .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hours_week_2: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Average number of hours worked per week at your second most recent job",
    )

    job_title_2: str = Field(
        default="",
        description=(
            "Your job title or position at your second most recent employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    starting_salary_2: str = Field(
        default="",
        description=(
            "Starting salary or wage for your second most recent job .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_salary_2: str = Field(
        default="",
        description=(
            "Most recent or ending salary or wage for your second most recent job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    supervisors_name_2: str = Field(
        default="",
        description=(
            "Name of your immediate supervisor at your second most recent job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reason_for_leaving_2: str = Field(
        default="",
        description=(
            "Brief explanation of why you left your second most recent job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    describe_your_duties_line_1_2: str = Field(
        default="",
        description=(
            "First line describing your main responsibilities and duties in your second "
            'most recent job .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    describe_your_duties_line_2_2: str = Field(
        default="",
        description=(
            "Second line for additional description of your responsibilities and duties in "
            'your second most recent job .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class WorkExperienceJob3(BaseModel):
    """Details for the third most recent job"""

    employer_3: str = Field(
        default="",
        description=(
            "Name of the employer for your third most recent job .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dates_worked_from_3: str = Field(
        default="", description="Start date of employment for your third most recent job"
    )  # YYYY-MM-DD format

    dates_worked_to_3: str = Field(
        default="", description="End date of employment for your third most recent job"
    )  # YYYY-MM-DD format

    address_3: str = Field(
        default="",
        description=(
            "Mailing address of the employer for your third most recent job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone_3: str = Field(
        default="",
        description=(
            "Employer’s phone number for your third most recent job .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hours_week_3: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Average number of hours worked per week at your third most recent job",
    )

    job_title_3: str = Field(
        default="",
        description=(
            "Your job title or position at your third most recent employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    starting_salary_3: str = Field(
        default="",
        description=(
            "Starting salary or wage for your third most recent job .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_salary_3: str = Field(
        default="",
        description=(
            "Most recent or ending salary or wage for your third most recent job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    supervisors_name_3: str = Field(
        default="",
        description=(
            "Name of your immediate supervisor at your third most recent job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reason_for_leaving_3: str = Field(
        default="",
        description=(
            "Brief explanation of why you left your third most recent job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    describe_your_duties_line_1_3: str = Field(
        default="",
        description=(
            "First line describing your main responsibilities and duties in your third most "
            'recent job .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    describe_your_duties_line_2_3: str = Field(
        default="",
        description=(
            "Second line for additional description of your responsibilities and duties in "
            'your third most recent job .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class WorkExperience(BaseModel):
    """
    WORK EXPERIENCE

    Please list complete information on your three most recent jobs. You may attach a resume or a separate sheet with additional employment information if you wish.
    """

    work_experience___job_1: WorkExperienceJob1 = Field(..., description="Work Experience - Job 1")
    work_experience___job_2: WorkExperienceJob2 = Field(..., description="Work Experience - Job 2")
    work_experience___job_3: WorkExperienceJob3 = Field(..., description="Work Experience - Job 3")
