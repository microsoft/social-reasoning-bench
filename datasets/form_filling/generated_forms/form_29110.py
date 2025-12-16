from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmploymentHistory(BaseModel):
    """Current and former employers for the past three years"""

    date_of_employment_from_month_year: str = Field(
        ..., description="Starting month and year of this employment period"
    )  # YYYY-MM-DD format

    date_of_employment_to_month_year: str = Field(
        ..., description="Ending month and year of this employment period"
    )  # YYYY-MM-DD format

    employer: str = Field(
        ...,
        description=(
            "Name of the employer for this position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_of_your_position: str = Field(
        ...,
        description=(
            "Job title or position held with this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    may_we_contact_yes: BooleanLike = Field(
        default="", description="Check if the employer may be contacted for a reference (Yes)"
    )

    may_we_contact_no: BooleanLike = Field(
        default="", description="Check if the employer may NOT be contacted for a reference (No)"
    )

    hours_worked_per_week: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of hours worked per week in this position"
    )

    address: str = Field(
        default="",
        description=(
            'Street address of the employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        default="",
        description=(
            'City where the employer is located .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_zip: str = Field(
        default="",
        description=(
            "State and ZIP code of the employer’s address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_while_employed_here: str = Field(
        default="",
        description=(
            "Name used during this employment if different from current name .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    salary_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Base salary or wage amount for this position"
    )

    salary_per_time_period: str = Field(
        default="",
        description=(
            "Time period for the salary (e.g., hour, week, month, year) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name_and_phone_number: str = Field(
        default="",
        description=(
            "Name and phone number of your supervisor at this job .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving: str = Field(
        default="",
        description=(
            "Brief explanation of why you left this position .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    duties_description_1: str = Field(
        default="",
        description=(
            "Description of primary job duties and responsibilities (line 1) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    duties_description_2: str = Field(
        default="",
        description=(
            "Additional description of job duties and responsibilities (line 2) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_employment_from_month_year_2: str = Field(
        default="", description="Starting month and year of the second listed employment period"
    )  # YYYY-MM-DD format

    date_of_employment_to_month_year_2: str = Field(
        default="", description="Ending month and year of the second listed employment period"
    )  # YYYY-MM-DD format

    employer_2: str = Field(
        default="",
        description=(
            "Name of the employer for the second listed position .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_of_your_position_2: str = Field(
        default="",
        description=(
            "Job title or position held with the second employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    may_we_contact_yes_2: BooleanLike = Field(
        default="", description="For the second employer, check if they may be contacted (Yes)"
    )

    may_we_contact_no_2: BooleanLike = Field(
        default="", description="For the second employer, check if they may NOT be contacted (No)"
    )

    hours_worked_per_week_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of hours worked per week for the second position"
    )

    address_2: str = Field(
        default="",
        description=(
            'Street address of the second employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_2: str = Field(
        default="",
        description=(
            "City where the second employer is located .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_zip_2: str = Field(
        default="",
        description=(
            "State and ZIP code of the second employer’s address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_while_employed_here_2: str = Field(
        default="",
        description=(
            "Name used during employment with the second employer, if different .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    salary_amount_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Base salary or wage amount for the second position"
    )

    salary_per_time_period_2: str = Field(
        default="",
        description=(
            "Time period for the salary for the second position (e.g., hour, week, month, "
            'year) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    supervisors_name_and_phone_number_2: str = Field(
        default="",
        description=(
            "Name and phone number of your supervisor at the second job .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_2: str = Field(
        default="",
        description=(
            "Brief explanation of why you left the second position .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    duties_description_1_2: str = Field(
        default="",
        description=(
            "Description of primary job duties for the second position (line 1) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    duties_description_2_2: str = Field(
        default="",
        description=(
            "Additional description of job duties for the second position (line 2) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_employment_from_month_year_3: str = Field(
        default="", description="Starting month and year of the third listed employment period"
    )  # YYYY-MM-DD format

    date_of_employment_to_month_year_3: str = Field(
        default="", description="Ending month and year of the third listed employment period"
    )  # YYYY-MM-DD format

    employer_3: str = Field(
        default="",
        description=(
            "Name of the employer for the third listed position .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_of_your_position_3: str = Field(
        default="",
        description=(
            "Job title or position held with the third employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    may_we_contact_yes_3: BooleanLike = Field(
        default="", description="For the third employer, check if they may be contacted (Yes)"
    )

    may_we_contact_no_3: BooleanLike = Field(
        default="", description="For the third employer, check if they may NOT be contacted (No)"
    )

    hours_worked_per_week_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of hours worked per week for the third position"
    )

    address_3: str = Field(
        default="",
        description=(
            'Street address of the third employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_3: str = Field(
        default="",
        description=(
            "City where the third employer is located .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_zip_3: str = Field(
        default="",
        description=(
            "State and ZIP code of the third employer’s address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_while_employed_here_3: str = Field(
        default="",
        description=(
            "Name used during employment with the third employer, if different .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    salary_amount_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Base salary or wage amount for the third position"
    )

    salary_per_time_period_3: str = Field(
        default="",
        description=(
            "Time period for the salary for the third position (e.g., hour, week, month, "
            'year) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    supervisors_name_and_phone_number_3: str = Field(
        default="",
        description=(
            "Name and phone number of your supervisor at the third job .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_3: str = Field(
        default="",
        description=(
            "Brief explanation of why you left the third position .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    duties_description_1_3: str = Field(
        default="",
        description=(
            "Description of primary job duties for the third position (line 1) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    duties_description_2_3: str = Field(
        default="",
        description=(
            "Additional description of job duties for the third position (line 2) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class TrainingandCertification(BaseModel):
    """Special studies, training, qualifications, and activities"""

    subjects_of_special_study_or_research_work_description_1: str = Field(
        default="",
        description=(
            "First line describing any subjects of special study or research work .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    subjects_of_special_study_or_research_work_description_2: str = Field(
        default="",
        description=(
            "Second line for additional subjects of special study or research work .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    special_training_or_qualifications_description_1: str = Field(
        default="",
        description=(
            "First line describing any special training or qualifications .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    special_training_or_qualifications_description_2: str = Field(
        default="",
        description=(
            "Second line for additional special training or qualifications .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    activities_civic_athletic_etc: str = Field(
        default="",
        description=(
            "Civic, athletic, or other activities you participate in (excluding protected "
            'memberships) .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class EmploymentHistory(BaseModel):
    """
    EMPLOYMENT HISTORY

    List your current and former employers for the past three (3) years, starting with the most recent. If you need additional space, please continue on a separate sheet of paper.
    """

    employment_history: EmploymentHistory = Field(..., description="Employment History")
    training_and_certification: TrainingandCertification = Field(
        ..., description="Training and Certification"
    )
