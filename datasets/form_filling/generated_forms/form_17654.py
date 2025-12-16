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
    """Basic information about the youth participant"""

    full_name: str = Field(
        ...,
        description=(
            'Participant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_number: str = Field(
        ...,
        description=(
            "Primary emergency contact phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    troop_number: str = Field(
        ...,
        description=(
            'Trail Life USA troop number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class AdultsAuthorizedtoTransportYouth(BaseModel):
    """Adults who are allowed to take the youth to and from events"""

    authorized_adult_1_name: str = Field(
        ...,
        description=(
            "Name of first adult authorized to take youth to and from events .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    authorized_adult_1_telephone: str = Field(
        ...,
        description=(
            "Telephone number for first authorized adult .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    authorized_adult_2_name: str = Field(
        default="",
        description=(
            "Name of second adult authorized to take youth to and from events .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    authorized_adult_2_telephone: str = Field(
        default="",
        description=(
            "Telephone number for second authorized adult .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    authorized_adult_3_name: str = Field(
        default="",
        description=(
            "Name of third adult authorized to take youth to and from events .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    authorized_adult_3_telephone: str = Field(
        default="",
        description=(
            "Telephone number for third authorized adult .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdultsNOTAuthorizedtoTransportYouth(BaseModel):
    """Adults who are not allowed to take the youth to and from events"""

    not_authorized_adult_1_name: str = Field(
        default="",
        description=(
            "Name of first adult NOT authorized to take youth to and from events .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    not_authorized_adult_1_telephone: str = Field(
        default="",
        description=(
            "Telephone number for first non-authorized adult .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    not_authorized_adult_2_name: str = Field(
        default="",
        description=(
            "Name of second adult NOT authorized to take youth to and from events .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    not_authorized_adult_2_telephone: str = Field(
        default="",
        description=(
            "Telephone number for second non-authorized adult .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    not_authorized_adult_3_name: str = Field(
        default="",
        description=(
            "Name of third adult NOT authorized to take youth to and from events .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    not_authorized_adult_3_telephone: str = Field(
        default="",
        description=(
            "Telephone number for third non-authorized adult .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NotesandLimitations(BaseModel):
    """Additional notes or limitations regarding participation or treatment"""

    notes_line_1: str = Field(
        default="",
        description=(
            "First line for additional notes or limitations .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    notes_line_2: str = Field(
        default="",
        description=(
            "Second line for additional notes or limitations .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SignaturesandConsent(BaseModel):
    """Signatures confirming consent and accuracy of information"""

    participants_signature: str = Field(
        ...,
        description=(
            'Signature of the participant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    participant_signature_date: str = Field(
        ..., description="Date participant signed the form"
    )  # YYYY-MM-DD format

    parent_guardian_signature: str = Field(
        ...,
        description=(
            "Signature of parent or guardian if participant is under age 18 .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    parent_guardian_signature_date: str = Field(
        ..., description="Date parent or guardian signed the form"
    )  # YYYY-MM-DD format

    second_parent_guardian_signature: str = Field(
        default="",
        description=(
            "Signature of second parent or guardian if required .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    second_parent_guardian_signature_date: str = Field(
        default="", description="Date second parent or guardian signed the form"
    )  # YYYY-MM-DD format


class TrailLifeUsaYouthMemberparticipantHealthMedicalForm(BaseModel):
    """
    Trail Life USA | Youth Member/Participant Health & Medical Form

    ''
    """

    participant_information: ParticipantInformation = Field(
        ..., description="Participant Information"
    )
    adults_authorized_to_transport_youth: AdultsAuthorizedtoTransportYouth = Field(
        ..., description="Adults Authorized to Transport Youth"
    )
    adults_not_authorized_to_transport_youth: AdultsNOTAuthorizedtoTransportYouth = Field(
        ..., description="Adults NOT Authorized to Transport Youth"
    )
    notes_and_limitations: NotesandLimitations = Field(..., description="Notes and Limitations")
    signatures_and_consent: SignaturesandConsent = Field(..., description="Signatures and Consent")
