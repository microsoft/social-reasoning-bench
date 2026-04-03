from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SpecificDescriptionLocationRow(BaseModel):
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
        ..., description="Check if this is a new customer or client."
    )

    customer_client_status_existing: BooleanLike = Field(
        ..., description="Check if this is an existing customer or client."
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
            "Point of contact name for this client or project. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    bldg_permit_if_applicable: str = Field(
        default="",
        description=(
            "Building permit number, if applicable. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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

    e_mail: str = Field(
        ...,
        description=(
            "Email address for correspondence and reports. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SampleType(BaseModel):
    """Type of water or sample submitted"""

    drinking_water_treated: BooleanLike = Field(
        ..., description="Check if the sample type is treated drinking water."
    )

    ground_water: BooleanLike = Field(..., description="Check if the sample type is groundwater.")

    surface_water_marine_river_etc: BooleanLike = Field(
        ..., description="Check if the sample type is surface water such as marine or river water."
    )

    recreational_water_pools_etc: BooleanLike = Field(
        ..., description="Check if the sample type is recreational water such as pools."
    )

    wastewater_effluent_etc: BooleanLike = Field(
        ..., description="Check if the sample type is wastewater or effluent."
    )

    other_s: str = Field(
        default="",
        description=(
            "Describe the sample type if it does not fit the listed categories. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class TurnAroundTime(BaseModel):
    """Requested analysis completion time"""

    regular_7_working_days: BooleanLike = Field(
        ..., description="Check if regular 7 working day turnaround time is requested."
    )

    rush_working_days: BooleanLike = Field(
        ...,
        description=(
            "Check if rush turnaround time is requested (2x total analysis cost, "
            "pre-payment required)."
        ),
    )

    urgent_3_working_days: BooleanLike = Field(
        ...,
        description=(
            "Check if urgent 3 working day turnaround time is requested (3x total analysis "
            "cost, pre-payment required)."
        ),
    )


class SampleDelivery(BaseModel):
    """Method and party delivering the sample"""

    customer_client: BooleanLike = Field(
        ..., description="Check if the samples were delivered by the customer or client."
    )

    courier: BooleanLike = Field(
        ..., description="Check if the samples were delivered by a courier."
    )

    epa_certified_operator: BooleanLike = Field(
        ..., description="Check if the samples were delivered by an EPA-certified operator."
    )

    business_agency: str = Field(
        default="",
        description=(
            "Name of the business or agency delivering the samples, if applicable. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SampleInformation(BaseModel):
    """Details about sampling and sample location"""

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
            "Name and location of the facility or residence where the sample was collected. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
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
    """Per-sample description and collection details"""

    specific_description_location: List[SpecificDescriptionLocationRow] = Field(
        ...,
        description=(
            "For each sample, record the specific description/location, date, time, and volume."
        ),
    )  # List of table rows

    date: str = Field(
        default="",
        description="Date associated with the relevant action or entry (context-specific).",
    )  # YYYY-MM-DD format

    time: str = Field(
        default="",
        description=(
            "Time associated with the relevant action or entry (context-specific). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    volume: str = Field(
        default="",
        description=(
            "Sample volume for each entry in the analysis request table. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ChainofCustodyAcknowledgment(BaseModel):
    """Relinquishing, receiving, and lab acceptance of samples"""

    sampler_collector: str = Field(
        ...,
        description=(
            "Printed name and/or signature of the sampler or collector relinquishing the "
            'samples. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    relinquished_by_date: str = Field(
        ...,
        description="Date the sampler/collector relinquished the samples to the lab or courier.",
    )  # YYYY-MM-DD format

    relinquished_by_time: str = Field(
        ...,
        description=(
            "Time the sampler/collector relinquished the samples. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    deliverer_receiver: str = Field(
        ...,
        description=(
            "Printed name and/or signature of the person receiving the samples. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    received_by_date: str = Field(
        ..., description="Date the samples were received by the deliverer/receiver."
    )  # YYYY-MM-DD format

    received_by_time: str = Field(
        ...,
        description=(
            "Time the samples were received by the deliverer/receiver. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weri_lab_reviewed_accepted_by: str = Field(
        ...,
        description=(
            "Name or signature of the WERI lab staff member who reviewed and accepted the "
            'samples. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    weri_lab_date: str = Field(
        ..., description="Date the WERI lab staff reviewed and accepted the samples."
    )  # YYYY-MM-DD format

    weri_lab_time: str = Field(
        ...,
        description=(
            "Time the WERI lab staff reviewed and accepted the samples. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WERIOfficialUse(BaseModel):
    """Internal lab order and payment processing details"""

    weri_lab_order_number: str = Field(
        default="",
        description=(
            "Internal WERI lab order number (for official use). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
            "UOG WERI financial reference number (for official use). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weri_invoice_number: str = Field(
        default="",
        description=(
            "WERI invoice number associated with this request. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cash: BooleanLike = Field(default="", description="Check if payment is made in cash.")

    cash_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid in cash."
    )

    check: BooleanLike = Field(default="", description="Check if payment is made by check.")

    check_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid by check."
    )

    check_number: str = Field(
        default="",
        description=(
            'Check number for the payment. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    funds_transfer_acct_inter_agency_approval_req: str = Field(
        default="",
        description=(
            "Funds transfer account number for inter-agency payments (approval required). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    credit_card: BooleanLike = Field(
        default="", description="Check if payment is made by credit card."
    )

    credit_card_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount charged to the credit card."
    )

    auth_code: str = Field(
        default="",
        description=(
            "Authorization code for the credit card transaction. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DocumentControl(BaseModel):
    """Form pagination and control information"""

    page_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current page number of this form."
    )

    total_pages: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of pages in this form."
    )


class WaterQualityLabChainOfCustodyAnalysisRequest(BaseModel):
    """
        UOG WERI WATER QUALITY LABORATORY
    WERI LAB QUALITY MANAGEMENT PROGRAM
    Chain-of-Custody (COC) & Analysis Request

        WERI LAB QUALITY MANAGEMENT PROGRAM Chain-of-Custody (COC) & Analysis Request
    """

    customerclient_information: CustomerClientInformation = Field(
        ..., description="Customer/Client Information"
    )
    sample_type: SampleType = Field(..., description="Sample Type")
    turn_around_time: TurnAroundTime = Field(..., description="Turn-Around-Time")
    sample_delivery: SampleDelivery = Field(..., description="Sample Delivery")
    sample_information: SampleInformation = Field(..., description="Sample Information")
    analysis_requested: AnalysisRequested = Field(..., description="Analysis Requested")
    chain_of_custody__acknowledgment: ChainofCustodyAcknowledgment = Field(
        ..., description="Chain of Custody / Acknowledgment"
    )
    weri_official_use: WERIOfficialUse = Field(..., description="WERI Official Use")
    document_control: DocumentControl = Field(..., description="Document Control")
