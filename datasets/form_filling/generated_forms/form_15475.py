from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AdditionalDetails(BaseModel):
    """Further information related to previous answers"""

    if_yes_please_give_details: str = Field(
        default="",
        description=(
            "Provide further details if you answered yes to the preceding question. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class References(BaseModel):
    """Details of two referees"""

    reference_1_name: str = Field(
        ...,
        description=(
            'Full name of your first referee. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_name: str = Field(
        ...,
        description=(
            'Full name of your second referee. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_address_line_1: str = Field(
        ...,
        description=(
            "First line of the postal address for your first referee. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the postal address for your first referee (if applicable). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reference_1_address_line_3: str = Field(
        default="",
        description=(
            "Third line of the postal address for your first referee (e.g. town, county, "
            'postcode). .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    reference_2_address_line_1: str = Field(
        ...,
        description=(
            "First line of the postal address for your second referee. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the postal address for your second referee (if applicable). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reference_2_address_line_3: str = Field(
        default="",
        description=(
            "Third line of the postal address for your second referee (e.g. town, county, "
            'postcode). .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    reference_1_job_title: str = Field(
        ...,
        description=(
            "Job title or role of your first referee. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_job_title: str = Field(
        ...,
        description=(
            "Job title or role of your second referee. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_relationship_to_you: str = Field(
        ...,
        description=(
            "Describe how your first referee knows you (e.g. teacher, doctor, manager). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reference_2_relationship_to_you: str = Field(
        ...,
        description=(
            "Describe how your second referee knows you (e.g. teacher, doctor, manager). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    reference_1_phone: str = Field(
        ...,
        description=(
            "Telephone number for your first referee. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_phone: str = Field(
        ...,
        description=(
            "Telephone number for your second referee. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_email: str = Field(
        ...,
        description=(
            'Email address for your first referee. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_email: str = Field(
        ...,
        description=(
            "Email address for your second referee. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    no_reference_without_notifying_me: BooleanLike = Field(
        default="",
        description=(
            "Tick this box if you want to be notified before the employer contacts your referees."
        ),
    )


class PersonalDeclaration(BaseModel):
    """Applicant’s confirmation and signing of the declaration"""

    signature: str = Field(
        ...,
        description=(
            "Applicant’s handwritten or electronic signature confirming the declaration. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    date_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of the month you signed this form (DD)."
    )

    date_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month you signed this form (MM)."
    )

    date_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year you signed this form (YYYY)."
    )


class MunroApplicationForEmploymentApprenticeshipApplicationForm(BaseModel):
    """
        MUNRO

    Application for Employment
    Apprenticeship Application Form

        ''
    """

    additional_details: AdditionalDetails = Field(..., description="Additional Details")
    references: References = Field(..., description="References")
    personal_declaration: PersonalDeclaration = Field(..., description="Personal Declaration")
