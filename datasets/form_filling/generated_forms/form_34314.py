from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmploymentDetails(BaseModel):
    """Basic information about the employee and position"""

    name: str = Field(
        ...,
        description=(
            'Employee\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Employee's MIT or primary email address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Employee\'s primary phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    job_title: str = Field(
        ...,
        description=(
            "Title of the student employment position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    start_end_date_end_by_6_30_2016: str = Field(
        ...,
        description=(
            "Employment start and end dates (end date must be on or before 6/30/2016) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mit_id_if_applicable: str = Field(
        default="",
        description=(
            "MIT identification number, if the employee has one .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    student_organization: str = Field(
        ...,
        description=(
            "Name of the sponsoring student organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cost_object_main_account_number: str = Field(
        ...,
        description=(
            "Cost object or main account number funding this position .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    monthly_rate_of_pay: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly pay rate in dollars for this position"
    )

    total_financial_commitment: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Total dollar amount the organization commits to pay over the full term of employment"
        ),
    )


class Authorization(BaseModel):
    """Approval and agreement to the terms of employment"""

    authorization_name: str = Field(
        ...,
        description=(
            "Name of the person authorizing this employment agreement .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the authorizing individual .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PositionDescription(BaseModel):
    """Narrative description of the role and its responsibilities"""

    position_overview: str = Field(
        ...,
        description=(
            "Brief, high-level overview of the position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    principal_duties_and_responsibilities_essential_functions: str = Field(
        ...,
        description=(
            "Description of the principal duties, responsibilities, and essential functions "
            "of the position, including approximate time allocations if possible .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class EmploymentAgreement(BaseModel):
    """
    Employment Agreement

    ''
    """

    employment_details: EmploymentDetails = Field(..., description="Employment Details")
    authorization: Authorization = Field(..., description="Authorization")
    position_description: PositionDescription = Field(..., description="Position Description")
