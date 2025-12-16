from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrganisationContactDetails(BaseModel):
    """Basic information about the organisation and primary contact"""

    organisation_name: str = Field(
        ...,
        description=(
            "Legal name of the organisation applying for the grant .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_name: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    position_of_contact: str = Field(
        ...,
        description=(
            "Role or position of the contact person within the organisation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Primary landline or main contact phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mobile: str = Field(
        default="",
        description=(
            "Mobile phone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Email address for correspondence about this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address of the organisation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    postal_address: str = Field(
        default="",
        description=(
            "Postal mailing address if different from street address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BankingFundingDetails(BaseModel):
    """Bank account and funding request information"""

    account_name: str = Field(
        ...,
        description=(
            "Name of the bank account to receive grant funds .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    account_number: str = Field(
        ...,
        description=(
            "Bank account number for payment of funds .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    bsb: str = Field(
        ...,
        description=(
            "Bank State Branch (BSB) number for the account .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    amount_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount of funding requested (between $501 and $2000)"
    )

    abn: str = Field(
        default="",
        description=(
            "Australian Business Number of the organisation, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ActivityDetails(BaseModel):
    """Details of the proposed activity or event"""

    activity_name: str = Field(
        ...,
        description=(
            "Title or name of the project, event or activity .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    activity_date: str = Field(
        ..., description="Planned date or start date of the activity"
    )  # YYYY-MM-DD format

    location_of_activity: str = Field(
        ...,
        description=(
            "Venue or location where the activity will take place .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    environmental_initiative: BooleanLike = Field(
        default="", description="Indicate if the request is for an environmental initiative"
    )


class RequiredAttachments(BaseModel):
    """Documentation to be attached to the written application"""

    details_of_project_event_or_activity_supporting_material_and_need_for_support: BooleanLike = (
        Field(
            ...,
            description=(
                "Checkbox to confirm that detailed project information and supporting material "
                "are attached"
            ),
        )
    )

    proof_of_registration_as_community_nfp_or_incorporated_body: BooleanLike = Field(
        ..., description="Checkbox to confirm proof of registration is attached"
    )

    contact_details_of_elected_office_holders: BooleanLike = Field(
        ...,
        description="Checkbox to confirm contact details of elected office holders are attached",
    )

    proof_of_appropriate_insurance_certificate_of_currency: BooleanLike = Field(
        ...,
        description="Checkbox to confirm proof of insurance and certificate of currency are attached",
    )

    minuted_details_of_your_organisations_resolution_to_request_funding: BooleanLike = Field(
        ..., description="Checkbox to confirm minuted resolution to request funding is attached"
    )


class CommunityBenefitAlignment(BaseModel):
    """How the activity benefits the community and aligns with the Community Plan"""

    funding_benefit_to_palmerston_community: str = Field(
        ...,
        description=(
            "Describe how the proposed activity, event or item will benefit the Palmerston "
            'community .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    goals_and_strategies_in_the_city_of_palmerston_community_plan: str = Field(
        ...,
        description=(
            "Explain how the proposal relates to the goals and strategies in the City of "
            'Palmerston Community Plan .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class Declaration(BaseModel):
    """Applicant declaration and signing"""

    signed: str = Field(
        ...,
        description=(
            "Signature of authorised representative of the organisation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the application form is signed")  # YYYY-MM-DD format


class ApplicationFormGrantsAndDonationsRequests501To2000(BaseModel):
    """APPLICATION FORM
    GRANTS AND DONATIONS
    REQUESTS $501 TO $2000"""

    organisation__contact_details: OrganisationContactDetails = Field(
        ..., description="Organisation & Contact Details"
    )
    banking__funding_details: BankingFundingDetails = Field(
        ..., description="Banking & Funding Details"
    )
    activity_details: ActivityDetails = Field(..., description="Activity Details")
    required_attachments: RequiredAttachments = Field(..., description="Required Attachments")
    community_benefit__alignment: CommunityBenefitAlignment = Field(
        ..., description="Community Benefit & Alignment"
    )
    declaration: Declaration = Field(..., description="Declaration")
