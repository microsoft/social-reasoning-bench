from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PropertyContactInformation(BaseModel):
    """Basic information about the property and primary contacts"""

    business_name_if_any: str = Field(
        default="",
        description=(
            "Business name associated with the property, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    property_address: str = Field(
        ...,
        description=(
            "Street address of the property for which trespass authorization is requested "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Primary contact person for this property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_primary_contact: str = Field(
        ...,
        description=(
            "Phone number for the primary contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_emergency_contact: str = Field(
        default="",
        description=(
            "Name of an additional emergency contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_other_emergency_contact: str = Field(
        default="",
        description=(
            "Phone number for the additional emergency contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProblemsExperienced(BaseModel):
    """Types of problems occurring at the property and their impact"""

    defecating: BooleanLike = Field(
        default="", description="Check if defecating has been a problem at the property"
    )

    drinking: BooleanLike = Field(
        default="", description="Check if drinking has been a problem at the property"
    )

    illegal_lodging: BooleanLike = Field(
        default="", description="Check if illegal lodging has been a problem at the property"
    )

    littering: BooleanLike = Field(
        default="", description="Check if littering has been a problem at the property"
    )

    urinating: BooleanLike = Field(
        default="", description="Check if urinating has been a problem at the property"
    )

    vandalism: BooleanLike = Field(
        default="", description="Check if vandalism has been a problem at the property"
    )

    other_problem: str = Field(
        default="",
        description=(
            "Describe any other problems experienced at the property .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    this_activity_affects_me_in_the_following_way: str = Field(
        default="",
        description=(
            "Explain how the described activity impacts you or your property .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class AuthorizationPeriodSignature(BaseModel):
    """Authorization time frame and signer information"""

    beginning_twelve_month_period: str = Field(
        ..., description="Start date of the twelve-month trespass authorization period"
    )  # YYYY-MM-DD format

    continuing_through_twelve_month_period: str = Field(
        ..., description="End date of the twelve-month trespass authorization period"
    )  # YYYY-MM-DD format

    signature: str = Field(
        ...,
        description=(
            "Signature of the property owner or authorized agent .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_signature: str = Field(
        ..., description="Date the trespass authorization form is signed"
    )  # YYYY-MM-DD format


class MailingAddressIfDifferent(BaseModel):
    """Mailing address for the owner/agent if different from property address"""

    name_mailing: str = Field(
        default="",
        description=(
            "Name for mailing address, if different from property location .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address_mailing: str = Field(
        default="",
        description=(
            "Mailing address, if different from the property address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DepartmentUseOnly(BaseModel):
    """For Banning Police Department administrative processing"""

    received_by: str = Field(
        default="",
        description=(
            "Name of BPD Administration staff member who received the form .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_received_by: str = Field(
        default="", description="Date the form was received by BPD Administration"
    )  # YYYY-MM-DD format

    entered_by: str = Field(
        default="",
        description=(
            "Name of BPD staff member who entered the form information .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_entered_by: str = Field(
        default="", description="Date the form information was entered"
    )  # YYYY-MM-DD format

    bpd_dept: str = Field(
        default="",
        description=(
            "Banning Police Department unit or department handling the form .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class TrespassLetterOfAuthorization(BaseModel):
    """
    TRESPASS LETTER OF AUTHORIZATION

    As OWNER/AGENT of the property located above, I request that officers of the Banning Police Department enforce the criminal laws governing trespass and request that officers prosecute anyone who is loitering on the property and/or is engaged in any unlawful activity for the next twelve-month period beginning ________________ and continuing through _________________. Any persons who are not tenants of this property, or who are not otherwise permitted upon this property for legitimate purposes, are trespassing, and I authorize the arrest and prosecution of these violators.
    """

    property__contact_information: PropertyContactInformation = Field(
        ..., description="Property & Contact Information"
    )
    problems_experienced: ProblemsExperienced = Field(..., description="Problems Experienced")
    authorization_period__signature: AuthorizationPeriodSignature = Field(
        ..., description="Authorization Period & Signature"
    )
    mailing_address_if_different: MailingAddressIfDifferent = Field(
        ..., description="Mailing Address (If Different)"
    )
    department_use_only: DepartmentUseOnly = Field(..., description="Department Use Only")
