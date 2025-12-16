from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmploymentorInternshipDiscrimination(BaseModel):
    """Information about your employment or internship status with the company"""

    how_many_employees_does_this_company_have_a_1_3: Literal[
        "1-3", "4-14", "15 or more", "20 or more", "Don't know", "N/A", ""
    ] = Field(
        ..., description="Select the range that best describes how many employees the company has."
    )

    how_many_employees_does_this_company_have_b_4_14: Literal[
        "1-3", "4-14", "15 or more", "20 or more", "Don't know", "N/A", ""
    ] = Field(
        ..., description="Select the range that best describes how many employees the company has."
    )

    how_many_employees_does_this_company_have_c_15_or_more: Literal[
        "1-3", "4-14", "15 or more", "20 or more", "Don't know", "N/A", ""
    ] = Field(
        ..., description="Select the range that best describes how many employees the company has."
    )

    how_many_employees_does_this_company_have_d_20_or_more: Literal[
        "1-3", "4-14", "15 or more", "20 or more", "Don't know", "N/A", ""
    ] = Field(
        ..., description="Select the range that best describes how many employees the company has."
    )

    how_many_employees_does_this_company_have_e_dont_know: Literal[
        "1-3", "4-14", "15 or more", "20 or more", "Don't know", "N/A", ""
    ] = Field(
        ..., description="Select the range that best describes how many employees the company has."
    )

    are_you_currently_working_for_the_company_yes: BooleanLike = Field(
        ..., description="Check if you are currently working for the company."
    )

    date_of_hire_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month you were hired (MM)."
    )

    date_of_hire_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day you were hired (DD)."
    )

    date_of_hire_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you were hired (YYYY)."
    )

    what_is_your_job_title: str = Field(
        default="",
        description=(
            "Your current job title with the company. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    are_you_currently_working_for_the_company_no: BooleanLike = Field(
        ..., description="Check if you are not currently working for the company."
    )

    last_day_of_work_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month of your last day of work (MM)."
    )

    last_day_of_work_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day of your last day of work (DD)."
    )

    last_day_of_work_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year of your last day of work (YYYY)."
    )

    what_was_your_job_title: str = Field(
        default="",
        description=(
            "Your job title at the time your employment ended. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    i_was_not_hired_by_the_company: BooleanLike = Field(
        default="", description="Check if you applied but were not hired by the company."
    )

    date_of_application_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month you applied for the job (MM)."
    )

    date_of_application_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day you applied for the job (DD)."
    )

    date_of_application_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you applied for the job (YYYY)."
    )


class ActsofDiscrimination(BaseModel):
    """What the person or company did; select all that apply"""

    refused_to_hire_me: BooleanLike = Field(
        default="", description="Check if the company refused to hire you."
    )

    fired_me_laid_me_off: BooleanLike = Field(
        default="", description="Check if you were fired or laid off."
    )

    did_not_call_me_back_after_a_lay_off: BooleanLike = Field(
        default="", description="Check if the company did not recall you after a lay-off."
    )

    demoted_me: BooleanLike = Field(default="", description="Check if you were demoted.")

    suspended_me: BooleanLike = Field(default="", description="Check if you were suspended.")

    sexually_harassed_me: BooleanLike = Field(
        default="", description="Check if you were sexually harassed."
    )

    harassed_or_intimidated_me_other_than_sexual_harassment: BooleanLike = Field(
        default="", description="Check if you were harassed or intimidated in a non-sexual way."
    )

    denied_me_training: BooleanLike = Field(
        default="", description="Check if you were denied training opportunities."
    )

    denied_me_a_promotion_or_pay_raise: BooleanLike = Field(
        default="", description="Check if you were denied a promotion or pay raise."
    )

    denied_me_leave_time_or_other_benefits: BooleanLike = Field(
        default="", description="Check if you were denied leave time or other benefits."
    )

    paid_me_a_lower_salary_than_other_workers_in_my_same_title: BooleanLike = Field(
        default="", description="Check if you were paid less than others with the same job title."
    )

    gave_me_different_or_worse_job_duties_than_other_workers_in_my_same_title: BooleanLike = Field(
        default="",
        description=(
            "Check if you were given different or worse job duties than others with the same title."
        ),
    )

    denied_me_an_accommodation_for_my_disability: BooleanLike = Field(
        default="",
        description="Check if you were denied a reasonable accommodation for your disability.",
    )

    denied_me_an_accommodation_for_my_religious_practices: BooleanLike = Field(
        default="",
        description=(
            "Check if you were denied a reasonable accommodation for your religious practices."
        ),
    )

    gave_me_a_disciplinary_notice_or_negative_performance_evaluation: BooleanLike = Field(
        default="",
        description="Check if you received a disciplinary notice or negative performance evaluation.",
    )

    other: str = Field(
        default="",
        description=(
            "Describe any other discriminatory actions not listed above. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class EmploymentOrInternshipDiscrimination(BaseModel):
    """
    EMPLOYMENT OR INTERNSHIP DISCRIMINATION

    Please answer the questions on this page only if you were discriminated against in the area of employment or internship. If not, turn to the next page.
    """

    employment_or_internship_discrimination: EmploymentorInternshipDiscrimination = Field(
        ..., description="Employment or Internship Discrimination"
    )
    acts_of_discrimination: ActsofDiscrimination = Field(..., description="Acts of Discrimination")
