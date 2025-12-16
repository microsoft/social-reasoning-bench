from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Applicant name and membership selection"""

    applicant_name: str = Field(
        ...,
        description=(
            "Full name of the applicant requesting 2021 membership .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    local_nhmr_affiliates: BooleanLike = Field(
        default="", description="Select if applying as a Local NHMR Affiliate"
    )

    local_state_affiliate: BooleanLike = Field(
        default="", description="Select if applying as a combined Local & State Affiliate"
    )

    corporate_sponsor_premiere: BooleanLike = Field(
        default="", description="Check if selecting the Premiere level Corporate Sponsor option"
    )

    corporate_sponsor_platinum: BooleanLike = Field(
        default="", description="Check if selecting the Platinum level Corporate Sponsor option"
    )

    corporate_sponsor_gold: BooleanLike = Field(
        default="", description="Check if selecting the Gold level Corporate Sponsor option"
    )

    corporate_sponsor_silver: BooleanLike = Field(
        default="", description="Check if selecting the Silver level Corporate Sponsor option"
    )

    corporate_sponsor_ypn: BooleanLike = Field(
        default="", description="Check if selecting the YPN Corporate Sponsor option"
    )

    event_sponsor: str = Field(
        default="",
        description=(
            "Describe the type or name of the event sponsorship .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_me_to_discuss_options: BooleanLike = Field(
        default="",
        description=(
            "Check if you would like someone to contact you to discuss "
            "membership/sponsorship options"
        ),
    )


class CompanyContactInformation(BaseModel):
    """Company details and primary contact information"""

    company_name: str = Field(
        ...,
        description=(
            'Legal name of the company .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    company_address: str = Field(
        ...,
        description=(
            'Street address of the company .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            'Primary company phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fax_number: str = Field(
        default="",
        description=(
            'Company fax number, if applicable .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary contact email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Company website URL .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class PaymentInformation(BaseModel):
    """Payment amount, method, and credit card details"""

    payment_amount: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total amount to be paid for membership or sponsorship"
    )

    check_number: str = Field(
        default="",
        description=(
            'Number printed on the enclosed check .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    check_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of the enclosed check"
    )

    visa: BooleanLike = Field(default="", description="Select if paying by Visa credit card")

    mastercard: BooleanLike = Field(
        default="", description="Select if paying by MasterCard credit card"
    )

    amex: BooleanLike = Field(
        default="", description="Select if paying by American Express credit card"
    )

    discover: BooleanLike = Field(
        default="", description="Select if paying by Discover credit card"
    )

    cardholder_name_as_it_appears_on_card: str = Field(
        ...,
        description=(
            "Name of the cardholder exactly as it appears on the credit card .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    credit_card_number: str = Field(
        ...,
        description=(
            'Full credit card number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    expiration_date: str = Field(
        ..., description="Credit card expiration date (month and year)"
    )  # YYYY-MM-DD format

    security_code: str = Field(
        ...,
        description=(
            'Credit card security code (CVV/CVC) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    billing_address: str = Field(
        ...,
        description=(
            "Billing street address associated with the credit card .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    billing_address_zip_code: str = Field(..., description="Zip code for the billing address")


class NHMiddlesexRealtors2021AffiliateSponsorApp(BaseModel):
    """
        New Haven Middlesex Association of REALTORS

    2021 Affiliate/Sponsor Application

        I, ________________________________________________, hereby apply for 2021 Membership with New Haven Middlesex Association, and will pay by credit card below or enclose my check made payable to NHMR.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    company__contact_information: CompanyContactInformation = Field(
        ..., description="Company & Contact Information"
    )
    payment_information: PaymentInformation = Field(..., description="Payment Information")
