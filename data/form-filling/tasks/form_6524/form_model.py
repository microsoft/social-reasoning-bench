from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecordofEmployment(BaseModel):
    """Employment history, most recent first"""

    name_and_address_of_company_and_type_of_business_1: str = Field(
        default="",
        description=(
            "Name, full address, and type of business for the most recent employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    from_month_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting month of employment (MM) for this employer"
    )

    from_year_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting year of employment (YYYY) for this employer"
    )

    to_month_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending month of employment (MM) for this employer"
    )

    to_year_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending year of employment (YYYY) for this employer"
    )

    monthly_starting_salary_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly starting salary for this position"
    )

    monthly_last_salary_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final monthly salary for this position"
    )

    reason_for_leaving_1: str = Field(
        default="",
        description=(
            'Reason you left this employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_1: str = Field(
        default="",
        description=(
            "Supervisor's full name at this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_1: str = Field(
        default="",
        description=(
            "Job title and a brief description of your duties for this employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    telephone_1: str = Field(
        default="",
        description=(
            'Telephone number for this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_and_address_of_company_and_type_of_business_2: str = Field(
        default="",
        description=(
            "Name, full address, and type of business for the second most recent employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    from_month_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting month of employment (MM) for this employer"
    )

    from_year_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting year of employment (YYYY) for this employer"
    )

    to_month_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending month of employment (MM) for this employer"
    )

    to_year_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending year of employment (YYYY) for this employer"
    )

    monthly_starting_salary_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly starting salary for this position"
    )

    monthly_last_salary_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final monthly salary for this position"
    )

    reason_for_leaving_2: str = Field(
        default="",
        description=(
            'Reason you left this employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_2: str = Field(
        default="",
        description=(
            "Supervisor's full name at this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_2: str = Field(
        default="",
        description=(
            "Job title and a brief description of your duties for this employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    telephone_2: str = Field(
        default="",
        description=(
            'Telephone number for this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_and_address_of_company_and_type_of_business_3: str = Field(
        default="",
        description=(
            "Name, full address, and type of business for the third most recent employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    from_month_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting month of employment (MM) for this employer"
    )

    from_year_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting year of employment (YYYY) for this employer"
    )

    to_month_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending month of employment (MM) for this employer"
    )

    to_year_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending year of employment (YYYY) for this employer"
    )

    monthly_starting_salary_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly starting salary for this position"
    )

    monthly_last_salary_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final monthly salary for this position"
    )

    reason_for_leaving_3: str = Field(
        default="",
        description=(
            'Reason you left this employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_3: str = Field(
        default="",
        description=(
            "Supervisor's full name at this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_3: str = Field(
        default="",
        description=(
            "Job title and a brief description of your duties for this employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    telephone_3: str = Field(
        default="",
        description=(
            'Telephone number for this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_and_address_of_company_and_type_of_business_4: str = Field(
        default="",
        description=(
            "Name, full address, and type of business for the fourth most recent employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    from_month_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting month of employment (MM) for this employer"
    )

    from_year_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting year of employment (YYYY) for this employer"
    )

    to_month_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending month of employment (MM) for this employer"
    )

    to_year_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending year of employment (YYYY) for this employer"
    )

    monthly_starting_salary_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly starting salary for this position"
    )

    monthly_last_salary_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final monthly salary for this position"
    )

    reason_for_leaving_4: str = Field(
        default="",
        description=(
            'Reason you left this employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_4: str = Field(
        default="",
        description=(
            "Supervisor's full name at this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_4: str = Field(
        default="",
        description=(
            "Job title and a brief description of your duties for this employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    telephone_4: str = Field(
        default="",
        description=(
            'Telephone number for this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AuthorizationandAdditionalInformation(BaseModel):
    """Permission to contact employers and additional qualifications"""

    signed: str = Field(
        ...,
        description=(
            "Applicant's signature authorizing contact with listed employers .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employers_you_do_not_wish_us_to_contact: str = Field(
        default="",
        description=(
            "List any employers from above that you prefer the bank not contact .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    skills_and_aptitudes_that_would_qualify_you_for_a_position_with_unity_national_bank_line_1: str = Field(
        default="",
        description=(
            "First line describing skills and aptitudes that qualify you for a position .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    skills_and_aptitudes_that_would_qualify_you_for_a_position_with_unity_national_bank_line_2: str = Field(
        default="",
        description=(
            "Second line describing skills and aptitudes that qualify you for a position "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    skills_and_aptitudes_that_would_qualify_you_for_a_position_with_unity_national_bank_line_3: str = Field(
        default="",
        description=(
            "Third line describing skills and aptitudes that qualify you for a position .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class UnityNationalBankRecordOfEmployment(BaseModel):
    """
        UNITY
    National Bank

    Record of Employment

        Please list most recent employment first.
    """

    record_of_employment: RecordofEmployment = Field(..., description="Record of Employment")
    authorization_and_additional_information: AuthorizationandAdditionalInformation = Field(
        ..., description="Authorization and Additional Information"
    )
