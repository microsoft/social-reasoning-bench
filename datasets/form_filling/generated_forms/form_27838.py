from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class JobSource(BaseModel):
    """How the applicant heard about the job"""

    internet: BooleanLike = Field(
        default="", description="Check if you heard about the job via the internet"
    )

    ad: str = Field(
        default="",
        description=(
            "Specify the advertisement source where you saw the job .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employee_referral: str = Field(
        default="",
        description=(
            'Name of the employee who referred you .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class EmploymentHistoryMostRecentorCurrentEmployer(BaseModel):
    """Details for the most recent or current employment"""

    most_recent_or_current_employers_name: str = Field(
        ...,
        description=(
            "Name of your most recent or current employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Telephone number for your most recent or current employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Address of your most recent or current employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employed_month_year_from: str = Field(
        ...,
        description=(
            "Month and year you started with your most recent or current employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    employed_month_year_to: str = Field(
        ...,
        description=(
            "Month and year you ended employment with your most recent or current employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    last_job_title: str = Field(
        ...,
        description=(
            "Your last job title with your most recent or current employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    rate_of_pay_starting: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Starting rate of pay for your most recent or current job"
    )

    rate_of_pay_ending: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Ending rate of pay for your most recent or current job"
    )

    describe_your_job_duties: str = Field(
        ...,
        description=(
            "Description of your job duties for your most recent or current employer .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reason_for_leaving: str = Field(
        ...,
        description=(
            "Reason you left your most recent or current employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name: str = Field(
        ...,
        description=(
            "Name of your supervisor at your most recent or current employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class EmploymentHistorySecondEmployer(BaseModel):
    """Details for the second most recent employment"""

    employers_name_second_employment: str = Field(
        default="",
        description=(
            "Name of your second most recent employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_second_employment: str = Field(
        default="",
        description=(
            "Telephone number for your second most recent employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_second_employment: str = Field(
        default="",
        description=(
            "Address of your second most recent employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employed_month_year_from_second_employment: str = Field(
        default="",
        description=(
            "Month and year you started with your second most recent employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    employed_month_year_to_second_employment: str = Field(
        default="",
        description=(
            "Month and year you ended employment with your second most recent employer .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    last_job_title_second_employment: str = Field(
        default="",
        description=(
            "Your last job title with your second most recent employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    rate_of_pay_starting_second_employment: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting rate of pay for your second most recent job"
    )

    rate_of_pay_ending_second_employment: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending rate of pay for your second most recent job"
    )

    describe_your_job_duties_second_employment: str = Field(
        default="",
        description=(
            "Description of your job duties for your second most recent employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reason_for_leaving_second_employment: str = Field(
        default="",
        description=(
            "Reason you left your second most recent employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name_second_employment: str = Field(
        default="",
        description=(
            "Name of your supervisor at your second most recent employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class EmploymentHistoryThirdEmployer(BaseModel):
    """Details for the third most recent employment"""

    employers_name_third_employment: str = Field(
        default="",
        description=(
            "Name of your third most recent employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_third_employment: str = Field(
        default="",
        description=(
            "Telephone number for your third most recent employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_third_employment: str = Field(
        default="",
        description=(
            "Address of your third most recent employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employed_month_year_from_third_employment: str = Field(
        default="",
        description=(
            "Month and year you started with your third most recent employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employed_month_year_to_third_employment: str = Field(
        default="",
        description=(
            "Month and year you ended employment with your third most recent employer .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    last_job_title_third_employment: str = Field(
        default="",
        description=(
            "Your last job title with your third most recent employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    rate_of_pay_starting_third_employment: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting rate of pay for your third most recent job"
    )

    rate_of_pay_ending_third_employment: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending rate of pay for your third most recent job"
    )

    describe_your_job_duties_third_employment: str = Field(
        default="",
        description=(
            "Description of your job duties for your third most recent employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reason_for_leaving_third_employment: str = Field(
        default="",
        description=(
            "Reason you left your third most recent employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name_third_employment: str = Field(
        default="",
        description=(
            "Name of your supervisor at your third most recent employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RustsFlyingService(BaseModel):
    """
    Rust's FLYING SERVICE

    Please attach resume if available. This section must be completed-do not list “see resume” except for job duties.
    """

    job_source: JobSource = Field(..., description="Job Source")
    employment_history___most_recent_or_current_employer: EmploymentHistoryMostRecentorCurrentEmployer = Field(
        ..., description="Employment History - Most Recent or Current Employer"
    )
    employment_history___second_employer: EmploymentHistorySecondEmployer = Field(
        ..., description="Employment History - Second Employer"
    )
    employment_history___third_employer: EmploymentHistoryThirdEmployer = Field(
        ..., description="Employment History - Third Employer"
    )
