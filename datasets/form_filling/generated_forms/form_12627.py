from typing import List, Literal, Optional, Union

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
            "Time period the requested records should cover (e.g., specific dates or "
            'months). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    maximum_fees_authorized: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Maximum dollar amount you authorize for fees before the Health Center must "
            "contact you."
        ),
    )

    request_the_fees_be_waived_to_serve_the_publics_interest: BooleanLike = Field(
        default="",
        description=(
            "Check if you are requesting that fees be waived because the request serves the "
            "public interest."
        ),
    )

    how_and_why_the_information_will_be_used_in_public_interest: str = Field(
        default="",
        description=(
            "Explain how and why the requested information will be used in the public "
            'interest. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class RequesterInformation(BaseModel):
    """Contact and identifying information for the person making the request"""

    records_requested_by_first_name: str = Field(
        ...,
        description=(
            "First name of the person requesting the records. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    records_requested_by_last_name: str = Field(
        ...,
        description=(
            "Last name of the person requesting the records. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
            "Email address of the person requesting the records. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        default="",
        description=(
            "Phone number of the person requesting the records. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_person_making_request: str = Field(
        ...,
        description=(
            "Signature of the individual submitting the records request. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_of_request: str = Field(
        ..., description="Date on which the records request is made."
    )  # YYYY-MM-DD format


class OfficeUseOnly(BaseModel):
    """Internal processing and disposition of the request"""

    disposition_of_request_approved: BooleanLike = Field(
        default="", description="Indicates that the records request has been approved."
    )

    disposition_of_request_denied: BooleanLike = Field(
        default="", description="Indicates that the records request has been denied."
    )

    date_information_provided: str = Field(
        default="",
        description="Date on which the requested information was provided to the requester.",
    )  # YYYY-MM-DD format

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
        default="", description="Date on which processing of the request was completed."
    )  # YYYY-MM-DD format


class RecordsRequestSunshineLawCgcphc(BaseModel):
    """
    RECORDS REQUEST, SUNSHINE LAW – CGCPHC

    This is a request for records under the Missouri Sunshine Law, Chapter 610, RSMo. The Health Center makes every effort to comply with requests for records and as such will provide you with a response by the end of the third business day (excluding legal holidays and weekends) following the date the request is received. A response constitutes either compliance of the records requested, a reason for delay or explanation as to why the records may not be available as requested.
    Fees for copies are based upon the actual hourly rate it takes to research and duplicate the material plus $0.10 per page. Fees for electronic and other reproductions will be based on actual costs plus any duplication time. These fees are payable in advance prior to release. If you believe your request serves the public interest, and is not just for personal or commercial interest, you may ask that fees be waived.
    """

    records_request_details: RecordsRequestDetails = Field(
        ..., description="Records Request Details"
    )
    requester_information: RequesterInformation = Field(..., description="Requester Information")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
