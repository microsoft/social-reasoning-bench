from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IdentifyingInformation(BaseModel):
    """Basic vendor identification and assignment details"""

    vendor_legal_name: str = Field(
        ...,
        description=(
            "Full legal name of the vendor, including LLC or Inc. if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    vendor_id: str = Field(
        default="",
        description=(
            "Internal or assigned vendor identification number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    payment_status: str = Field(
        default="",
        description=(
            "Current payment status for this vendor (e.g., paid, pending) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    assigned_space_number: str = Field(
        default="",
        description=(
            "Booth or space number assigned to the vendor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AddressInformation(BaseModel):
    """Vendor contact and mailing information"""

    contact_name: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address for the vendor or contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State or province for the mailing address")

    postal_zip: str = Field(..., description="Postal or ZIP code for the mailing address")

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
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
            'Vendor website URL, if applicable .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SpaceSelection(BaseModel):
    """Booth space selection and equipment needs"""

    space_single: BooleanLike = Field(
        default="",
        description="Select if requesting a single booth space (10' Wide x 8' Deep | $400)",
    )

    space_double: BooleanLike = Field(
        default="",
        description="Select if requesting a double booth space (20' Wide x 8' Deep | $750)",
    )

    space_triple: BooleanLike = Field(
        default="",
        description="Select if requesting a triple booth space (30' Wide x 8' Deep | $950)",
    )

    space_custom_width: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Custom booth width in feet for a non-standard space"
    )

    space_custom_price: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Price in dollars for the custom booth space"
    )

    tables_count: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of tables requested for the booth"
    )

    chairs_count: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of chairs requested for the booth"
    )


class ProgramInformation(BaseModel):
    """Worlds program advertisement selections"""

    full_page_color: BooleanLike = Field(
        default="", description="Select if purchasing a full-page color advertisement ($350)"
    )

    full_page_discounted_bw: BooleanLike = Field(
        default="",
        description="Select if purchasing a full-page discounted black & white advertisement ($200)",
    )

    half_page_color: BooleanLike = Field(
        default="", description="Select if purchasing a half-page color advertisement ($250)"
    )

    half_page_discounted_bw: BooleanLike = Field(
        default="",
        description="Select if purchasing a half-page discounted black & white advertisement ($125)",
    )

    quarter_page_color: BooleanLike = Field(
        default="", description="Select if purchasing a quarter-page color advertisement ($150)"
    )

    quarter_page_discounted_bw: BooleanLike = Field(
        default="",
        description=(
            "Select if purchasing a quarter-page discounted black & white advertisement ($75)"
        ),
    )

    custom_ad_description: str = Field(
        default="",
        description=(
            "Description of any custom advertisement (full bleed, cover, special page, "
            'etc.) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    product_descriptions_line_1: str = Field(
        default="",
        description=(
            "First line of product or service description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    product_descriptions_line_2: str = Field(
        default="",
        description=(
            "Second line of product or service description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    product_descriptions_line_3: str = Field(
        default="",
        description=(
            "Third line of product or service description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class VendorBallroomPassAssignment(BaseModel):
    """Assigned names and contact details for vendor ballroom passes"""

    vendor_ballroom_pass_name_1: str = Field(
        default="",
        description=(
            "Name of the first person assigned a vendor ballroom pass .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    vendor_ballroom_pass_email_1: str = Field(
        default="",
        description=(
            "Email of the first person assigned a vendor ballroom pass .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    vendor_ballroom_pass_phone_1: str = Field(
        default="",
        description=(
            "Phone number of the first person assigned a vendor ballroom pass .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    vendor_ballroom_pass_name_2: str = Field(
        default="",
        description=(
            "Name of the second person assigned a vendor ballroom pass .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    vendor_ballroom_pass_email_2: str = Field(
        default="",
        description=(
            "Email of the second person assigned a vendor ballroom pass .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    vendor_ballroom_pass_phone_2: str = Field(
        default="",
        description=(
            "Phone number of the second person assigned a vendor ballroom pass .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Totals(BaseModel):
    """Order totals for booth space and program ads"""

    booth_space_total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount for booth space selected"
    )

    program_ad_total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount for program advertisements selected"
    )

    total_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Grand total amount due (booth space plus program ads)"
    )


class Payment(BaseModel):
    """Payment method and credit card details"""

    payment_credit_card: BooleanLike = Field(
        default="", description="Select if paying by credit card"
    )

    payment_check: BooleanLike = Field(default="", description="Select if paying by check")

    payment_paypal: BooleanLike = Field(
        default="", description="Select if paying via PayPal to treasurer@ucwdc.org"
    )

    visa_mc_number: str = Field(
        default="",
        description=(
            "Credit card number for Visa or MasterCard payments .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cvv_code: str = Field(
        default="",
        description=(
            "Card security code (CVV) from the back of the credit card .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    amount_usd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Charge amount in US dollars for this credit card payment"
    )

    cardholders_name: str = Field(
        default="",
        description=(
            "Name of the cardholder as it appears on the credit card .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cardholders_signature: str = Field(
        default="",
        description=(
            "Signature of the cardholder authorizing the charge .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class UcwdcCountryDanceWorldChampionshipsVendorForm(BaseModel):
    """
    UCWDC Country Dance World Championships Vendor Form

    UCWDC Country Dance World Championships Vendor Form. Please type or print the required information and return the completed form to Marketing@ucwdc.org. This form is used to collect vendor identifying and contact information, select booth space and program advertising options, describe products, assign vendor ballroom passes, and provide payment details for participation as a vendor at the UCWDC Country Dance World Championships.
    """

    identifying_information: IdentifyingInformation = Field(
        ..., description="Identifying Information"
    )
    address_information: AddressInformation = Field(..., description="Address Information")
    space_selection: SpaceSelection = Field(..., description="Space Selection")
    program_information: ProgramInformation = Field(..., description="Program Information")
    vendor_ballroom_pass_assignment: VendorBallroomPassAssignment = Field(
        ..., description="Vendor Ballroom Pass Assignment"
    )
    totals: Totals = Field(..., description="Totals")
    payment: Payment = Field(..., description="Payment")
