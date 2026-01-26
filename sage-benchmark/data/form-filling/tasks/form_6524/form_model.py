from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecordofEmploymentEmployer1(BaseModel):
    """Details for most recent employer (1)"""

    name_and_address_of_company_and_type_of_business_1: str = Field(
        ...,
        description=(
            "Full name, mailing address, and type of business for your most recent employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    from_mo_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Starting month of employment (two‑digit month) for this employer"
    )

    from_yr_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Starting year of employment (four‑digit year) for this employer"
    )

    to_mo_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Ending month of employment (two‑digit month) for this employer"
    )

    to_yr_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Ending year of employment (four‑digit year) for this employer"
    )

    monthly_starting_salary_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly salary when you started this job (numbers only)"
    )

    monthly_last_salary_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly salary at the end of this job (numbers only)"
    )

    reason_for_leaving_1: str = Field(
        ...,
        description=(
            "Brief reason why you left this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_1: str = Field(
        default="",
        description=(
            "Immediate supervisor’s full name at this employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_1: str = Field(
        ...,
        description=(
            "Your job title and a brief description of your main duties for this employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
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


class RecordofEmploymentEmployer2(BaseModel):
    """Details for previous employer (2)"""

    name_and_address_of_company_and_type_of_business_2: str = Field(
        default="",
        description=(
            "Full name, mailing address, and type of business for your second most recent "
            'employer .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    from_mo_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting month of employment (two‑digit month) for this employer"
    )

    from_yr_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting year of employment (four‑digit year) for this employer"
    )

    to_mo_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending month of employment (two‑digit month) for this employer"
    )

    to_yr_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending year of employment (four‑digit year) for this employer"
    )

    monthly_starting_salary_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary when you started this job (numbers only)"
    )

    monthly_last_salary_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary at the end of this job (numbers only)"
    )

    reason_for_leaving_2: str = Field(
        default="",
        description=(
            "Brief reason why you left this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_2: str = Field(
        default="",
        description=(
            "Immediate supervisor’s full name at this employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_2: str = Field(
        default="",
        description=(
            "Your job title and a brief description of your main duties for this employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
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


class RecordofEmploymentEmployer3(BaseModel):
    """Details for previous employer (3)"""

    name_and_address_of_company_and_type_of_business_3: str = Field(
        default="",
        description=(
            "Full name, mailing address, and type of business for your third most recent "
            'employer .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    from_mo_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting month of employment (two‑digit month) for this employer"
    )

    from_yr_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Starting year of employment (four‑digit year) for this employer"
    )

    to_mo_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending month of employment (two‑digit month) for this employer"
    )

    to_yr_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Ending year of employment (four‑digit year) for this employer"
    )

    monthly_starting_salary_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary when you started this job (numbers only)"
    )

    monthly_last_salary_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly salary at the end of this job (numbers only)"
    )

    reason_for_leaving_3: str = Field(
        default="",
        description=(
            "Brief reason why you left this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_supervisor_3: str = Field(
        default="",
        description=(
            "Immediate supervisor’s full name at this employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_job_duties_3: str = Field(
        default="",
        description=(
            "Your job title and a brief description of your main duties for this employer "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
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


class AdditionalEmploymentInformation(BaseModel):
    """Additional information related to prior employment and qualifications"""

    different_name_used_with_previous_employers: str = Field(
        default="",
        description=(
            "Any other name(s) you used while working for the employers listed above .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signed: str = Field(
        ...,
        description=(
            "Applicant’s signature authorizing contact with listed employers .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employers_you_do_not_wish_us_to_contact: str = Field(
        default="",
        description=(
            "List any employers from the above record that you prefer not to be contacted "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    skills_and_aptitudes_that_would_qualify_you_for_a_position_with_unity_national_bank: str = (
        Field(
            default="",
            description=(
                "Describe relevant skills, experience, and aptitudes that qualify you to work "
                'at Unity National Bank .If you cannot fill this, write "N/A". If this field '
                "should not be filled by you (for example, it belongs to another person or "
                'office), leave it blank (empty string "").'
            ),
        )
    )


class RecordOfEmployment(BaseModel):
    """
    Record of Employment

    Please list most recent employment first.
    """

    record_of_employment___employer_1: RecordofEmploymentEmployer1 = Field(
        ..., description="Record of Employment - Employer 1"
    )
    record_of_employment___employer_2: RecordofEmploymentEmployer2 = Field(
        ..., description="Record of Employment - Employer 2"
    )
    record_of_employment___employer_3: RecordofEmploymentEmployer3 = Field(
        ..., description="Record of Employment - Employer 3"
    )
    additional_employment_information: AdditionalEmploymentInformation = Field(
        ..., description="Additional Employment Information"
    )
