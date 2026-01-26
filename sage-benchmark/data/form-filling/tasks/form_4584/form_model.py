from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AnalysisRequestedTableRow(BaseModel):
    """Single row in Specific Description/Location"""

    specific_description_location: str = Field(
        default="", description="Specific_Description_Location"
    )
    date: str = Field(default="", description="Date")
    time: str = Field(default="", description="Time")
    volume: str = Field(default="", description="Volume")


class CustomerClientInformation(BaseModel):
    """Customer/client contact and account details"""

    customer_client_status_new: BooleanLike = Field(
        default="", description="Check if this is a new customer or client."
    )

    customer_client_status_existing: BooleanLike = Field(
        default="", description="Check if this is an existing customer or client."
    )

    client_customer_name: str = Field(
        ...,
        description=(
            "Full legal name of the client or customer. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    poc_name: str = Field(
        ...,
        description=(
            "Point of contact name for this request. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_physical_address: str = Field(
        ...,
        description=(
            "Mailing or physical address of the client or sampling location. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    bldg_permit_applicable: str = Field(
        default="",
        description=(
            "Applicable building permit number, if relevant. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    po_rfq_agreement_number: str = Field(
        default="",
        description=(
            "Purchase order, RFQ, or agreement number associated with this request. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Email address for correspondence and reporting. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SampleTypeTurnAroundTime(BaseModel):
    """Type of sample and requested analysis turn-around time"""

    sample_type_drinking_water_treated: BooleanLike = Field(
        default="", description="Check if the sample is treated drinking water."
    )

    sample_type_ground_water: BooleanLike = Field(
        default="", description="Check if the sample is groundwater."
    )

    sample_type_surface_water: BooleanLike = Field(
        default="",
        description="Check if the sample is surface water such as marine or river water.",
    )

    sample_type_recreational_water: BooleanLike = Field(
        default="", description="Check if the sample is recreational water such as pools."
    )

    sample_type_wastewater: BooleanLike = Field(
        default="", description="Check if the sample is wastewater or effluent."
    )

    sample_type_other: str = Field(
        default="",
        description=(
            "Describe the sample type if it does not fit the listed categories. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    tat_regular_7_working_days: BooleanLike = Field(
        default="", description="Select if regular 7 working days turnaround time is requested."
    )

    tat_rush_5_working_days: BooleanLike = Field(
        default="",
        description=(
            "Select if rush 5 working days turnaround time is requested (2x cost, "
            "pre-payment required)."
        ),
    )

    tat_urgent_3_working_days: BooleanLike = Field(
        default="",
        description=(
            "Select if urgent 3 working days turnaround time is requested (3x cost, "
            "pre-payment required)."
        ),
    )


class SampleDelivery(BaseModel):
    """How the sample is delivered to the lab"""

    sample_delivery_customer_client: BooleanLike = Field(
        default="",
        description="Check if the sample is delivered directly by the customer or client.",
    )

    sample_delivery_courier: BooleanLike = Field(
        default="", description="Check if the sample is delivered by a courier."
    )

    sample_delivery_epa_certified_operator: BooleanLike = Field(
        default="", description="Check if the sample is delivered by an EPA-certified operator."
    )

    sample_delivery_business_agency: BooleanLike = Field(
        default="", description="Check if the sample is delivered by a business or agency."
    )


class SampleInformation(BaseModel):
    """Details about sampling, location, and notes"""

    sampled_by_name_agency: str = Field(
        ...,
        description=(
            "Name and agency of the person who collected the sample. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    witnessed_by_name_agency: str = Field(
        default="",
        description=(
            "Name and agency of the person who witnessed the sampling, if applicable. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    facility_residential_name_and_location: str = Field(
        ...,
        description=(
            "Name and location of the facility or residence where the sample was taken. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    notes_instructions: str = Field(
        default="",
        description=(
            "Additional notes or special instructions related to the samples or analyses. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class AnalysisRequested(BaseModel):
    """Requested analyses and sample details"""

    analysis_requested_table: List[AnalysisRequestedTableRow] = Field(
        ...,
        description=(
            "Table to record each sample's specific description/location, date, time, and volume."
        ),
    )  # List of table rows

    analysis_requested_date: str = Field(
        default="",
        description="Date of sample collection for each entry in the analysis requested table.",
    )  # YYYY-MM-DD format

    analysis_requested_time: str = Field(
        default="",
        description=(
            "Time of sample collection for each entry in the analysis requested table. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    analysis_requested_volume: str = Field(
        default="",
        description=(
            "Sample volume for each entry in the analysis requested table. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    weri_lab_id: str = Field(
        default="",
        description=(
            "Unique WERI laboratory identification number assigned to the sample batch. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ChainofCustody(BaseModel):
    """Relinquishing, receiving, and review of samples"""

    relinquished_by: str = Field(
        ...,
        description=(
            "Name and signature of the person relinquishing the sample(s). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    relinquished_by_date: str = Field(
        ..., description="Date when the sample(s) were relinquished to the laboratory."
    )  # YYYY-MM-DD format

    relinquished_by_time: str = Field(
        ...,
        description=(
            "Time when the sample(s) were relinquished to the laboratory. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    received_by: str = Field(
        ...,
        description=(
            "Name and signature of the person receiving the sample(s) at the laboratory. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    received_by_date: str = Field(
        ..., description="Date when the sample(s) were received at the laboratory."
    )  # YYYY-MM-DD format

    received_by_time: str = Field(
        ...,
        description=(
            "Time when the sample(s) were received at the laboratory. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reviewed_accepted_by: str = Field(
        default="",
        description=(
            "Name and signature of the WERI lab staff who reviewed and accepted the "
            'samples. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    reviewed_accepted_by_date: str = Field(
        default="",
        description="Date when the samples were reviewed and accepted by WERI lab staff.",
    )  # YYYY-MM-DD format

    reviewed_accepted_by_time: str = Field(
        default="",
        description=(
            "Time when the samples were reviewed and accepted by WERI lab staff. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class WERIOfficialUse(BaseModel):
    """Internal WERI lab order and billing references"""

    weri_lab_order_number: str = Field(
        default="",
        description=(
            "Internal WERI laboratory order number. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    pymt_receiving_agent_date: str = Field(
        default="",
        description=(
            "Name of the payment receiving agent and the date payment was received. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    uog_weri_fr_number: str = Field(
        default="",
        description=(
            "UOG WERI financial reference (FR) number. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    weri_invoice_number: str = Field(
        default="",
        description=(
            "Invoice number issued by WERI for this request. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PaymentDetails(BaseModel):
    """Payment method and authorization information"""

    payment_cash_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid in cash."
    )

    payment_check_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid by check."
    )

    payment_check_number: str = Field(
        default="",
        description=(
            'Check number for the payment. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    funds_transfer_acct_number: str = Field(
        default="",
        description=(
            "Account number for inter-agency funds transfer (approval required). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    payment_credit_card_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid by credit card."
    )

    auth_code: str = Field(
        default="",
        description=(
            "Authorization code for the credit card transaction. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PageInformation(BaseModel):
    """Page numbering for the form"""

    page_x_of_y: str = Field(
        default="",
        description=(
            "Page numbering field (e.g., page X of Y). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class pythonWaterQualityLabManagementCOCAnalysisRequest(BaseModel):
    """
        UOG WERI WATER QUALITY LABORATORY
    WERI LAB QUALITY MANAGEMENT PROGRAM
    Chain-of-Custody (COC) & Analysis Request

        WERI LAB QUALITY MANAGEMENT PROGRAM
        Chain-of-Custody (COC) & Analysis Request
    """

    customerclient_information: CustomerClientInformation = Field(
        ..., description="Customer/Client Information"
    )
    sample_type__turn_around_time: SampleTypeTurnAroundTime = Field(
        ..., description="Sample Type & Turn-Around-Time"
    )
    sample_delivery: SampleDelivery = Field(..., description="Sample Delivery")
    sample_information: SampleInformation = Field(..., description="Sample Information")
    analysis_requested: AnalysisRequested = Field(..., description="Analysis Requested")
    chain_of_custody: ChainofCustody = Field(..., description="Chain of Custody")
    weri_official_use: WERIOfficialUse = Field(..., description="WERI Official Use")
    payment_details: PaymentDetails = Field(..., description="Payment Details")
    page_information: PageInformation = Field(..., description="Page Information")
