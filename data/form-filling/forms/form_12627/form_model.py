from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecordsRequestDetails(BaseModel):
    """Information about the records being requested and any applicable fees"""

    description_of_records_being_requested: str = Field(
        ...,
        description=(
            "Describe the records you are requesting as specifically as possible. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    time_frame_requesting: str = Field(
        default="",
        description=(
            "Time period the requested records should cover. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    i_understand_that_fees_are_allowed_to_be_charged_for_staff_time_for_research_of_records_copying_scanning_or_other_as_needed_t_be_disclosed_i_authorize_the_health_center_to_proceed_unless_fees_exceed_the_amount_of: BooleanLike = Field(
        default="",
        description=(
            "Check to authorize processing of the request up to the specified maximum fee amount."
        ),
    )

    i_request_the_fees_be_waived_to_serve_the_publics_interest: BooleanLike = Field(
        default="",
        description=(
            "Check if you are requesting that fees be waived because the request serves the "
            "public interest."
        ),
    )

    how_and_why_the_info_will_be_used_in_public_interest: str = Field(
        default="",
        description=(
            "Explain how and why the requested information will be used in the public "
            'interest. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class RequesterInformation(BaseModel):
    """Contact information and signature of the person making the request"""

    records_requested_by: str = Field(
        ...,
        description=(
            "Name of the person requesting the records (printed). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Requestor’s first name. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Requestor’s last name. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the person requesting the records. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            "Email address for contacting the requestor. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        default="",
        description=(
            "Phone number for contacting the requestor. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_person_making_request: str = Field(
        ...,
        description=(
            "Signature of the person submitting the records request. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_request: str = Field(
        ..., description="Date the records request is signed and submitted."
    )  # YYYY-MM-DD format


class OfficeUseOnly(BaseModel):
    """Internal processing and disposition of the request"""

    approved: BooleanLike = Field(
        default="", description="Indicates that the records request has been approved."
    )

    date_information_provided: str = Field(
        default="", description="Date on which the requested information was provided."
    )  # YYYY-MM-DD format

    denied: BooleanLike = Field(
        default="", description="Indicates that the records request has been denied."
    )

    reason_for_denial: str = Field(
        default="",
        description=(
            "Explanation of why the records request was denied. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_staff_completing_request: str = Field(
        default="",
        description=(
            "Signature of the staff member who completed processing the request. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_completion_of_request: str = Field(
        default="", description="Date the request processing was completed."
    )  # YYYY-MM-DD format


class RecordsRequestSunshineLawCgcphc(BaseModel):
    """
    RECORDS REQUEST, SUNSHINE LAW – CGCPHC

    This is a request for records under the Missouri Sunshine Law, Chapter 610, RSMo. The Health Center makes every effort to comply with requests for records and as such will provide you with a response by the end of the third business day (excluding legal holidays and weekends) following the date the request is received. A response constitutes either compliance of the records requested, a reason for delay or explanation as to why the records may not be available as requested.
    """

    records_request_details: RecordsRequestDetails = Field(
        ..., description="Records Request Details"
    )
    requester_information: RequesterInformation = Field(..., description="Requester Information")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
