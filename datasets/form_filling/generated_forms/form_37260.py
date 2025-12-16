from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationFeesandTierSelection(BaseModel):
    """Fee payments and cultivation tier selection"""

    application_fee_500: BooleanLike = Field(
        ..., description="Check to indicate payment of the $500 application fee"
    )

    sbi_21_00_each_owner: BooleanLike = Field(
        ..., description="Check to indicate SBI fee of $21.00 has been paid for each owner"
    )

    tier_1_500: BooleanLike = Field(..., description="Check if applying for Tier 1 license at $500")

    tier_2_5_000: BooleanLike = Field(
        ..., description="Check if applying for Tier 2 license at $5,000"
    )

    tier_3_10_000: BooleanLike = Field(
        ..., description="Check if applying for Tier 3 license at $10,000"
    )


class Business(BaseModel):
    """Business information and contact details"""

    business_name_d_b_a: str = Field(
        ...,
        description=(
            "Legal business name or doing-business-as name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_business: str = Field(
        ...,
        description=(
            'Primary business phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    location_address: str = Field(
        ...,
        description=(
            "Physical address where the marijuana cultivation will occur .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    if_new_what_was_formerly_at_this_location: str = Field(
        default="",
        description=(
            "Description of the prior use or business at this location, if newly "
            'established .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    mailing_address_business: str = Field(
        ...,
        description=(
            "Mailing address for the business, if different from location address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_contact_information_website_fax_email_etc: str = Field(
        default="",
        description=(
            "Any additional business contact details such as website, fax, or extra email "
            'addresses .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Owner(BaseModel):
    """Owner contact information"""

    name_owner: str = Field(
        ...,
        description=(
            "Full name of the owner or ownership entity representative .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_owner: str = Field(
        ...,
        description=(
            'Primary phone number for the owner .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_owner: str = Field(
        ...,
        description=(
            'Email address for the owner .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_owner: str = Field(
        ...,
        description=(
            'Mailing address for the owner .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContact(BaseModel):
    """Emergency contact person details"""

    name_emergency_contact: str = Field(
        ...,
        description=(
            "Full name of the emergency contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_emergency_contact: str = Field(
        ...,
        description=(
            "Primary phone number for the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_emergency_contact: str = Field(
        ...,
        description=(
            "Email address for the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_emergency_contact: str = Field(
        ...,
        description=(
            "Mailing address for the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CommunityRelationsLiaison(BaseModel):
    """Designated community relations liaison contact information"""

    name_community_relations_liaison: str = Field(
        default="",
        description=(
            "Full name of the designated community relations liaison .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_community_relations_liaison: str = Field(
        default="",
        description=(
            "Phone number for the community relations liaison .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_community_relations_liaison: str = Field(
        default="",
        description=(
            "Email address for the community relations liaison .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_community_relations_liaison: str = Field(
        default="",
        description=(
            "Mailing address for the community relations liaison .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LocalAuthorizedAgentforService(BaseModel):
    """Local authorized agent for service of process"""

    name_local_authorized_agent_for_service: str = Field(
        default="",
        description=(
            "Full name of the local authorized agent for service of process .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone_local_authorized_agent_for_service: str = Field(
        default="",
        description=(
            "Phone number for the local authorized agent for service .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_local_authorized_agent_for_service: str = Field(
        default="",
        description=(
            "Email address for the local authorized agent for service .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_local_authorized_agent_for_service: str = Field(
        default="",
        description=(
            "Mailing address for the local authorized agent for service .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PortlandPermitInspectionsMarijuanaCultivationLicenseApp(BaseModel):
    """
        CITY OF PORTLAND
    Permitting and Inspections Department

    Application for Marijuana Cultivation License

        Application for Marijuana Cultivation License
    """

    application_fees_and_tier_selection: ApplicationFeesandTierSelection = Field(
        ..., description="Application Fees and Tier Selection"
    )
    business: Business = Field(..., description="Business")
    owner: Owner = Field(..., description="Owner")
    emergency_contact: EmergencyContact = Field(..., description="Emergency Contact")
    community_relations_liaison: CommunityRelationsLiaison = Field(
        ..., description="Community Relations Liaison"
    )
    local_authorized_agent_for_service: LocalAuthorizedAgentforService = Field(
        ..., description="Local Authorized Agent for Service"
    )
