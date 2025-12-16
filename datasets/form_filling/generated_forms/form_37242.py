from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EducationHistoryRow(BaseModel):
    """Single row in Schools/College/University"""

    schools_college_university: str = Field(default="", description="Schools_College_University")
    qualifications_gained: str = Field(default="", description="Qualifications_Gained")


class PositionAppliedFor(BaseModel):
    """Role the applicant is applying for"""

    position_applied_for: str = Field(
        ...,
        description=(
            "Job title or role you are applying for .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PersonalDetails(BaseModel):
    """Basic personal and contact information"""

    surname: str = Field(
        ...,
        description=(
            'Your family name / last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    forenames: str = Field(
        ...,
        description=(
            'Your first name and any middle names .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        default="",
        description=(
            "Preferred title (e.g. Mr, Mrs, Ms, Dr) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Your full current postal address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    postcode: str = Field(
        ...,
        description=(
            'Postcode for your address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Your email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    tel_no: str = Field(
        ...,
        description=(
            'Your main contact telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class UKEmploymentRestrictions(BaseModel):
    """Eligibility and restrictions on working in the UK"""

    uk_employment_restrictions_yes: BooleanLike = Field(
        ...,
        description=(
            "Tick to indicate you ARE aware of restrictions on taking up employment in the UK"
        ),
    )

    uk_employment_restrictions_no: BooleanLike = Field(
        ...,
        description=(
            "Tick to indicate you are NOT aware of any restrictions on taking up employment "
            "in the UK"
        ),
    )

    details_of_restrictions: str = Field(
        default="",
        description=(
            "Provide details of any restrictions on your ability to work in the UK .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class EducationHistory(BaseModel):
    """Schools, colleges, universities and qualifications gained"""

    education_history: List[EducationHistoryRow] = Field(
        default="",
        description="List each school, college, or university attended and the qualifications gained",
    )  # List of table rows

    qualifications_gained: str = Field(
        default="",
        description=(
            "Heading for qualifications column in the education history table .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicationForEmployment(BaseModel):
    """
    APPLICATION FOR EMPLOYMENT

    ''
    """

    position_applied_for: PositionAppliedFor = Field(..., description="Position Applied For")
    personal_details: PersonalDetails = Field(..., description="Personal Details")
    uk_employment_restrictions: UKEmploymentRestrictions = Field(
        ..., description="UK Employment Restrictions"
    )
    education_history: EducationHistory = Field(..., description="Education History")
