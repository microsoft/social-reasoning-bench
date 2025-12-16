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
    """Contact details and delivery preferences for the person making the request"""

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
            'Email address for the requestor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Street mailing address for correspondence .If you cannot fill this, write "
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
            "Primary telephone number for the requestor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Fax number for the requestor .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    preferred_delivery_pick_up: BooleanLike = Field(
        default="", description="Select if you prefer to pick up the records in person"
    )

    preferred_delivery_us_mail: BooleanLike = Field(
        default="", description="Select if you prefer to receive the records by US Mail"
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

    certification_of_conviction_status_i_have_i_have_not_been_convicted: Literal[
        "I HAVE been convicted", "I HAVE NOT been convicted", "N/A", ""
    ] = Field(
        ...,
        description=(
            "Certification under penalty of law whether the requestor has been convicted of "
            "any indictable offense"
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the requestor certifying the information provided .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(
        ..., description="Date the request form is signed by the requestor"
    )  # YYYY-MM-DD format


class RecordRequestInformation(BaseModel):
    """Details of the records being requested"""

    record_request_information: str = Field(
        ...,
        description=(
            "Detailed description of the government records being requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PaymentInformation(BaseModel):
    """Payment authorization and method selection"""

    maximum_authorization_cost: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Maximum dollar amount the requestor authorizes for fulfilling this request",
    )

    cash: BooleanLike = Field(
        default="", description="Select if cash will be used as the payment method"
    )

    check: BooleanLike = Field(
        default="", description="Select if check will be used as the payment method"
    )

    money_order: BooleanLike = Field(
        default="", description="Select if money order will be used as the payment method"
    )


class AgencyUseOnlyCostEstimate(BaseModel):
    """Internal agency fields for estimating costs and deposits"""

    est_document_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated cost of the documents requested (agency use only)"
    )

    est_delivery_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated cost of delivery/postage (agency use only)"
    )

    est_extras_cost: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Estimated cost of any extra services or materials (agency use only)",
    )

    total_est_cost: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Total estimated cost combining documents, delivery, and extras (agency use only)"
        ),
    )

    deposit_amount: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Deposit amount collected toward the estimated cost (agency use only)",
    )

    estimated_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated remaining balance after deposit (agency use only)"
    )

    deposit_date: str = Field(
        default="", description="Date the deposit was received (agency use only)"
    )  # YYYY-MM-DD format


class AgencyUseOnlyDisposition(BaseModel):
    """Internal agency fields for documenting disposition of the request"""

    disposition_notes: str = Field(
        default="",
        description=(
            "Notes by the custodian explaining disposition or any denial reasons .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    in_progress_open: BooleanLike = Field(
        default="",
        description="Indicates the request is in progress and remains open (agency use only)",
    )

    denied_closed: BooleanLike = Field(
        default="", description="Indicates the request has been denied and closed (agency use only)"
    )

    filled_closed: BooleanLike = Field(
        default="", description="Indicates the request has been filled and closed (agency use only)"
    )

    partial_closed: BooleanLike = Field(
        default="",
        description="Indicates the request has been partially filled and closed (agency use only)",
    )


class AgencyUseOnlyTrackingFinalCost(BaseModel):
    """Internal tracking information and final cost details"""

    tracking_number: str = Field(
        default="",
        description=(
            "Internal tracking number assigned to the request (agency use only) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    recd_date: str = Field(
        default="", description="Date the request was received by the agency (agency use only)"
    )  # YYYY-MM-DD format

    ready_date: str = Field(
        default="", description="Date the records will be or were ready (agency use only)"
    )  # YYYY-MM-DD format

    total_pages: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of pages provided (agency use only)"
    )

    total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final total cost for the request (agency use only)"
    )

    deposit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Deposit amount applied to the final cost (agency use only)"
    )

    balance_due: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Remaining balance owed (agency use only)"
    )

    balance_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount of balance paid (agency use only)"
    )

    custodian_signature: str = Field(
        default="",
        description=(
            "Signature of the records custodian confirming records provided .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    custodian_signature_date: str = Field(
        default="", description="Date the custodian signed the form"
    )  # YYYY-MM-DD format


class BoroughOfProspectParkOpenPublicRecordsActRequestForm(BaseModel):
    """
        BOROUGH OF PROSPECT PARK
    OPEN PUBLIC RECORDS ACT REQUEST FORM

        Important Notice
        The last page of this form contains important information related to your rights concerning government records. Please read it carefully.
    """

    requestor_information: RequestorInformation = Field(..., description="Requestor Information")
    record_request_information: RecordRequestInformation = Field(
        ..., description="Record Request Information"
    )
    payment_information: PaymentInformation = Field(..., description="Payment Information")
    agency_use_only___cost_estimate: AgencyUseOnlyCostEstimate = Field(
        ..., description="Agency Use Only - Cost Estimate"
    )
    agency_use_only___disposition: AgencyUseOnlyDisposition = Field(
        ..., description="Agency Use Only - Disposition"
    )
    agency_use_only___tracking__final_cost: AgencyUseOnlyTrackingFinalCost = Field(
        ..., description="Agency Use Only - Tracking & Final Cost"
    )
