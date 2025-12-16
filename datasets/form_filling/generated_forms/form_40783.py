from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequestorInformation(BaseModel):
    """Contact details and certification for the person making the records request"""

    first_name: str = Field(
        ...,
        description=(
            'Requestor\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mi: str = Field(
        default="",
        description=(
            'Middle initial of the requestor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Requestor\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        default="",
        description=(
            'Requestor\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Street mailing address of the requestor .If you cannot fill this, write "
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

    state: str = Field(..., description="State for the mailing address")

    zip: str = Field(..., description="ZIP code for the mailing address")

    telephone: str = Field(
        default="",
        description=(
            'Requestor\'s primary telephone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Requestor\'s fax number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    preferred_delivery_pick_up: BooleanLike = Field(
        default="", description="Select if you prefer to pick up the records in person"
    )

    preferred_delivery_us_mail: BooleanLike = Field(
        default="", description="Select if you prefer to receive the records by U.S. Mail"
    )

    preferred_delivery_on_site_inspect: BooleanLike = Field(
        default="", description="Select if you prefer to inspect the records on-site"
    )

    preferred_delivery_fax: BooleanLike = Field(
        default="", description="Select if you prefer to receive the records by fax"
    )

    preferred_delivery_e_mail: BooleanLike = Field(
        default="", description="Select if you prefer to receive the records by email"
    )

    certification_conviction_status: Literal[
        "I HAVE been convicted of an indictable offense",
        "I HAVE NOT been convicted of an indictable offense",
        "N/A",
        "",
    ] = Field(
        ...,
        description=(
            "Certify whether you have been convicted of any indictable offense under the "
            "laws of New Jersey, any other state, or the United States"
        ),
    )

    requestor_signature: str = Field(
        ...,
        description=(
            "Signature of the requestor certifying the statement above .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    requestor_date: str = Field(
        ..., description="Date the requestor signed the form"
    )  # YYYY-MM-DD format


class PaymentInformation(BaseModel):
    """Authorization of costs and selected payment method"""

    maximum_authorization_cost: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Maximum dollar amount you authorize for fulfilling this records request",
    )

    select_payment_method_cash: BooleanLike = Field(
        default="", description="Select if you will pay by cash"
    )

    select_payment_method_check: BooleanLike = Field(
        default="", description="Select if you will pay by check"
    )

    select_payment_method_money_order: BooleanLike = Field(
        default="", description="Select if you will pay by money order"
    )


class RecordRequestInformation(BaseModel):
    """Description of the government records being requested"""

    record_request_information_line_1: str = Field(
        ...,
        description=(
            "Description of the records being requested (line 1) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_line_2: str = Field(
        default="",
        description=(
            "Description of the records being requested (line 2) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_line_3: str = Field(
        default="",
        description=(
            "Description of the records being requested (line 3) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_line_4: str = Field(
        default="",
        description=(
            "Description of the records being requested (line 4) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_line_5: str = Field(
        default="",
        description=(
            "Description of the records being requested (line 5) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_line_6: str = Field(
        default="",
        description=(
            "Description of the records being requested (line 6) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AgencyUseOnlyCostEstimate(BaseModel):
    """Agency’s estimated costs and deposit information"""

    est_document_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated cost of the documents requested"
    )

    est_delivery_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated cost of delivering the documents"
    )

    est_extras_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated cost of any extra services or materials"
    )

    total_est_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total estimated cost (documents, delivery, and extras)"
    )

    deposit_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Deposit amount collected toward the estimated cost"
    )

    estimated_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated remaining balance after deposit"
    )

    deposit_date: str = Field(
        default="", description="Date the deposit was received"
    )  # YYYY-MM-DD format


class AgencyUseOnlyDisposition(BaseModel):
    """Agency disposition status of the request"""

    in_progress_open: BooleanLike = Field(
        default="", description="Indicates the request is in progress and open"
    )

    denied_closed: BooleanLike = Field(
        default="", description="Indicates the request was denied and closed"
    )

    filled_closed: BooleanLike = Field(
        default="", description="Indicates the request was filled and closed"
    )

    partial_closed: BooleanLike = Field(
        default="", description="Indicates the request was partially filled and closed"
    )


class AgencyUseOnlyTrackingInformationandFinalCost(BaseModel):
    """Tracking details, final costs, and custodian sign-off"""

    tracking_number: str = Field(
        default="",
        description=(
            "Internal tracking number for this request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    recd_date: str = Field(
        default="", description="Date the request was received by the agency"
    )  # YYYY-MM-DD format

    ready_date: str = Field(
        default="", description="Date the records will be or were ready"
    )  # YYYY-MM-DD format

    total_pages: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of pages provided"
    )

    final_total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final total cost for the request"
    )

    final_deposit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Deposit amount applied to the final cost"
    )

    balance_due: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Remaining balance due after deposit"
    )

    balance_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount of balance that has been paid"
    )

    custodian_signature: str = Field(
        default="",
        description=(
            'Signature of the records custodian .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    custodian_date: str = Field(
        default="", description="Date the custodian signed"
    )  # YYYY-MM-DD format


class SouthHunterdonRegionalSchoolDistrictOPRARequestForm(BaseModel):
    """
        South Hunterdon Regional School District
    OPEN PUBLIC RECORDS ACT REQUEST FORM

        The last page of this form contains important information related to your rights concerning government records. Please read it carefully.
    """

    requestor_information: RequestorInformation = Field(..., description="Requestor Information")
    payment_information: PaymentInformation = Field(..., description="Payment Information")
    record_request_information: RecordRequestInformation = Field(
        ..., description="Record Request Information"
    )
    agency_use_only___cost_estimate: AgencyUseOnlyCostEstimate = Field(
        ..., description="Agency Use Only - Cost Estimate"
    )
    agency_use_only___disposition: AgencyUseOnlyDisposition = Field(
        ..., description="Agency Use Only - Disposition"
    )
    agency_use_only___tracking_information_and_final_cost: AgencyUseOnlyTrackingInformationandFinalCost = Field(
        ..., description="Agency Use Only - Tracking Information and Final Cost"
    )
