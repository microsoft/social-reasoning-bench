from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParticipantInformation(BaseModel):
    """Basic information about the participant"""

    name_of_participant: str = Field(
        ...,
        description=(
            'Full legal name of the participant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    preferred_nickname: str = Field(
        default="",
        description=(
            "Name the participant prefers to be called .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    age_of_participant: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Age of the participant in years"
    )

    gender: str = Field(
        ...,
        description=(
            'Gender of the participant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    t_shirt_size: str = Field(
        ...,
        description=(
            "T-shirt size for the participant (e.g., Youth M, Adult L) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    shoe_size: str = Field(
        ...,
        description=(
            'Shoe size for the participant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    participant_cell_phone: str = Field(
        default="",
        description=(
            "Participant’s cell phone number if they have one and may be called .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ParentGuardianInformation(BaseModel):
    """Contact details for parent(s) or guardian(s)"""

    name_of_parents_guardians: str = Field(
        ...,
        description=(
            "Full name or names of the participant’s parent(s) or legal guardian(s) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    parent_guardian_emails: str = Field(
        ...,
        description=(
            "Email address or addresses for the parent(s) or guardian(s) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    parent_guardian_phones: str = Field(
        ...,
        description=(
            "Phone number or numbers for the parent(s) or guardian(s) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Mailing address for the participant or household .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ParticipantBackground(BaseModel):
    """Experience and characteristics relevant to program participation"""

    previous_outdoor_experience_skill_level: str = Field(
        default="",
        description=(
            "Description of the participant’s prior outdoor activities and skill level .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    physical_emotional_behavioral_characteristics: str = Field(
        default="",
        description=(
            "Any physical, emotional, or behavioral information staff should know to "
            'support the participant .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class EmergencyandPickupContacts(BaseModel):
    """Primary, secondary, and backup contacts for emergencies and pickup/drop-off"""

    contact_1: str = Field(
        ...,
        description=(
            "Identifier or description for the first primary contact .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_1_name: str = Field(
        ...,
        description=(
            'Full name of the first contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_1_relationship: str = Field(
        ...,
        description=(
            "Relationship of Contact #1 to the participant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_1_best_contact_phone_number: str = Field(
        ...,
        description=(
            'Best phone number to reach Contact #1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_2: str = Field(
        ...,
        description=(
            "Identifier or description for the second contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_2_name: str = Field(
        ...,
        description=(
            "Full name of the second contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_2_relationship: str = Field(
        ...,
        description=(
            "Relationship of Contact #2 to the participant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_2_best_contact_phone_number: str = Field(
        ...,
        description=(
            'Best phone number to reach Contact #2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_3: str = Field(
        ...,
        description=(
            "Identifier or description for the third contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_3_name: str = Field(
        ...,
        description=(
            'Full name of the third contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_3_relationship: str = Field(
        ...,
        description=(
            "Relationship of Contact #3 to the participant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_3_best_contact_phone_number: str = Field(
        ...,
        description=(
            'Best phone number to reach Contact #3 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class OapParticipantInfoForm(BaseModel):
    """
    OAP - PARTICIPANT INFO FORM

    ''
    """

    participant_information: ParticipantInformation = Field(
        ..., description="Participant Information"
    )
    parentguardian_information: ParentGuardianInformation = Field(
        ..., description="Parent/Guardian Information"
    )
    participant_background: ParticipantBackground = Field(..., description="Participant Background")
    emergency_and_pickup_contacts: EmergencyandPickupContacts = Field(
        ..., description="Emergency and Pickup Contacts"
    )
