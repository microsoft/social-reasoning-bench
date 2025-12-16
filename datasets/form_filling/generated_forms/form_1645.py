from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CommunityServiceSchoolInvolvementTableRow(BaseModel):
    """Single row in Community Service & School Involvement"""

    community_service_organization_role: str = Field(
        default="", description="Community_Service_Organization_Role"
    )
    school_activity_role: str = Field(default="", description="School_Activity_Role")


class PersonalInformation(BaseModel):
    """Applicant’s basic personal and contact details"""

    name_last_first_mi: str = Field(
        ...,
        description=(
            "Applicant's full name (last, first, middle initial) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dob_mm_dd_yy_age: str = Field(
        ...,
        description=(
            "Date of birth in mm/dd/yy format and current age .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
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

    state: str = Field(..., description="State of residence (abbreviation)")

    zip: str = Field(..., description="Zip or postal code")

    home_phone_cel_phone: str = Field(
        ...,
        description=(
            'Home and/or cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    parents_legal_guardians_name: str = Field(
        ...,
        description=(
            "Name(s) of parent(s) or legal guardian(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parents_legal_guardians_email: str = Field(
        ...,
        description=(
            "Email address for parent(s) or legal guardian(s) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class HighSchoolInformation(BaseModel):
    """Current school and academic information"""

    school_name: str = Field(
        ...,
        description=(
            'Name of current high school .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    current_grade_gpa: str = Field(
        ...,
        description=(
            'Current grade level and GPA .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    school_address: str = Field(
        default="",
        description=(
            "Mailing address of current high school .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CommunityServiceSchoolInvolvement(BaseModel):
    """Activities, roles, and involvement in community and school"""

    community_service_school_involvement_table: List[CommunityServiceSchoolInvolvementTableRow] = (
        Field(
            default="",
            description="Table to list community service organizations/roles and school activities/roles",
        )
    )  # List of table rows


class HonorsAwards(BaseModel):
    """Recognition, honors, and awards received"""

    honors_awards_line_1: str = Field(
        default="",
        description=(
            'Honors and awards (first line) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    honors_awards_line_2: str = Field(
        default="",
        description=(
            'Honors and awards (second line) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalInformation(BaseModel):
    """Delta Academy status and other information for selection"""

    are_you_a_delta_academy_graduate: BooleanLike = Field(
        default="",
        description="Indicates whether the applicant is a Delta Academy graduate (yes or no)",
    )

    is_there_anything_youd_like_to_share: str = Field(
        default="",
        description=(
            "Additional information about the applicant that may assist the committee in "
            'the selection process .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class DeltaSigmaThetaSTLAlumnaeDeltaGemsReturningParticipant(BaseModel):
    """
        Delta Sigma Theta Sorority, Incorporated
    Saint Louis Alumnae Chapter
    Delta G.E.M.S. APPLICATION   Returning Participant

        ''
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    high_school_information: HighSchoolInformation = Field(
        ..., description="High School Information"
    )
    community_service__school_involvement: CommunityServiceSchoolInvolvement = Field(
        ..., description="Community Service & School Involvement"
    )
    honors__awards: HonorsAwards = Field(..., description="Honors & Awards")
    additional_information: AdditionalInformation = Field(..., description="Additional Information")
