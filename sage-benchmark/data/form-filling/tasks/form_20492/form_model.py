from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrganizationContactInformation(BaseModel):
    """Basic information about the organization and applicant"""

    organization_name: str = Field(
        ...,
        description=(
            "Legal name of the organization applying for RoundUP funds .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
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

    non_profit_yes: BooleanLike = Field(
        ..., description="Select if the organization is a non-profit"
    )

    non_profit_no: BooleanLike = Field(
        ..., description="Select if the organization is not a non-profit"
    )

    type_of_request_personal: BooleanLike = Field(
        ..., description="Check if the funding request is for a personal need"
    )

    type_of_request_group: BooleanLike = Field(
        ..., description="Check if the funding request is for a group need"
    )

    type_of_request_community: BooleanLike = Field(
        ..., description="Check if the funding request is for a community-wide need"
    )


class FundingRequestDetails(BaseModel):
    """Details about how funds will be used and community impact"""

    how_will_the_funds_be_used: str = Field(
        ...,
        description=(
            "Describe specifically how the requested funds will be spent .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    benefits_to_stoughton_community: str = Field(
        ...,
        description=(
            "Explain how this request will benefit the Stoughton community .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_information_to_share: str = Field(
        default="",
        description=(
            "Any additional details or context you would like to provide .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ApplicantSignatures(BaseModel):
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

    organization__contact_information: OrganizationContactInformation = Field(
        ..., description="Organization & Contact Information"
    )
    funding_request_details: FundingRequestDetails = Field(
        ..., description="Funding Request Details"
    )
    applicant_signatures: ApplicantSignatures = Field(..., description="Applicant Signatures")
