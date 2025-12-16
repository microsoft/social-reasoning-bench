from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalInformation(BaseModel):
    """Basic personal and contact details"""

    last_name: str = Field(
        ...,
        description=(
            'Student\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    first: str = Field(
        ...,
        description=(
            'Student\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    initial: str = Field(
        default="",
        description=(
            'Student\'s middle initial .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    birth_date: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            'Student\'s street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of residence")

    zip: str = Field(..., description="ZIP or postal code")

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class AcademicInformation(BaseModel):
    """Current and planned academic details"""

    high_school_attending_ed: str = Field(
        ...,
        description=(
            "Name of the high school currently attending or attended .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    grade_point_average: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current cumulative grade point average (GPA)"
    )

    college_planning_to_attend: str = Field(
        default="",
        description=(
            "Name of the college the student plans to attend .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_if_known: str = Field(
        default="",
        description=(
            'Intended college major, if known .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SchoolActivitiesSportsInvolvement(BaseModel):
    """Extracurricular school activities and sports involvement"""

    school_activities_sports_involvement_include_offices_held_honors_awards_and_dates_if_available: str = Field(
        default="",
        description=(
            "Description of school activities and sports involvement, including offices "
            "held, honors, awards, and dates if available .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CivicandCommunityInvolvement(BaseModel):
    """Civic and community activities and service"""

    civic_and_community_involvement: str = Field(
        default="",
        description=(
            "Description of civic and community activities and involvement .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class EmploymentRecord(BaseModel):
    """Employment history, if any"""

    employment_record_if_any: str = Field(
        default="",
        description=(
            "Summary of any employment history, including positions and dates .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Verification(BaseModel):
    """Counselor or principal verification signature"""

    signature_of_verification: str = Field(
        ...,
        description=(
            "Signature of counselor or principal verifying the information .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PersonalInformation(BaseModel):
    """PERSONAL INFORMATION"""

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    academic_information: AcademicInformation = Field(..., description="Academic Information")
    school_activities__sports_involvement: SchoolActivitiesSportsInvolvement = Field(
        ..., description="School Activities / Sports Involvement"
    )
    civic_and_community_involvement: CivicandCommunityInvolvement = Field(
        ..., description="Civic and Community Involvement"
    )
    employment_record: EmploymentRecord = Field(..., description="Employment Record")
    verification: Verification = Field(..., description="Verification")
