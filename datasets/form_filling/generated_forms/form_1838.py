from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class TeamInformation(BaseModel):
    """Team or company details for the event"""

    team_or_company_name: str = Field(
        ...,
        description=(
            "Name of the team or company you are paddling with .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PaddlerInformation(BaseModel):
    """Your personal and contact information"""

    name: str = Field(
        ...,
        description=(
            'Your full legal name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        ...,
        description=(
            'Your mobile phone number .If you cannot fill this, write "N/A". If this '
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
            'City of your mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of your mailing address")

    zip: str = Field(..., description="ZIP or postal code of your mailing address")

    medical_condition_flag: BooleanLike = Field(
        ..., description="Indicate if you have any medical condition organizers should know about"
    )

    medical_condition_description: str = Field(
        default="",
        description=(
            "Describe any relevant medical conditions if you answered yes above .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class EmergencyContact(BaseModel):
    """Contact person in case of emergency"""

    emergency_contact_name: str = Field(
        ...,
        description=(
            "Full name of an adult emergency contact who will not be in the boat .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    emergency_contact_cell_phone: str = Field(
        ...,
        description=(
            "Mobile phone number of your emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Waiver and consent signatures"""

    signature: str = Field(
        ...,
        description=(
            "Participant’s signature acknowledging and agreeing to the waiver .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the participant signed the waiver"
    )  # YYYY-MM-DD format

    parent_guardian_signature: str = Field(
        default="",
        description=(
            "Signature of a parent or legal guardian if the participant is under 18 .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    parent_guardian_date: str = Field(
        default="", description="Date the parent or legal guardian signed"
    )  # YYYY-MM-DD format

    parent_guardian_printed_name: str = Field(
        default="",
        description=(
            "Printed name of the parent or legal guardian who signed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PaddlerWaiverForm(BaseModel):
    """
    PADDLER WAIVER FORM

    All Paddlers must read, sign and return in order to paddle with the Solomons Dragon Boat Festival.
    Do not sign this waiver form for any other person than yourself.
    By submitting this form, you are waiving important legal rights.
    """

    team_information: TeamInformation = Field(..., description="Team Information")
    paddler_information: PaddlerInformation = Field(..., description="Paddler Information")
    emergency_contact: EmergencyContact = Field(..., description="Emergency Contact")
    signatures: Signatures = Field(..., description="Signatures")
