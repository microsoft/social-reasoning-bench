from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalDetails(BaseModel):
    """Personal and contact details of the under-18 staff/volunteer"""

    surname: str = Field(
        ...,
        description=(
            "Family name (last name) of the staff member or volunteer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    given_names: str = Field(
        ...,
        description=(
            "All given/first and middle names of the staff member or volunteer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    previous_names_if_applicable: str = Field(
        default="",
        description=(
            "Any former names or aliases previously used, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Date of birth of the staff member or volunteer"
    )  # YYYY-MM-DD format

    gender: str = Field(
        ...,
        description=(
            "Gender of the staff member or volunteer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Residential mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for contact .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    wwcc_number: str = Field(
        default="",
        description=(
            "Working With Children Check number, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    health_conditions: str = Field(
        default="",
        description=(
            "Details of any medical or health conditions relevant to the person’s "
            'participation .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class ParentGuardianDetails(BaseModel):
    """Contact details for the parent or guardian"""

    parent_guardian_name: str = Field(
        ...,
        description=(
            "Full name of the parent or legal guardian .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parent_guardian_contact_number: str = Field(
        ...,
        description=(
            "Contact phone number for the parent or legal guardian .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SafeMinistryScreeningQuestionnaire(BaseModel):
    """
    Safe ministry screening questionnaire

    For staff and volunteers under 18 years of age who are serving as a volunteer or junior volunteer/helper.
    """

    personal_details: PersonalDetails = Field(..., description="Personal Details")
    parentguardian_details: ParentGuardianDetails = Field(
        ..., description="Parent/Guardian Details"
    )
