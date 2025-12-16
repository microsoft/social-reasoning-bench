from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WorkHistoryJob1(BaseModel):
    """Details for most recent or current position"""

    job_title_1: str = Field(
        default="",
        description=(
            "Title of your most recent or current position for Job #1 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    start_date_job_1: str = Field(
        default="", description="Start date for Job #1 in month/day/year format"
    )  # YYYY-MM-DD format

    end_date_job_1: str = Field(
        default="", description="End date for Job #1 in month/day/year format"
    )  # YYYY-MM-DD format

    company_name_job_1: str = Field(
        default="",
        description=(
            'Name of the employer for Job #1 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name_job_1: str = Field(
        default="",
        description=(
            "Name of your direct supervisor for Job #1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number_job_1: str = Field(
        default="",
        description=(
            "Phone number for the employer or supervisor for Job #1 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_job_1: str = Field(
        default="",
        description=(
            'City where Job #1 was located .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_job_1: str = Field(default="", description="State where Job #1 was located")

    zip_job_1: str = Field(default="", description="ZIP code for the location of Job #1")

    duties_job_1: str = Field(
        default="",
        description=(
            "Describe your main responsibilities and duties for Job #1 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_job_1: str = Field(
        default="",
        description=(
            'Explain why you left Job #1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    starting_salary_job_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting salary or wage for Job #1"
    )

    ending_salary_job_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final salary or wage for Job #1"
    )

    may_we_contact_your_present_employer: Literal["Yes", "No", "N/A", "N/A", ""] = Field(
        default="", description="Indicate whether the employer may contact your current employer"
    )

    may_we_contact_present_employer_yes: BooleanLike = Field(
        default="", description="Check if the employer may contact your present employer"
    )

    may_we_contact_present_employer_no: BooleanLike = Field(
        default="", description="Check if the employer may not contact your present employer"
    )

    may_we_contact_present_employer_na: BooleanLike = Field(
        default="",
        description="Check if this question is not applicable (e.g., you are not currently employed)",
    )


class WorkHistoryJob2(BaseModel):
    """Details for previous position #2"""

    job_title_2: str = Field(
        default="",
        description=(
            "Title of your previous position for Job #2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    start_date_job_2: str = Field(
        default="", description="Start date for Job #2 in month/day/year format"
    )  # YYYY-MM-DD format

    end_date_job_2: str = Field(
        default="", description="End date for Job #2 in month/day/year format"
    )  # YYYY-MM-DD format

    company_name_job_2: str = Field(
        default="",
        description=(
            'Name of the employer for Job #2 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name_job_2: str = Field(
        default="",
        description=(
            "Name of your direct supervisor for Job #2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number_job_2: str = Field(
        default="",
        description=(
            "Phone number for the employer or supervisor for Job #2 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_job_2: str = Field(
        default="",
        description=(
            'City where Job #2 was located .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_job_2: str = Field(default="", description="State where Job #2 was located")

    zip_job_2: str = Field(default="", description="ZIP code for the location of Job #2")

    duties_job_2: str = Field(
        default="",
        description=(
            "Describe your main responsibilities and duties for Job #2 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_job_2: str = Field(
        default="",
        description=(
            'Explain why you left Job #2 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    starting_salary_job_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting salary or wage for Job #2"
    )

    ending_salary_job_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final salary or wage for Job #2"
    )


class WorkHistoryJob3(BaseModel):
    """Details for previous position #3"""

    job_title_3: str = Field(
        default="",
        description=(
            "Title of your previous position for Job #3 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    start_date_job_3: str = Field(
        default="", description="Start date for Job #3 in month/day/year format"
    )  # YYYY-MM-DD format

    end_date_job_3: str = Field(
        default="", description="End date for Job #3 in month/day/year format"
    )  # YYYY-MM-DD format

    company_name_job_3: str = Field(
        default="",
        description=(
            'Name of the employer for Job #3 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name_job_3: str = Field(
        default="",
        description=(
            "Name of your direct supervisor for Job #3 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number_job_3: str = Field(
        default="",
        description=(
            "Phone number for the employer or supervisor for Job #3 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_job_3: str = Field(
        default="",
        description=(
            'City where Job #3 was located .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_job_3: str = Field(default="", description="State where Job #3 was located")

    zip_job_3: str = Field(default="", description="ZIP code for the location of Job #3")

    duties_job_3: str = Field(
        default="",
        description=(
            "Describe your main responsibilities and duties for Job #3 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_job_3: str = Field(
        default="",
        description=(
            'Explain why you left Job #3 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    starting_salary_job_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting salary or wage for Job #3"
    )

    ending_salary_job_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final salary or wage for Job #3"
    )


class WorkHistoryJob4(BaseModel):
    """Details for previous position #4"""

    job_title_4: str = Field(
        default="",
        description=(
            "Title of your previous position for Job #4 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    start_date_job_4: str = Field(
        default="", description="Start date for Job #4 in month/day/year format"
    )  # YYYY-MM-DD format

    end_date_job_4: str = Field(
        default="", description="End date for Job #4 in month/day/year format"
    )  # YYYY-MM-DD format

    company_name_job_4: str = Field(
        default="",
        description=(
            'Name of the employer for Job #4 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name_job_4: str = Field(
        default="",
        description=(
            "Name of your direct supervisor for Job #4 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number_job_4: str = Field(
        default="",
        description=(
            "Phone number for the employer or supervisor for Job #4 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_job_4: str = Field(
        default="",
        description=(
            'City where Job #4 was located .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_job_4: str = Field(default="", description="State where Job #4 was located")

    zip_job_4: str = Field(default="", description="ZIP code for the location of Job #4")

    duties_job_4: str = Field(
        default="",
        description=(
            "Describe your main responsibilities and duties for Job #4 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_job_4: str = Field(
        default="",
        description=(
            'Explain why you left Job #4 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    starting_salary_job_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting salary or wage for Job #4"
    )

    ending_salary_job_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final salary or wage for Job #4"
    )


class ApplicantCertification(BaseModel):
    """Applicant signature and date acknowledging certification and at-will statement"""

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant certifying the accuracy of the information provided "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    date: str = Field(..., description="Date the application was signed")  # YYYY-MM-DD format


class WorkHistory(BaseModel):
    """
    WORK HISTORY

    Start with your present or most recent employment and work back. Use separate sheet if necessary. (INCLUDE PAID AND UNPAID POSITIONS)
    """

    work_history___job_1: WorkHistoryJob1 = Field(..., description="Work History - Job #1")
    work_history___job_2: WorkHistoryJob2 = Field(..., description="Work History - Job #2")
    work_history___job_3: WorkHistoryJob3 = Field(..., description="Work History - Job #3")
    work_history___job_4: WorkHistoryJob4 = Field(..., description="Work History - Job #4")
    applicant_certification: ApplicantCertification = Field(
        ..., description="Applicant Certification"
    )
