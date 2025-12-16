from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GiftSelection(BaseModel):
    """Select your GRACE Gala gift level"""

    donor: Literal["Donor", "Supporter", "Member", "N/A", ""] = Field(
        default="",
        description=(
            "Select the Donor level if you wish to give $1,000 and receive two Gala admissions."
        ),
    )

    supporter: Literal["Donor", "Supporter", "Member", "N/A", ""] = Field(
        default="",
        description=(
            "Select the Supporter level if you wish to give $2,500 and receive four Gala "
            "admissions and two VIP party invites."
        ),
    )

    member: Literal["Donor", "Supporter", "Member", "N/A", ""] = Field(
        default="",
        description=(
            "Select the Member level if you wish to give $5,000 and receive four Gala "
            "admissions and four VIP party invites."
        ),
    )


class DonorInformation(BaseModel):
    """Contact details for the donating family or individual"""

    name: str = Field(
        ...,
        description=(
            "Primary donor or family name for this gift. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street mailing address. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    city_state_zip_code: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the mailing address. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        default="",
        description=(
            'Best contact phone number. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class PaymentInformation(BaseModel):
    """Credit card payment details"""

    visa: BooleanLike = Field(default="", description="Check if paying by Visa credit card.")

    mastercard: BooleanLike = Field(
        default="", description="Check if paying by Mastercard credit card."
    )

    amex: BooleanLike = Field(
        default="", description="Check if paying by American Express credit card."
    )

    cc_number: str = Field(
        default="",
        description=(
            'Credit card number for payment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    exp: str = Field(
        default="",
        description=(
            'Credit card expiration date (MM/YY). .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cvc: str = Field(
        default="",
        description=(
            'Credit card security code (CVC/CVV). .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class RecognitionInvoicing(BaseModel):
    """Invoicing email and how your name will appear on Gala materials"""

    invoice_me_at_email_address: str = Field(
        default="",
        description=(
            "Email address where the invoice should be sent if you prefer to be invoiced. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    gala_listing_name: str = Field(
        default="",
        description=(
            "Exact name or family name as you would like it to appear in Gala materials. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class Family2Family(BaseModel):
    """
    Family 2 Family

    We would all give our lives for our children, give them the last crumb on our plate. Please consider extending that sense of your generosity to neighbors in need. Together, your family can directly impact another by making a donation to the GRACE Gala as a family endeavor. The best example you will provide your children is to demonstrate compassion for those less fortunate by providing much needed assistance to individuals and families in crisis.
    """

    gift_selection: GiftSelection = Field(..., description="Gift Selection")
    donor_information: DonorInformation = Field(..., description="Donor Information")
    payment_information: PaymentInformation = Field(..., description="Payment Information")
    recognition__invoicing: RecognitionInvoicing = Field(..., description="Recognition & Invoicing")
