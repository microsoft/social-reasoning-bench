from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CustomerClientInformation(BaseModel):
    """Customer/client status and contact details"""

    customer_client_status_new: BooleanLike = Field(
        default="", description="Indicate if the customer/client is new."
    )

    customer_client_status_existing: BooleanLike = Field(
        default="", description="Indicate if the customer/client is an existing client."
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
            "Mailing or physical address of the client/customer. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    email: str = Field(
        ...,
        description=(
            "Email address for correspondence and reporting. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SampleTypeTurnaroundTime(BaseModel):
    """Sample classification and requested processing time"""

    sample_type_drinking_water_treated: BooleanLike = Field(
        default="", description="Check if the sample is treated drinking water."
    )

    sample_type_ground_water: BooleanLike = Field(
        default="", description="Check if the sample is ground water."
    )

    sample_type_surface_water_marine_river_etc: BooleanLike = Field(
        default="",
        description="Check if the sample is surface water such as marine or river water.",
    )

    sample_type_recreational_water_pools_etc: BooleanLike = Field(
        default="", description="Check if the sample is recreational water such as pools."
    )

    sample_type_wastewater_effluent_etc: BooleanLike = Field(
        default="", description="Check if the sample is wastewater or effluent."
    )

    sample_type_other_s: str = Field(
        default="",
        description=(
            "Describe the sample type if it does not fit the listed categories. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    turn_around_time_regular_7_working_days: BooleanLike = Field(
        default="", description="Select if regular 7 working day turnaround is requested."
    )

    turn_around_time_rush_working_days: BooleanLike = Field(
        default="",
        description=(
            "Select if rush turnaround is requested (2x total analysis cost, pre-payment required)."
        ),
    )

    turn_around_time_urgent_3_working_days: BooleanLike = Field(
        default="",
        description=(
            "Select if urgent 3 working day turnaround is requested (3x total analysis "
            "cost, pre-payment required)."
        ),
    )


class SampleDelivery(BaseModel):
    """Method of sample delivery"""

    sample_delivery_customer_client: BooleanLike = Field(
        default="", description="Check if the sample was delivered by the customer/client."
    )

    sample_delivery_courier: BooleanLike = Field(
        default="", description="Check if the sample was delivered by a courier."
    )

    sample_delivery_epa_certified_operator: BooleanLike = Field(
        default="", description="Check if the sample was delivered by an EPA-certified operator."
    )

    sample_delivery_business_agency: BooleanLike = Field(
        default="", description="Check if the sample was delivered by a business or agency."
    )


class SampleInformation(BaseModel):
    """Sampling personnel, location, and notes"""

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
            "Additional notes or special instructions regarding the sample or analysis. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AnalysisRequested(BaseModel):
    """Requested analyses and sample identifiers"""

    weri_lab_id: str = Field(
        default="",
        description=(
            "WERI laboratory identification number for the sample (lab use). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    specific_description_location: str = Field(
        ...,
        description=(
            "Detailed description and location of the sampling point. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Sampling date corresponding to the specific description/location."
    )  # YYYY-MM-DD format

    time: str = Field(
        ...,
        description=(
            "Sampling time corresponding to the specific description/location. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    volume: str = Field(
        ...,
        description=(
            "Volume of the sample collected for each entry. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ChainofCustody(BaseModel):
    """Relinquishing, receiving, and lab review details"""

    sample_collector: str = Field(
        ...,
        description=(
            "Printed name and signature of the person relinquishing the sample. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    relinquished_by_date: str = Field(
        ..., description="Date the sample was relinquished by the collector."
    )  # YYYY-MM-DD format

    relinquished_by_time: str = Field(
        ...,
        description=(
            "Time the sample was relinquished by the collector. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    deliverer_receiver: str = Field(
        ...,
        description=(
            "Printed name and signature of the person receiving the sample. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    received_by_date: str = Field(
        ..., description="Date the sample was received by the lab or receiving party."
    )  # YYYY-MM-DD format

    received_by_time: str = Field(
        ...,
        description=(
            "Time the sample was received by the lab or receiving party. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    weri_lab_reviewed_accepted_by: str = Field(
        default="",
        description=(
            "Name of WERI lab staff who reviewed and accepted the sample. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    weri_lab_reviewed_accepted_date: str = Field(
        default="", description="Date the sample was reviewed and accepted by WERI lab."
    )  # YYYY-MM-DD format

    weri_lab_reviewed_accepted_time: str = Field(
        default="",
        description=(
            "Time the sample was reviewed and accepted by WERI lab. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WERIOfficialUse(BaseModel):
    """Internal WERI lab order and reference numbers"""

    weri_lab_order_number: str = Field(
        default="",
        description=(
            'Internal WERI lab order number. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pymt_receiving_agent_date: str = Field(
        default="",
        description=(
            "Name of payment receiving agent and date payment was received. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    uog_weri_fr_number: str = Field(
        default="",
        description=(
            "UOG WERI financial record (FR) number. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    weri_invoice_number: str = Field(
        default="",
        description=(
            "WERI invoice number associated with this order. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PaymentDetails(BaseModel):
    """Payment method and transaction details"""

    payment_cash_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid in cash."
    )

    payment_check_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid by check."
    )

    payment_check_number: str = Field(
        default="",
        description=(
            'Check number used for payment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    payment_funds_transfer_acct_number_inter_agency_approval_req: str = Field(
        default="",
        description=(
            "Funds transfer account number for inter-agency payments (approval required). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    payment_credit_card_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount charged to the credit card."
    )

    payment_credit_card_auth_code: str = Field(
        default="",
        description=(
            "Authorization code for the credit card transaction. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DocumentControl(BaseModel):
    """Uncontrolled copy page numbering"""

    uncontrolled_copy_page_number: str = Field(
        default="",
        description=(
            "Page numbering for uncontrolled copy (e.g., 1 of 2). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WaterQualityLabChainOfCustodyAnalysisRequest(BaseModel):
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
    sample_type__turn_around_time: SampleTypeTurnaroundTime = Field(
        ..., description="Sample Type & Turn-around Time"
    )
    sample_delivery: SampleDelivery = Field(..., description="Sample Delivery")
    sample_information: SampleInformation = Field(..., description="Sample Information")
    analysis_requested: AnalysisRequested = Field(..., description="Analysis Requested")
    chain_of_custody: ChainofCustody = Field(..., description="Chain of Custody")
    weri_official_use: WERIOfficialUse = Field(..., description="WERI Official Use")
    payment_details: PaymentDetails = Field(..., description="Payment Details")
    document_control: DocumentControl = Field(..., description="Document Control")
