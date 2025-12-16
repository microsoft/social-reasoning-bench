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

    name_and_address_of_company_and_type_of_business_employment_1: str = Field(
        ...,
        description=(
            "Name, full mailing address, and type of business for your most recent employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    from_month_employment_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Starting month (MM) for this employment"
    )

    from_year_employment_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Starting year (YYYY) for this employment"
    )

    to_month_employment_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Ending month (MM) for this employment"
    )

    to_year_employment_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Ending year (YYYY) for this employment"
    )

    monthly_starting_salary_employment_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly starting salary for this job"
    )

    monthly_last_salary_employment_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Final monthly salary for this job"
    )

    reason_for_leaving_employment_1: str = Field(
        ...,
        description=(
            'Brief reason you left this employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_employment_1: str = Field(
        ...,
        description=(
            "Immediate supervisor's full name at this job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_employment_1: str = Field(
        ...,
        description=(
            "Your job title and a brief description of your main duties .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_employment_1: str = Field(
        ...,
        description=(
            'Telephone number for this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_and_address_of_company_and_type_of_business_employment_2: str = Field(
        default="",
        description=(
            "Name, full mailing address, and type of business for a previous employer .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    from_month_employment_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting month (MM) for this employment"
    )

    from_year_employment_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting year (YYYY) for this employment"
    )

    to_month_employment_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending month (MM) for this employment"
    )

    to_year_employment_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending year (YYYY) for this employment"
    )

    monthly_starting_salary_employment_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly starting salary for this job"
    )

    monthly_last_salary_employment_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final monthly salary for this job"
    )

    reason_for_leaving_employment_2: str = Field(
        default="",
        description=(
            'Brief reason you left this employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_employment_2: str = Field(
        default="",
        description=(
            "Immediate supervisor's full name at this job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_employment_2: str = Field(
        default="",
        description=(
            "Your job title and a brief description of your main duties .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_employment_2: str = Field(
        default="",
        description=(
            'Telephone number for this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_and_address_of_company_and_type_of_business_employment_3: str = Field(
        default="",
        description=(
            "Name, full mailing address, and type of business for a previous employer .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    from_month_employment_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting month (MM) for this employment"
    )

    from_year_employment_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting year (YYYY) for this employment"
    )

    to_month_employment_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending month (MM) for this employment"
    )

    to_year_employment_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending year (YYYY) for this employment"
    )

    monthly_starting_salary_employment_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly starting salary for this job"
    )

    monthly_last_salary_employment_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final monthly salary for this job"
    )

    reason_for_leaving_employment_3: str = Field(
        default="",
        description=(
            'Brief reason you left this employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_employment_3: str = Field(
        default="",
        description=(
            "Immediate supervisor's full name at this job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_employment_3: str = Field(
        default="",
        description=(
            "Your job title and a brief description of your main duties .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_employment_3: str = Field(
        default="",
        description=(
            'Telephone number for this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_and_address_of_company_and_type_of_business_employment_4: str = Field(
        default="",
        description=(
            "Name, full mailing address, and type of business for a previous employer .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    from_month_employment_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting month (MM) for this employment"
    )

    from_year_employment_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting year (YYYY) for this employment"
    )

    to_month_employment_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending month (MM) for this employment"
    )

    to_year_employment_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending year (YYYY) for this employment"
    )

    monthly_starting_salary_employment_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly starting salary for this job"
    )

    monthly_last_salary_employment_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final monthly salary for this job"
    )

    reason_for_leaving_employment_4: str = Field(
        default="",
        description=(
            'Brief reason you left this employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_employment_4: str = Field(
        default="",
        description=(
            "Immediate supervisor's full name at this job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_employment_4: str = Field(
        default="",
        description=(
            "Your job title and a brief description of your main duties .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_employment_4: str = Field(
        default="",
        description=(
            'Telephone number for this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AuthorizationandRestrictions(BaseModel):
    """Permission to contact employers and any contact restrictions"""

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
            "List any employers from above that you prefer not to be contacted .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SkillsandQualifications(BaseModel):
    """Skills and aptitudes relevant to a position with Unity National Bank"""

    skills_and_aptitudes_that_would_qualify_you_for_a_position_with_unity_national_bank: str = (
        Field(
            ...,
            description=(
                "Describe relevant skills, experience, and aptitudes for a position with Unity "
                'National Bank .If you cannot fill this, write "N/A". If this field should '
                "not be filled by you (for example, it belongs to another person or office), "
                'leave it blank (empty string "").'
            ),
        )
    )


class RecordOfEmployment(BaseModel):
    """
    Record of Employment

    Please list most recent employment first.
    """

    record_of_employment: RecordofEmployment = Field(..., description="Record of Employment")
    authorization_and_restrictions: AuthorizationandRestrictions = Field(
        ..., description="Authorization and Restrictions"
    )
    skills_and_qualifications: SkillsandQualifications = Field(
        ..., description="Skills and Qualifications"
    )
