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
    """Customer/client status and contact details"""

    customer_client_status_new: BooleanLike = Field(
        ..., description="Indicate if the customer/client is new"
    )

    customer_client_status_existing: BooleanLike = Field(
        ..., description="Indicate if the customer/client is an existing client"
    )

    client_customer_name: str = Field(
        ...,
        description=(
            "Full legal name of the client or customer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    poc_name: str = Field(
        ...,
        description=(
            "Point of contact name for this client/customer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_physical_address: str = Field(
        ...,
        description=(
            "Mailing or physical address of the client/customer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    bldg_permit_if_applicable: str = Field(
        default="",
        description=(
            'Building permit number, if applicable .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    po_rfq_agreement_number: str = Field(
        default="",
        description=(
            "Purchase order, RFQ, or agreement number associated with this request .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address for correspondence and reporting .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SampleTypeTurnaroundTime(BaseModel):
    """Type of sample, requested processing speed, and delivery method"""

    drinking_water_treated: BooleanLike = Field(
        ..., description="Check if the sample type is treated drinking water"
    )

    ground_water: BooleanLike = Field(..., description="Check if the sample type is ground water")

    surface_water_marine_river_etc: BooleanLike = Field(
        ..., description="Check if the sample type is surface water (marine, river, etc.)"
    )

    recreational_water_pools_etc: BooleanLike = Field(
        ..., description="Check if the sample type is recreational water (pools, etc.)"
    )

    wastewater_effluent_etc: BooleanLike = Field(
        ..., description="Check if the sample type is wastewater (effluent, etc.)"
    )

    other_s: str = Field(
        default="",
        description=(
            "Describe the sample type if it is not listed among the options .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    turn_around_time_regular_7_working_days: BooleanLike = Field(
        ..., description="Select if regular 7 working days turn-around time is requested"
    )

    turn_around_time_rush_5_working_days_2x_cost: BooleanLike = Field(
        ...,
        description=(
            "Select if rush 5 working days turn-around time is requested (2x cost, "
            "pre-payment required)"
        ),
    )

    turn_around_time_urgent_3_working_days_3x_cost: BooleanLike = Field(
        ...,
        description=(
            "Select if urgent 3 working days turn-around time is requested (3x cost, "
            "pre-payment required)"
        ),
    )

    sample_delivery_customer_client: BooleanLike = Field(
        ..., description="Check if the sample was delivered by the customer/client"
    )

    sample_delivery_courier: BooleanLike = Field(
        ..., description="Check if the sample was delivered by a courier"
    )

    sample_delivery_epa_certified_operator: BooleanLike = Field(
        ..., description="Check if the sample was delivered by an EPA-certified operator"
    )

    sample_delivery_business_agency: BooleanLike = Field(
        ..., description="Check if the sample was delivered by a business or agency"
    )


class SampleInformation(BaseModel):
    """Details about sampling, location, and notes"""

    sampled_by_name_agency: str = Field(
        ...,
        description=(
            "Name and agency of the person who collected the sample .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    witnessed_by_name_agency: str = Field(
        default="",
        description=(
            "Name and agency of the person who witnessed the sampling, if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    facility_residential_name_and_location: str = Field(
        ...,
        description=(
            "Name and location of the facility or residence where the sample was taken .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    notes_instructions: str = Field(
        default="",
        description=(
            "Additional notes or special instructions regarding the samples or analysis .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AnalysisRequested(BaseModel):
    """Requested analyses and lab identifiers"""

    weri_lab_id: str = Field(
        default="",
        description=(
            "WERI laboratory identification number (for lab official use) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    analysis_requested_table: List[AnalysisRequestedTableRow] = Field(
        ...,
        description=(
            "Table to record specific sample description/location, date, time, and volume "
            "for each sample"
        ),
    )  # List of table rows


class ChainofCustodySignatures(BaseModel):
    """Relinquishing, receiving, and review/acceptance details"""

    relinquished_by_print_sign: str = Field(
        ...,
        description=(
            "Printed name and signature of the person relinquishing the sample(s) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    relinquished_by_date: str = Field(
        ..., description="Date the sample(s) were relinquished by the sampler/collector"
    )  # YYYY-MM-DD format

    relinquished_by_time: str = Field(
        ...,
        description=(
            "Time the sample(s) were relinquished by the sampler/collector .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    received_by_print_sign: str = Field(
        ...,
        description=(
            "Printed name and signature of the person receiving the sample(s) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    received_by_date: str = Field(
        ..., description="Date the sample(s) were received"
    )  # YYYY-MM-DD format

    received_by_time: str = Field(
        ...,
        description=(
            'Time the sample(s) were received .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reviewed_accepted_by: str = Field(
        ...,
        description=(
            "Name and signature of WERI lab staff who reviewed/accepted the samples .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reviewed_accepted_by_date: str = Field(
        ..., description="Date the samples were reviewed/accepted by WERI lab"
    )  # YYYY-MM-DD format

    reviewed_accepted_by_time: str = Field(
        ...,
        description=(
            "Time the samples were reviewed/accepted by WERI lab .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WERIOfficialUse(BaseModel):
    """Internal lab order and invoice tracking"""

    weri_lab_order_number: str = Field(
        default="",
        description=(
            'Internal WERI lab order number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pymt_receiving_agent_date: str = Field(
        default="",
        description=(
            "Name of payment receiving agent and date payment was received .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    uog_weri_fr_number: str = Field(
        default="",
        description=(
            'UOG WERI financial record (FR) number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    weri_invoice_number: str = Field(
        default="",
        description=(
            "WERI invoice number associated with this request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PaymentDetails(BaseModel):
    """Payment method and authorization information"""

    cash_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid in cash"
    )

    check_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid by check"
    )

    check_number: str = Field(
        default="",
        description=(
            'Check number for the payment .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    funds_transfer_acct_inter_agency_approval_req: str = Field(
        default="",
        description=(
            "Account number for inter-agency funds transfer (approval required) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    credit_card_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid by credit card"
    )

    credit_card_auth_code: str = Field(
        default="",
        description=(
            "Authorization code for the credit card transaction .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    of_line: str = Field(
        default="",
        description=(
            "Free-form field (e.g., signature or designation line) labeled as 'of' .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class UogWeriWaterQualityLabManagementCOCAnalysisRequest(BaseModel):
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
    sample_information: SampleInformation = Field(..., description="Sample Information")
    analysis_requested: AnalysisRequested = Field(..., description="Analysis Requested")
    chain_of_custody_signatures: ChainofCustodySignatures = Field(
        ..., description="Chain of Custody Signatures"
    )
    weri_official_use: WERIOfficialUse = Field(..., description="WERI Official Use")
    payment_details: PaymentDetails = Field(..., description="Payment Details")
