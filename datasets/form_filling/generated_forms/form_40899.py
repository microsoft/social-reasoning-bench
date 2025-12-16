from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentSchoolInformation(BaseModel):
    """Basic information about the student and school"""

    student: str = Field(
        ...,
        description=(
            "Full name of the student being referred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this referral form is completed")  # YYYY-MM-DD format

    school: str = Field(
        ...,
        description=(
            "Name of the school the student attends .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format

    teacher: str = Field(
        ...,
        description=(
            'Name of the student\'s primary teacher .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        ...,
        description=(
            'Student\'s current grade level .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    parent: str = Field(
        ...,
        description=(
            "Name of the student's parent or guardian .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary contact phone number for the parent or guardian .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        default="",
        description=(
            "Mailing address for the student or parent/guardian .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReferralDetails(BaseModel):
    """Information about the referral and referrer"""

    referred_by: str = Field(
        ...,
        description=(
            "Name of the person making the Section 504 referral .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position: str = Field(
        ...,
        description=(
            "Role or job title of the person making the referral .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_referral: str = Field(
        ...,
        description=(
            "Detailed explanation of why the student is being referred for Section 504 "
            'consideration .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    accommodations_and_interventions_attempted: str = Field(
        ...,
        description=(
            "Description of accommodations and interventions already tried with the student "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class Section504Referral(BaseModel):
    """
    Section 504 Referral

    ''
    """

    student__school_information: StudentSchoolInformation = Field(
        ..., description="Student & School Information"
    )
    referral_details: ReferralDetails = Field(..., description="Referral Details")
