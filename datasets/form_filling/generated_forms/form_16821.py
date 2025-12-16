from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ExhibitorDetails(BaseModel):
    """Details of the exhibiting company"""

    company_name: str = Field(
        ...,
        description=(
            "Legal or trading name of the exhibiting company .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Primary contact person for this exhibition booking .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tel_number: str = Field(
        ...,
        description=(
            "Telephone number for the contact person or company .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Email address for correspondence about the exhibition .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    company_address: str = Field(
        ...,
        description=(
            "Physical or postal address of the company .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    company_vat_number: str = Field(
        default="",
        description=(
            "Company VAT registration number, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    company_registration_number: str = Field(
        default="",
        description=(
            'Official company registration number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ExhibitionDetails(BaseModel):
    """Information about what will be exhibited"""

    type_of_exhibition: Literal[
        "Display",
        "Product launch",
        "Database build-up",
        "Product sampling",
        "Product/service awareness",
        "Customer feedback",
        "Other",
        "N/A",
        "",
    ] = Field(..., description="Overall type or purpose of the exhibition")

    display: BooleanLike = Field(
        default="", description="Select if the exhibition is primarily a display"
    )

    product_launch: BooleanLike = Field(
        default="", description="Select if the exhibition is for a product launch"
    )

    database_build_up: BooleanLike = Field(
        default="", description="Select if the exhibition is for building a customer database"
    )

    product_sampling: BooleanLike = Field(
        default="", description="Select if the exhibition involves product sampling"
    )

    product_service_awareness: BooleanLike = Field(
        default="",
        description="Select if the exhibition is to create awareness of a product or service",
    )

    customer_feedback: BooleanLike = Field(
        default="", description="Select if the exhibition is focused on gathering customer feedback"
    )

    other: BooleanLike = Field(
        default="",
        description="Select if the exhibition type is not listed and will be specified separately",
    )

    if_other_please_describe: str = Field(
        default="",
        description=(
            "Describe the exhibition type if 'Other' was selected .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CourtRequested(BaseModel):
    """Court and stand requirements for the exhibition"""

    court_required: Literal["1", "2", "3", "N/A", ""] = Field(
        ..., description="Select which court or area is requested for the exhibition"
    )

    court_1: BooleanLike = Field(default="", description="Select if Court 1 is requested")

    court_2: BooleanLike = Field(default="", description="Select if Court 2 is requested")

    court_3: BooleanLike = Field(default="", description="Select if Court 3 is requested")

    commencement_date: str = Field(
        ..., description="Start date of the exhibition"
    )  # YYYY-MM-DD format

    completion_date: str = Field(..., description="End date of the exhibition")  # YYYY-MM-DD format

    size_of_stand: str = Field(
        ...,
        description=(
            "Dimensions or area of the exhibition stand requested .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    would_you_require_power: Literal["Yes", "No", "N/A", ""] = Field(
        ..., description="Indicate whether electrical power is required for the stand"
    )

    yes_power_required: BooleanLike = Field(
        default="", description="Select if electrical power is required"
    )

    no_power_not_required: BooleanLike = Field(
        default="", description="Select if electrical power is not required"
    )


class SpecialRequests(BaseModel):
    """Additional requests and stand description"""

    special_requests: str = Field(
        default="",
        description=(
            "Any special requirements or additional requests for the exhibition .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    detailed_description_of_exhibition_including_dimensions: str = Field(
        ...,
        description=(
            "Detailed description of the exhibition setup, including stand dimensions and "
            'layout .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ForOfficeUse(BaseModel):
    """Internal approval information"""

    approved: Literal["Yes", "No", "N/A", ""] = Field(
        default="",
        description="Indicates whether the exhibition booking has been approved (office use only)",
    )

    yes_approved: BooleanLike = Field(default="", description="Select if the booking is approved")

    no_not_approved: BooleanLike = Field(
        default="", description="Select if the booking is not approved"
    )

    approved_by: str = Field(
        default="",
        description=(
            "Name or designation of the person approving the booking (office use only) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_approval: str = Field(
        default="", description="Date on which the booking was approved (office use only)"
    )  # YYYY-MM-DD format


class ExhibitionBookingRequest(BaseModel):
    """
    exhibition booking request

    Please complete and email to marketing@ferndaleonrepublic.co.za
    """

    exhibitor_details: ExhibitorDetails = Field(..., description="Exhibitor Details")
    exhibition_details: ExhibitionDetails = Field(..., description="Exhibition Details")
    court_requested: CourtRequested = Field(..., description="Court Requested")
    special_requests: SpecialRequests = Field(..., description="Special Requests")
    for_office_use: ForOfficeUse = Field(..., description="For Office Use")
