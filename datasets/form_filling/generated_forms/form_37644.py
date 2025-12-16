from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MembershipInformation(BaseModel):
    """Member status, names, children, membership type, and guest passes"""

    are_you_a_senior_65_yes: BooleanLike = Field(
        default="", description="Check if the primary member is a senior aged 65 or older"
    )

    are_you_a_senior_65_no: BooleanLike = Field(
        default="", description="Check if the primary member is not a senior aged 65 or older"
    )

    returning_member_yes: BooleanLike = Field(
        default="", description="Check if you were a member in a previous season"
    )

    returning_member_no: BooleanLike = Field(
        default="", description="Check if this is your first time joining as a member"
    )

    family_last_name: str = Field(
        ...,
        description=(
            "Family or household last name for the membership .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    adult_first_names: str = Field(
        ...,
        description=(
            "First names of all adult members on the membership .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    children_names_ages_1: str = Field(
        default="",
        description=(
            "Name and age of child 1 included in the membership .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    children_names_ages_2: str = Field(
        default="",
        description=(
            "Name and age of child 2 included in the membership .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    children_names_ages_3_plus_45: str = Field(
        default="",
        description=(
            "Name and age of child 3; additional fee applies for this child .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    children_names_ages_4_plus_45: str = Field(
        default="",
        description=(
            "Name and age of child 4; additional fee applies for this child .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    children_names_ages_5_plus_45: str = Field(
        default="",
        description=(
            "Name and age of child 5; additional fee applies for this child .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    children_names_ages_6_plus_45: str = Field(
        default="",
        description=(
            "Name and age of child 6; additional fee applies for this child .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    type_of_membership_single: BooleanLike = Field(
        ..., description="Select if this is a single-person membership"
    )

    type_of_membership_couple: BooleanLike = Field(
        ..., description="Select if this is a couple membership"
    )

    type_of_membership_family: BooleanLike = Field(
        ..., description="Select if this is a family membership"
    )

    type_of_membership_senior_single_65: BooleanLike = Field(
        ..., description="Select if this is a senior single membership for ages 65 and up"
    )

    type_of_membership_senior_couple: BooleanLike = Field(
        ..., description="Select if this is a senior couple membership"
    )

    type_of_membership_senior_couple_with_grandchildren: BooleanLike = Field(
        ..., description="Select if this is a senior couple membership that includes grandchildren"
    )

    enhance_membership_guest_passes_yes: BooleanLike = Field(
        default="", description="Check Yes to add 4 guest passes for an additional $30"
    )

    enhance_membership_guest_passes_no: BooleanLike = Field(
        default="", description="Check No if you do not want to add guest passes"
    )


class ContactInformation(BaseModel):
    """Mailing address and primary contact numbers/emails"""

    address: str = Field(
        ...,
        description=(
            "Mailing address for the primary member .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            'Primary home phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            "Primary email address for membership communication .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Primary cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    second_cell_phone: str = Field(
        default="",
        description=(
            'Secondary cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    work_phone: str = Field(
        default="",
        description=(
            'Primary work phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    second_work_phone: str = Field(
        default="",
        description=(
            'Secondary work phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContact(BaseModel):
    """Emergency contact person and relationship"""

    emergency_contact_name: str = Field(
        ...,
        description=(
            'Full name of emergency contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_phone: str = Field(
        ...,
        description=(
            "Primary phone number for emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_alt_phone: str = Field(
        default="",
        description=(
            "Alternate phone number for emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_relationship: str = Field(
        ...,
        description=(
            "Relationship of the emergency contact to the member .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class HealthConditions(BaseModel):
    """Health or physical conditions that may affect safety"""

    health_conditions_line_1: str = Field(
        default="",
        description=(
            "First line to describe any health or physical conditions that may increase "
            'risk .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    health_conditions_line_2: str = Field(
        default="",
        description=(
            "Second line to describe any health or physical conditions that may increase "
            'risk .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    health_conditions_line_3: str = Field(
        default="",
        description=(
            "Third line to describe any health or physical conditions that may increase "
            'risk .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Member signatures acknowledging bylaws and waiver"""

    signature_and_date_1: str = Field(
        ...,
        description=(
            "Signature and date of first adult member acknowledging terms .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    signature_and_date_2: str = Field(
        default="",
        description=(
            "Signature and date of second adult member, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_and_date_3: str = Field(
        default="",
        description=(
            "Signature and date of third adult member, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ForOfficeUse(BaseModel):
    """Internal processing and tracking by office staff"""

    for_office_use_respond: BooleanLike = Field(
        default="", description="Office use only: mark if a response is required or has been sent"
    )

    for_office_use_gft: BooleanLike = Field(
        default="", description="Office use only: mark if this is a gift membership"
    )

    for_office_use_xtra_pss: BooleanLike = Field(
        default="", description="Office use only: mark if extra passes were issued"
    )

    for_office_use_mem_crd: BooleanLike = Field(
        default="", description="Office use only: mark when membership card has been issued"
    )

    for_office_use_emer_dot: BooleanLike = Field(
        default="", description="Office use only: mark when emergency information is documented"
    )

    for_office_use_other: str = Field(
        default="",
        description=(
            "Office use only: specify any other notes or actions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WilsonHarborPoolClub2021MembershipApplication(BaseModel):
    """WILSON HARBOR POOL CLUB

    2021 Membership Application"""

    membership_information: MembershipInformation = Field(..., description="Membership Information")
    contact_information: ContactInformation = Field(..., description="Contact Information")
    emergency_contact: EmergencyContact = Field(..., description="Emergency Contact")
    health_conditions: HealthConditions = Field(..., description="Health Conditions")
    signatures: Signatures = Field(..., description="Signatures")
    for_office_use: ForOfficeUse = Field(..., description="For Office Use")
