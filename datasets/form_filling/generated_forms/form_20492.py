from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrganizationInformation(BaseModel):
    """Basic information about the organization and applicant"""

    organization_name: str = Field(
        ...,
        description=(
            "Legal or common name of the organization applying for funds .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the organization or contact person .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    organization_address: str = Field(
        ...,
        description=(
            'Mailing address of the organization .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_individual_submitting_application: str = Field(
        ...,
        description=(
            "Full name of the person completing and submitting this application .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    yes_are_you_a_non_profit_organization: BooleanLike = Field(
        ..., description="Select yes if the organization is a registered non-profit"
    )

    no_are_you_a_non_profit_organization: BooleanLike = Field(
        ..., description="Select no if the organization is not a registered non-profit"
    )


class RequestDetails(BaseModel):
    """Details about the type of request and use of funds"""

    personal_type_of_request: BooleanLike = Field(
        ..., description="Check if this funding request is for a personal/individual need"
    )

    group_type_of_request: BooleanLike = Field(
        ..., description="Check if this funding request is for a group"
    )

    community_type_of_request: BooleanLike = Field(
        ..., description="Check if this funding request is for a community-wide purpose"
    )

    how_will_the_funds_be_used: str = Field(
        ...,
        description=(
            "Describe specifically how the requested funds will be spent .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    what_are_the_benefits_to_the_stoughton_community: str = Field(
        ...,
        description=(
            "Explain how this request will benefit the Stoughton community .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    what_other_information_would_you_like_to_share: str = Field(
        default="",
        description=(
            "Provide any additional details or context you would like to include .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Signatures(BaseModel):
    """Applicant signatures and dates"""

    applicant_signature_1: str = Field(
        ...,
        description=(
            "Signature of the first applicant or authorized representative .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_1: str = Field(
        ..., description="Date the first applicant signed the form"
    )  # YYYY-MM-DD format

    applicant_signature_2: str = Field(
        default="",
        description=(
            "Signature of the second applicant or additional authorized representative, if "
            'applicable .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    date_2: str = Field(
        default="", description="Date the second applicant signed the form"
    )  # YYYY-MM-DD format


class ApplicationForFundsFromRoundupProgramDonation(BaseModel):
    """
    Application for Funds from RoundUP Program Donation

    Application for Funds from RoundUP Program Donation
    """

    organization_information: OrganizationInformation = Field(
        ..., description="Organization Information"
    )
    request_details: RequestDetails = Field(..., description="Request Details")
    signatures: Signatures = Field(..., description="Signatures")
