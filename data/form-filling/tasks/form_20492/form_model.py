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
            "Legal name of the organization applying for funds .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    are_you_a_non_profit_organization_yes: BooleanLike = Field(
        ..., description="Select if the organization is a non-profit"
    )

    are_you_a_non_profit_organization_no: BooleanLike = Field(
        ..., description="Select if the organization is not a non-profit"
    )

    type_of_request_personal: BooleanLike = Field(
        ..., description="Check if the funding request is for a personal need"
    )

    type_of_request_group: BooleanLike = Field(
        ..., description="Check if the funding request is for a group"
    )

    type_of_request_community: BooleanLike = Field(
        ..., description="Check if the funding request is for a community project or purpose"
    )


class FundingRequestDetails(BaseModel):
    """Details about how the requested funds will be used and community impact"""

    how_will_the_funds_be_used: str = Field(
        ...,
        description=(
            "Describe specifically how the requested funds will be used .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
            "Provide any additional information relevant to this request .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Signatures(BaseModel):
    """Applicant signatures and dates"""

    applicant_signature_1: str = Field(
        ...,
        description=(
            'Signature of the applicant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_1: str = Field(
        ..., description="Date the first applicant signed the form"
    )  # YYYY-MM-DD format

    applicant_signature_2: str = Field(
        default="",
        description=(
            "Signature of a second applicant or authorized representative (if applicable) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
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
    funding_request_details: FundingRequestDetails = Field(
        ..., description="Funding Request Details"
    )
    signatures: Signatures = Field(..., description="Signatures")
