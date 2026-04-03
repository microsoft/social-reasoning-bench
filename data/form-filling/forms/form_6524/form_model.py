from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecordofEmployment(BaseModel):
    """Employment history and related details"""

    name_and_address_of_company_and_type_of_business_1: str = Field(
        ...,
        description=(
            "Full name and mailing address of the first most recent employer and the type "
            'of business .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    from_mo_yr_1: str = Field(
        ...,
        description=(
            "Month and year you started working for the first employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to_mo_yr_1: str = Field(
        ...,
        description=(
            "Month and year you stopped working for the first employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    monthly_starting_salary_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly salary when you started with the first employer"
    )

    monthly_last_salary_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly salary at the time you left the first employer"
    )

    reason_for_leaving_1: str = Field(
        ...,
        description=(
            'Reason you left the first employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_1: str = Field(
        default="",
        description=(
            "Name of your immediate supervisor at the first employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_1: str = Field(
        ...,
        description=(
            "Your job title and a brief description of your duties for the first employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    telephone_1: str = Field(
        default="",
        description=(
            "Telephone number for the first employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_and_address_of_company_and_type_of_business_2: str = Field(
        default="",
        description=(
            "Full name and mailing address of the second most recent employer and the type "
            'of business .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    from_mo_yr_2: str = Field(
        default="",
        description=(
            "Month and year you started working for the second employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to_mo_yr_2: str = Field(
        default="",
        description=(
            "Month and year you stopped working for the second employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    monthly_starting_salary_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary when you started with the second employer"
    )

    monthly_last_salary_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary at the time you left the second employer"
    )

    reason_for_leaving_2: str = Field(
        default="",
        description=(
            'Reason you left the second employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_2: str = Field(
        default="",
        description=(
            "Name of your immediate supervisor at the second employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_2: str = Field(
        default="",
        description=(
            "Your job title and a brief description of your duties for the second employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    telephone_2: str = Field(
        default="",
        description=(
            "Telephone number for the second employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_and_address_of_company_and_type_of_business_3: str = Field(
        default="",
        description=(
            "Full name and mailing address of the third most recent employer and the type "
            'of business .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    from_mo_yr_3: str = Field(
        default="",
        description=(
            "Month and year you started working for the third employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to_mo_yr_3: str = Field(
        default="",
        description=(
            "Month and year you stopped working for the third employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    monthly_starting_salary_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary when you started with the third employer"
    )

    monthly_last_salary_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary at the time you left the third employer"
    )

    reason_for_leaving_3: str = Field(
        default="",
        description=(
            'Reason you left the third employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_3: str = Field(
        default="",
        description=(
            "Name of your immediate supervisor at the third employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_3: str = Field(
        default="",
        description=(
            "Your job title and a brief description of your duties for the third employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    telephone_3: str = Field(
        default="",
        description=(
            "Telephone number for the third employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_and_address_of_company_and_type_of_business_4: str = Field(
        default="",
        description=(
            "Full name and mailing address of the fourth most recent employer and the type "
            'of business .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    from_mo_yr_4: str = Field(
        default="",
        description=(
            "Month and year you started working for the fourth employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to_mo_yr_4: str = Field(
        default="",
        description=(
            "Month and year you stopped working for the fourth employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    monthly_starting_salary_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary when you started with the fourth employer"
    )

    monthly_last_salary_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary at the time you left the fourth employer"
    )

    reason_for_leaving_4: str = Field(
        default="",
        description=(
            'Reason you left the fourth employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_4: str = Field(
        default="",
        description=(
            "Name of your immediate supervisor at the fourth employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_4: str = Field(
        default="",
        description=(
            "Your job title and a brief description of your duties for the fourth employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    telephone_4: str = Field(
        default="",
        description=(
            "Telephone number for the fourth employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AuthorizationandContactPreferences(BaseModel):
    """Permission to contact employers and any exceptions"""

    signed: str = Field(
        ...,
        description=(
            "Applicant’s signature authorizing contact with listed employers .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employers_you_do_not_wish_to_contact: str = Field(
        default="",
        description=(
            "List any previous employers that you prefer the bank not contact .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SkillsandAptitudes(BaseModel):
    """Skills and aptitudes that qualify you for a position with Unity National Bank"""

    skills_and_aptitudes_qualify_unity_national_bank_line_1: str = Field(
        ...,
        description=(
            "First line describing skills and aptitudes that qualify you for a position .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    skills_and_aptitudes_qualify_unity_national_bank_line_2: str = Field(
        default="",
        description=(
            "Second line describing skills and aptitudes that qualify you for a position "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    skills_and_aptitudes_qualify_unity_national_bank_line_3: str = Field(
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
    authorization_and_contact_preferences: AuthorizationandContactPreferences = Field(
        ..., description="Authorization and Contact Preferences"
    )
    skills_and_aptitudes: SkillsandAptitudes = Field(..., description="Skills and Aptitudes")
