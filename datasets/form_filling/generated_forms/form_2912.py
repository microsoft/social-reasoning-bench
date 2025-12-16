from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParentGuardianInformation(BaseModel):
    """Primary parent/guardian contact details"""

    parent_guardian_name: str = Field(
        ...,
        description=(
            'Full name of the parent or guardian .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    parent_guardian_email: str = Field(
        ...,
        description=(
            "Email address of the parent or guardian .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parent_guardian_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the parent or guardian .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_guardian_relationship: str = Field(
        ...,
        description=(
            "Relationship of this person to the child (e.g., mother, father, guardian) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class MediaRelease(BaseModel):
    """Permissions for use of photos and video"""

    media_release_give_permission: BooleanLike = Field(
        ..., description="Check if you give permission for media (photos/video) use as described"
    )

    media_release_do_not_give_permission: BooleanLike = Field(
        ...,
        description="Check if you do NOT give permission for media (photos/video) use as described",
    )


class HealthRelatedInformation(BaseModel):
    """Health and support information for the child"""

    health_related_information_details_line_1: str = Field(
        default="",
        description=(
            "Health or support information for the child (allergies, diagnoses, "
            "limitations, home changes, trauma history, etc.) - first line .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    health_related_information_details_line_2: str = Field(
        default="",
        description=(
            "Continuation of health or support information for the child - second line .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    health_related_information_details_line_3: str = Field(
        default="",
        description=(
            "Continuation of health or support information for the child - third line .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    health_related_information_details_line_4: str = Field(
        default="",
        description=(
            "Continuation of health or support information for the child - fourth line .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class EmergencyContact(BaseModel):
    """Non-parent/guardian emergency contact details"""

    emergency_contact_name: str = Field(
        ...,
        description=(
            "Full name of the emergency contact (not a parent/guardian listed above) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    emergency_contact_phone: str = Field(
        ...,
        description=(
            "Phone number for the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_relationship: str = Field(
        ...,
        description=(
            "Relationship of the emergency contact to the child .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TransportationInformation(BaseModel):
    """Authorized pickup and permission to walk home"""

    transportation_name_1: str = Field(
        default="",
        description=(
            "Name of first person authorized to pick up the child .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    transportation_relationship_1: str = Field(
        default="",
        description=(
            "Relationship of first authorized person to the child .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    transportation_contact_number_1: str = Field(
        default="",
        description=(
            "Contact number for first authorized person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    transportation_name_2: str = Field(
        default="",
        description=(
            "Name of second person authorized to pick up the child .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    transportation_relationship_2: str = Field(
        default="",
        description=(
            "Relationship of second authorized person to the child .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    transportation_contact_number_2: str = Field(
        default="",
        description=(
            "Contact number for second authorized person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    transportation_name_3: str = Field(
        default="",
        description=(
            "Name of third person authorized to pick up the child .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    transportation_relationship_3: str = Field(
        default="",
        description=(
            "Relationship of third authorized person to the child .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    transportation_contact_number_3: str = Field(
        default="",
        description=(
            "Contact number for third authorized person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    permission_to_walk_home_yes: BooleanLike = Field(
        ..., description="Select if the child has permission to walk home"
    )

    permission_to_walk_home_no: BooleanLike = Field(
        ..., description="Select if the child does NOT have permission to walk home"
    )


class MemberAgreement(BaseModel):
    """Parent/guardian agreement and signature"""

    parent_guardian_signature: str = Field(
        ...,
        description=(
            "Signature of parent or guardian agreeing to the member agreement .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    parent_guardian_signature_date_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of month for parent/guardian signature date"
    )

    parent_guardian_signature_date_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month for parent/guardian signature date"
    )

    parent_guardian_signature_date_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year for parent/guardian signature date"
    )


class OfficeUseOnly(BaseModel):
    """Internal membership and processing details"""

    membership_year_20: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Last two digits of the membership year (e.g., 24 for 2024)"
    )

    membership_new: BooleanLike = Field(default="", description="Check if this is a new membership")

    membership_renew: BooleanLike = Field(
        default="", description="Check if this is a membership renewal"
    )

    office_use_date_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day of month for office use membership date"
    )

    office_use_date_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month for office use membership date"
    )


class ParentGuardianInformation(BaseModel):
    """
    Parent / Guardian Information

    OF NOTE: Personal information is protected under the Municipal Freedom of Information and Protection of Privacy Act, 1989. Personal information is collected pursuant to the Municipal Act, R.S.O. 1990, Chapter M-45 as amended, S. 207, Par. 28, and will be used to register participants. This information will NOT be shared with anyone for any purpose. Inquiries may be directed to 905-830-0776
    """

    parent__guardian_information: ParentGuardianInformation = Field(
        ..., description="Parent / Guardian Information"
    )
    media_release: MediaRelease = Field(..., description="Media Release")
    health_related_information: HealthRelatedInformation = Field(
        ..., description="Health Related Information"
    )
    emergency_contact: EmergencyContact = Field(..., description="Emergency Contact")
    transportation_information: TransportationInformation = Field(
        ..., description="Transportation Information"
    )
    member_agreement: MemberAgreement = Field(..., description="Member Agreement")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
