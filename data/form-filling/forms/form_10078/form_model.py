from typing import Literal, Optional, List, Union
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
        ...,
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
            'Requestor\'s telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
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

    signature: str = Field(
        ...,
        description=(
            "Signature of the requestor certifying the information provided .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(..., description="Date the request form is signed")  # YYYY-MM-DD format


class PaymentInformation(BaseModel):
    """Maximum cost authorization and selected payment method"""

    maximum_authorization_cost: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Maximum dollar amount you authorize for fulfilling this records request",
    )

    payment_method_cash: BooleanLike = Field(
        default="", description="Select if you will pay by cash"
    )

    payment_method_check: BooleanLike = Field(
        default="", description="Select if you will pay by check"
    )

    payment_method_money_order: BooleanLike = Field(
        default="", description="Select if you will pay by money order"
    )


class RecordRequestInformation(BaseModel):
    """Description of the records being requested"""

    record_request_information_description_line_1: str = Field(
        ...,
        description=(
            "Description of requested records (line 1) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_description_line_2: str = Field(
        default="",
        description=(
            "Description of requested records (line 2) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_description_line_3: str = Field(
        default="",
        description=(
            "Description of requested records (line 3) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_description_line_4: str = Field(
        default="",
        description=(
            "Description of requested records (line 4) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_description_line_5: str = Field(
        default="",
        description=(
            "Description of requested records (line 5) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_description_line_6: str = Field(
        default="",
        description=(
            "Description of requested records (line 6) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_description_line_7: str = Field(
        default="",
        description=(
            "Description of requested records (line 7) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_description_line_8: str = Field(
        default="",
        description=(
            "Description of requested records (line 8) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    record_request_information_description_line_9: str = Field(
        default="",
        description=(
            "Description of requested records (line 9) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AgencyUseOnlyCostEstimate(BaseModel):
    """Agency’s estimated costs and deposit information"""

    est_document_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated cost for document pages"
    )

    est_delivery_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated cost for delivery/postage"
    )

    est_extras_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated cost for any extra services or materials"
    )

    total_est_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total estimated cost for fulfilling the request"
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
    """Notes and final disposition status of the request"""

    disposition_notes: str = Field(
        default="",
        description=(
            "Custodian notes explaining disposition or delays in fulfilling the request .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    in_progress_open: BooleanLike = Field(
        default="", description="Indicate that the request is in progress and remains open"
    )

    denied_closed: BooleanLike = Field(
        default="", description="Indicate that the request was denied and the case is closed"
    )

    filled_closed: BooleanLike = Field(
        default="", description="Indicate that the request was filled and the case is closed"
    )

    partial_closed: BooleanLike = Field(
        default="",
        description="Indicate that the request was partially filled and the case is closed",
    )


class AgencyUseOnlyTrackingFinalization(BaseModel):
    """Tracking information, final costs, and records delivery details"""

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
        default="", description="Date the records are ready for release"
    )  # YYYY-MM-DD format

    total_pages: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of pages provided"
    )

    final_cost_total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Final total cost for the request"
    )

    final_cost_deposit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Deposit amount applied to the final cost"
    )

    balance_due: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Remaining balance due from the requestor"
    )

    balance_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount of balance that has been paid"
    )

    records_provided: str = Field(
        default="",
        description=(
            "Description or list of records actually provided .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    custodian_signature: str = Field(
        default="",
        description=(
            'Signature of the records custodian .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    custodian_signature_date: str = Field(
        default="", description="Date the custodian signed"
    )  # YYYY-MM-DD format


class BoroughOfProspectParkOpenPublicRecordsActRequestForm(BaseModel):
    """
        BOROUGH OF PROSPECT PARK
    OPEN PUBLIC RECORDS ACT REQUEST FORM

        Important Notice
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
    agency_use_only___tracking__finalization: AgencyUseOnlyTrackingFinalization = Field(
        ..., description="Agency Use Only - Tracking & Finalization"
    )
